########################################################################################################################################
'''
	Script by Rocky5
	Removed all the .tbn/dds file inside the "thumbnail\programs\" directory for said profile.
	
	Update: 08 August 2016
	-- Added dynamic progress dialogues and improved the code.
	
	Update: 28 July 2016
	-- Added a Yes No dialog and a OK dialog at the end, also cleaned it up a bit.
'''
########################################################################################################################################


import os
import xbmc
import xbmcgui
import glob
import time
import shutil


UseGamesTBNFiles	= 0
ThumbPath			= xbmc.translatePath( "special://profile/thumbnails/programs" )
Sub_Directories		= [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "fanart" ]
Games_Directories	= [ "E:\\Games", "F:\\Games", "G:\\Games" ]
Profile_Directory	= xbmc.translatePath( 'special://profile/' )
pDialog				= xbmcgui.DialogProgress()
dialog				= xbmcgui.Dialog()
pDialog.update( 0 )


########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\Clean Thumbs.py loaded."
print "| ------------------------------------------------------------------------------"


if dialog.yesno( 'Thumbnail Cleaner','','Remove all the [B]Game[/B] Thumbsnails?','They will be reloaded when you enter the games section.' ) == 1:
	pDialog.create( 'Cleaning Thumbnails' )
	
	progress = 0
	for TBN_Folders in Sub_Directories:
		Thumbs_Directory = os.path.join( ThumbPath, TBN_Folders )
		progress += 1
		if progress == 1:	pDialog.update( 0,"Removing Game Thumbnails","Processing" )
		if os.path.isdir( Thumbs_Directory ) :
			TBNFiles = glob.glob( os.path.join( Thumbs_Directory, "*.tbn" ) )
			for tbn in TBNFiles:
				if os.path.isfile(tbn):
					os.remove(tbn)
					pDialog.update( int ( progress / float( len ( Sub_Directories ) ) *100 ),"Removing Game Thumbnails",tbn )
			DDSFiles = glob.glob( os.path.join( Thumbs_Directory, "*.dds" ) )
			for dds in DDSFiles:
				if os.path.isfile(dds):
					os.remove(dds)
					pDialog.update( int ( progress / float( len ( Sub_Directories ) ) *100 ),"Removing Game Thumbnails",dds )

	if UseGamesTBNFiles == 1:
		progress = 0
		for Folders in Games_Directories:
			for Game_Folder in sorted( os.listdir( Folders ) ):
				Game_Directory = os.path.join( Folders, Game_Folder)
				progress += 1
				pDialog.update( int ( progress / float( len ( sorted( os.listdir( Folders ) ) ) ) *100 ),"Generating Game Thumbnails",Game_Folder )
				if os.path.isdir( Game_Directory ):
					XBEFiles = glob.glob( os.path.join( Game_Directory, "default.xbe" ) )
					for DefaultXBE in XBEFiles:
						if os.path.isfile( DefaultXBE ):
							ThumbCache = xbmc.getCacheThumbName( DefaultXBE )
							ThumbPath = ( Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache )
							TBNFiles = glob.glob( os.path.join( Game_Directory, "default.tbn" ) )
					for DefaultTBN in TBNFiles:
						if os.path.isfile( DefaultTBN ):
								shutil.copy2( DefaultTBN,ThumbPath )
	else:
		pass


	print '| Removed all .tbn/dds files from "' + ThumbPath + '"'
	print "================================================================================"

	pDialog.close()
	dialog.ok( "Thumbnail Cleaner","","That's it all done :)." )
else:
	print '| You picked no.'
	print "================================================================================"