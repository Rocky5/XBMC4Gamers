########################################################################################################################################
'''
	Script by Rocky5 (original idea DivideByZer0)
	Used to select a random directory from a folder of directories, to use as the screenshot screensaver.
'''
########################################################################################################################################


import os
import xbmc
import fileinput
import random
import time


Music_Path = "G:/Music/My Music/" 
Pictures_Path = "C:/Images/Backgrounds/"


########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\Random Screensaver Images.py loaded."
print "| ------------------------------------------------------------------------------"


#########################################################################################################
# Play random file (disabled)
#########################################################################################################
#list = os.listdir( Music_Path )
#xbmc.executebuiltin( 'PlayMedia(' + Music_Path + random.choice(list) + ')' )


#########################################################################################################
# Get a random subdirectory of Pictures_Path.
#########################################################################################################
List_Root_Directory = os.listdir(Pictures_Path)
Directory_Name = random.choice(List_Root_Directory)
New_Path = '<slideshowpath pathversion="1">' + Pictures_Path + Directory_Name + '/</slideshowpath>\n'
GUISettings_Path = fileinput.input( xbmc.translatePath( 'special://profile/guisettings.xml' ), inplace=1)
for line in GUISettings_Path:
	if "slideshowpath" in line:
		line = New_Path
	sys.stdout.write(line)
print ("| New Path = " + Pictures_Path + Directory_Name + "/")
print "================================================================================"