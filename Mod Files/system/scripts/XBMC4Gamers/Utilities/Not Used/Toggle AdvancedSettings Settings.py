'''
	Script by Rocky5
	Used to toggle advanced settings options
'''

import fileinput
import os
import shutil
import xbmc
import xbmcgui
import sys

Backup_Profile_AdvSettings = xbmc.translatePath('special://root/system/backups/advancedsettings.xml')
Current_Profile_AdvSettings = xbmc.translatePath('special://profile/advancedsettings.xml')

if not os.path.isfile(Current_Profile_AdvSettings):
	shutil.copy2(Backup_Profile_AdvSettings, Current_Profile_AdvSettings)

def toggle_setting(arg):
	if arg:
		for line in fileinput.input(Current_Profile_AdvSettings, inplace=True):
			if '<{}>'.format(arg) in line:
				line = line.replace('true', 'TMP').replace('false', 'true').replace('TMP', 'false')
			print line,

try:
	arg1 = sys.argv[1] if len(sys.argv) > 1 else None
	arg2 = sys.argv[2] if len(sys.argv) > 2 else None
except Exception as e:
	arg1 = None
	arg2 = None
	xbmc.log("Error parsing arguments: {}".format(e), level=xbmc.LOGERROR)

toggle_setting(arg1)
toggle_setting(arg2)
