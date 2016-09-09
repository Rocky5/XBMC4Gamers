'''
	Script by Rocky5
	Removes all the .tbn/dds file inside the "thumbnail\programs\" directory that no longer in use.
	
	Update: 01 September 2016
	-- Added some error checking and exception code & improved and reduced the code.
	
	Update: 21 August 2016
	-- Updated the progress bars code & added arguments to do extra tasks.

	Update: 08 August 2016
	-- Added dynamic progress dialogues and improved the code.

	Update: 28 July 2016
	-- Added a Yes No dialog and a OK dialog at the end, also cleaned it up a bit.
	
	Useage:
		Remove unused cached thumbnails							= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Clean Thumbs.py )
		Remove all cached thumbnails							= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Clean Thumbs.py,0,1 )
		Remove all cached thumbnails & re-cache default.tbn		= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Clean Thumbs.py,1,0 )
'''


import sys
import os
import xbmc
import xbmcgui
import time
import shutil
import sqlite3


try:
	UseGamesTBNFiles = sys.argv[1:][0]
	RemoveThumbnails = sys.argv[2:][0]
except:
	UseGamesTBNFiles = "0"
	RemoveThumbnails = "0"


MyPrograms6_db			= xbmc.translatePath( "special://profile/database/MyPrograms6.db" )
ThumbDirectory			= xbmc.translatePath( "special://profile/thumbnails/programs/" )
Temp_Profile_Directory	= xbmc.translatePath( "special://profile/thumbnails/temp/" )
Sub_Directories			= [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f" ]
pDialog					= xbmcgui.DialogProgress()
dialog					= xbmcgui.Dialog()
pDialog.update( 0 )


#####	Start markings for the log file.
print "================================================================================"
print "| Scripts\XBMC4Kids Extras\Clean Program Thumbs\resources\lib\default.py loaded."
print "| ------------------------------------------------------------------------------"

if os.path.isfile( MyPrograms6_db ):

	for Sub_Directories in Sub_Directories:
		if not os.path.isdir( Temp_Profile_Directory ): os.mkdir( Temp_Profile_Directory )
		if not os.path.isdir( os.path.join( Temp_Profile_Directory, Sub_Directories ) ): os.mkdir( os.path.join( Temp_Profile_Directory, Sub_Directories ) )
	try:
		rows = sqlite3.connect( xbmc.translatePath( MyPrograms6_db ) ).cursor().execute( "SELECT * FROM files" ).fetchall()
		if UseGamesTBNFiles == "0" and RemoveThumbnails == "0":
			CountList = 1
			for row in rows:
				Game_Title = row[3]
				ThumbCache = xbmc.getCacheThumbName( row[1] )
				if os.path.isdir( row[1][:9] ):
					if os.path.isfile( row[1] ):
						if CountList == 1: pDialog.create( "Cleaning Thumbnails" )
						pDialog.update( ( CountList * 100 ) / len( os.listdir( row[1][:9] ) ),"Processing",Game_Title,ThumbCache )
						if os.path.isfile( ThumbDirectory + ThumbCache[0] + "\\" + ThumbCache ):
							shutil.copy2( ThumbDirectory + ThumbCache[0] + "\\" + ThumbCache, Temp_Profile_Directory + ThumbCache[0] + "\\" + ThumbCache )
						CountList = CountList + 1

		elif UseGamesTBNFiles == "0" and RemoveThumbnails == "1":
			CountList = 1
			for row in rows:
				Game_Title = row[3]
				ThumbCache = xbmc.getCacheThumbName( row[1] )
				if os.path.isdir( row[1][:9] ):
					if os.path.isfile( row[1] ):
						if CountList == 1: pDialog.create( "Remove Thumbnails" )
						pDialog.update( ( CountList * 100 ) / len( os.listdir( row[1][:9] ) ),"Removing",ThumbCache )
						CountList = CountList + 1

		elif UseGamesTBNFiles == "1" and RemoveThumbnails == "0":
			CountList = 1
			for row in rows:
				Game_Title = row[3]
				DefaultTBN = row[1][:-3] + "tbn"
				ThumbCache = xbmc.getCacheThumbName( row[1] )
				if os.path.isdir( row[1][:9] ):
					if os.path.isfile( row[1] ):
						if CountList == 1: pDialog.create( "Generating Thumbnails" )
						pDialog.update( ( CountList * 100 ) / len( os.listdir( row[1][:9] ) ),"Scanning Games",Game_Title,ThumbCache )
						if os.path.isfile( DefaultTBN ):
							shutil.copy2( DefaultTBN, Temp_Profile_Directory + ThumbCache[0] + "\\" + ThumbCache )
						CountList = CountList + 1

		else:
			pass
		if os.path.isdir( ThumbDirectory ): shutil.rmtree( ThumbDirectory )
		os.rename( Temp_Profile_Directory[:-1], Temp_Profile_Directory[:-5] + "Programs" )
		print '| Cleaned all thumbnails.'
		print "================================================================================"
		pDialog.close()
		dialog.ok( "Thumbnail Cleaner","","Process Complete" )
	except:
		dialog.ok( "Error","","Database is empty.","Enter the games menu so XBMC can scan in your games." )
else:
	dialog.ok( "Error","","MyPrograms6.db is missing." )