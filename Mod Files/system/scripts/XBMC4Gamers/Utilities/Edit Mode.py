'''
Script by Rocky5
Used to enable/disable edit mode control file.
'''

import os
import xbmcgui
import xbmc
import sys

dialog = xbmcgui.Dialog()
enabler_path = "Q:/system/keymaps/Enabled"

print "| Scripts/XBMC4Gamers/Utilities/Edit Mode.py loaded."

def toggle_edit_mode():
	if os.path.isfile(enabler_path):
		os.remove(enabler_path)
		dialog.ok(
			"Kiosk Mode",
			"[CR]Kiosk mode has been enabled.[CR]Your access to features is now limited."
		)
		xbmc.executebuiltin('Skin.Reset(kioskmode)')
	else:
		with open(enabler_path, "w") as profile:
			profile.write(" ")
		dialog.ok(
			"Kiosk Mode",
			"[CR]Kiosk mode has been disabled.[CR]You now have full access to all features."
		)
		xbmc.executebuiltin('Skin.SetBool(kioskmode)')

	xbmc.executebuiltin("ReloadSkin")

	if xbmcgui.getCurrentWindowId() == 11111:
		home_window_source = xbmc.getInfoLabel('skin.String(HomeWindowSource)')
		xbmc.executebuiltin('ReplaceWindow({})'.format(home_window_source))

	# xbmc.executebuiltin("Action(reloadkeymaps)")
	# xbmc.executebuiltin("RestartApp")

def toggle_kiosk_mode():
	if os.path.isfile(enabler_path):
		xbmc.executebuiltin('Skin.SetBool(kioskmode)')
	else:
		xbmc.executebuiltin('Skin.reset(kioskmode)')

if __name__ == "__main__":
	arg = sys.argv[1] if len(sys.argv) > 1 else '1'
	if arg == '1':
		toggle_edit_mode()
	else:
		toggle_kiosk_mode()