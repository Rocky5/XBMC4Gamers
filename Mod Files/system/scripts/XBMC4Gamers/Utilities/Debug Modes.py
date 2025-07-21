# -*- coding: utf-8 -*-
from fileinput import input as fileinput
from os.path import isfile
from shutil import copy2
from sys import argv
from xbmc import executehttpapi, log, translatePath
from xbmcgui import Dialog

BACKUP_ADV_SETTINGS = translatePath('Special://root/system/backups/advancedsettings.xml')
CURRENT_ADV_SETTINGS = translatePath('Special://profile/advancedsettings.xml')
MODE_LIST = [
	'No logging',
	'Normal logging',
	'Debug logging',
	'Debug logging with on screen info',
	'Debug/smb logging with on screen info'
]

def main():
	# Restore advanced settings if the current profile doesn't have it
	if not isfile(CURRENT_ADV_SETTINGS):
		copy2(BACKUP_ADV_SETTINGS, CURRENT_ADV_SETTINGS)

	try:
		arg1 = argv[1]
	except IndexError:
		arg1 = "false"
	
	mode = Dialog().select('Debug logging modes', MODE_LIST, 10000)
	if mode != -1:
		value = get_logging_value(MODE_LIST[mode])
		if update_logging_level(CURRENT_ADV_SETTINGS, arg1, value):
			executehttpapi('SetLogLevel({})'.format(value))

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

def update_logging_level(file_path, hide_value, log_level):
	new_line = '\t<loglevel hide="{}">{}</loglevel>\n'.format(hide_value, log_level)

	try:
		with open(file_path, 'r') as f:
			lines = f.readlines()
		updated = False
		for i in range(len(lines)):
			if '<loglevel hide=' in lines[i]:
				lines[i] = new_line
				updated = True
				break
		if not updated:
			lines.insert(1, new_line)

		with open(file_path, 'w') as f:
			f.writelines(lines)
		return True

	except Exception as error:
		print "Failed to update logging level:", error
		return False

if __name__ == "__main__":
	main()