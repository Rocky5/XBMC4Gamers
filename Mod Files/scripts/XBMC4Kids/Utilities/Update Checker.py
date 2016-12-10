'''
	Script by Rocky5
	Used to check for the updater folder & also cleanup when the update is done.
'''


import os
import xbmcgui
import xbmc
import shutil
import time


#####	Start markings for the log file.
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\Update Checker.py loaded."
print "| ------------------------------------------------------------------------------"


pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

if os.path.isfile( xbmc.translatePath( "special://xbmc/Updater/default.xbe" ) ):
	if os.path.isfile( xbmc.translatePath( "special://xbmc/Updater/update_complete" ) ):
		dialog.ok("Update Successful","","Will do some cleanup now.")
		pDialog.create( "CleanUp Process" )
		pDialog.update(0,"Working","Please Wait..."," " )
		
		if os.path.exists(xbmc.translatePath("special://xbmc/Updater")):
			pDialog.update(50,"Working","Please Wait..."," " )
			shutil.rmtree( xbmc.translatePath( "special://xbmc/Updater" ) )
			
		pDialog.update(100," ","Done."," " )
		time.sleep(2)
		pDialog.close()
		dialog.ok( "Done","","That's you all updated :)" )
		xbmc.executebuiltin( "Skin.SetBool(editmode)" )
		xbmc.executebuiltin( "SetFocus(52)" )
	else:
		if dialog.yesno( "XBMC4Kids Updater","", "Update Folder found, would you like to install the update?","","Update Later","Update Now" ) == 1:
			xbmc.executebuiltin( "XBMC.RunXBE( %sDefault.xbe )" % xbmc.translatePath( "special://xbmc/Updater/" ) )
		else:
			xbmc.executebuiltin( "SetFocus(52)" )
else:
	xbmc.executebuiltin( "SetFocus(52)" )
print "================================================================================"