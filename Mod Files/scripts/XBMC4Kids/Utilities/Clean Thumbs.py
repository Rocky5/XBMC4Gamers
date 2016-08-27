########################################################################################################################################
'''
	Script by Rocky5
	Removed all the .tbn/dds file inside the "thumbnail\programs\" directory for said profile.
	
	Update: 21 August 2016
	-- Updated the progress bars code & .

	Update: 08 August 2016
	-- Added dynamic progress dialogues and improved the code.

	Update: 28 July 2016
	-- Added a Yes No dialog and a OK dialog at the end, also cleaned it up a bit.
'''
########################################################################################################################################


import sys
import os
import xbmc
import xbmcgui
import time
import shutil
import sqlite3


# Remove unused cached thumbnails						= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Clean Thumbs.py )
# Remove all cached thumbnails							= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Clean Thumbs.py,0,1 )
# Remove all cached thumbnails & re-cache default.tbn	= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Clean Thumbs.py,1,0 )
try:
	UseGamesTBNFiles = sys.argv[1:][0]
	RemoveThumbnails = sys.argv[2:][0]
except:
	UseGamesTBNFiles = "0"
	RemoveThumbnails = "0"


rows					= sqlite3.connect(xbmc.translatePath( "special://Profile/Database/MyPrograms6.db" )).cursor().execute("SELECT * FROM files").fetchall()
ThumbDirectory			= xbmc.translatePath( "special://profile/thumbnails/programs/" )
Profile_Directory		= xbmc.translatePath( 'special://profile/' )
Temp_Profile_Directory	= xbmc.translatePath( "special://profile/thumbnails/temp/" )
pDialog					= xbmcgui.DialogProgress()
dialog					= xbmcgui.Dialog()
pDialog.update( 0 )


########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\Clean Thumbs.py loaded."
print "| ------------------------------------------------------------------------------"

	
if UseGamesTBNFiles == "0" and RemoveThumbnails == "0":
	CountList = 1
	for row in rows:
		Game_Title = row[3]
		ThumbCache = xbmc.getCacheThumbName( row[1] )
		if os.path.isdir( row[1][:9] ):
			if os.path.isfile( row[1] ):
				if not os.path.isdir( Temp_Profile_Directory ): os.mkdir( Temp_Profile_Directory )
				if not os.path.isdir( Temp_Profile_Directory + ThumbCache[0] ): os.mkdir( Temp_Profile_Directory + ThumbCache[0] )
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
				if not os.path.isdir( Temp_Profile_Directory ): os.mkdir( Temp_Profile_Directory )
				if not os.path.isdir( Temp_Profile_Directory + ThumbCache[0] ): os.mkdir( Temp_Profile_Directory + ThumbCache[0] )
				if CountList == 1: pDialog.create( "Remove Thumbnails" )
				pDialog.update( ( CountList * 100 ) / len( os.listdir( row[1][:9] ) ),"Removing",ThumbCache )
				if os.path.isfile( ThumbDirectory + ThumbCache[0] + "\\" + ThumbCache ):
					shutil.copy2( ThumbDirectory + ThumbCache[0] + "\\" + ThumbCache, Temp_Profile_Directory + ThumbCache[0] + "\\" + ThumbCache )
					os.remove( Temp_Profile_Directory + ThumbCache[0] + "\\" + ThumbCache )
				CountList = CountList + 1

elif UseGamesTBNFiles == "1" and RemoveThumbnails == "0":
	CountList = 1
	for row in rows:
		Game_Title = row[3]
		DefaultTBN = row[1][:-11] + "default.tbn"
		ThumbCache = xbmc.getCacheThumbName( row[1] )
		if os.path.isdir( row[1][:9] ):
			if os.path.isfile( row[1] ):
				if not os.path.isdir( Temp_Profile_Directory ): os.mkdir( Temp_Profile_Directory )
				if not os.path.isdir( Temp_Profile_Directory + ThumbCache[0] ): os.mkdir( Temp_Profile_Directory + ThumbCache[0] )
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