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
	if iso_file.read(0x14).decode("ascii", "ignore") == 'MICROSOFT*XBOX*MEDIA':
		iso_info['sector_size'] = 0x800
		## read the directory table
		iso_file.seek(0x10014)
		iso_info['root_dir_sector'] = unpack('I', iso_file.read(4))[0] #dtable
		iso_info['root_dir_size'] = unpack('I', iso_file.read(4))[0]
		return iso_info
		iso_file.seek(0x107ec) # skip unused info
	elif iso_file.read(0x14).decode("ascii", "ignore") != 'MICROSOFT*XBOX*MEDIA':  # read tailend of header
		print("FATAL: header tail mismatch -- possible corruption?")
		print("FATAL: this doesn't appear to be an xbox iso image")
		return False
def extract_defaultxbe(iso_file, iso_info):
	#seek to root sector
	iso_file.seek((iso_info[ 'root_dir_sector' ] * iso_info[ 'sector_size' ]))
	# read the root sector into a bytes object
	root_sector_buffer = io.BytesIO()
	root_sector_buffer.write(iso_file.read(iso_info[ 'root_dir_size' ]))
	root_sector_buffer.seek(0)
	# case insensitive search of root sector for default.xbe
	for i in range(0, iso_info[ 'root_dir_size' ] - 12):
		root_sector_buffer.seek(i)
		root_sector_buffer.read(1)  # file_attribute
		if struct.unpack('<'+'B'*1, root_sector_buffer.read(1))[ 0 ] == 11:
			if root_sector_buffer.read(11).decode("ascii", "ignore").lower() == "default.xbe":
				# found default.xbe
				root_sector_buffer.seek(i - 8)
				file_sector = unpack('I', root_sector_buffer.read(4))[ 0 ]
				file_size	= unpack('I', root_sector_buffer.read(4))[ 0 ]
				# dump the xbe quarterly for huge xbe file.
				file_size	= file_size / 4
				# seek to default.xbe
				iso_file.seek(file_sector * iso_info[ 'sector_size' ])
				# write default.xbe to a file
				# Had to split the xbe in quarters so the Xbox doesn't run out of memory.
				f = open(os.path.join(iso_folder,"default.xbe"),"wb")
				f.write(iso_file.read(file_size))
				f.close()
				iso_file.seek(file_sector * iso_info[ 'sector_size' ]+file_size)
				f = open(os.path.join(iso_folder,"default.xbe"),"wb")
				f.seek(file_size)
				f.write(iso_file.read(file_size))
				f.close()
				iso_file.seek(file_sector * iso_info[ 'sector_size' ]+file_size+file_size)
				f = open(os.path.join(iso_folder,"default.xbe"),"wb")
				f.seek(file_size+file_size)
				f.write(iso_file.read(file_size))
				f.close()
				iso_file.seek(file_sector * iso_info[ 'sector_size' ]+file_size+file_size+file_size)
				f = open(os.path.join(iso_folder,"default.xbe"),"wb")
				f.seek(file_size+file_size+file_size)
				f.write(iso_file.read(file_size))
				f.close()
	root_sector_buffer.close()
def prepare_attachxbe(iso_filename):
	iso_name	= iso_filename[:-4].replace('_1','').replace('_2','').replace('.1','').replace('.2','').split('(',1)[0]
	iso_folder_name	= (iso_name[:36]) if len(iso_name) > 36 else iso_name # truncate the name to 42 characters, reason is the .iso.
	iso_folder		= os.path.join(ISO_Directory, iso_folder_name+' (ISO)')
	copyfile(os.path.join(Working_Directory,"attach.xbe"), os.path.join(iso_folder,"attach.xbe"))
	## DEFAULT XBE TITLE
	default_xbe_file = open(os.path.join(iso_folder,'default.xbe'),'rb')
	#move to base address
	default_xbe_file.seek(260, 0)
	base = default_xbe_file.read(4)
	#move to cert address
	default_xbe_file.seek(280, 0)
	cert = default_xbe_file.read(4)
	#get the location of the cert
	certAddress = unpack("i", cert) # init32 values
	baseAddress = unpack("i", base) # init32 values
	loc = certAddress[0] - baseAddress[0]
	#move to the titleid
	default_xbe_file.seek(loc+8, 0)
	xbe_certificate = default_xbe_file.read(168)
	default_xbe_file.close()
	##
	# I'm not too worried about reuising all these vars...
	# ATTACH XBE FILE
	attach_xbe_file = open(os.path.join(iso_folder,'attach.xbe'), 'r+b')
	#move to base address
	attach_xbe_file.seek(260, 0)
	base = attach_xbe_file.read(4)
	#move to cert address
	attach_xbe_file.seek( 280, 0)
	cert = attach_xbe_file.read(4)
	#get the location of the cert
	certAddress = unpack("i", cert) # init32 values
	baseAddress = unpack("i", base) # init32 values
	loc = certAddress[0] - baseAddress[0]
	#move to the titleid
	attach_xbe_file.seek(loc+8, 0)
	attach_xbe_file.write(xbe_certificate)
	attach_xbe_file.close()
	##	
	try: # this is to move on if there is an error with extracting the image.
		xbeinfo(os.path.join(iso_folder,"default.xbe")).image_png()
	except:
		print "| Error: Memory ran out when trying to extract TitleImage.xbx."
		print "|        So using alternative way."
		try: # if the memory runs out this one works.
			XBE(os.path.join(iso_folder,"default.xbe")).Get_title_image().Write_PNG(os.path.join("Z:\\default.png"))
		except:
			print "| Error: Cannot extract the default.png, haven't a clue why maybe its in DDS format?"
	if os.path.isfile('Z:\\default.png'):	shutil.move('Z:\\default.png',os.path.join(iso_folder,'default.tbn'))
	if os.path.isfile(os.path.join(iso_folder,'default.tbn')):	shutil.copy2(os.path.join(iso_folder,'default.tbn'),os.path.join(iso_folder,'icon.png'))
	if os.path.isfile('Z:\\TitleImage.xbx'):	os.remove('Z:\\TitleImage.xbx')
	os.remove(os.path.join(iso_folder,"default.xbe"))
	os.rename(os.path.join(iso_folder,"attach.xbe"),os.path.join(iso_folder,"default.xbe"))
def search_tree():
	global iso_folder
	CountList = 1
	for Item in sorted(os.listdir(ISO_Directory)):
		if os.path.isfile(os.path.join(ISO_Directory, Item)):
			if Item.lower().endswith(('.iso')):
				current_iso = os.path.join(ISO_Directory, Item)
				# progress bar
				if CountList == 1:
					pDialog.create("XISO to HDD Installer")
					pDialog.update(0)
					time.sleep(0.7)
				pDialog.update((CountList * 100) / len(os.listdir(ISO_Directory)),"Scanning XISO Files",ISO_Directory+Item,)
				iso_file = open(current_iso, 'rb') # open iso
				iso_full_name   = Item[:-4].replace('_1','').replace('_2','').replace('.1','').replace('.2','')
				iso_name        = iso_full_name.split('(',1)[0] # make a new folder for the current game
				iso_folder_name	= (iso_name[:36]) if len(iso_name) > 36 else iso_name # truncate the name to 42 characters, reason is the .iso.
				iso_folder		= os.path.join(ISO_Directory, iso_folder_name+' (ISO)')
				iso_info = check_iso(iso_file) # check iso is an xbox game and record some details
				if iso_info is False: # doesn't work, if no xbe files is found inside the xiso. (yeah I was testing and forgot the xbe lol)
					iso_file.close()
				os.mkdir(iso_folder)
				extract_defaultxbe(iso_file, iso_info) # find and extract default.xbe from the iso
				iso_file.close() # close iso
				try:
					# Patch the title+id into attach.xbe...
					prepare_attachxbe(Item)
					# Move the game ISO to its own folder!
					shutil.move(current_iso, iso_folder)
					# Search for other parts of current ISO and move them into the directory.
					if '.1.' in Item:
						for alt_images in glob.glob(os.path.join(ISO_Directory,iso_full_name+'.*.iso')):
							shutil.move(os.path.join(ISO_Directory,alt_images),iso_folder)
					if '_1' in Item:
						for alt_images in glob.glob(os.path.join(ISO_Directory,iso_full_name+'_*.iso')):
							shutil.move(os.path.join(ISO_Directory,alt_images),iso_folder)
					CountList = CountList+1
				except:
					pDialog.close()
					shutil.rmtree(iso_folder)
					print "ERROR 2 : Not a valid XISO?"
					print "ERROR 2 : Could not extract the Default.xbe"
					dialog.ok("ERROR: 2 ","Not a valid XISO?","Could not extract the [B]Default.xbe[/B]",current_iso)
Working_Directory	= os.getcwd()
ISO_Found = "False"
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
pDialog.update(0)
Root_Directory = dialog.browse(0,"Select a folder","files")
if Root_Directory !="":
	for Items in sorted(glob.glob(Root_Directory+"*.iso")):
		if os.path.isfile(Items):
			ISO_Directory = Root_Directory		
			ISO_Found = "True"
			try:
				search_tree()
				pDialog.close()
				dialog.ok("XISO to HDD Installer","","Everything is setup.","You just launch the game, or games like normal.")
			except:
				pDialog.close()
				print "ERROR: Script has failed"
				dialog.ok("ERROR:","",'Script has failed\nlast entry = '+Items)
	if not ISO_Found == "True":
		dialog.ok("ERROR:","","No XISO files found")
	print "================================================================================"