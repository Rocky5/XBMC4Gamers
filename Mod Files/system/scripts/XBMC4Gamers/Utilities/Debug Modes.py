# -*- coding: utf-8 -*-
import fileinput
import os
import shutil
import xbmc
import xbmcgui
import sys

BACKUP_ADV_SETTINGS = xbmc.translatePath('Special://root/system/backups/advancedsettings.xml')
CURRENT_ADV_SETTINGS = xbmc.translatePath('Special://profile/advancedsettings.xml')
MODE_LIST = [
	'No logging',
	'Normal logging',
	'Debug logging',
	'Debug logging with on screen info',
	'Debug/smb logging with on screen info'
]

def main():
	pDialog = xbmcgui.DialogProgress()
	dialog = xbmcgui.Dialog()

	# Restore advanced settings if the current profile doesn't have it
	if not os.path.isfile(CURRENT_ADV_SETTINGS):
		shutil.copy2(BACKUP_ADV_SETTINGS, CURRENT_ADV_SETTINGS)

	try:
		arg1 = sys.argv[1]
	except IndexError:
		arg1 = "false"

	mode = dialog.select('Debug logging modes', MODE_LIST, 10000)

	if mode != -1:
		value = get_logging_value(MODE_LIST[mode])
		if update_logging_level(CURRENT_ADV_SETTINGS, arg1, value):
			if value >= 2:
				xbmc.executebuiltin('EnableDebugMode')
			else:
				xbmc.executebuiltin('DisableDebugMode')

			xbmc.executebuiltin('ReloadAdvancedSettings')

def get_logging_value(mode):
	if mode == "No logging":
		return -1
	elif mode == "Normal logging":
		return 0
	elif mode == "Debug logging":
		return 1
	elif mode == "Debug logging with on screen info":
		return 2
	return 3

def update_logging_level(file_path, arg1, value):
	new_line = '        <loglevel hide="{}">{}</loglevel>\n'.format(arg1, value)
	line_found = False

	try:
		for line in fileinput.input(file_path, inplace=1):
			if '<loglevel hide=' in line:
				line = new_line
				line_found = True
			print line,

		if not line_found:
			with open(file_path, 'r') as f:
				lines = f.readlines()
			lines.insert(1, new_line)
			with open(file_path, 'w') as f:
				f.writelines(lines)

		return True
	except Exception as error:
		xbmc.log("Failed to update logging level: {}".format(error), xbmc.LOGERROR)
		return False

if __name__ == "__main__":
	main()