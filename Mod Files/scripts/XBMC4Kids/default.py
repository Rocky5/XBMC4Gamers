########################################################################################################################################
'''
	Script by Rocky5
	Used to switch between save directories.

	Updated: 12 July 2016
	-- Now incorporated the CheckEditMode.py, since this script is loaded on skin load every time.
	   Also cleaned the script up somewhat.
	   
	Updated: 29 June 2016
	-- Now change to a custom window after the script is finished doing its work, this way the home screen doesn't load if your running
	   the script for the first time.


	Updated: 23 June 2016
	-- Updated the script to look for the "Disable Profile.py Script" toggle & proceed in the appropriate way.


	Updated: 04 June 2016
	-- Due to changes in the way I add profiles, I updated the script to just bypass the "Manage Profiles" and "DVD2Xbox" profile.


	Updated: 09 February 2016
	-- Added copying of the sources.xml this way it doesn't matter if you select use new sources when making a new profile.

	Updated: 21 December 2014

	Now copied softmod saves if they exist to new created profiles.
	Now automatically sets the skin for the new profiles.
	Now has a nice progress bar.
	Refined the script
'''
########################################################################################################################################


import os
import xbmcgui
import xbmc
import shutil
import glob
import fileinput
import time


########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\default.py loaded."
print "| ------------------------------------------------------------------------------"
	

########################################################################################################################################
# Sets paths, for profiles names & locations.
########################################################################################################################################
Working_Directory = os.getcwd() + "\\"
Dashboard_Path = xbmc.translatePath( 'special://xbmc/' )
EditMode_Enabler = xbmc.translatePath( "special://xbmc/system/keymaps/Enabled" )
##
Username = xbmc.getInfoLabel('system.profilename')
##
Current_Profile_Name = (Username  +  '.profile')
Current_Profile_Save_Profile = ('E:/UDATA/'  +  Current_Profile_Name)
Current_Profile_Save_Directory = ('E:/UDATA '  +  Username)
Current_Profile_Save_Profile_Alt = ('E:/UDATA '  +  Username  +  '/'  +  Current_Profile_Name)
##
Current_Profile_Directory = xbmc.translatePath( 'special://profile/' )
Current_Profile_GUISettings = xbmc.translatePath( 'special://profile/guisettings.xml' )
##
Master_Profile = xbmc.translatePath( 'special://UserData/' )
Master_Profile_AdvancedSettings = xbmc.translatePath( 'special://UserData/advancedsettings.xml' )
Master_Profile_GUISettings = xbmc.translatePath( 'special://UserData/guisettings.xml' )
Master_Profile_Sources = xbmc.translatePath( 'special://UserData/sources.xml' )
##
LaunchMenuLoader = "ActivateWindow(1114)"
##


########################################################################################################################################
# Check if editmode is enabled
########################################################################################################################################
if os.path.isfile(EditMode_Enabler) == True: xbmc.executebuiltin('Skin.SetBool(editmode)')
if os.path.isfile(EditMode_Enabler) == False: xbmc.executebuiltin('Skin.reset(editmode)')


########################################################################################################################################
# Check to see if the current profile loaded is the Manage Profiles or DVD2Xbox profile & do nothing.
########################################################################################################################################
SkipScript = "false"
if Username == "Manage Profiles":
	SkipScript = "true"

if Username == "DVD2Xbox":
	SkipScript = "true"
	

########################################################################################################################################
# Check to see if script is enabled or disabled.
########################################################################################################################################
if SkipScript == "false":
	if 'Manage Profiles Skin.useprofiles">true<' in open(Master_Profile_GUISettings).read():


			
########################################################################################################################################
# Check if UDATA exist if not make one.
########################################################################################################################################
		if not os.path.exists("E:/UDATA"):
			os.mkdir("E:/UDATA")
			print "| UDATA created"
		else:
			print "| UDATA folder present"


########################################################################################################################################
# Removes XBMC save folder, so I can rename UDATA.
########################################################################################################################################
		if os.path.isdir('E:/UDATA/0face008/'):
			shutil.rmtree('E:/UDATA/0face008/')
			print "| Removed XBMC save directory"
		else:
			print "| Already removed XBMC save directory"

			
########################################################################################################################################
# Check if Backup.profile exist if not make one.
########################################################################################################################################
		if not os.path.exists("E:/UDATA Backup"):
			profile = open("E:\UDATA\Backup.profile","w")
			profile.write(" ")
			profile.close()	
			print "| UDATA backup created"
		else:
			print "| UDATA backup present"
			

########################################################################################################################################
# Get current profile from UDATA folder.
########################################################################################################################################
		for TMPProfile in glob.glob(r'E:\UDATA\*.profile'):
			dirname, TMPProfile = os.path.split(TMPProfile)
			Previous_Profile_Save_Name, fileExtension = os.path.splitext(TMPProfile)
			Previous_Profile_Save_Directory = ('E:/UDATA '  +  Previous_Profile_Save_Name)
			Previous_Profile_Save_Profile = ('E:/UDATA/'  +  Previous_Profile_Save_Name  +  '.profile')


########################################################################################################################################
# Check to see if the current user is the current save folder.
########################################################################################################################################
		if os.path.isfile(Previous_Profile_Save_Profile) and os.path.isfile(Current_Profile_Save_Profile):
			xbmc.executebuiltin(LaunchMenuLoader)
			print "| " + Username + "'s save directory already loaded"
			print "================================================================================"
			

########################################################################################################################################
# If user created folder rename to UDATA, if not then create folder.
########################################################################################################################################
		elif os.path.isfile(Current_Profile_Save_Profile_Alt) and os.path.isfile(Previous_Profile_Save_Profile):
			os.rename('E:/UDATA' , Previous_Profile_Save_Directory)
			os.rename(Current_Profile_Save_Directory , 'E:/UDATA')
			xbmc.executebuiltin(LaunchMenuLoader)
			print "| Loaded " + Username + "'s save directory"
			print "================================================================================"


########################################################################################################################################
# Checks for the presence of the user UDATA folder & if not present creates it.
########################################################################################################################################
		elif not os.path.isfile(Current_Profile_Save_Profile_Alt):
			pDialog = xbmcgui.DialogProgress()
			pDialog.create('Preping save directory for ' + Username)
			pDialog.update(0, 'Please wait')
			time.sleep(1.0)
			os.mkdir("E:/UDATA "  +  Username)
			print "| " + Username + "'s"" UDATA created"
			profile = open(Current_Profile_Save_Profile_Alt,"w")
			profile.write(" ")
			profile.close()
			os.rename('E:/UDATA' , Previous_Profile_Save_Directory)
			os.rename(Current_Profile_Save_Directory , 'E:/UDATA')
			

########################################################################################################################################
# Prepare the new users save directory & copy a few saves/tools if they exist.
########################################################################################################################################
			if os.path.exists("E:/UDATA Backup/4541000d"):
				pDialog.update(5, 'Copying 007 Save')
				shutil.copytree("E:/UDATA Backup/4541000d", "E:/UDATA/4541000d")
				print "| Copied 007 save folder"
				time.sleep(0.1)
			else:
				print "| No 007 save folder found"
				
			if os.path.exists("E:/UDATA Backup/4d530017"):
				pDialog.update(15, 'Copying Mechassault Save.')
				shutil.copytree("E:/UDATA Backup/4d530017", "E:/UDATA/4d530017")
				print "| Copied Mechassault save folder"
				time.sleep(0.1)
			else:
				print "| No Mechassault save folder found"
				
			if os.path.exists("E:/UDATA Backup/5553000c"):
				pDialog.update(30, 'Copying Splinter cell Save')
				shutil.copytree("E:/UDATA Backup/5553000c", "E:/UDATA/5553000c")
				print "| Copied Splinter cell save folder"
				time.sleep(0.1)
			else:
				print "| No Splinter cell save folder found"
				
			if os.path.exists("E:/UDATA Backup/21585554"):
				pDialog.update(45, 'Copying Softmod files Save')
				shutil.copytree("E:/UDATA Backup/21585554", "E:/UDATA/21585554")
				print "| Copied Softmod save folder"
				time.sleep(0.1)
			else:
				print "| No Softmod save folder found"
				
			if os.path.exists("E:/UDATA Backup/rescuedash"):
				pDialog.update(75, 'Copying Rescue Dashboard folder')
				shutil.copytree("E:/UDATA Backup/rescuedash", "E:/UDATA/rescuedash")
				print "| Copied Rescue Dashboard folder"
				time.sleep(0.1)
			else:
				print "| No Rescue Dashboard folder found"
				
			if os.path.exists(Master_Profile):
				pDialog.update(95, 'Copying Sources.xml')
				shutil.copy(Master_Profile_Sources, Current_Profile_Directory)
				print "| Copied Sources.xml"
				time.sleep(0.1)
				pDialog.update(97, 'Copying Guisettings.xml')
				shutil.copy(Master_Profile_GUISettings, Current_Profile_Directory)
				print "| Copied Guisettings.xml"
				time.sleep(0.1)
				#pDialog.update(99, 'Copying AdvancedSettings.xml')
				#shutil.copy(Master_Profile_AdvancedSettings, Current_Profile_Directory)
				#print "| Copied AdvancedSettings.xml"	
				#time.sleep(0.1)
			
			else:
				print "| No Sources.xml file found"
				print "| No Guisettings.xml file found"


########################################################################################################################################
# Change user skin & skin settings names.
########################################################################################################################################
			time.sleep(0.5)
			for line in fileinput.input(Current_Profile_GUISettings, inplace=True):
				print(line.replace('Manage Profiles Skin', 'Profile skin'))
				
			print "================================================================================"

			pDialog.update(100, 'Compleate' )
			pDialog.update(100, 'Done')
			time.sleep(1.0)
			pDialog.close()
			dialog = xbmcgui.Dialog()
			dialog.ok("That's everything setup","","I need to restart XBMC","so that the changes take affect.")
			xbmc.executebuiltin("System.LogOff()")
			xbmc.executebuiltin("RestartApp")


########################################################################################################################################
# If the script is disabled in the Manage Profiles profile settings, edit current skin & log out.
########################################################################################################################################
	else:
		if "Manage Profiles Skin" in open(Current_Profile_GUISettings).read():
			shutil.copy(Master_Profile_Sources, Current_Profile_Directory)
			print "| Copied Sources.xml"
			shutil.copy(Master_Profile_GUISettings, Current_Profile_Directory)
			print "| Copied Guisettings.xml"
			#shutil.copy(Master_Profile_AdvancedSettings, Current_Profile_Directory)
			#print "| Copied AdvancedSettings.xml"
			time.sleep(0.5)
			for line in fileinput.input(Current_Profile_GUISettings, inplace=True):
				print(line.replace('Manage Profiles Skin', 'Profile skin'))
				
			print "================================================================================"

			dialog = xbmcgui.Dialog()
			dialog.ok("That's everything setup","","I need to restart XBMC","so that the changes take affect.")
			xbmc.executebuiltin("System.LogOff()")
			xbmc.executebuiltin("RestartApp")
			
		
		else:
			xbmc.executebuiltin(LaunchMenuLoader)
			print "| Nothing to do."
			print "================================================================================"

else:
	xbmc.executebuiltin(LaunchMenuLoader)
	print "================================================================================"
	print "| Nothing to do."
	print "================================================================================"