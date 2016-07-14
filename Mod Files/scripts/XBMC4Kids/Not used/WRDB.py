########################################################################################################################################
'''
	Script by Rocky5
	Test Script to see if I can write to a new DB & read entries from it.
'''
########################################################################################################################################


import os
import xbmcgui
import xbmc
import shutil
import glob
import fileinput
import time
import sqlite3


########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\WRDB.py loaded."
print "| ------------------------------------------------------------------------------"
	

########################################################################################################################################
# Sets paths, for profiles names & locations.
########################################################################################################################################
Working_Directory = os.getcwd() + "\\"
Dashboard_Path = xbmc.translatePath( 'special://xbmc/' )
NewDB = os.path.join( Dashboard_Path,"NewDB.db" )
##
Username = xbmc.getInfoLabel('system.profilename')

print NewDB


conn = sqlite3.connect(NewDB)
c = conn.cursor()
	
try:
	c.execute( "CREATE TABLE user (username text, savedir text, profile text)" )
	c.execute( "CREATE TABLE lastuser (username text, savedir text, profile text)" )
	c.execute( "INSERT INTO user VALUES (?, ?, ?)", (Username,"UDATA "+Username, Username+".profile"))
	c.execute( "INSERT INTO lastuser VALUES (?, ?, ?)", (Username,"UDATA "+Username, Username+".profile"))
	conn.commit()
	conn.close()
except:
	xbmc.executebuiltin( "Xbmc.Notification(,Already created DB.)" )
	conn.commit()
	conn.close()

conn = sqlite3.connect(NewDB)
c = conn.cursor()

try:
	conn.text_factory = str
	c.execute( "SELECT * from lastuser" )
	lastdata = c.fetchone() # (lastdata[0]) (lastdata[1]) (lastdata[2])
	c.execute( "UPDATE user SET username=?, savedir=?, profile=?", (Username,"UDATA "+Username, Username+".profile") )
	c.execute( "UPDATE lastuser SET username=?, savedir=?, profile=?", (Username,"UDATA "+Username, Username+".profile") )
	c.execute( "SELECT * from lastuser" )
	curdata = c.fetchone() # (curdata[0]) (curdata[1]) (curdata[2])
	xbmc.executebuiltin( "Xbmc.Notification(,update.)" )
	conn.commit()
	conn.close()
except:
	xbmc.executebuiltin( "Xbmc.Notification(,WTF?!!!... hmp! update failed.)" )
	conn.commit()
	conn.close()

print (lastdata[0])
print (lastdata[1])
print (lastdata[2])
print (curdata[0])
print (curdata[1])
print (curdata[2])




