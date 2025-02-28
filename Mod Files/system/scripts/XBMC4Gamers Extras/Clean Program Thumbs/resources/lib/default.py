# -*- coding: utf-8 -*- 
'''
	Script by Rocky5
	Removes all the .tbn/dds files inside the "thumbnail\programs\" directory that are no longer in use.
	Usage:
		Remove unused cached thumbnails                          = RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Clean Thumbs.py)
		Remove all cached thumbnails                             = RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Clean Thumbs.py,0,1)
		Remove all cached thumbnails & re-cache default.tbn      = RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Clean Thumbs.py,1,0)
'''

import os
import sys
import time
import xbmcgui
import shutil
import sqlite3

UseGamesTBNFiles = sys.argv[1] if len(sys.argv) > 1 else "0"
RemoveThumbnails = sys.argv[2] if len(sys.argv) > 2 else "0"

MyPrograms_db = xbmc.translatePath("special://profile/database/MyPrograms6.db")
ThumbDirectory = xbmc.translatePath("special://profile/thumbnails/programs/")
Temp_Profile_Directory = xbmc.translatePath("special://profile/thumbnails/temp/")
Sub_Directories = [str(i) for i in range(10)] + list("abcdef")

MyPrograms_db = MyPrograms_db.decode('utf-8')
ThumbDirectory = ThumbDirectory.decode('utf-8')
Temp_Profile_Directory = Temp_Profile_Directory.decode('utf-8')

pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

pDialog.update(0)
print "| Scripts\\XBMC4Gamers Extras\\Clean Program Thumbs\\resources\\lib\\default.py loaded."

def create_directories():
	if not os.path.isdir(Temp_Profile_Directory):
		os.makedirs(Temp_Profile_Directory)
	for sub_dir in Sub_Directories:
		sub_dir_path = os.path.join(Temp_Profile_Directory, sub_dir)
		if not os.path.isdir(sub_dir_path):
			os.mkdir(sub_dir_path)

def clean_thumbnails(rows):
	CountList = 0
	total_rows = len(rows)
	pDialog.create("Cleaning Thumbnails")
	
	for row in rows:
		CountList += 1
		Game_Title = row[3]
		ThumbCache = xbmc.getCacheThumbName(row[1])

		thumb_path = os.path.join(ThumbDirectory, ThumbCache[0], ThumbCache)
		
		if os.path.isdir(row[1][:9].decode('utf-8')) and os.path.isfile(row[1].decode('utf-8')):
			progress = (CountList * 100) // total_rows
			# pDialog.update(progress, "Processing", '{}[CR]{}'.format(Game_Title, ThumbCache))
			pDialog.update(progress, "Processing", '{}'.format(Game_Title))
			
			if os.path.isfile(thumb_path):
				shutil.copy2(thumb_path, os.path.join(Temp_Profile_Directory, ThumbCache[0], ThumbCache))

def generate_thumbnails(rows):
	CountList = 0
	total_rows = len(rows)
	pDialog.create("Generating Thumbnails")

	for row in rows:
		CountList += 1
		Game_Title = row[3]
		DefaultTBN = row[1][:-3] + "tbn"

		Check_Synopsis = os.path.join(row[23].decode('utf-8'), u"artwork/synopsis.jpg")
		Check_Poster = os.path.join(row[23].decode('utf-8'), u"artwork/poster.jpg")

		if os.path.isfile(Check_Poster):
			DefaultTBN = Check_Poster
		if os.path.isfile(Check_Synopsis):
			DefaultTBN = Check_Synopsis
			
		ThumbCache = xbmc.getCacheThumbName(row[1])

		if os.path.isdir(row[1][:9].decode('utf-8')) and os.path.isfile(row[1].decode('utf-8')):
			progress = (CountList * 100) // total_rows
			# pDialog.update(progress, "Scanning Database", '{}[CR]{}'.format(Game_Title, ThumbCache))
			pDialog.update(progress, "Scanning Database", '{}'.format(Game_Title))
			time.sleep(0.05) # Required or the progress bar doesn't work.
			xbmc.executebuiltin("CacheThumbnail({},{})".format(DefaultTBN, os.path.join(Temp_Profile_Directory, ThumbCache[0], ThumbCache)))

if os.path.isfile(MyPrograms_db) or RemoveThumbnails:
	create_directories()

	try:
		if UseGamesTBNFiles == "0" and RemoveThumbnails == "0" or UseGamesTBNFiles == "1" and RemoveThumbnails == "0":
			con = sqlite3.connect(MyPrograms_db, check_same_thread=False)
			cur = con.cursor()
			con.text_factory = str
			cur.execute("SELECT * FROM files")
			rows = cur.fetchall()

			if UseGamesTBNFiles == "0" and RemoveThumbnails == "0":
				clean_thumbnails(rows)
				Complete = "Cleaned all thumbnails."
			elif UseGamesTBNFiles == "1" and RemoveThumbnails == "0":
				generate_thumbnails(rows)
				Complete = "Generated thumbnails."
		elif UseGamesTBNFiles == "0" and RemoveThumbnails == "1":
			pDialog.create("Remove Thumbnails", "", "Removing")
			time.sleep(1)
			Complete = "Thumbnails deleted."

	finally:
		if 'con' in locals():
			con.close()

	if os.path.isdir(ThumbDirectory):
		shutil.rmtree(ThumbDirectory)
	os.rename(Temp_Profile_Directory[:-1], Temp_Profile_Directory[:-5] + "Programs")
	pDialog.close()
	dialog.ok("Thumbnail Cleaner", "", Complete)
else:
	dialog.ok("Error", "", "MyPrograms6.db is missing.")
