########################################################################################################################################
'''
	Script by Rocky5
	Removed all the .tbn/dds file inside the "thumbnail\programs\" directory for said profile.
	
	Update: 28 July 2016
	-- Added a Yes No dialog and a OK dialog at the end, also cleaned it up a bit.
'''
########################################################################################################################################


import os
import xbmc
import xbmcgui
import glob
import time


ThumbPath			= xbmc.translatePath( "special://profile/thumbnails/programs" )
Sub_Directories		= [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "fanart" ]
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()


########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\CleanThumbs.py loaded."
print "| ------------------------------------------------------------------------------"

if dialog.yesno('Thumbnail Cleaner','','Remove all the [B]Game[/B] Thumbsnails?','They will be reloaded when you enter the games section.') == 1:
	pDialog.create('Cleaning Thumbnails')
	pDialog.update(0, 'Please wait')
	time.sleep(0.1)
	pDialog.update(20, 'Please wait')
	time.sleep(0.1)
	pDialog.update(50, 'Please wait')

	for Sub_Directories in Sub_Directories :
		Thumbs_Directory = os.path.join( ThumbPath, Sub_Directories )
		if os.path.isdir( Thumbs_Directory ) :
			TBNFiles = glob.glob( os.path.join( Thumbs_Directory, "*.tbn" ) )
			for tbn in TBNFiles:
				os.remove(tbn)
				DDSFiles = glob.glob( os.path.join( Thumbs_Directory, "*.dds" ) )
				for dds in DDSFiles:
					os.remove(dds)

	pDialog.update(55, 'Please wait')
	time.sleep(0.1)
	pDialog.update(80, 'Please wait')

	print '| Removed all .tbn/dds files from "' + ThumbPath + '"'
	print "================================================================================"

	pDialog.update(100, 'Please wait')
	pDialog.close()
	dialog.ok('Thumbnail Cleaner','','All Thumbnails Removed.')
else:
	print '| You picked no.'
	print "================================================================================"