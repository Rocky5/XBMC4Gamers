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
		# Rename directories
		rename_pairs = [
			(os.path.join(root_directory, 'skins/Profile Skin'), os.path.join(root_directory, 'skins/Profile')),
			(os.path.join(root_directory, 'skins/Manage Profiles Skin'), os.path.join(root_directory, 'skins/Add User')),
			(os.path.join(root_directory, 'skins/Manage Profiles'), os.path.join(root_directory, 'skins/Add User')),
			(os.path.join(root_directory, 'system.intro'), os.path.join(root_directory, 'system/intros'))
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
				'Includes_Snow.xml',
				'LoginScreen_old.xml'
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
				'Custom_Synopsis.xml',
				'Includes_Busy_ScriptBusy.xml',
				'Includes_Context_Buttons.xml',
				'Includes_Fallback_View.xml',
				'Includes_Insignia_Sessions.xml',
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
			'Apps',
			'E:/TDATA/Rocky5 needs these Logs/XBMC4Gamers',
			'E:/UDATA/09999990',
			'skins/Add User/720p',
			'skins/Profile/720p',
			'skins/Profile/backgrounds/night/background.jpg',
			'skins/Profile/extras/folder fanart/examples.zip',
			'skins/Profile/extras/splashes',
			'skins/Profile/extras/xmls/rounded byzantium.xml',
			'skins/Profile/extras/xmls/rounded default.xml',
			'skins/Profile/extras/xmls/rounded night.xml',
			'skins/Profile/media/backgrounds',
			'skins/Profile/sounds/back.wav',
			'skins/Profile/sounds/click.wav',
			'skins/Profile/sounds/cursor.wav',
			'skins/Profile/sounds/notify.wav',
			'skins/Profile/sounds/out.wav',
			'skins/Profile/sounds/shutter.wav',
			'skins/Profile/sounds/sounds.xml',
			'skins/Profile/xml/views',
			'system/python/modules',
			'system/scripts/.modules',
			'system/scripts/XBMC4Gamers Extras/480p Game Loaders/resources/lib/loaders',
			'system/scripts/XBMC4Gamers Extras/File Patcher/patches',
			'system/scripts/XBMC4Gamers Extras/File Patcher/resources/lib/patches',
			'system/scripts/XBMC4Gamers Extras/Insignia Sessions',
			'system/scripts/XBMC4Gamers Extras/Synopsis',
			'system/scripts/XBMC4Gamers',
			'system/toggles',
			'system/UserData/Thumbnails/Profiles/ManageProfiles.tbn'
		]
		for path in paths_to_remove:
			path = os.path.join(root_directory, path)
			if os.path.isdir(path):
				shutil.rmtree(path)
			elif os.path.isfile(path):
				os.remove(path)

		# if extracted lib folder exists remove it only if it's from python27.zlib
		lib_path = os.path.join(root_directory, 'system/python/lib')
		if os.path.isfile(os.path.join(lib_path, 'tty.py')):
			shutil.rmtree(lib_path)

		# Remove .pyo files
		root_directories = [
			'system/python',
			'system/scripts'
		]

		for root_dir in root_directories:
			root_dir = os.path.join(root_directory, root_dir)
			for dirpath, _, filenames in os.walk(root_dir):
				for filename in filenames:
					if filename.endswith('.pyo'):
						file_path = os.path.join(dirpath, filename)
						os.remove(file_path)

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
		if os.path.isfile(profilesxml):
			tree = ET.parse(profilesxml)
			root = tree.getroot()

			def remove_profile_by_name(profile_name):
				profiles_parent = root
				for profile in list(profiles_parent.findall("./profile")):
					name_element = profile.find("name")
					if name_element is not None and name_element.text.strip().lower() == profile_name.lower():
						profiles_parent.remove(profile)
						adjust_lastloaded()

			def update_profile_name(old_name, new_name):
				for profile in root.findall(".//profile[name='{}']".format(old_name)):
					profile.find("name").text = new_name

			def adjust_lastloaded():
				lastloaded_element = root.find("./lastloaded")
				if lastloaded_element is not None:
					try:
						val = int(lastloaded_element.text)
					except ValueError:
						return
					if val > 1:
						lastloaded_element.text = str(val - 1)


			def update_thumbnail(profile_name, new_thumbnail_path):
				for profile in root.findall(".//profile[name='{}']".format(profile_name)):
					directory = profile.find("directory")
					if directory is not None and directory.text == "special://masterprofile/":
						thumbnail = profile.find("thumbnail")
						if thumbnail is not None:
							thumbnail.text = new_thumbnail_path

			remove_profile_by_name("DVD2Xbox")
			update_profile_name("Manage Profiles", "Add User")
			update_thumbnail("Add User", "special://masterprofile/Thumbnails/Profiles/AddUser.tbn")

			tree.write(profilesxml, encoding="utf-8", xml_declaration=False)

		# for editing the xml GUIsettings.
		def remove_element_by_tag(parent, tag):
			for element in parent.findall(tag):
				parent.remove(element)

		def update_element_value(parent, child, value):
			parent = root.find(parent)
			if parent is not None:
				element = parent.find(child)
				if element is not None:
					element.text = value

		def remove_elements_by_attribute(attribute_name):
			for parent in root.findall(".//*"):
				for element in parent.findall(".//setting[@name='{}']".format(attribute_name)):
					parent.remove(element)
					
		def remove_elements_by_name_prefix(prefix):
			for parent in root.findall(".//*"):
				for element in parent.findall(".//setting[@name]"):
					name_value = element.get("name")
					if name_value and name_value.startswith(prefix):
						parent.remove(element)

		def update_element_by_name(attribute_name, attribute_type, value):
			for element in root.findall(".//setting[@name='{}']".format(attribute_name)):
				element.set("type", attribute_type)
				element.text = value

		def update_element_name_attribute(old_name, new_name):
			for element in root.findall(".//setting[@name='{}']".format(old_name)):
				element.set("name", new_name)

		def update_element_name_prefix(old_prefix, new_prefix):
			for element in root.findall(".//setting[@name]"):
				name_value = element.get("name")
				if name_value and name_value.startswith(old_prefix):
					element.set("name", name_value.replace(old_prefix, new_prefix, 1))
					
		def add_to_skinsettings(settings):
			skinsettings = root.find("skinsettings")
			if skinsettings is None:
				skinsettings = ET.SubElement(root, "skinsettings")

			for name, setting_type, value in settings:
				setting_exists = any(
					element.get("name") == name and element.get("type") == setting_type
					for element in skinsettings.findall("setting")
				)

				if not setting_exists:
					ET.SubElement(skinsettings, "setting", {"type": setting_type, "name": name}).text = value

		def get_skinsetting_value(root, setting_name):
			skinsettings = root.find("skinsettings")
			if skinsettings is not None:
				element = skinsettings.find(".//setting[@name='{}']".format(setting_name))
				if element is not None:
					return element.text
			return None

		# Fix Add User Guisettings.xml
		# set the master profile to default(dashboard) for network
		guisettings_path = root_directory + 'system/userdata/guisettings.xml'
		if os.path.isfile(guisettings_path):
			tree = ET.parse(guisettings_path)
			root = tree.getroot()

			remove_elements_by_attribute("Manage Profiles.loginfade")
			remove_elements_by_attribute("Add User.loginfade")

			update_element_name_prefix("Manage Profiles Skin.", "Add User.")
			update_element_name_prefix("Manage Profiles.", "Add User.")

			if root.find('./lookandfeel') is not None:
				update_element_value('lookandfeel', 'skin', 'Add User')
				update_element_value('lookandfeel', 'font', 'default')
				update_element_value('lookandfeel', 'skincolors', 'default')
				update_element_value('lookandfeel', 'skintheme', 'default')
				update_element_value('lookandfeel', 'soundskin', 'default')

			if root.find('./network') is not None:
				update_element_value('network', 'assignment', '0')
				update_element_value('network', 'timeserveraddress', 'pool.ntp.org')

			if root.find('./dvdplayercache') is not None:
				update_element_value('dvdplayercache', 'audio', '256')
				update_element_value('dvdplayercache', 'audiotime', '30')
				update_element_value('dvdplayercache', 'video', '512')
				update_element_value('dvdplayercache', 'videotime', '30')

			tree.write(guisettings_path, encoding="utf-8", xml_declaration=False)
		
		# Fix Profiles Guisettings.xml and added update database bool
		for Profiles in os.listdir(os.path.join(root_directory, 'system/userdata/profiles')):
			guisettings_path = os.path.join(root_directory, 'system/userdata/profiles', Profiles, 'guisettings.xml')
			if os.path.isfile(guisettings_path):
				tree = ET.parse(guisettings_path)
				root = tree.getroot()

				settings_to_add = [
					("Profile.updatedb", "bool", "false")
				]

				add_to_skinsettings(settings_to_add)
				update_element_by_name("Profile.updatedb", "bool", "true")
				
				# for i in range(50, 80):
					# update_element_by_name("Profile.view{}_disabled".format(i), "bool", "false")
				
				remove_elements_by_attribute("Manage Profiles.loginfade")
				remove_elements_by_attribute("Add User.loginfade")
				remove_elements_by_attribute("Profile.background_color")
				remove_elements_by_attribute("Profile.background_custom_color")
				remove_elements_by_attribute("Profile.randomtheme")
				remove_elements_by_attribute("Profile.customviewtype_id_87_jpg)")
				
				if get_skinsetting_value(root, "Profile.custom_wallpaper_set") == "false":
					remove_elements_by_attribute("Profile.background_image")
				
				remove_elements_by_name_prefix("Manage Profiles Skin.")
				remove_elements_by_name_prefix("Manage Profiles.")
				remove_elements_by_name_prefix("Add User.")
				remove_elements_by_name_prefix("XBox Extended.")
				
				if root.find('./lookandfeel') is not None:
					update_element_value('lookandfeel', 'skin', 'Profile')
					update_element_value('lookandfeel', 'font', 'default')
					update_element_value('lookandfeel', 'skincolors', 'default')
					update_element_value('lookandfeel', 'skintheme', 'default')
					update_element_value('lookandfeel', 'soundskin', 'default')
				
				if root.find('./network') is not None:
					update_element_value('network', 'timeserveraddress', 'pool.ntp.org')

				if root.find('./dvdplayercache') is not None:
					update_element_value('dvdplayercache', 'audio', '256')
					update_element_value('dvdplayercache', 'audiotime', '30')
					update_element_value('dvdplayercache', 'video', '512')
					update_element_value('dvdplayercache', 'videotime', '30')

				tree.write(guisettings_path, encoding="utf-8", xml_declaration=False)

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
			</images>"""
			# <wallpaper>720x405</wallpaper>
			# <wallpaper_128mb>1280x720</wallpaper_128mb>
			try:
				if os.path.isfile(advancedsettings_path):
					tree = ET.parse(advancedsettings_path)
					root = tree.getroot()
					
					def remove_element_by_tag(parent, tag):
						for element in parent.findall(tag):
							parent.remove(element)

					remove_element_by_tag(root, '_resources')
					remove_element_by_tag(root, 'wallpaper')
					remove_element_by_tag(root, 'powersaving')
					remove_element_by_tag(root, 'fanartheight')
					remove_element_by_tag(root, 'enableintro')
					
					images_element = root.find('images')
					
					try:
						remove_element_by_tag(images_element, 'wallpaper')
						remove_element_by_tag(images_element, 'wallpaper_128mb')
					except:
						pass
					
					if images_element is None:
						new_elements_root = ET.fromstring(new_elements)
						root.append(new_elements_root)
					# else:
						# wallpaper_128mb_element = images_element.find('wallpaper_128mb')
						# if wallpaper_128mb_element is None:
							# new_elements_root = ET.fromstring('<wallpaper_128mb>1280x720</wallpaper_128mb>')
							# images_element.append(new_elements_root)

					utf_string = ET.tostring(root, 'utf-8')
					prettify = xml.dom.minidom.parseString(utf_string)
					prettify_xml = prettify.toprettyxml(indent="    ")
					lines = prettify_xml.split('\n')
					lines = [line for line in lines if line.strip() != '']
					new_prettify_xml = '\n'.join(lines)
					
					with open(advancedsettings_path, 'w') as file:
						file.write(new_prettify_xml)
			except Exception as error:
				print("Error- {}".format(error))
				continue

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
				except Exception as error:
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