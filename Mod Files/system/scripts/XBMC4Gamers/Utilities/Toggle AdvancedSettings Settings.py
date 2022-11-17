'''
	Script by Rocky5
	Used to toggle advanced settings options
'''
import fileinput, os, shutil, xbmc, xbmcgui

Backup_Profile_AdvSettings = xbmc.translatePath('Special://root/system/backups/advancedsettings.xml')
Current_Profile_AdvSettings = xbmc.translatePath('Special://profile/advancedsettings.xml')
if not os.path.isfile(Current_Profile_AdvSettings): shutil.copy2(Backup_Profile_AdvSettings,Current_Profile_AdvSettings)

try:
	arg1 = sys.argv[1:][0]
	arg2 = sys.argv[2:][0]
except:
	arg1 = 0
	arg2 = 0


if arg1:
	for line in fileinput.input(Current_Profile_AdvSettings, inplace=1):
		if '<'+arg1+'>' in line:
			if 'true' in line:
				line = line = '		<'+arg1+'>false</'+arg1+'>\n'
			else:
				line = line = '		<'+arg1+'>true</'+arg1+'>\n'
		print line,


if arg2:
	for line in fileinput.input(Current_Profile_AdvSettings, inplace=1):
		if '<'+arg2+'>' in line:
			if 'true' in line:
				line = line = '		<'+arg2+'>false</'+arg2+'>\n'
			else:
				line = line = '		<'+arg2+'>true</'+arg2+'>\n'
		print line,