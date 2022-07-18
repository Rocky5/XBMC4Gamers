'''
	Script by Rocky5
	Used to prep a XISO so it can be playd from the Xbox HDD. It also extracts images and the xbe header so trainers work.
	Original script by headphone - http://www.emuxtras.net/forum/viewtopic.php?f=187&t=3228&start=40#p70178
'''
import glob
import os
import shutil
import traceback
from io import BytesIO
from struct import unpack

from xbe import *
from xbeinfo import *
from xbmc import log, LOGDEBUG, LOGERROR, LOGFATAL
from xbmcgui import Dialog, DialogProgress


# -----------------------------------------------------------------------------------
# Inspiration/code from: xbox360iso.py Copyright (c) 2014 Rob Lambell (MIT License)
#                        xbiso.pl (c) 30/06/2004 codex(at)bogus.net
#                        xboxsig.py Copyright (c) <2015> <Pete Stanley>
# -----------------------------------------------------------------------------------
def check_iso(iso_file):
	iso_info = {}
	# check for validity
	iso_file.seek(0x10000)
	if iso_file.read(0x14).decode("ascii", "ignore") == 'MICROSOFT*XBOX*MEDIA':  # read tailend of header
		iso_info['sector_size'] = 0x800
		# read the directory table
		iso_file.seek(0x10014)
		iso_info['root_dir_sector'] = unpack('I', iso_file.read(4))[0]  # dtable
		iso_info['root_dir_size'] = unpack('I', iso_file.read(4))[0]
	else:
		log("header tail mismatch -- possible corruption?", LOGFATAL)
		log("this doesn't appear to be an xbox iso image", LOGFATAL)

	# an empty dictionary is falsy, so just return the iso_info.
	log(str.format("iso_info -> {}", iso_info), LOGDEBUG)
	return iso_info

def extract_files(iso_file, iso_info, iso_folder, xbe_partitions=8, files={"default.xbe", "game.xbe"}):
	# seek to root sector
	iso_file.seek(iso_info['root_dir_sector'] * iso_info['sector_size'])

	# read the root sector into a bytes object
	with BytesIO() as root_sector_buffer:
		root_sector_buffer.write(iso_file.read(iso_info['root_dir_size']))
		root_sector_buffer.seek(0)

		# case insensitive search of root sector for default.xbe
		for i in range(0, iso_info['root_dir_size']):
			root_sector_buffer.seek(i)
			root_sector_buffer.read(1) # No idea why we're reading 1 byte here

			try:
				filename_length = unpack('<' + 'B' * 1,  root_sector_buffer.read(1))[ 0 ] # file_attribute
			except:
				continue

			for filename in files:
				if filename_length == len(filename) and root_sector_buffer.read(len(filename)).decode("ascii", "ignore").lower() == filename:
					root_sector_buffer.seek(i - 8)
					file_sector = unpack('I', root_sector_buffer.read(4))[0]
					file_size = unpack('I', root_sector_buffer.read(4))[0]

					# dump the xbe in parts for huge xbe files.
					# adding dangling size if xbe is not cleanly divisble by xbe_partitions
					dangling_partition_size = file_size % xbe_partitions
					file_partition_size = file_size / xbe_partitions

					with open(os.path.join(iso_folder, 'default.xbe'), "ab") as default_xbe:
						log(str.format("{} size is {} bytes, partition size is {} bytes, dangling size is {} bytes", filename, file_size, file_partition_size, dangling_partition_size), LOGDEBUG)
						for partition in range(0, xbe_partitions):
							iso_file.seek(file_sector * iso_info['sector_size'] + (file_partition_size*partition))
							default_xbe.write(iso_file.read(file_partition_size))

						# write the remainder of the the default.xbe
						if dangling_partition_size > 0:
							iso_file.seek(file_sector * iso_info['sector_size'] + (file_partition_size*xbe_partitions))
							default_xbe.write(iso_file.read(dangling_partition_size))

					log(str.format("Done extracting '{}' from '{}'", filename, os.path.basename(iso_file.name)), LOGDEBUG)
					return  # Return as there is only one file present, either 'game.xbe' or 'default.xbe'

def prepare_attachxbe(iso_folder):
	shutil.copyfile(os.path.join(os.getcwd(), "attach.xbe"), os.path.join(iso_folder, "attach.xbe"))

	# DEFAULT XBE TITLE
	with open(os.path.join(iso_folder, 'default.xbe'), 'rb', buffering=4096) as default_xbe:
		# move to base address
		default_xbe.seek(260, 0)
		base = default_xbe.read(4)
		# move to cert address
		default_xbe.seek(280, 0)
		cert = default_xbe.read(4)
		# get the location of the cert
		certAddress = unpack("i", cert)  # init32 values
		baseAddress = unpack("i", base)  # init32 values
		loc = certAddress[0] - baseAddress[0]
		# move to the titleid
		default_xbe.seek(loc + 8, 0)
		xbe_certificate = default_xbe.read(168)

	# I'm not too worried about reuising all these vars...
	# ATTACH XBE FILE
	with open(os.path.join(iso_folder, 'attach.xbe'), 'r+b', buffering=4096) as attach_xbe:
		# move to base address
		attach_xbe.seek(260, 0)
		base = attach_xbe.read(4)
		# move to cert address
		attach_xbe.seek( 280, 0)
		cert = attach_xbe.read(4)
		# get the location of the cert
		certAddress = unpack("i", cert)  # init32 values
		baseAddress = unpack("i", base)  # init32 values
		loc = certAddress[0] - baseAddress[0]
		# move to the titleid
		attach_xbe.seek(loc + 8, 0)
		attach_xbe.write(xbe_certificate)

	default_xbe = os.path.join(iso_folder, "default.xbe")

	try:  # this is to move on if there is an error with extracting the image.
		XBE(default_xbe).Get_title_image().Write_PNG(os.path.join("Z:\\default.png"))
	except:
		log("Memory ran out when trying to extract TitleImage.xbx.", LOGERROR)
		log("So using alternative way.", LOGERROR)

		try:  # if the memory runs out this one works.
			xbeinfo(default_xbe).image_png()
		except:
			log("Cannot extract TitleImage.xbx.", LOGERROR)
			log("Unsupported format or XBE is to large for current system memory.", LOGERROR)
			traceback.print_exc()

	default_tbn = os.path.join(iso_folder, 'default.tbn')
	if os.path.isfile('Z:\\default.png'):
		shutil.move('Z:\\default.png', default_tbn)
		shutil.copy2(default_tbn, os.path.join(iso_folder, 'icon.png'))
	else:
		shutil.copy2(os.path.join(os.getcwd(), 'missing.jpg'), default_tbn)
		shutil.copy2(os.path.join(os.getcwd(), 'missing.jpg'), os.path.join(iso_folder, 'icon.png'))
	if os.path.isfile('Z:\\TitleImage.png'): os.remove('Z:\\TitleImage.xbx')

	os.remove(default_xbe)
	os.rename(os.path.join(iso_folder, "attach.xbe"), default_xbe)

def process_iso_name(file_name):
	iso_full_name = file_name[:-4].replace('_1', '').replace('_2', '').replace('.1', '').replace('.2', '')
	iso_name = iso_full_name.split('(', 1)[0]
	iso_folder_name = iso_name[:36] if len(iso_name) > 36 else iso_name  # truncate the name to 42 characters, reason is the .iso

	return iso_full_name, iso_folder_name

def process_iso(file_path, iso_directory):
	iso_info = None
	file_name = os.path.basename(file_path)
	iso_full_name, iso_folder_name = process_iso_name(file_name)
	iso_folder = os.path.join(iso_directory, iso_folder_name + ' (ISO)')

	log(str.format("Processing {}", file_name))

	with open(file_path, 'rb') as iso_file:
		iso_info = check_iso(iso_file)  # check that iso is an xbox game and extract some details

		if iso_info:  # doesn't work, if no xbe files is found inside the xiso. (yeah I was testing and forgot the xbe lol)
			if not os.path.isdir(iso_folder):
				os.mkdir(iso_folder)  # make a new folder for the current game
			extract_files(iso_file, iso_info, iso_folder)  # find and extract default.xbe from the iso

	if iso_info:
		try:
			# Patch the title+id into attach.xbe...
			prepare_attachxbe(iso_folder)

			# Search for other parts of current ISO and move them into the directory.
			if '.1.' in file_name:
				for iso_part_image in glob.iglob(os.path.join(iso_directory, iso_full_name + '.*.iso')):
					shutil.move(os.path.join(iso_directory, iso_part_image), iso_folder)
			if '_1' in file_name:
				for iso_part_image in glob.iglob(os.path.join(iso_directory, iso_full_name + '_*.iso')):
					shutil.move(os.path.join(iso_directory, iso_part_image), iso_folder)

		except:
			shutil.rmtree(iso_folder)
			log("Not a valid XISO?", LOGERROR)
			log("Could not prepare the attach.xbe with extracted values from default.xbe", LOGERROR)
			traceback.print_exc()
			dialog.ok("ERROR: 2 ", "Not a valid XISO?", "Could not prepare the [B]attach.xbe[/B]", file_path)
	else:
		log(str.format("ISO info could not be obtained, skipping '{}'", file_name), LOGDEBUG)

if __name__ == "__main__":
	log("| Scripts\XBMC4Gamers Extras\XISO to HDD Installer\default.py loaded.")
	progress_dialog = DialogProgress()
	dialog = Dialog()
	search_directory = dialog.browse(0, "Select a folder", "files")

	if search_directory:
		# progress bar
		progress_dialog.create("XISO to HDD Installer")
		progress_dialog.update(0)

		num_iso_files = len([ iso for iso in glob.iglob(search_directory + "*.iso")])

		log(str.format("Searching '{}' for iso files!", search_directory), LOGDEBUG)
		for idx, iso_file in enumerate(sorted(glob.iglob(search_directory + "*.iso"))):
			# If second part of ISO has been moved by process_iso, we skip to the next part.
			if os.path.isfile(iso_file):
				progress_dialog.update(((idx + 1) * 100) / num_iso_files, "Scanning XISO Files", iso_file,)
				try:
					process_iso(iso_file, search_directory)
				except:
					progress_dialog.close()
					log("Script has failed", LOGERROR)
					traceback.print_exc()
					dialog.ok("ERROR:", "", 'Script has failed\nlast entry = ' + iso_file)
					break
		else:
			progress_dialog.close()
			dialog.ok("XISO to HDD Installer", "", "Everything is setup.", "You just launch the game/s like normal.")

		if num_iso_files == 0:
			dialog.ok("ERROR:", "", "No XISO files found")
	else:
		log("No search directory was defined!", LOGDEBUG)

	log("================================================================================")