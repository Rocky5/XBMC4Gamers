######################################################################
# Script by Rocky5
# Used to disable Master lock mode on all Profiles.
#
# Update: 05 January 2015
#
######################################################################

import os
import xbmcgui
import xbmc
import fileinput
import time

Profile = xbmc.translatePath( "special://xbmc/UserData/profiles.xml" )

for line in fileinput.input(Profile, inplace=True):
	print(line.replace('<lockmode>2</lockmode>','<lockmode>0</lockmode>'))
else:
	print ""

dialog = xbmcgui.Dialog()
dialog.ok("Disabling Master lock Mode","","This is no longer needed.","Reboot is required")

xbmc.executebuiltin("Skin.SetBool(MasterModeDisabled)")
xbmc.executebuiltin("reboot")