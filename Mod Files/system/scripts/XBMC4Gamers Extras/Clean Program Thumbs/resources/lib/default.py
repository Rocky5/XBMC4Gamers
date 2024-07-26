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

# Get script arguments
UseGamesTBNFiles = sys.argv[1] if len(sys.argv) > 1 else "0"
RemoveThumbnails = sys.argv[2] if len(sys.argv) > 2 else "0"

# Define paths
MyPrograms_db = xbmc.translatePath("special://profile/database/MyPrograms6.db")
ThumbDirectory = xbmc.translatePath("special://profile/thumbnails/programs/")
Temp_Profile_Directory = xbmc.translatePath("special://profile/thumbnails/temp/")
Sub_Directories = [str(i) for i in range(10)] + list("abcdef")

# Initialize dialogs
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

pDialog.update(0)
print "| Scripts\\XBMC4Gamers Extras\\Clean Program Thumbs\\resources\\lib\\default.py loaded."

def create_directories():
    """Create necessary directories if they don't exist."""
    if not os.path.isdir(Temp_Profile_Directory):
        os.makedirs(Temp_Profile_Directory)
    for sub_dir in Sub_Directories:
        sub_dir_path = os.path.join(Temp_Profile_Directory, sub_dir)
        if not os.path.isdir(sub_dir_path):
            os.mkdir(sub_dir_path)

def clean_thumbnails(rows):
    """Clean unused thumbnails."""
    CountList = 1
    for row in rows:
        Game_Title = row[3]
        ThumbCache = xbmc.getCacheThumbName(row[1])
        if os.path.isdir(row[1][:9]) and os.path.isfile(row[1]):
            if CountList == 1:
                pDialog.create("Cleaning Thumbnails")
            pDialog.update((CountList * 100) / len(rows), "Processing", Game_Title, ThumbCache)
            thumb_path = os.path.join(ThumbDirectory, ThumbCache[0], ThumbCache)
            if os.path.isfile(thumb_path):
                shutil.copy2(thumb_path, os.path.join(Temp_Profile_Directory, ThumbCache[0], ThumbCache))
            CountList += 1

def generate_thumbnails(rows):
    """Generate thumbnails from default.tbn files."""
    CountList = 1
    for row in rows:
        Game_Title = row[3]
        DefaultTBN = row[1][:-3] + "tbn"
        ThumbCache = xbmc.getCacheThumbName(row[1])
        if os.path.isdir(row[1][:9]) and os.path.isfile(row[1]):
            if CountList == 1:
                pDialog.create("Generating Thumbnails")
            pDialog.update((CountList * 100) / len(rows), "Scanning Games", Game_Title, ThumbCache)
            if os.path.isfile(DefaultTBN):
                shutil.copy2(DefaultTBN, os.path.join(Temp_Profile_Directory, ThumbCache[0], ThumbCache))
            CountList += 1

if os.path.isfile(MyPrograms_db) or RemoveThumbnails:
    create_directories()

    try:
        if (UseGamesTBNFiles == "0" and RemoveThumbnails == "0") or (UseGamesTBNFiles == "1" and RemoveThumbnails == "0"):
            con = sqlite3.connect(MyPrograms_db, check_same_thread=False)
            cur = con.cursor()
            con.text_factory = str
            cur.execute("SELECT * FROM files")
            rows = cur.fetchall()

            if UseGamesTBNFiles == "0" and RemoveThumbnails == "0":
                clean_thumbnails(rows)
            elif UseGamesTBNFiles == "1" and RemoveThumbnails == "0":
                generate_thumbnails(rows)
        
        elif UseGamesTBNFiles == "0" and RemoveThumbnails == "1":
            pDialog.create("Remove Thumbnails", "", "Removing")
            time.sleep(1)
        
    finally:
        if 'con' in locals():
            con.close()

    if os.path.isdir(ThumbDirectory):
        shutil.rmtree(ThumbDirectory)
    os.rename(Temp_Profile_Directory[:-1], Temp_Profile_Directory[:-5] + "Programs")
    print '| Cleaned all thumbnails.'
    pDialog.close()
    dialog.ok("Thumbnail Cleaner", "", "Process Complete")
else:
    dialog.ok("Error", "", "MyPrograms6.db is missing.")
