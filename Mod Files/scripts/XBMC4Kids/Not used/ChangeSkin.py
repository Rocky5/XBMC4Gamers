################################################################################
# Script by Rocky5
# Used to switch to the Profile Skin if not using the Profiles.py.
################################################################################

import os
import xbmcgui
import xbmc
import shutil
import glob
import fileinput
import time

# Start markings for the log file.
print "============================================================"
print "============================================================"
	
	
# Sets paths, for profiles names & locations.
Username = xbmc.getInfoLabel('system.profilename')
MasProfileGuiSettings = xbmc.translatePath( 'special://UserData/guisettings.xml' )
CurProfileGuiSettings = xbmc.translatePath( 'special://profile/guisettings.xml' )
MasProfileSources = xbmc.translatePath( 'special://UserData/sources.xml' )
CurProfileSources = xbmc.translatePath( 'special://profile/sources.xml' )


if Username == "Manage Profiles":
	MPLoaded = "1234" # done this so if either profile is loaded it will always be false.
else:
	MPLoaded = "false"
	
if Username == "DVD2Xbox":
	D2XLoaded = "5678" # done this so if either profile is loaded it will always be false.
else:
	D2XLoaded = "false"

if MPLoaded == D2XLoaded:

	if "<skin>Manage Profiles Skin</skin>" in open(CurProfileGuiSettings).read():
		# Edit current skin & log out.
		dialog = xbmcgui.Dialog()
		dialog.ok("That's everything setup","I will need to log you out "+Username+".","So I can complete the process.","Hope you understand.")
		shutil.copyfile(MasProfileSources, CurProfileSources)
		print "Copied Sources.xml"
		shutil.copyfile(MasProfileGuiSettings, CurProfileGuiSettings)
		print "Copied Guisettings.xml"		
		for line in fileinput.input(CurProfileGuiSettings, inplace=True):
			print(line.replace("<skin>Manage Profiles Skin</skin>", "<skin>Profile skin</skin>"))
			xbmc.executebuiltin("System.LogOff()")
	else:
		print "Profile Skin already set"
		
	# End markings for the log file.
	print "============================================================"
	print "============================================================"
else:
	print "============================================================"
	print "ChangeSkin.py - Nothing to do."
	print "============================================================"