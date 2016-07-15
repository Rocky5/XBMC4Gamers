########################################################################################################################################
'''
	Script by Rocky5
	Removed all the .tbn/dds file inside the "thumbnail\programs\" directory for said profile.
'''
########################################################################################################################################


import os
import xbmc
import xbmcgui
import glob
import time


ThumbPath			= xbmc.translatePath( "special://profile/thumbnails/programs" )
Sub_Directories		= [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "fanart" ]

########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\CleanThumbs.py loaded."
print "| ------------------------------------------------------------------------------"


pDialog = xbmcgui.DialogProgress()
pDialog.create('Cleaning Thumbnails')
pDialog.update(0, 'Please wait')
time.sleep(0.2)
pDialog.update(20, 'Please wait')
time.sleep(0.2)
pDialog.update(50, 'Please wait')
time.sleep(0.2)
pDialog.update(55, 'Please wait')
time.sleep(0.2)
pDialog.update(80, 'Please wait')

for Sub_Directories in Sub_Directories :
	Thumbs_Directory = os.path.join( ThumbPath, Sub_Directories )
	if os.path.isdir( Thumbs_Directory ) :
		TBNFiles = glob.glob( os.path.join( Thumbs_Directory, "*.tbn" ) )
		DDSFiles = glob.glob( os.path.join( Thumbs_Directory, "*.dds" ) )
		for tbn in TBNFiles:
			#print tbn
			os.remove(tbn)
			for dds in DDSFiles:
				#print tbn
				os.remove(dds)

print '| Removed all .tbn/dds files from "' + ThumbPath + '"'
print "================================================================================"

pDialog.update(100, 'Program Thumbnails cleaned.')
time.sleep(1.0)	