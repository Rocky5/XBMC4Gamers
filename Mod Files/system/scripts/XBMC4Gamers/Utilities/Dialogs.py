from xbmcgui import Dialog
from sys import argv
from xbmc import executebuiltin

argv.extend(["", "", "Change me", "", "", "", xbmc.getLocalizedString(106), xbmc.getLocalizedString(107), "", "no"])
settings, dialog_type, title, line1, line2, line3, no, yes, commands, runcommands = argv[1:11]

def execute_commands(commands):
	if commands:
		for command in commands.split('~'):
			executebuiltin(command)

def main():
	if dialog_type.lower() == "yesno":
		if Dialog().yesno(title, line1, line2, line3, no, yes):
			if settings:
				execute_commands(settings)
			if runcommands.lower() == "yes" and commands:
				execute_commands(commands)
	elif dialog_type.lower() == "ok":
		Dialog().ok(title, line1, line2, line3)
		if settings:
			execute_commands(settings)
		if runcommands.lower() == "yes" and commands:
			execute_commands(commands)

if __name__ == "__main__":
	main()
