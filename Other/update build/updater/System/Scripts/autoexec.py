# -*- coding: utf-8 -*-
import os
import shutil
import hashlib
import zipfile
import fileinput
import time
import xbmcgui
import zipfile

root_directory	= xbmc.translatePath("Special://root/")[:-8]

zip_file = os.path.join(root_directory, 'updater/Update Files/update-files.zip')
hash_file = os.path.join(root_directory, 'updater/Update Files/md5hash.bin')

xbmc.executebuiltin('Skin.SetString(DashboardUpdatedSmall,0)')
xbmc.executebuiltin('Skin.Reset(DashboardUpdated)')

pDialog	= xbmcgui.DialogProgress()
dialog	= xbmcgui.Dialog()

md5hash = hashlib.md5()
cleanupafter = 0
failed = 0


if os.path.isfile(zip_file):
	with open(hash_file,"r") as ziphash:
		zip_hash = ziphash.readline().rstrip()
	
	with open(zip_file,"rb", buffering=4096) as updatefile:
		md5hash.update(updatefile.read())
	
	if md5hash.hexdigest() == zip_hash:
		pDialog.create('Stage 2 of 2')
		pDialog.update(0,"Download complete","Updating dashboard")
		
		if not os.path.isfile(root_directory+'system/keymaps/Enabled'):
			cleanupafter = 1

		# Rename skin directories
		rename_pairs = [
			(os.path.join(root_directory, 'skins/Profile Skin'), os.path.join(root_directory, 'skins/Profile')),
			(os.path.join(root_directory, 'skins/Manage Profiles Skin'), os.path.join(root_directory, 'skins/Manage Profiles'))
		]
		for old_path, new_path in rename_pairs:
			if os.path.isdir(old_path) and not os.path.isdir(new_path):
				os.rename(old_path, new_path)

		# Removals for Manage Profiles files
		manage_profiles_xml = os.path.join(root_directory, 'skins/Manage Profiles/xml')
		if os.path.isdir(manage_profiles_xml):
			files_to_remove = [
				'Includes_Context_Buttons.xml',
				'Includes_Snow.xml',
				'Includes_Birthday.xml',
				'Includes_Easter.xml',
				'Includes_Particles.xml'
			]
			for file in files_to_remove:
				file_path = os.path.join(manage_profiles_xml, file)
				if os.path.isfile(file_path):
					os.remove(file_path)

		# Removals for Profile files
		profile_xml = os.path.join(root_directory, 'skins/Profile/xml')
		if os.path.isdir(profile_xml):
			files_to_remove = [
				'Custom_View_Options.xml',
				'Includes_Recent_Played.xml',
				'Viewtype_54_Panel.xml',
				'Viewtype_56_Card.xml',
				'Viewtype_61_CarouselSmaller.xml',
				'_Script_Synopsis.xml',
				'Includes_Busy_ScriptBusy.xml',
				'Includes_Theme_Override.xml',
				'Includes_Context_Buttons.xml',
				'Includes_Fallback_View.xml',
				'Includes_Variables.xml',
				'Includes_View_Options.xml',
				'Custom_Skin_Settings.xml',
				'Custom_Skin_Setting.xml'
			]
			for file in files_to_remove:
				file_path = os.path.join(profile_xml, file)
				if os.path.isfile(file_path):
					os.remove(file_path)

			# Remove files starting with 'Viewtype_View' and 'Viewtype_'
			for viewfile in os.listdir(profile_xml):
				if viewfile.startswith('Viewtype_View') or viewfile.startswith('Viewtype_'):
					os.remove(os.path.join(profile_xml, viewfile))

		# Remove directories and files
		paths_to_remove = [
			os.path.join(root_directory, 'system/scripts/.modules'),
			os.path.join(root_directory, 'system/toggles'),
			os.path.join(root_directory, 'skins/Manage Profiles/720p'),
			os.path.join(root_directory, 'skins/Profile/720p'),
			os.path.join(root_directory, 'skins/Profile/media/backgrounds'),
			os.path.join(root_directory, 'skins/Profile/extras/splashes'),
			os.path.join(root_directory, 'skins/Profile/extras/folder fanart/examples.zip'),
			os.path.join(root_directory, 'Apps'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers/Utilities/dialog res check.py'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers/Utilities/Run Artwork Installer.py'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers/Utilities/Random Items.py'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers/Utilities/yes-no.py'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers/Utilities/Views Builder.py'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers/default old.py'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers Extras/File Patcher/patches'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers Extras/Synopsis'),
			os.path.join(root_directory, 'system/UserData/setup.bin'),
			'E:/UDATA/09999990',
			'E:/TDATA/Rocky5 needs these Logs/XBMC4Gamers'
		]
		for path in paths_to_remove:
			if os.path.isdir(path):
				shutil.rmtree(path)
			elif os.path.isfile(path):
				os.remove(path)
				
		# Remove old patcher files
		old_patcher_resources = os.path.join(root_directory, 'system/scripts/XBMC4Gamers Extras/File Patcher/resources/lib/patches')
		if os.path.isdir(old_patcher_resources):
			for files in os.listdir(old_patcher_resources):
				try:
					if '-' in files.split('(')[1]:
						os.remove(os.path.join(old_patcher_resources, files))
				except:
					pass

		# Backup directories
		backup_dir = os.path.join(root_directory, 'system/backup')
		backups_dir = os.path.join(root_directory, 'system/backups')
		if os.path.isdir(backups_dir) and os.path.isdir(backup_dir):
			shutil.rmtree(backup_dir)
		elif os.path.isdir(backup_dir):
			os.rename(backup_dir, backups_dir)

		# Extract the dashboard zip
		with zipfile.ZipFile(zip_file) as zip:
			total_txt_files = len(zip.namelist()) or 1
			divide = 100.0 / total_txt_files
			percent = 0
			for item in zip.namelist():
				xbmc.executebuiltin('Skin.SetString(DashboardUpdatedSmall,' + str(int(percent)) + ')')
				percent += divide
				pDialog.update(int(percent), "Download complete", "Updating dashboard")
				try:
					zip.extract(item, root_directory)
				except:
					print "Failed - " + item
			pDialog.update(100, "Download complete", "Updating dashboard complete")
			xbmc.executebuiltin('Skin.SetBool(DashboardUpdated)')
			time.sleep(3)
		
		# Remove DVD2Xbox Skin
		if os.path.isdir(root_directory+'skins/DVD2Xbox Skin'):
			shutil.rmtree(root_directory+'skins/DVD2Xbox Skin')
		input = fileinput.input(root_directory + 'system/userdata/profiles.xml', inplace=True)
		skip = False
		for line in input:
			if '<name>DVD2Xbox</name>' in line:
				skip = True
			if skip and '<profile>' in line:
				skip = False
				continue
			if not skip:
				print line,  # Note the comma to avoid adding extra newline
		
		# Fix Manage Profiles Guisettings.xml
		if os.path.isfile(root_directory+'system/userdata/guisettings.xml'): # set the master profile to default(dashboard) for network
			for line in fileinput.input(root_directory+'system/userdata/guisettings.xml', inplace=1):
				line = line.replace('<assignment>1','<assignment>0')
				line = line.replace('<assignment>2','<assignment>0')
				line = line.replace('<audio>384','<audio>0')
				line = line.replace('<audiotime>8','<audiotime>0')
				line = line.replace('<video>1024','<video>0')
				line = line.replace('<timeserveraddress>time.google.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
				line = line.replace('<timeserveraddress>time.windows.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
				line = line.replace('Manage Profiles Skin','Manage Profiles')
				print line,
		
		# Fix Profiles Guisettings.xml
		for Profiles in os.listdir(os.path.join(root_directory,'system/userdata/profiles')):
			guisettings = os.path.join(root_directory,'system/userdata/profiles',Profiles,'guisettings.xml')
			if os.path.isfile(guisettings):
				for line in fileinput.input(guisettings, inplace=1):
					line = line.replace('<audio>384','<audio>0')
					line = line.replace('<audiotime>8','<audiotime>0')
					line = line.replace('<video>1024','<video>0')
					line = line.replace('<videotime>8','<videotime>0')
					line = line.replace('<videotime>8','<videotime>0')
					line = line.replace('<timeserveraddress>time.google.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
					line = line.replace('<timeserveraddress>time.windows.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
					line = line.replace('Profile Skin','Profile')
					if '<font>' in line and not '<font>Arial.ttf</font>' in line: 
						line = line = '<font>default.ttf</font>\n'
					if '<skincolors>' in line: 
						line = line = '<skincolors>default.xml</skincolors>\n'
					if '<skintheme>' in line: 
						line = line = '<skintheme>default.xpr</skintheme>\n'
					if ' name="Manage Profiles Skin.' in line: 
						line = line = '\n'
					if ' name="Manage Profiles.' in line: 
						line = line = '\n'
					print line,
		
		# Remove setup.bin as it's an update
		if os.path.isfile(root_directory+'system/UserData/setup.bin'):
				os.remove(root_directory+'system/UserData/setup.bin')

		# After extraction cleanup any files that the user didn't have enabled
		if cleanupafter:
			os.remove(root_directory+'system/keymaps/Enabled')
	else:
		print "Remote: {}".format(zip_hash)
		print "Local: ()".format(md5hash.hexdigest())
		dialog.ok('ERROR','Update file validation failed','Please redownload the update')
		failed = 1
else:
	pDialog.create('Error')
	pDialog.update(0,"Download complete","Files are missing")
	time.sleep(5)

# Write the cleanup script and reload the dashboard xbe
success_data = '''import os, time, xbmc, xbmcgui
tmp = 'E:/CACHE/tmp.bin'
if os.path.isfile(tmp):
	while True:
		current_window_id = xbmcgui.getCurrentWindowId()
		time.sleep(1)
		if current_window_id in [10000, 10001, 10029]:
			if os.path.isfile('Q:/system/keymaps/Enabled'):
				xbmc.executebuiltin('Skin.SetBool(editmode)')
			os.remove(tmp)
			xbmcgui.Dialog().textviewer('Changes.txt', open('Special://root/system/SystemInfo/changes.txt').read())
			break'''

failed_data = '''import os
tmp = 'E:/CACHE/tmp.bin'
if os.path.isfile(tmp):
	if os.path.isfile('Q:/system/keymaps/Enabled'): xbmc.executebuiltin('Skin.SetBool(editmode)')
	os.remove(tmp)'''

with open(os.path.join(root_directory,'system/scripts/autoexec.py') , 'w') as autoexec: autoexec.write(success_data)

if failed:
	with open(os.path.join(root_directory,'system/scripts/autoexec.py') , 'w') as autoexec: autoexec.write(failed_data)

with open("E:/CACHE/tmp.bin", 'w') as tmp: tmp.write('')

time.sleep(3)

os.remove(xbmc.translatePath("Special://root/default.xbe"))

xbmc.executebuiltin('RunXBE('+ root_directory +'default.xbe)')