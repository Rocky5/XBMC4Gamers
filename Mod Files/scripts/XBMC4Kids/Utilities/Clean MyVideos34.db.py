'''
	Script by Dan Dar3
	Modified by Rocky5
	
	Removes the video bookmark when seeking or playing back of a video.
	It seems to be broken in XBMC 3.5.3
'''


import sqlite3
import time


#####	Start markings for the log file.
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\Clean MyVideos34.db.py loaded."
print "| ------------------------------------------------------------------------------"


CurVideoDB = xbmc.translatePath( 'special://Database/MyVideos34.db' )
time.sleep(0.5)
connection = sqlite3.connect(CurVideoDB)
connection.cursor().execute("DELETE from bookmark")
time.sleep(0.1)
connection.commit()
connection.close()
print "| MyVideos34.db bookmarks removed."
print "================================================================================"