'''
Script by Rocky5
Used to enable/disable edit mode control file.
'''

import os
import xbmcgui
import xbmc

dialog = xbmcgui.Dialog()
enabler_path = "Q:/system/keymaps/Enabled"

print "| Scripts/XBMC4Gamers/Utilities/Edit Mode.py loaded."

def toggle_edit_mode():
	if os.path.isfile(enabler_path):
		os.remove(enabler_path)
		dialog.ok(	"Kiosk Mode",
					"",
					"Enabled, you have limited access to features."	)
		xbmc.executebuiltin('Skin.reset(kioskmode)')
	else:
		with open(enabler_path, "w") as profile:
			profile.write(" ")
		dialog.ok(	"Kiosk Mode",
					"",
					"Disabled, you now have full access to all features."	)
		xbmc.executebuiltin('Skin.SetBool(kioskmode)')

	xbmc.executebuiltin("ReloadSkin")

	if xbmcgui.getCurrentWindowId() == 11111:
		home_window_source = xbmc.getInfoLabel('skin.String(HomeWindowSource)')
		xbmc.executebuiltin('ReplaceWindow(' + home_window_source + ')')

# Uncomment the following lines if needed
# xbmc.executebuiltin("Action(reloadkeymaps)")
# xbmc.executebuiltin("RestartApp")

toggle_edit_mode()
