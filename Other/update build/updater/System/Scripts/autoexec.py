# -*- coding: utf-8 -*-
import fileinput
import hashlib
import os
import shutil
import time
import xbmc
import xbmcgui
import zipfile
import xml.etree.ElementTree as ET
import xml.dom.minidom

root_directory	= xbmc.translatePath("Special://root/")[:-8]

zip_file = os.path.join(root_directory, 'updater/Update Files/update-files.zip')
hash_file = os.path.join(root_directory, 'updater/Update Files/md5hash.bin')

xbmc.executebuiltin('Skin.SetString(DashboardUpdatedSmall,0)')
xbmc.executebuiltin('Skin.Reset(DashboardUpdated)')

pDialog	= xbmcgui.DialogProgress()
dialog	= xbmcgui.Dialog()

md5hash = hashlib.md5()
failed = 0


if os.path.isfile(zip_file):
	pDialog.create('Stage 2 of 2')
	pDialog.update(0, "Download complete", "Validating update 1 of 1","")
	
	with open(hash_file,"r") as ziphash:
		update_zip_hash = ziphash.readline().rstrip()
	with open(zip_file, "rb", buffering=16384) as updatefile:
		while True:
			chunk = updatefile.read(16384)
			if not chunk:
				break
			md5hash.update(chunk)
	
	if md5hash.hexdigest() == update_zip_hash:
		# Rename skin directories
		rename_pairs = [
			(os.path.join(root_directory, 'skins/Profile Skin'), os.path.join(root_directory, 'skins/Profile')),
			(os.path.join(root_directory, 'skins/Manage Profiles Skin'), os.path.join(root_directory, 'skins/Add User')),
			(os.path.join(root_directory, 'skins/Manage Profiles'), os.path.join(root_directory, 'skins/Add User'))
		]
		for old_path, new_path in rename_pairs:
			if os.path.isdir(old_path) and not os.path.isdir(new_path):
				os.rename(old_path, new_path)

		# Removals for Add User files
		manage_profiles_xml = os.path.join(root_directory, 'skins/Add User/xml')
		if os.path.isdir(manage_profiles_xml):
			files_to_remove = [
				'Custom_Controls.xml',
				'Includes_Context_Buttons.xml',
				'Pointer.xml',
				'Includes_Birthday.xml',
				'Includes_Easter.xml',
				'Includes_Particles.xml',
				'Includes_Snow.xml'
			]
			for file in files_to_remove:
				file_path = os.path.join(manage_profiles_xml, file)
				if os.path.isfile(file_path):
					os.remove(file_path)

		# Removals for Profile files
		profile_xml = os.path.join(root_directory, 'skins/Profile/xml')
		if os.path.isdir(profile_xml):
			files_to_remove = [
				'Custom_Recent.xml',
				'Custom_Skin_Setting.xml',
				'Custom_Skin_Settings.xml',
				'Custom_View_Options.xml',
				'Includes_Busy_ScriptBusy.xml',
				'Includes_Context_Buttons.xml',
				'Includes_Fallback_View.xml',
				'Includes_Recent_Played.xml',
				'Includes_Theme_Override.xml',
				'Includes_Variables.xml',
				'Includes_View_Options.xml',
				'LockSettings.xml',
				'Pointer.xml',
				'SettingsProfile.xml',
				'Viewtype_54_Panel.xml',
				'Viewtype_56_Card.xml',
				'Viewtype_61_CarouselSmaller.xml',
				'_Script_Synopsis.xml',
				'includes/Fallback_View.xml'
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
			os.path.join(root_directory, 'Apps'),
			os.path.join(root_directory, 'E:/TDATA/Rocky5 needs these Logs/XBMC4Gamers'),
			os.path.join(root_directory, 'E:/UDATA/09999990'),
			os.path.join(root_directory, 'skins/Add User/720p'),
			os.path.join(root_directory, 'skins/Profile/720p'),
			os.path.join(root_directory, 'skins/Profile/backgrounds/night/background.jpg'),
			os.path.join(root_directory, 'skins/Profile/extras/folder fanart/examples.zip'),
			os.path.join(root_directory, 'skins/Profile/extras/splashes'),
			os.path.join(root_directory, 'skins/Profile/extras/xmls/rounded byzantium.xml'),
			os.path.join(root_directory, 'skins/Profile/extras/xmls/rounded default.xml'),
			os.path.join(root_directory, 'skins/Profile/extras/xmls/rounded night.xml'),
			os.path.join(root_directory, 'skins/Profile/media/backgrounds'),
			os.path.join(root_directory, 'skins/Profile/sounds/back.wav'),
			os.path.join(root_directory, 'skins/Profile/sounds/click.wav'),
			os.path.join(root_directory, 'skins/Profile/sounds/cursor.wav'),
			os.path.join(root_directory, 'skins/Profile/sounds/notify.wav'),
			os.path.join(root_directory, 'skins/Profile/sounds/out.wav'),
			os.path.join(root_directory, 'skins/Profile/sounds/shutter.wav'),
			os.path.join(root_directory, 'skins/Profile/sounds/sounds.xml'),
			os.path.join(root_directory, 'skins/Profile/xml/views'),
			os.path.join(root_directory, 'system/scripts/.modules'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers Extras/File Patcher/patches'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers Extras/Synopsis'),
			os.path.join(root_directory, 'system/scripts/XBMC4Gamers'),
			os.path.join(root_directory, 'system/toggles'),
			os.path.join(root_directory, 'system/UserData/Thumbnails/Profiles/ManageProfiles.tbn')
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
			
		# Move folder fanart files to new location
		source_dir = os.path.join(root_directory, 'skins/Profile/extras/folder fanart')
		destination_dir = os.path.join(root_directory, 'skins/Profile/extras/folder fanart/default')
		if not os.path.exists(destination_dir):
			os.makedirs(destination_dir)
		for filename in os.listdir(source_dir):
			if filename.endswith('.jpg'):
				source_file = os.path.join(source_dir, filename)
				destination_file = os.path.join(destination_dir, filename)
				shutil.move(source_file, destination_file)
				print 'Moved:{}->{}'.format(source_file, destination_file)

		# Check for custom view files and move them to new location if possible.
		global_folder = os.path.join(root_directory, 'skins/Profile/xml/custom views/_global')
		old_folder = os.path.join(root_directory, 'skins/Profile/xml/custom views')
		for ID in range(80, 90):
			global_xml_file = os.path.join(global_folder, "CustomViewtype_id_{}.xml".format(ID))
			global_jpg_file = os.path.join(global_folder, "CustomViewtype_id_{}.jpg".format(ID))
			old_xml_file = os.path.join(old_folder, "CustomViewtype_id_{}.xml".format(ID))
			old_jpg_file = os.path.join(old_folder, "CustomViewtype_id_{}.jpg".format(ID))
			if (not os.path.isfile(global_xml_file) and not os.path.isfile(global_jpg_file)) and (os.path.isfile(old_xml_file) and os.path.isfile(old_jpg_file)):
				shutil.copyfile(old_xml_file, global_xml_file)
				shutil.copyfile(old_jpg_file, global_jpg_file)
				os.remove(old_xml_file)
				os.remove(old_jpg_file)
			# Remove old example xmls
			try: os.remove(os.path.join(old_folder, "CustomViewtype_id_example.xml"))
			except: pass				
			try: os.remove(os.path.join(old_folder, "CustomViewtype_id_example.jpg"))
			except: pass				
		
		# Remove DVD2Xbox Skin and update master profile name
		if os.path.isdir(root_directory + 'skins/DVD2Xbox Skin'):
			shutil.rmtree(root_directory + 'skins/DVD2Xbox Skin')
		profilesxml = root_directory + 'system/userdata/profiles.xml'
		with open(profilesxml, 'r') as readxml:
			content = readxml.read()
		processxml = False
		if '<name>DVD2Xbox</name>' in content or '<name>Manage Profiles</name>' in content:
			processxml = True
		input = fileinput.input(profilesxml, inplace=True)

		if processxml:
			lastloaded_value = None
			new_lastloaded = None
			skip = False
			replace_next_line = False
			replaced = False
			for line in input:
				if '<name>Manage Profiles</name>' in line:
					line = line.replace('<name>Manage Profiles</name>', '<name>Add User</name>')
				if '<name>DVD2Xbox</name>' in line:
					skip = True
				if skip and '<profile>' in line:
					skip = False
					continue
				if not skip:
					if '<directory pathversion="1">special://masterprofile/</directory>' in line and not replaced:
						replace_next_line = True
						print line,
						continue
					if replace_next_line:
						line = '<thumbnail pathversion="1">special://masterprofile/Thumbnails/Profiles/AddUser.tbn</thumbnail>\n'
						replace_next_line = False
						replaced = True
					if '<lastloaded>' in line:
						lastloaded_value = int(line.split('<lastloaded>')[1].split('</lastloaded>')[0])
						new_lastloaded = max(1, lastloaded_value - 1)
						line = line.replace(str(lastloaded_value), str(new_lastloaded))
					print line,
		else:
			replace_next_line = False
			replaced = False
			for line in input:
				if '<name>Manage Profiles</name>' in line:
					line = line.replace('<name>Manage Profiles</name>', '<name>Add User</name>')
				if '<directory pathversion="1">special://masterprofile/</directory>' in line and not replaced:
					replace_next_line = True
					print line,
					continue
				if replace_next_line:
					line = '<thumbnail pathversion="1">special://masterprofile/Thumbnails/Profiles/AddUser.tbn</thumbnail>\n'
					replace_next_line = False
					replaced = True
				print line,

		# Fix Add User Guisettings.xml
		# set the master profile to default(dashboard) for network
		if os.path.isfile(root_directory+'system/userdata/guisettings.xml'):
			for line in fileinput.input(root_directory+'system/userdata/guisettings.xml', inplace=1):
				line = line.replace('<assignment>1','<assignment>0')
				line = line.replace('<assignment>2','<assignment>0')
				line = line.replace('<audio>384','<audio>0')
				line = line.replace('<audiotime>8','<audiotime>0')
				# line = line.replace('<video>1024','<video>0')
				line = line.replace('<video>0','<video>512')
				line = line.replace('<videotime>8','<videotime>5')
				line = line.replace('<videotime>0','<videotime>5')
				line = line.replace('<timeserveraddress>time.google.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
				line = line.replace('<timeserveraddress>time.windows.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
				line = line.replace('<setting type="bool" name="Manage Profiles.loginfade">true</setting>', '<setting type="bool" name="Add User.loginfade">false</setting>')
				line = line.replace('<setting type="bool" name="Add User.loginfade">true</setting>', '<setting type="bool" name="Add User.loginfade">false</setting>')
				line = line.replace(' name="Manage Profiles Skin.',' name="Add User.')
				line = line.replace(' name="Manage Profiles.',' name="Add User.')
				
				if '<skin>' in line:
					line = '<skin>Add User</skin>\n'
				print line,				
		
		# Fix Profiles Guisettings.xml and added update database bool
		for Profiles in os.listdir(os.path.join(root_directory, 'system/userdata/profiles')):
			guisettings = os.path.join(root_directory, 'system/userdata/profiles', Profiles, 'guisettings.xml')
			if os.path.isfile(guisettings):
				found = False
				skinsettings_found = False
				lines = []
				with open(guisettings, 'r') as file:
					for line in file:
						if 'Profile.updatedb"' in line:
							found = True
							line = '\t\t<setting type="bool" name="Profile.updatedb">true</setting>\n'
						if '</skinsettings>' in line:
							skinsettings_found = True
						lines.append(line)
				if not skinsettings_found:
					with open(guisettings, 'w') as file:
						for line in lines:
							if '</weather>' in line:
								file.write(line)
								file.write('\t<skinsettings>\n')
								file.write('\t\t<setting type="bool" name="Profile.updatedb">true</setting>\n')
								file.write('\t</skinsettings>\n')
							else:
								file.write(line)
				else:
					with open(guisettings, 'w') as file:
						for line in lines:
							file.write(line)
					if not found:
						with open(guisettings, 'r+') as file:
							lines = file.readlines()
							file.seek(0)
							file.truncate()
							for line in lines:
								if '</skinsettings>' in line:
									file.write('\t\t<setting type="bool" name="Profile.updatedb">true</setting>\n')
									file.write(line)
								else:
									file.write(line)
							
				for line in fileinput.input(guisettings, inplace=True):
					line = line.replace('<audio>384', '<audio>0')
					line = line.replace('<audiotime>8', '<audiotime>0')
					# line = line.replace('<video>1024', '<video>0')
					line = line.replace('<video>0', '<video>512')
					line = line.replace('<videotime>8', '<videotime>5')
					line = line.replace('<videotime>0', '<videotime>5')
					line = line.replace('<timeserveraddress>time.google.com</timeserveraddress>', '<timeserveraddress>pool.ntp.org</timeserveraddress>')
					line = line.replace('<timeserveraddress>time.windows.com</timeserveraddress>', '<timeserveraddress>pool.ntp.org</timeserveraddress>')
					line = line.replace('<setting type="bool" name="Profile.loginfade">true</setting>', '<setting type="bool" name="Profile.loginfade">false</setting>')
												   
					if '<font>' in line and not '<font>Arial.ttf</font>' in line:
						line = '<font>default.ttf</font>\n'
					if '<skincolors>' in line:
						line = '<skincolors>default.xml</skincolors>\n'
					if '<skintheme>' in line:
						line = '<skintheme>default.xpr</skintheme>\n'
					if '<soundskin>' in line:
						line = '<soundskin>default</soundskin>\n'
					if 'name="Profile.randomtheme"' in line:
						line = '\n'
					if ' name="Manage Profiles Skin.' in line:
						line = '\n'
					if ' name="Manage Profiles.' in line:
						line = '\n'
					if ' name="Add User.' in line:
						line = '\n'
					if '<skin>' in line:
						line = '<skin>Profile</skin>\n'
					print line,

		# Update advancedsettings.xml file
		advancedsettings_path = os.path.join(root_directory, 'system/userdata/profiles', Profiles, 'advancedsettings.xml')
		new_elements = """\
		<images>
			<_resources>
				<banner>448x84</banner>
				<cd>256x256</cd>
				<cd_small>64x64</cd_small>
				<cdposter>200x283</cdposter>
				<dual3d>256x256</dual3d>
				<fanart>640x360</fanart>
				<fanart_blur>220x124</fanart_blur>
				<fanart_thumb>360x203</fanart_thumb>
				<fog>8x8</fog>
				<icon>149x263</icon>
				<opencase>149x263</opencase>
				<poster>200x283</poster>
				<poster_small>64x91</poster_small>
				<synopsis>362x512</synopsis>
				<thumb>227x129</thumb>
			</_resources>
			<wallpaper>720x405</wallpaper>
			<wallpaper_128mb>1280x720</wallpaper_128mb>
		</images>"""

		if os.path.isfile(advancedsettings_path):
			tree = ET.parse(advancedsettings_path)
			root = tree.getroot()
			
			def remove_element_by_tag(parent, tag):
				for element in parent.findall(tag):
					parent.remove(element)
			
			remove_element_by_tag(root, '_resources')
			remove_element_by_tag(root, 'wallpaper')
			remove_element_by_tag(root, 'powersaving')
			
			for element in root.findall('fanartheight'):
				if element.text == "360":
					root.remove(element)
			
			images_element = root.find('images')
			
			if images_element is None:
				new_elements_root = ET.fromstring(new_elements)
				root.append(new_elements_root)
			else:
				wallpaper_128mb_element = images_element.find('wallpaper_128mb')
				if wallpaper_128mb_element is None:
					new_elements_root = ET.fromstring('<wallpaper_128mb>1280x720</wallpaper_128mb>')
					images_element.append(new_elements_root)

			utf_string = ET.tostring(root, 'utf-8')
			prettify = xml.dom.minidom.parseString(utf_string)
			prettify_xml = prettify.toprettyxml(indent="    ")
			lines = prettify_xml.split('\n')
			lines = [line for line in lines if line.strip() != '']
			new_prettify_xml = '\n'.join(lines)
			
			with open(advancedsettings_path, 'w') as file:
				file.write(new_prettify_xml)

		# Extract the dashboard update zip
		with zipfile.ZipFile(zip_file) as zip:
			total_size = sum((zip.getinfo(item).file_size for item in zip.namelist()))
			extracted_size = 0
			update_threshold = 5 * 1024 * 1024
			percent = 0
			total_txt_files = len(zip.namelist()) or 1
			divide = 100.0 / total_txt_files
			for item in zip.namelist():
				try:
					zip.extract(item, root_directory)
				except Exception as e:
					print("Failed - {}".format(item))
					continue
				extracted_size += zip.getinfo(item).file_size
				if extracted_size >= update_threshold:
					xbmc.executebuiltin('Skin.SetString(DashboardUpdatedSmall,' + str(int(percent)) + ')')
					pDialog.update(int(percent), "Download complete", "Updating dashboard")
					extracted_size = 0
				percent += divide
		
		xbmc.executebuiltin('Skin.SetString(DashboardUpdatedSmall,100)')
		pDialog.update(100, "Download complete", "Dashboard update complete")
		
		# Remove setup.bin as it's an update
		if os.path.isfile(root_directory+'system/UserData/setup.bin'):
				os.remove(root_directory+'system/UserData/setup.bin')

	else:
		pDialog.update(0, "Download complete", "Verification failed, redownload update", "")
		time.sleep(3)
		failed = 1
else:
	pDialog.create('Error')
	pDialog.update(0, "Download complete", "Files missing, redownload update", "")
	time.sleep(3)

# Write the cleanup script and reload the dashboard xbe
success_data = '''import os, time, xbmc, xbmcgui
tmp = 'E:/CACHE/tmp.bin'
if os.path.isfile(tmp):
	if os.path.isfile('Q:/system/keymaps/Enabled'):
		xbmc.executebuiltin('Skin.SetBool(editmode)')
	os.remove(tmp)'''

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