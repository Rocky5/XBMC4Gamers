'''
	Script by Rocky5
	Used to prep a XISO so it can be playd from the Xbox HDD. It also extracts images and the xbe header so trainers work.
	Original script by headphone - http://www.emuxtras.net/forum/viewtopic.php?f=187&t=3228&start=40#p70178
'''
import binascii, io, os, shutil, string, struct, sys, time, xbmcgui, glob
from shutil import copyfile
from struct import unpack
from limpp import Get_image
from xbe import *
from xbeinfo import *
print "| Scripts\XBMC4Gamers Extras\XISO to HDD Installer\default.py loaded."
#-----------------------------------------------------------------------------------
#Inspiration/code from:	xbox360iso.py Copyright (c) 2014 Rob Lambell (MIT License)
#						xbiso.pl (c) 30/06/2004 codex(at)bogus.net
#						xboxsig.py Copyright (c) <2015> <Pete Stanley>
#-----------------------------------------------------------------------------------
def check_iso(iso_file):
	iso_info = {}
	## check for validity
	iso_file.seek(0x10000)
	if iso_file.read(0x14).decode("ascii", "ignore") == 'MICROSOFT*XBOX*MEDIA': # read tailend of header
		iso_info['sector_size'] = 0x800
		## read the directory table
		iso_file.seek(0x10014)
		iso_info['root_dir_sector'] = unpack('I', iso_file.read(4))[0] #dtable
		iso_info['root_dir_size'] = unpack('I', iso_file.read(4))[0]
	else:
		print("FATAL: header tail mismatch -- possible corruption?")
		print("FATAL: this doesn't appear to be an xbox iso image")

	# an empty dictionary is falsy, so just return the iso_info.
	return iso_info

def extract_defaultxbe(iso_file, iso_info, xbe_partitions = 128):
	#seek to root sector
	iso_file.seek(iso_info['root_dir_sector'] * iso_info['sector_size'])
	# read the root sector into a bytes object
	with io.BytesIO() as root_sector_buffer:
		root_sector_buffer.write(iso_file.read(iso_info['root_dir_size']))
		root_sector_buffer.seek(0)
		# case insensitive search of root sector for default.xbe
		for i in range(0, iso_info['root_dir_size'] - 12):
			root_sector_buffer.seek(i)
			file_attribute = struct.unpack('<'+'B'*1, root_sector_buffer.read(1))[ 0 ] # file_attribute
			
			if file_attribute == 11 and root_sector_buffer.read(11).decode("ascii", "ignore").lower() == "default.xbe":
				# found default.xbe
				root_sector_buffer.seek(i - 8)
				file_sector = unpack('I', root_sector_buffer.read(4))[ 0 ]
				file_size	= unpack('I', root_sector_buffer.read(4))[ 0 ]
				
				# dump the xbe in parts for huge xbe files.
				# adding dangling size if xbe is not cleanly divisble by xbe_partitions
				dangling_partition_size = file_size % xbe_partitions 
				file_partition_size	= file_size / xbe_partitions

				with open(os.path.join(iso_folder, "default.xbe"), "ab") as default_xbe:
					print str.format("DEBUG: default.xbe size is {} bytes, partition size is {} bytes, dangling size is {} bytes", file_size, file_partition_size, dangling_partition_size)
					for partition in range(0, xbe_partitions):
						iso_file.seek(file_sector * iso_info['sector_size'] + (file_partition_size*partition))
						default_xbe.write(iso_file.read(file_partition_size))
					
					# write the remainder of the the default.xbe
					iso_file.seek(file_sector * iso_info['sector_size'] + (file_partition_size*xbe_partitions))
					default_xbe.write(iso_file.read(dangling_partition_size))
				
				print str.format("| DEBUG: Done writing default.xbe for '{}', file size: {}", os.path.basename(iso_file.name), str(os.path.getsize(os.path.join(iso_folder,"default.xbe"))))

def prepare_attachxbe(iso_folder):
	copyfile(os.path.join(Working_Directory, "attach.xbe"), os.path.join(iso_folder, "attach.xbe"))
	
	## DEFAULT XBE TITLE
	with open(os.path.join(iso_folder, 'default.xbe'), 'rb') as default_xbe:
		#move to base address
		default_xbe.seek(260, 0)
		base = default_xbe.read(4)
		#move to cert address
		default_xbe.seek(280, 0)
		cert = default_xbe.read(4)
		#get the location of the cert
		certAddress = unpack("i", cert) # init32 values
		baseAddress = unpack("i", base) # init32 values
		loc = certAddress[0] - baseAddress[0]
		#move to the titleid
		default_xbe.seek(loc + 8, 0)
		xbe_certificate = default_xbe.read(168)
		
	# I'm not too worried about reuising all these vars...
	# ATTACH XBE FILE
	with open(os.path.join(iso_folder, 'attach.xbe'), 'r+b') as attach_xbe:
		#move to base address
		attach_xbe.seek(260, 0)
		base = attach_xbe.read(4)
		#move to cert address
		attach_xbe.seek( 280, 0)
		cert = attach_xbe.read(4)
		#get the location of the cert
		certAddress = unpack("i", cert) # init32 values
		baseAddress = unpack("i", base) # init32 values
		loc = certAddress[0] - baseAddress[0]
		#move to the titleid
		attach_xbe.seek(loc + 8, 0)
		attach_xbe.write(xbe_certificate)

	default_xbe = os.path.join(iso_folder, "default.xbe")

	try: # this is to move on if there is an error with extracting the image.
		xbeinfo(default_xbe).image_png()
	except Exception as exc:
		print "| Error: Memory ran out when trying to extract TitleImage.xbx."
		print "|        So using alternative way.", exc

		try: # if the memory runs out this one works.
			XBE(default_xbe).Get_title_image().Write_PNG(os.path.join("Z:\\default.png"))
		except Exception as exc:
			print "| Error: Cannot extract the default.png, haven't a clue why maybe its in DDS format?", exc
	
	default_tbn = os.path.join(iso_folder, 'default.tbn')
	if os.path.isfile('Z:\\default.png'):
		shutil.move('Z:\\default.png', default_tbn)
	
	if os.path.isfile(default_tbn):
		shutil.copy2(default_tbn, os.path.join(iso_folder, 'icon.png'))
		
	if os.path.isfile('Z:\\TitleImage.xbx'):
		os.remove('Z:\\TitleImage.xbx')
	
	os.remove(default_xbe)
	os.rename(os.path.join(iso_folder, "attach.xbe"), default_xbe)

def search_tree():
	global iso_folder
	processed_files = []
	CountList = 1

	# progress bar
	pDialog.create("XISO to HDD Installer")
	pDialog.update(0)
	time.sleep(0.7)

	iso_files = [(item, os.path.join(ISO_Directory, item)) for item in sorted(os.listdir(ISO_Directory)) if os.path.isfile(os.path.join(ISO_Directory, item)) and item.lower().endswith('.iso')]


	for file_name, file_path in iso_files:
		iso_info        = None
		iso_full_name   = file_name[:-4].replace('_1', '').replace('_2', '').replace('.1', '').replace('.2', '')
		iso_name        = iso_full_name.split('(', 1)[0]
		iso_folder_name	= iso_name[:36] if len(iso_name) > 36 else iso_name # truncate the name to 42 characters, reason is the .iso
		iso_folder		= os.path.join(ISO_Directory, iso_folder_name + ' (ISO)')
		
		pDialog.update((CountList * 100) / len(iso_files), "Scanning XISO Files", file_path,)

		if iso_full_name in processed_files:
			CountList = CountList + 1
			continue
		
		print str.format("DEBUG: Processing {}", file_name)
		processed_files.append(iso_full_name)

		with open(file_path, 'rb') as iso_file:
			iso_info = check_iso(iso_file) # check iso is an xbox game and record some details
			
			if iso_info: # doesn't work, if no xbe files is found inside the xiso. (yeah I was testing and forgot the xbe lol)
				os.mkdir(iso_folder) # make a new folder for the current game
				extract_defaultxbe(iso_file, iso_info) # find and extract default.xbe from the iso
		
		if iso_info:
			try:
				# Patch the title+id into attach.xbe...
				prepare_attachxbe(iso_folder)
				
				# Move the game ISO to its own folder!
				shutil.move(file_path, iso_folder)
				
				# Search for other parts of current ISO and move them into the directory.
				if '.1.' in file_name:
					for iso_part_image in glob.glob(os.path.join(ISO_Directory, iso_full_name + '.*.iso')):
						shutil.move(os.path.join(ISO_Directory, iso_part_image), iso_folder)
				if '_1' in file_name:
					for iso_part_image in glob.glob(os.path.join(ISO_Directory, iso_full_name + '_*.iso')):
						shutil.move(os.path.join(ISO_Directory, iso_part_image), iso_folder)
				CountList = CountList + 1
			
			except Exception as exc:
				pDialog.close()
				shutil.rmtree(iso_folder)
				print "ERROR 2 : Not a valid XISO?"
				print "ERROR 2 : Could not extract the Default.xbe"
				print "ERROR 2 : Exception follows", exc
				dialog.ok("ERROR: 2 ", "Not a valid XISO?", "Could not extract the [B]Default.xbe[/B]", file_path)
		else:
			print str.format("DEBUG : ISO info could not be obtained, skipping '{}'", iso_full_name)

Working_Directory	= os.getcwd()
ISO_Found = "False"
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
pDialog.update(0)
Root_Directory = dialog.browse(0, "Select a folder", "files")
if Root_Directory !="":
	for Items in sorted(glob.glob(Root_Directory + "*.iso")):
		if os.path.isfile(Items):
			ISO_Directory = Root_Directory		
			ISO_Found = "True"
			try:
				search_tree()
				pDialog.close()
				dialog.ok("XISO to HDD Installer", "", "Everything is setup.", "You just launch the game, or games like normal.")
			except Exception as exc:
				pDialog.close()
				print "ERROR: Script has failed", exc
				dialog.ok("ERROR:", "", 'Script has failed\nlast entry = ' + Items)
	if not ISO_Found == "True":
		dialog.ok("ERROR:", "", "No XISO files found")
	print "================================================================================"