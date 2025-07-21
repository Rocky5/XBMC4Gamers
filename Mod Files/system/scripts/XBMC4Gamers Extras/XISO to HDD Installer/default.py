"""
	Script by Rocky5
	Used to prep a XISO so it can be playd from the Xbox HDD. It also extracts images and the xbe header so trainers work.
	Original script by headphone - https://www.emuxtras.net/forum/viewtopic.php?f=187&t=3228&start=40#p70178

	Updated by frehov (Fredr1kh#3002) thank you.
	Updated by me, changed a few things.
	Updated with the new Cerbios attach.xbe
"""
import glob
import os
import shutil
import time
import traceback
import zipfile
from binascii import unhexlify
from io import BytesIO
from itertools import groupby
from os.path import basename, dirname, getsize, isdir, isfile, join
from struct import pack, unpack, calcsize

from attacher import attacher_file
from xbe import *
from xbeinfo import *
from xbmc import log, LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO
from xbmcgui import Dialog, DialogProgress

# Close the script loading dialog
xbmc.executebuiltin('Dialog.Close(1100,true)')

# -----------------------------------------------------------------------------------
# Inspiration/code from: xbox360iso.py Copyright (c) 2014 Rob Lambell (MIT License)
#                        xbiso.pl (c) 30/06/2004 codex(at)bogus.net
#                        xboxsig.py Copyright (c) <2015> <Pete Stanley>
# -----------------------------------------------------------------------------------
def check_iso(iso_file):
	iso_info = {}
	with open(iso_file, 'rb') as iso:
		# check for validity
		iso.seek(0x10000)
		if iso.read(0x14).decode("ascii", "ignore") == 'MICROSOFT*XBOX*MEDIA':  # read tailend of header
			iso_info['sector_size'] = 0x800

			# read the directory table
			iso_info['root_dir_sector'] = unpack('I', iso.read(4))[0]  # dtable
			iso_info['root_dir_size'] = unpack('I', iso.read(4))[0]
		else:
			log("header tail mismatch -- possible corruption?", LOGFATAL)
			log("this doesn't appear to be an xbox iso image", LOGFATAL)

	# an empty dictionary is falsy, so just return the iso_info.
	log(str.format("iso_info -> {}", iso_info), LOGDEBUG)
	return iso_info

def extract_files(iso_files, iso_info, game_iso_folder, xbe_partitions=8, files={"default.xbe", "game.xbe"}):
	# write the remainder of the xbe
	buffer_size = 1048576 # 1mb buffer
	iso_size = getsize(iso_files[0])
	isos = [open(x, 'rb') for x in iso_files]

	try:
		iso = isos[0]
		with BytesIO() as root_sector_buffer:
			# seek to root sector
			iso.seek(iso_info['root_dir_sector'] * iso_info['sector_size'])

			# read the root sector into a bytes object
			root_sector_buffer.write(iso.read(iso_info['root_dir_size']))
			root_sector_buffer.seek(0)

			# case insensitive search of root sector for default.xbe
			for i in range(0, iso_info['root_dir_size']):
				root_sector_buffer.seek(i)
				root_sector_buffer.read(1)  # No idea why we're reading 1 byte here (script fails to extract if it's not here)

				try:
					filename_length = unpack('<' + 'B' * 1,  root_sector_buffer.read(1))[0]  # filename length in directory table
				except:
					continue

				for filename in files:
					if filename_length == len(filename) and root_sector_buffer.read(len(filename)).decode("ascii", "ignore").lower() == filename:
						root_sector_buffer.seek(i - 8)
						file_sector = unpack('I', root_sector_buffer.read(4))[0]
						file_size = unpack('I', root_sector_buffer.read(4))[0]
						file_offset = file_sector * iso_info['sector_size']

						# dump the xbe in parts for huge xbe files.
						# adding dangling size if xbe is not cleanly divisible by xbe_partitions
						dangling_partition_size = file_size % xbe_partitions
						file_partition_size = file_size / xbe_partitions

						# File could be located in part 2 of the iso.
						if file_offset > iso_size:
							log(str.format("{} is not located in '{}', skipping to '{}', file_sector {}, file_offset {}", filename, basename(iso.name), basename(iso_files[1]), file_sector, file_offset), LOGDEBUG)
							file_offset = file_offset - iso_size  # Set the correct offset for second iso(?).
							iso = isos[1]  # switch file handle

						iso.seek(file_offset)  # Move to the correct file

						log(str.format("{} size is {} bytes, partition size is {} bytes, dangling size is {} bytes", filename, file_size, file_partition_size, dangling_partition_size), LOGDEBUG)
						with open(join(game_iso_folder, filename), "wb") as xbe:  # write binary, truncating file before writing.
							for partition in range(0, xbe_partitions):
								try:
									xbe.write(iso.read(file_partition_size))
								except:
									while file_partition_size > 0:
										if file_partition_size < buffer_size:
											buffer_size = file_partition_size
										xbe.write(iso.read(buffer_size))
										file_partition_size -= buffer_size

							# write the remainder of the xbe
							if dangling_partition_size > 0:
								try:
									xbe.write(iso.read(dangling_partition_size))
								except:
									while dangling_partition_size > 0:
										if dangling_partition_size < buffer_size:
											buffer_size = dangling_partition_size
										xbe.write(iso.read(buffer_size))
										dangling_partition_size -= buffer_size

						log(str.format("Done extracting '{}' from '{}', size is {} bytes", filename, basename(iso.name), getsize(join(game_iso_folder, filename))), LOGDEBUG)
				iso = isos[0]  # Reset filehandle back to file number 1.
	finally:
		for iso in isos:
			iso.close()

def prepare_attachxbe(game_iso_folder):
	default_xbe_path = join(game_iso_folder, "default.xbe")
	attacher_xbe_path = join(game_iso_folder, 'attach.xbe')

	# attach.xbe in hex
	attach_bytes = unhexlify(attacher_file)
	with open(attacher_xbe_path, 'wb') as attach_xbe:
		attach_xbe.write(attach_bytes)

	# DEFAULT XBE TITLE
	with open(default_xbe_path, 'rb', buffering=4096) as default_xbe:
		default_xbe.seek(260, 0)  # move to base address
		base = default_xbe.read(4)

		default_xbe.seek(280, 0)  # move to cert address
		cert = default_xbe.read(4)

		# get the location of the cert
		certAddress = unpack("i", cert)[0]  # init32 values
		baseAddress = unpack("i", base)[0]  # init32 values

		default_xbe.seek((certAddress - baseAddress), 0)  # move to the titleid
		xbe_certificate = default_xbe.read(464) # grab the full certificate

	# ATTACH XBE FILE
	with open(attacher_xbe_path, 'r+b') as attach_xbe:
		attach_xbe.seek(260, 0)  # move to base address
		base = attach_xbe.read(4)

		attach_xbe.seek(280, 0)  # move to cert address
		cert = attach_xbe.read(4)
		
		# get the location of the cert
		certAddress = unpack("i", cert)[0]  # init32 values
		baseAddress = unpack("i", base)[0]  # init32 values

		attach_xbe.seek((certAddress - baseAddress), 0)  # move to the titleid
		attach_xbe.write(xbe_certificate)
		
		attach_xbe.seek((certAddress - baseAddress + 172), 0)  # move to the version
		attach_xbe.write(unhexlify('01000080'))

		# I'm not too worried about reusing all these vars...
		# Read titleimage.xbx
		if isfile('Z:\\TitleImage.xbx'):
			with open('Z:\\TitleImage.xbx', 'rb') as xbe_xbx:
				image_data = xbe_xbx.read()
				xbx_size = getsize('Z:\\TitleImage.xbx')
				xbx_sizehex = "%08x" % int(xbx_size)
				
				print xbx_sizehex
				
				attach_xbe.seek(1060, 0)  # move to xpr0 virtual address
				imageAddress = unpack("i", attach_xbe.read(4))[0]  # init32 values

				base_size = (xbx_size + imageAddress) # <-- is the data size before the XPR0 required
				base_sizehex = "%08x" % int(base_size)
				
				# Write values to attach.xbe
				attach_xbe.seek(268, 0)  # move to base file size
				attach_xbe.write(to_little_endian(base_sizehex))
				
				attach_xbe.seek(1056, 0)  # move to xpr0 virtual size address
				attach_xbe.write(to_little_endian(xbx_sizehex))
				
				attach_xbe.seek(1064, 0)  # move to xpr0 raw size address
				attach_xbe.write(to_little_endian(xbx_sizehex))
				
				attach_xbe.seek(imageAddress, 0)  # move to xpr0 start offset
				attach_xbe.write(image_data)

			os.remove('Z:\\TitleImage.xbx')

	os.remove(default_xbe_path)
	os.rename(attacher_xbe_path, default_xbe_path)

def to_little_endian(hex_str):
    swapped = hex_str[6:8] + hex_str[4:6] + hex_str[2:4] + hex_str[0:2]
    return unhexlify(swapped)

def install_artwork_resources(game_iso_folder, artwork_zip):
	try:
		extract_zip(artwork_zip, game_iso_folder)

		game_artwork_path = join(game_iso_folder, "_resources", "artwork")
		for source_file, destination_file in [("thumb.jpg", "icon.png"), ("poster.jpg", "default.tbn"), ("fanart.jpg", "fanart.jpg")]:
			shutil.copy2(join(game_artwork_path, source_file), join(game_iso_folder, destination_file))

	except:
		pass  # This shouldn't happen

def get_artwork_resources(artwork_path):
	artwork = {}
	try:
		artwork_db = join(artwork_path, "system", "scripts", "Artwork Info.txt")
		artwork_root_folder = join(artwork_path, "system", "scripts", "Artwork")

		if isfile(artwork_db):
			with open(artwork_db, 'r') as database:
				log(database.readline(), LOGDEBUG)  # Skip the first line containing amount of artwork

				for entry in database:
					if not entry.startswith("n/a"):
						title_id, artwork_folder = entry.strip().split('|')
						artwork[title_id.lower()] = join(artwork_root_folder, artwork_folder, "_resources.zip")
	except:
		traceback.print_exc()
		log("Something went wrong installing artwork. Corrupt zip?", LOGERROR)

	return artwork

def extract_title_image(game_iso_folder):
	script_root_dir = os.getcwd()
	default_xbe = join(game_iso_folder, "default.xbe")
	
	if isfile('Z:\\TitleImage.xbx'): # cleanup so there are no errors when starting
		os.remove('Z:\\TitleImage.xbx')

	log("Trying to extract TitleImage.xbx.", LOGINFO)
	# XBE(default_xbe).Get_title_image().Write_PNG(join("Z:\\default.png"))
	XBE(default_xbe).Get_title_xpr0()

	if not isfile('Z:\\TitleImage.xbx'):
		try:  # if the memory runs out this one should work.
			log("Using alternative extraction method for TitleImage.xbx.", LOGINFO)
			xbeinfo(default_xbe).image_png()
			if isfile('Z:\\default.png'):
				# shutil.copy2('Z:\\default.png', join(game_iso_folder, 'default.tbn'))
				os.remove('Z:\\default.png')
		except:
			log("Cannot extract TitleImage.xbx.", LOGERROR)
			log("Unsupported format or XBE is to large for current system memory.", LOGERROR)
			traceback.print_exc()

	# Header check of extracted XPR0 file, as some games have PNG :/
	try:
		if isfile('Z:\\TitleImage.xbx'):
			with open('Z:\\TitleImage.xbx', 'rb') as xbx_check:
				header = xbx_check.read(4)
			if not header == "XPR0":
				os.remove('Z:\\TitleImage.xbx')
	except:
		log("TitleImage.xbx maybe corrupt.", LOGERROR)

	# If no titleimage is extracted or is invalid add missing image
	default_tbn = join(game_iso_folder, 'default.tbn')
	if not isfile('Z:\\TitleImage.xbx'):
		shutil.copy2(join(script_root_dir, 'missing.jpg'), default_tbn)
		shutil.copy2(default_tbn, join(game_iso_folder, 'icon.png'))

def extract_titleid(xbe_file):  # Need to use this as the xbe.py Get_title misses letter and causes string issues, even when using .encode or .decode
	with open(xbe_file, 'rb', buffering=4096) as xbe:
		xbe.seek(0x104)
		loadAddr = unpack('L', xbe.read(4))[0]

		xbe.seek(0x118)
		certLoc = unpack('L', xbe.read(4))[0]

		xbe.seek((certLoc - loadAddr) + 8)
		id_data = unpack('L', xbe.read(4))

		xbe_title = ''
		for dta in unpack("40H", xbe.read(calcsize("40H"))):
			try:
				if dta != 00:
					xbe_title += str(unichr(dta))
			except:
				pass

		return str(hex(id_data[0])[2:10]).upper().zfill(8)

def extract_zip(zip_file, game_iso_folder):
	with zipfile.ZipFile(zip_file, 'r') as resource:
		resource.extractall(game_iso_folder)

def check_for_gamexbe(game_iso_folder):
	default_xbe = join(game_iso_folder, 'default.xbe')
	game_xbe = join(game_iso_folder, 'game.xbe')

	if isfile(game_xbe):
		os.remove(default_xbe)
		os.rename(game_xbe, default_xbe)
		log(str.format("Found game.xbe: '{}' renaming to  '{}'", game_xbe, default_xbe), LOGDEBUG)

def process_iso_name(file_name):
	base_name, extension = basename(file_name).rsplit('.', 1)
	iso_full_name = (base_name[:-2]) if any(base_name.endswith(suffix) for suffix in ['_1', '_2', '.1', '.2']) else base_name
	iso_name = iso_full_name.split('(', 1)[0].strip()
	iso_folder_name = iso_name[:36] if len(iso_name) > 36 else iso_name  # truncate the name to 42 characters, reason is the .iso

	return iso_full_name, iso_folder_name

def process_iso(iso_files, root_iso_directory, artwork_resources):
	file_name = basename(iso_files[0])
	iso_full_name, iso_folder_name = process_iso_name(file_name)
	game_iso_folder = join(root_iso_directory, iso_folder_name + ' (ISO)')

	iso_info = check_iso(iso_files[0])  # check that iso is an xbox game and extract some details
	if iso_info:  # doesn't work, if no xbe files is found inside the xiso. (yeah I was testing and forgot the xbe lol)
		if not isdir(game_iso_folder):
			os.mkdir(game_iso_folder)  # make a new folder for the current game

		extract_files(iso_files, iso_info, game_iso_folder)  # find and extract default.xbe/game.xbe from the iso
		check_for_gamexbe(game_iso_folder)  # Check if we extracted a game.xbe and rename to default.xbe if found

		title_id = extract_titleid(join(game_iso_folder, "default.xbe")).lower()  # Get the titleid from default.xbe
		
		log(str.format("Extracting TitleImage.xbx for title id '{}' - '{}'", title_id, game_iso_folder), LOGDEBUG)
		try:
			extract_title_image(game_iso_folder)  # Extract title image from default.xbe
		except:
			log(str.format("Failed to extract TitleImage.xbx for title id '{}' - '{}'", title_id, game_iso_folder), LOGDEBUG)
		
		if title_id in artwork_resources:
			log(str.format("Installing artwork for title id '{}' to folder '{}'", title_id, game_iso_folder), LOGINFO)

			install_artwork_resources(game_iso_folder, artwork_resources[title_id])  # Install resources from artwork installer
			log(str.format("Artwork installed to '_resources'-folder for title id '{}' in '{}'", title_id, game_iso_folder), LOGINFO)

		try:
			# Patch the title+id into attach.xbe...
			prepare_attachxbe(game_iso_folder)
			# Search for all parts of current ISO and move them into the directory.
			try:
				for iso_part_image in iso_files:
					iso_name = basename(iso_part_image)
					folder_name = dirname(iso_part_image)
					log(str.format("Moving '{}' into '{}'", iso_part_image, game_iso_folder), LOGDEBUG)
					shutil.move(iso_part_image, game_iso_folder)
					if any(iso_part_image.endswith(suffix) for suffix in ['_1.iso', '_2.iso']):
						new_iso_name = join(game_iso_folder, basename(iso_part_image.replace("_1.", ".1.").replace("_2.", ".2.")))
						os.rename(join(game_iso_folder, iso_name), new_iso_name)
			except:
				shutil.move(join(game_iso_folder, iso_name), folder_name)
				log(str.format("Cant rename '{}' to '{}'", iso_name, basename(new_iso_name)), LOGERROR)
				traceback.print_exc()
				dialog.ok("ERROR: 2 Can't rename ISO file", "File already exists", "{}[CR]{}".format(iso_name, basename(new_iso_name)), '')
				# shutil.rmtree(game_iso_folder)
		except:
			log("Not a valid XISO?", LOGERROR)
			log("Could not prepare the attach.xbe with extracted values from default.xbe", LOGERROR)
			traceback.print_exc()
			dialog.ok("ERROR: 1 Not a valid XISO?", "", "Could not prepare the [B]attach.xbe[/B]", iso_files)
			shutil.rmtree(game_iso_folder)

	else:
		log(str.format("ISO info could not be obtained, skipping '{}'", file_name), LOGDEBUG)


if __name__ == "__main__":
	log("| Scripts\XBMC4Gamers Extras\XISO to HDD Installer\default.py loaded.")
	progress_dialog = DialogProgress()
	dialog = Dialog()
	search_directory = dialog.browse(0, "Select a folder", "files")
	artwork_installer = join("E:\\", "UDATA", "09999993", "location.bin")
	skip_artwork_install = False
	
	# Check if its online or offline installer
	if isfile(artwork_installer):
		with open(artwork_installer) as path:
			artwork_path = path.readline()
		artwork_homexml = join(artwork_path, "skins", "default", "xml", "home.xml")
		with open(artwork_homexml, 'r') as check:
			if 'online' in check.read().lower():
				# Try checking for the offline version just in case its in the same location
				artwork_path = artwork_path.replace(' Online', '')
				if not isdir(artwork_path):
					skip_artwork_install = True
					log(str.format("Online Artwork Installer found. Skipping artwork installation", artwork_path), LOGDEBUG)
	else:
		log("Artwork installer not installed or hasn't been run for the first time.", LOGERROR)

	if search_directory:
		log(str.format("Searching '{}' for iso files!", search_directory), LOGDEBUG)

		artwork_resources = "Null"
		if isfile(artwork_installer) and not skip_artwork_install:
			artwork_resources = get_artwork_resources(artwork_path)  # Prefetch artwork resource locations
		
		num_iso_files = len([iso for iso in glob.iglob(search_directory + "*.iso")])

		grouped_iso_files = groupby(
			sorted(glob.glob(search_directory + "*.iso")),
			lambda file_name: basename(process_iso_name(file_name)[0])
		)

		progress_dialog.create("XISO to HDD Installer")
		progress_dialog.update(0)

		if num_iso_files == 0:
			progress_dialog.close()
			dialog.ok("ERROR:", "", "No XISO files found")
		else:
			for idx, entry in enumerate(grouped_iso_files):
				name = entry[0]
				iso_files = list(entry[1])
				log(str.format("Processing {} - {}", name, iso_files))

				progress_dialog.update(((idx + 1) * 100) / num_iso_files, "Scanning XISO Files", iso_files[0],)  # TODO fix this after adding grouping
				try:
					process_iso(iso_files, search_directory, artwork_resources)
				except:
					log("Script has failed", LOGERROR)
					traceback.print_exc()
					dialog.ok("ERROR:", "", 'Script has failed\nlast entry = ' + iso_files[0])
					continue

				if progress_dialog.iscanceled():
					log(str.format("User terminated scanning, stopping after '{}'", iso_files[0]), LOGDEBUG)
					progress_dialog.close()
					break
			else:
				progress_dialog.close()
				dialog.ok("XISO to HDD Installer", "", "Everything is setup.", "You just launch the game/s like normal.")

	else:
		log("No search directory was defined!", LOGDEBUG)

	log("================================================================================")