'''
	Script by Rocky5
	Removes all the .tbn/dds file inside the "thumbnail\programs\" directory that no longer in use.
	Useage:
		Remove unused cached thumbnails							= RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Clean Thumbs.py)
		Remove all cached thumbnails							= RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Clean Thumbs.py,0,1)
		Remove all cached thumbnails & re-cache default.tbn		= RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Clean Thumbs.py,1,0)
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
MyPrograms_db			= xbmc.translatePath("special://profile/database/MyPrograms6.db")
ThumbDirectory			= xbmc.translatePath("special://profile/thumbnails/programs/")
Temp_Profile_Directory	= xbmc.translatePath("special://profile/thumbnails/temp/")
Sub_Directories			= [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f" ]
pDialog					= xbmcgui.DialogProgress()
dialog					= xbmcgui.Dialog()
pDialog.update(0)
print "| Scripts\XBMC4Gamers Extras\Clean Program Thumbs\resources\lib\default.py loaded."
if os.path.isfile(MyPrograms_db):
	for Sub_Directories in Sub_Directories:
		if not os.path.isdir(Temp_Profile_Directory): os.mkdir(Temp_Profile_Directory)
		if not os.path.isdir(os.path.join(Temp_Profile_Directory, Sub_Directories)): os.mkdir(os.path.join(Temp_Profile_Directory, Sub_Directories))
	try:
		con = sqlite3.connect(MyPrograms_db)
		cur = con.cursor()
		con.text_factory = str
		cur.execute("SELECT * FROM files")
		rows = cur.fetchall()
		
		if UseGamesTBNFiles == "0" and RemoveThumbnails == "0":
			CountList = 1
			for row in rows:
				Game_Title = row[3]
				ThumbCache = xbmc.getCacheThumbName(row[1])
				if os.path.isdir(row[1][:9]):
					if os.path.isfile(row[1]):
						if CountList == 1: pDialog.create("Cleaning Thumbnails")
						pDialog.update((CountList * 100) / len(os.listdir(row[1][:9])),"Processing",Game_Title,ThumbCache)
						if os.path.isfile(ThumbDirectory+ThumbCache[0]+"\\"+ThumbCache):
							shutil.copy2(ThumbDirectory+ThumbCache[0]+"\\"+ThumbCache, Temp_Profile_Directory+ThumbCache[0]+"\\"+ThumbCache)
						CountList = CountList+1
		elif UseGamesTBNFiles == "0" and RemoveThumbnails == "1":
			CountList = 1
			for row in rows:
				Game_Title = row[3]
				ThumbCache = xbmc.getCacheThumbName(row[1])
				if os.path.isdir(row[1][:9]):
					if os.path.isfile(row[1]):
						if CountList == 1: pDialog.create("Remove Thumbnails")
						pDialog.update((CountList * 100) / len(os.listdir(row[1][:9])),"Removing",ThumbCache)
						CountList = CountList+1
		elif UseGamesTBNFiles == "1" and RemoveThumbnails == "0":
			CountList = 1
			for row in rows:
				Game_Title = row[3]
				DefaultTBN = row[1][:-3]+"tbn"
				ThumbCache = xbmc.getCacheThumbName(row[1])
				if os.path.isdir(row[1][:9]):
					if os.path.isfile(row[1]):
						if CountList == 1: pDialog.create("Generating Thumbnails")
						pDialog.update((CountList * 100) / len(os.listdir(row[1][:9])),"Scanning Games",Game_Title,ThumbCache)
						if os.path.isfile(DefaultTBN):
							shutil.copy2(DefaultTBN, Temp_Profile_Directory+ThumbCache[0]+"\\"+ThumbCache)
						CountList = CountList+1
		else:
			pass
		if os.path.isdir(ThumbDirectory): shutil.rmtree(ThumbDirectory)
		os.rename(Temp_Profile_Directory[:-1], Temp_Profile_Directory[:-5]+"Programs")
		print '| Cleaned all thumbnails.'
		pDialog.close()
		dialog.ok("Thumbnail Cleaner","","Process Complete")
	except:
		dialog.ok("Error","","Database is empty.","Enter the games menu so XBMC can scan in your games.")
else:
	dialog.ok("Error","","MyPrograms6.db is missing.")