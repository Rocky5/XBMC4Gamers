'''	
	Script by Rocky5
	Used to enable/disable edit mode control file.
'''
import os
import xbmcgui
import xbmc
dialog = xbmcgui.Dialog()
Enabler = "Q:/system/keymaps/Enabled"
print "| Scripts\XBMC4Gamers\Utilities\Edit Mode.py loaded."
if os.path.isfile(Enabler):
	os.remove(Enabler)
	dialog.ok("Kios Mode","","Enabled, you have limited access to features.")
	xbmc.executebuiltin('Skin.reset(kioskmode)')
else:
	with open(Enabler,"w") as profile: profile.write(" ")
	dialog.ok("Kios Mode","","Disabled, you now have full access to all features.")
	xbmc.executebuiltin('Skin.SetBool(kioskmode)')

xbmc.executebuiltin("ReloadSkin")

if xbmcgui.getCurrentWindowId() == 11111:
	xbmc.executebuiltin('ReplaceWindow('+xbmc.getInfoLabel('skin.String(HomeWindowSource)')+')')

#xbmc.executebuiltin("Action(reloadkeymaps)")
#xbmc.executebuiltin("RestartApp")