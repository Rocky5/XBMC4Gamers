from xbmcgui import Dialog
import sys

sys.argv.extend(["", "", "Change me", "", "", "", "no", "yes", "", "no"])
settings, dialog_type, title, line1, line2, line3, no, yes, commands, runcommands = sys.argv[1:11]


if dialog_type == "yesno":
	if Dialog().yesno(title,line1,line2,line3,xbmc.getLocalizedString(106),xbmc.getLocalizedString(107)):
		if settings != "":
			for settings in settings.split('~'):
				xbmc.executebuiltin(settings)
	
		if runcommands == "yes" and commands != "":
			for commands in commands.split('~'):
				xbmc.executebuiltin(commands)

if dialog_type == "ok":
	Dialog().ok(title,line1,line2,line3)

	if runcommands == "yes" and commands != "":
		for commands in commands.split('~'):
			xbmc.executebuiltin(commands)