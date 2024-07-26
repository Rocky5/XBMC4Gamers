import fileinput
import os
import shutil
import xbmc
import xbmcgui
import sys

def main():
	pDialog = xbmcgui.DialogProgress()
	dialog = xbmcgui.Dialog()

	Backup_Profile_AdvSettings = xbmc.translatePath('Special://root/system/backups/advancedsettings.xml')
	Current_Profile_AdvSettings = xbmc.translatePath('Special://profile/advancedsettings.xml')

	if not os.path.isfile(Current_Profile_AdvSettings):
		shutil.copy2(Backup_Profile_AdvSettings, Current_Profile_AdvSettings)

	try:
		arg1 = sys.argv[1]
	except IndexError:
		arg1 = "false"

	mode_list = [
		'No logging',
		'Normal logging',
		'Debug logging',
		'Debug logging with on screen info',
		'Debug/smb logging with on screen info'
	]

	mode = dialog.select('Debug logging modes', mode_list, 10000)

	if mode != -1:
		mode = mode_list[mode]
		if mode == "No logging":
			value = -1
		elif mode == "Normal logging":
			value = 0
		elif mode == "Debug logging":
			value = 1
		elif mode == "Debug logging with on screen info":
			value = 2
		else:
			value = 3
			
		line_found = False
		new_line = '        <loglevel hide="%s">%s</loglevel>\n' % (arg1, value)
		
		for line in fileinput.input(Current_Profile_AdvSettings, inplace=1):
			if '<loglevel hide=' in line:
				line = new_line
				line_found = True
			print line,
		
		# if old advancedsettings.xml
		if not line_found:
			with open(Current_Profile_AdvSettings, 'r') as f:
				lines = f.readlines()
			lines.insert(1, new_line)  # Insert at index 1 (line 2)
			with open(Current_Profile_AdvSettings, 'w') as f:
				f.writelines(lines)
		
		if value >= 2:
			xbmc.executebuiltin('EnableDebugMode')
		else:
			xbmc.executebuiltin('DisableDebugMode')
		xbmc.executebuiltin('ReloadAdvancedSettings')
		# dialog.ok("Debug mode set to",mode)

if __name__ == "__main__":
	main()