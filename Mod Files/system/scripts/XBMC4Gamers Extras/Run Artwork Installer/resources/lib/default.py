import os
import re
import sys
import time
import xbmc
import xbmcgui

def location_file(path):
	if os.path.isfile(path):
		with open(path, 'r') as input_file:
			return input_file.readline().strip()
	return ""

def check_version(artwork_path):
	version_file = os.path.join(artwork_path, 'skins/Default/language/English/strings.po')
	try:
		with open(version_file, "r") as strings:
			for line in strings:
				if 'msgid "v' in line.lower():
					version_numbers = ''.join(re.findall(r'\d+', line))
					return int(version_numbers) >= 33 # version 3.3
	except IOError:
		return False
	return False

def grab_custompaths(artwork_path):
    guisettings_file = os.path.join(artwork_path, 'system/userdata/guisettings.xml')
    args_custompath = [""] * 20
    try:
        with open(guisettings_file, "r") as xml:
            for line in xml:
                for i in range(1, 21):
                    pattern = r'default\.custompath{}selected">(.*?)<'.format(i)
                    match = re.search(pattern, line.lower())
                    if match:
                        args_custompath[i-1] = match.group(1)
        custompath_args = sorted([arg for arg in args_custompath if arg], key=lambda s: s.upper())
        return ','.join(custompath_args) if custompath_args else ''
    except IOError:
        return ''

if __name__ == "__main__":
	path_file = 'E:\\UDATA\\09999993\\location.bin'
	dialog = xbmcgui.Dialog()
	pDialog = xbmcgui.DialogProgress()
	artwork_path = location_file(path_file)
	args = sys.argv[1:] + [False]*6
	Mode, Skip, Video_Install, Large_Fanart, Try_Folder_Names, Logging = [int(arg == 'True') for arg in args[:6]]
	
	if int(xbmc.getInfoLabel('System.memory(total_no_mb)')) == 64:
		xbmc.executebuiltin('Skin.Reset(ArtworkInstallerFanart)')
		Large_Fanart = 0

	if artwork_path:
		if check_version(artwork_path):
			if os.path.isfile(os.path.join(artwork_path, 'default.xbe')):
				if Mode:
					xbmc.executebuiltin('RunScript({},0,{},{},{},{},{},{})'.format(
						os.path.join(artwork_path, 'system\\scripts\\default.py'),
						Skip, Video_Install, Large_Fanart, Try_Folder_Names, Logging, grab_custompaths(artwork_path)))
				else:
					xbmc.executebuiltin('RunScript({},0,{},{},{})'.format(
						os.path.join(artwork_path, 'system\\scripts\\manual.py'),
						Video_Install, Large_Fanart, grab_custompaths(artwork_path)))
			else:
				dialog.ok('ERROR: NOT INSTALLED', "Please ensure that the application is installed correctly. If you haven't[CR]installed it yet, download the latest version and once installed, try again.")
				xbmc.executebuiltin('Dialog.Close(1100,false)')
		else:
			dialog.ok('ERROR: OUT OF DATE','The installed version is out of date. Please update to the latest version[CR](3.3 or higher) to ensure compatibility and access to the latest features.')
			xbmc.executebuiltin('Dialog.Close(1100,false)')
	else:
		dialog.ok('ERROR: LOCATION NOT FOUND', 'The specified location for the Xbox Artwork Installer could not be[CR]found. Please ensure that the application is correctly installed.')
		xbmc.executebuiltin('Dialog.Close(1100,false)')