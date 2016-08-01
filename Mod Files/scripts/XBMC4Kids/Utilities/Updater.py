########################################################################################################################################
'''
	Script by Rocky5
	Used to check for the updater folder & also cleanup when the update is done.
'''
########################################################################################################################################


import os, xbmcgui, xbmc, shutil
########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\Updater.py loaded."
print "| ------------------------------------------------------------------------------"

dialog = xbmcgui.Dialog()

if os.path.isfile(xbmc.translatePath("special://xbmc/Updater/default.xbe")):
	if os.path.isfile(xbmc.translatePath("special://xbmc/Updater/update_complete")):
		pDialog = xbmcgui.DialogProgress()
		dialog = xbmcgui.Dialog()
		dialog.ok("","", "Update Successful.")
		pDialog.create("Cleaning Up","", "Please wait")
		pDialog.update(50,"", "Please wait")
		try:
			if os.path.exists(xbmc.translatePath("special://xbmc/Updater")):
				shutil.rmtree(xbmc.translatePath("special://xbmc/Updater"))
		except:
			pass
		pDialog.update(100,"", "Please wait")
		pDialog.close()
		dialog.ok("Done","","Thats you all updated :)")
		xbmc.executebuiltin('Skin.SetBool(editmode)')
	else:
		if dialog.yesno("XBMC4Kids Updater","", "Update Folder found, would you like to install the update?") == 1:
			xbmc.executebuiltin("XBMC.RunXBE(%sDefault.xbe)" % xbmc.translatePath("special://xbmc/Updater/"))
		else:
			pass
			
print "================================================================================"