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

pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

USEGAMESTBNFILES = sys.argv[1] if len(sys.argv) > 1 else "0"
REMOVETHUMBNAILS = sys.argv[2] if len(sys.argv) > 2 else "0"
MYPROGRAMS_DB = xbmc.translatePath("special://profile/database/MyPrograms6.db").decode('utf-8')
THUMBDIRECTORY = xbmc.translatePath("special://profile/thumbnails/programs/").decode('utf-8')
TEMP_PROFILE_DIRECTORY = xbmc.translatePath("special://profile/thumbnails/temp/").decode('utf-8')
SUB_DIRECTORIES = [str(i) for i in range(10)] + list("abcdef")

def create_directories():
	if not os.path.isdir(TEMP_PROFILE_DIRECTORY):
		os.makedirs(TEMP_PROFILE_DIRECTORY)
	for sub_dir in SUB_DIRECTORIES:
		sub_dir_path = os.path.join(TEMP_PROFILE_DIRECTORY, sub_dir)
		if not os.path.isdir(sub_dir_path):
			os.mkdir(sub_dir_path)

def clean_thumbnails(rows):
	pDialog.create("Cleaning Thumbnails")
	for count, row in enumerate(rows, 1):
		if pDialog.iscanceled():
			pDialog.close()
			dialog.ok("Cancelled", "", "Cancelled cleaning process")
			return 0
		game_title, thumb_cache = row[3], xbmc.getCacheThumbName(row[1])
		thumb_path = os.path.join(THUMBDIRECTORY, thumb_cache[0], thumb_cache)
		
		progress = (count * 100) / len(rows)
		pDialog.update(progress, "", "Processing:[CR]{}".format(game_title))
		
		if os.path.isfile(thumb_path):
			shutil.copy2(thumb_path, os.path.join(TEMP_PROFILE_DIRECTORY, thumb_cache[0], thumb_cache))

	pDialog.close()
	return 1

def generate_thumbnails(rows):
	pDialog.create("Generating Thumbnails")
	for count, row in enumerate(rows, 1):
		if pDialog.iscanceled():
			pDialog.close()
			dialog.ok("Cancelled", "", "Cancelled thumbnail creation")
			return 0
		game_title, default_tbn, thumb_cache = row[3], row[1][:-3] + "tbn", xbmc.getCacheThumbName(row[1])
		synopsis, poster = os.path.join(row[23].decode('utf-8'), "artwork/synopsis.jpg"), os.path.join(row[23].decode('utf-8'), "artwork/poster.jpg")

		default_tbn = poster if os.path.isfile(poster) else (synopsis if os.path.isfile(synopsis) else default_tbn)
		progress = (count * 100) / len(rows)
		pDialog.update(progress, "", "Generation thumbnails for:[CR]{}".format(game_title))
		time.sleep(0.05) # Ensures the progress bar updates properly

		xbmc.executebuiltin('CacheThumbnail("{}","{}")'.format(default_tbn, os.path.join(TEMP_PROFILE_DIRECTORY, thumb_cache[0], thumb_cache)))

	pDialog.close()
	return 1

def main():
	# Close the script loading dialog
	xbmc.executebuiltin('Dialog.Close(1100,false)')
	
	not_cancelled = 1
	
	if not (os.path.isfile(MYPROGRAMS_DB) or REMOVETHUMBNAILS):
		dialog.ok("Error", "MyPrograms6.db is missing.")
		return

	create_directories()
	try:
		if USEGAMESTBNFILES == "0" and REMOVETHUMBNAILS == "0":
			with sqlite3.connect(MYPROGRAMS_DB, check_same_thread=False) as con:
				con.text_factory = str
				rows = con.execute("SELECT * FROM files").fetchall()
				not_cancelled = clean_thumbnails(rows)
				if not_cancelled:
					dialog.ok("Thumbnail Cleaner", "", "Cleaned all thumbnails.")
		elif USEGAMESTBNFILES == "1" and REMOVETHUMBNAILS == "0":
			with sqlite3.connect(MYPROGRAMS_DB, check_same_thread=False) as con:
				con.text_factory = str
				rows = con.execute("SELECT * FROM files").fetchall()
				not_cancelled = generate_thumbnails(rows)
				if not_cancelled:
					dialog.ok("Thumbnail Cleaner", "", "Generated thumbnails.")
		elif REMOVETHUMBNAILS == "1":
			pDialog.create("Remove Thumbnails", "", "Removing thumbnails...")
			time.sleep(1)
			pDialog.close()
			dialog.ok("Thumbnail Cleaner", "", "Thumbnails deleted.")
	except Exception as e:
		dialog.ok("Error", "An error occurred: {}".format(e))
	finally:
		if os.path.isdir(THUMBDIRECTORY):
			shutil.rmtree(THUMBDIRECTORY)
		os.rename(TEMP_PROFILE_DIRECTORY.rstrip('/'), TEMP_PROFILE_DIRECTORY[:-5] + "Programs")

if __name__ == "__main__":
	main()