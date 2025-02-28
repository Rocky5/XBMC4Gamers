# -*- coding: utf-8 -*-
import os
import fileinput
import xbmc

PROFILES_DIRECTORY = 'Q:/system/userdata/profiles'
SETTING = xbmc.getInfoLabel('Skin.HasSetting(loginfade)')
GUI_SETTINGS_FILENAME = 'guisettings.xml'
PROFILE_SETTING_TAG = '<setting type="bool" name="Profile.loginfade">'

def modify_guisettings(profile_path):
	value = "true"
	if not SETTING:
		value = "false"
	
	guisettings = os.path.join(profile_path, GUI_SETTINGS_FILENAME)
	
	if os.path.isfile(guisettings):
		try:
			found_line = False
			for line in fileinput.input(guisettings, inplace=True):
				if PROFILE_SETTING_TAG in line:
					line = '        <setting type="bool" name="Profile.loginfade">{}</setting>\n'.format(value)
					found_line = True
				print line,
			
			if not found_line:
				with open(guisettings, 'r') as f:
					modified = f.read().replace('</skinsettings>', '        <setting type="bool" name="Profile.loginfade">{}</setting>\n</skinsettings>'.format(value))
				
				with open(guisettings, 'w') as f:
					f.write(modified)
		except IOError as error:
			print "Error modifying guisettings.xml:", error
	else:
		print "Error: guisettings.xml not found in", profile_path

def main():
	for profile in os.listdir(PROFILES_DIRECTORY):
		profile_path = os.path.join(PROFILES_DIRECTORY, profile)
		modify_guisettings(profile_path)
	xbmc.executebuiltin('ReloadSkin')

if __name__ == "__main__":
	main()