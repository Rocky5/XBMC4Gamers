'''	
	Script by Rocky5
	Used to enable/disable edit mode control file.

	Update: 25 June 2016
	-- Reverted back to restarting XBMC, reloading the keymap was causing issues with the skins & skin settings.
	   not entirely sure how or why, but strange stuff happened lol

	Update: 16 February 2016
	-- Now reload the current keymap with the undocumented command ;)

	Update: 15 December 2014
	-- Changed how the files are created, this fixes all issues.
	   Added a dialog popup.
'''


import os
import xbmcgui
import xbmc
import shutil
import time


Gamepad = xbmc.translatePath( "special://xbmc/system/keymaps/gamepad.xml" )
NormalMode = xbmc.translatePath( "special://xbmc/system/keymaps/UserMode.file" )
EditMode = xbmc.translatePath( "special://xbmc/system/keymaps/EditMode.file" )
Enabler = xbmc.translatePath( "special://xbmc/system/keymaps/Enabled" )
dialog = xbmcgui.Dialog()


#####	Start markings for the log file.
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\Edit Mode.py loaded."
print "| ------------------------------------------------------------------------------"

if os.path.isfile(Enabler):
	os.remove(Enabler)
	shutil.copy2(NormalMode, Gamepad)
	xbmc.executebuiltin('Skin.reset(editmode)')
	dialog.ok("My young padawan","","User mode is enabled, I need to restart XBMC","so that the changes take affect.")
	#dialog.ok("My young padawan","","User Mode Enabled","Press [B](A)[/B] to restart XBMC4Kids.")
	print "| User mode enabled."
	print "================================================================================"
else:
	profile = open(Enabler,"w")
	profile.write(" ")
	profile.close()	
	shutil.copy2(EditMode, Gamepad)
	xbmc.executebuiltin('Skin.SetBool(editmode)')
	dialog.ok("Now, I am the Master","","Edit mode is enabled, I need to restart XBMC","so that the changes take affect.")
	#dialog.ok("Now, I am the Master","","Edit Mode Enabled","Press [B](A)[/B] to restart XBMC4Kids.")
	print "| Edit mode enabled."
	print "================================================================================"

#xbmc.executebuiltin("Action(reloadkeymaps)")
xbmc.executebuiltin("RestartApp")