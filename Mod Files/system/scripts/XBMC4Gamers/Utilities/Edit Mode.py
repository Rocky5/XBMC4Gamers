'''	
	Script by Rocky5
	Used to enable/disable edit mode control file.
'''
import os
import xbmcgui
import xbmc
import shutil
import time
Gamepad = xbmc.translatePath("special://xbmc/system/keymaps/gamepad.xml")
NormalMode = xbmc.translatePath("special://xbmc/system/keymaps/UserMode.file")
EditMode = xbmc.translatePath("special://xbmc/system/keymaps/EditMode.file")
Enabler = xbmc.translatePath("special://xbmc/system/keymaps/Enabled")
dialog = xbmcgui.Dialog()
print "| Scripts\XBMC4Gamers\Utilities\Edit Mode.py loaded."
if os.path.isfile(Enabler):
	os.remove(Enabler)
	shutil.copy2(NormalMode, Gamepad)
	xbmc.executebuiltin('Skin.reset(editmode)')
	dialog.ok("My young padawan","","User mode is enabled, I need to restart XBMC","so that the changes take affect.")
	#dialog.ok("My young padawan","","User Mode Enabled","Press [B](A)[/B] to restart XBMC4Gamers.")
	print "| User mode enabled."
else:
	profile = open(Enabler,"w")
	profile.write(" ")
	profile.close()	
	shutil.copy2(EditMode, Gamepad)
	xbmc.executebuiltin('Skin.SetBool(editmode)')
	dialog.ok("Now, I am the Master","","Edit mode is enabled, I need to restart XBMC","so that the changes take affect.")
	#dialog.ok("Now, I am the Master","","Edit Mode Enabled","Press [B](A)[/B] to restart XBMC4Gamers.")
	print "| Edit mode enabled."
#xbmc.executebuiltin("Action(reloadkeymaps)")
xbmc.executebuiltin("RestartApp")