'''
Script by Rocky5
Used to enable/disable edit mode control file.
'''
from os.path import isfile
from os import remove
from sys import argv
from xbmc import executebuiltin, getInfoLabel
from xbmcgui import Dialog, getCurrentWindowId

ENABLER_PATH = "Q:/system/keymaps/Enabled"

# print "| Scripts/XBMC4Gamers/Utilities/Edit Mode.py loaded."

def toggle_edit_mode():
	if isfile(ENABLER_PATH):
		remove(ENABLER_PATH)
		Dialog().ok(
			"Kiosk Mode",
			"[CR]Kiosk mode has been enabled.[CR]Your access to features is now limited."
		)
		executebuiltin('Skin.Reset(kioskmode)')
	else:
		with open(ENABLER_PATH, "w") as profile:
			profile.write(" ")
		Dialog().ok(
			"Kiosk Mode",
			"[CR]Kiosk mode has been disabled.[CR]You now have full access to all features."
		)
		executebuiltin('Skin.SetBool(kioskmode)')

	executebuiltin("ReloadSkin")

	if getCurrentWindowId() == 11111:
		home_window_source = getInfoLabel('skin.String(HomeWindowSource)')
		executebuiltin('ReplaceWindow({})'.format(home_window_source))

	# executebuiltin("Action(reloadkeymaps)")
	# executebuiltin("RestartApp")

def check_kioskmode():
	if isfile(ENABLER_PATH):
		executebuiltin('Skin.SetBool(kioskmode)')
	else:
		executebuiltin('Skin.reset(kioskmode)')

if __name__ == "__main__":
	arg = argv[1] if len(argv) > 1 else '0'
	if arg == '1':
		toggle_edit_mode()
	else:
		check_kioskmode()