'''
	Script by Rocky5
	Used to switch between save directories.
'''
import fileinput, glob, os, shutil, time, xbmcgui, xbmc
###  Start markings for the log file.
print "| Scripts\XBMC4Gamers\default.py loaded."
###  Sets paths, for profiles names & locations.
Show_Log = 0
# if 'True' in xbmc.executehttpapi('SetGUISetting(1;debug.showloginfo)'): Show_Log = 1
Working_Directory = os.getcwd()+"\\"
Dashboard_Path = xbmc.translatePath('special://xbmc/')
EditMode_Enabler = xbmc.translatePath("special://xbmc/system/keymaps/Enabled")
Username = xbmc.getInfoLabel('system.profilename')
Current_Profile_Name = (Username+'.profile')
Current_Profile_Save_Profile = ('E:/UDATA/'+Current_Profile_Name)
Current_Profile_Save_Directory = ('E:/UDATA '+Username)
Current_Profile_Save_Profile_Alt = ('E:/UDATA '+Username+'/'+Current_Profile_Name)
Current_Profile_Directory = xbmc.translatePath('special://profile/')
Current_Profile_GUISettings = xbmc.translatePath('special://profile/guisettings.xml')
Master_Profile = xbmc.translatePath('special://UserData/')
Master_Profile_AdvancedSettings = xbmc.translatePath('special://UserData/advancedsettings.xml')
Master_Profile_GUISettings = xbmc.translatePath('special://UserData/guisettings.xml')
Master_Profile_Sources = xbmc.translatePath('special://UserData/sources.xml')
LaunchMenuLoader = "ActivateWindow(1114)"
Use_Individual_Profile_Saves = 0
if 'Manage Profiles Skin.useprofiles">true<' in open(Master_Profile_GUISettings).read(): Use_Individual_Profile_Saves = 1
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
###  Check if editmode is enabled
if os.path.isfile(EditMode_Enabler) == True: xbmc.executebuiltin('Skin.SetBool(editmode)')
if os.path.isfile(EditMode_Enabler) == False: xbmc.executebuiltin('Skin.reset(editmode)')
###  Check to see if the current profile loaded is the Manage Profiles & do nothing.
if Username == "Manage Profiles":
	xbmc.executebuiltin(LaunchMenuLoader)
else:
###  If the script is disabled in the Manage Profiles profile settings, edit current skin & log out.
	if Use_Individual_Profile_Saves == 0:
###  Removes XBMC save folder, so I can rename UDATA.
		try:
			if os.path.isdir('E:/UDATA/09999990/'):
				loop = 0
				while True:
					shutil.rmtree('E:/UDATA/09999990/')
					time.sleep(1)
					loop = loop+1
					if loop == 5 or not os.path.isdir('E:/UDATA/09999990'): break
				if Show_Log == 1: print "| Removed XBMC save directory"
			else:
				if Show_Log == 1: print "| Already removed XBMC save directory"
		except:
			if Show_Log == 1: print "| Cant remove Save folder"
###  Get current profile from UDATA folder and store its name.
		for TMPProfile in glob.glob(r'E:\UDATA\*.profile'):
			dirname, TMPProfile = os.path.split(TMPProfile)
			Previous_Profile_Save_Name, fileExtension = os.path.splitext(TMPProfile)
			Previous_Profile_Save_Directory = ('E:/UDATA '+Previous_Profile_Save_Name)
			Previous_Profile_Save_Profile = ('E:/UDATA/'+Previous_Profile_Save_Name+'.profile')
###  If user created folder rename to UDATA user and rename UDATA Backup to UDATA.
			if os.path.isfile(Previous_Profile_Save_Profile) and os.path.isdir('E:/UDATA Backup'):
				loop = 0
				while True:
					os.rename('E:/UDATA' , Previous_Profile_Save_Directory)
					if os.path.isdir('E:/UDATA Backup'): os.rename('E:/UDATA Backup' , 'E:/UDATA')
					time.sleep(1)
					loop = loop+1
					if loop == 5 or os.path.isdir(Previous_Profile_Save_Directory): break
		if "Manage Profiles Skin" in open(Current_Profile_GUISettings).read():
			time.sleep(2.0)
			dialog.ok("Notice","I need you to calibrate the screen to the size of your TV.","Move the top left and bottom right images to the corners","of your TV.")
			xbmc.executebuiltin("ReplaceWindow(11)")
			while True:
				time.sleep(1)
				if not xbmcgui.getCurrentWindowId() == 10011: break
			shutil.copy(Master_Profile_AdvancedSettings, Current_Profile_Directory)
			if Show_Log == 1: print "| Copied AdvancedSettings.xml"
			for line in fileinput.input(Current_Profile_GUISettings, inplace=1):
				line = line.replace('Manage Profiles Skin','Profile skin')
				print line,
			if not os.path.isdir('E:\\CACHE'): os.makedirs('E:\\CACHE')
			with open('E:\\CACHE\\tmp.bin','w') as tmp: tmp.write(' ')
			with open('Special://scripts/autoexec.py','w') as tmp: tmp.write("import os,xbmc\nif os.path.isfile('E:/CACHE/tmp.bin'):\n	xbmc.executebuiltin('LoadProfile("+Username+")')\n	os.remove('E:/CACHE/tmp.bin')")
			dialog.ok("That's everything setup","I need to restart XBMC","so that the changes take affect.")
			xbmc.executebuiltin("System.LogOff()")
			xbmc.executebuiltin("RestartApp")
		else:
			xbmc.executebuiltin(LaunchMenuLoader)
	if Use_Individual_Profile_Saves == 1:
###  Check if UDATA exist if not make one.
		if not os.path.exists("E:/UDATA"):
			os.mkdir("E:/UDATA")
			if Show_Log == 1: print "| UDATA created"
		else:
			if Show_Log == 1: print "| UDATA folder present"
###  Removes XBMC save folder, so I can rename UDATA.
		try:
			if os.path.isdir('E:/UDATA/09999990/'):
				loop = 0
				while True:
					shutil.rmtree('E:/UDATA/09999990/')
					time.sleep(1)
					loop = loop+1
					if loop == 5 or not os.path.isdir('E:/UDATA/09999990'): break
				if Show_Log == 1: print "| Removed XBMC save directory"
			else:
				if Show_Log == 1: print "| Already removed XBMC save directory"
		except:
			if Show_Log == 1: print "| Cant remove Save folder"
###  Check if Backup.profile exist if not make one.
		if not os.path.exists("E:/UDATA Backup"):
			with open("E:\UDATA\Backup.profile","w") as profile: profile.write(" ")
			if Show_Log == 1: print "| UDATA backup created"
		else:
			if Show_Log == 1: print "| UDATA backup present"
###  Get current profile from UDATA folder and store its name.
		for TMPProfile in glob.glob(r'E:\UDATA\*.profile'):
			dirname, TMPProfile = os.path.split(TMPProfile)
			Previous_Profile_Save_Name, fileExtension = os.path.splitext(TMPProfile)
			Previous_Profile_Save_Directory = ('E:/UDATA '+Previous_Profile_Save_Name)
			Previous_Profile_Save_Profile = ('E:/UDATA/'+Previous_Profile_Save_Name+'.profile')
###  Check to see if the current user is the current save folder.
		if os.path.isfile(Previous_Profile_Save_Profile) and os.path.isfile(Current_Profile_Save_Profile):
			xbmc.executebuiltin(LaunchMenuLoader)
			if Show_Log == 1: print "| "+Username+"'s save directory already loaded"
###  If user created folder rename to UDATA, if not then create folder.
		elif os.path.isfile(Current_Profile_Save_Profile_Alt) and os.path.isfile(Previous_Profile_Save_Profile):
			loop = 0
			while True:
				os.rename('E:/UDATA' , Previous_Profile_Save_Directory)
				os.rename(Current_Profile_Save_Directory , 'E:/UDATA')
				time.sleep(1)
				loop = loop+1
				if loop == 5 or os.path.isdir(Previous_Profile_Save_Directory): break
			xbmc.executebuiltin(LaunchMenuLoader)
			if Show_Log == 1: print "| Loaded "+Username+"'s save directory"
###  Checks for the presence of the user UDATA folder & if not present creates it.
		elif not os.path.isfile(Current_Profile_Save_Profile_Alt):
			pDialog.create('Preping save directory for '+Username)
			pDialog.update(0, '', 'Please wait')
			time.sleep(1.0)
			os.mkdir("E:/UDATA "+Username)
			if Show_Log == 1: print "| "+Username+"'s"" UDATA created"
			with open(Current_Profile_Save_Profile_Alt,"w") as profile: profile.write(" ")
			os.rename('E:/UDATA' , Previous_Profile_Save_Directory)
			os.rename(Current_Profile_Save_Directory , 'E:/UDATA')
###  Prepare the new users save directory & copy a few saves/tools if they exist.
			if os.path.exists("E:/UDATA Backup/4541000d"):
				pDialog.update(5, '', 'Copying 007 Save')
				shutil.copytree("E:/UDATA Backup/4541000d", "E:/UDATA/4541000d")
				if Show_Log == 1: print "| Copied 007 save folder"
				time.sleep(2)
			else:
				if Show_Log == 1: print "| No 007 save folder found"
			if os.path.exists("E:/UDATA Backup/4d530017"):
				pDialog.update(15, '', 'Copying Mechassault Save.')
				shutil.copytree("E:/UDATA Backup/4d530017", "E:/UDATA/4d530017")
				if Show_Log == 1: print "| Copied Mechassault save folder"
				time.sleep(2)
			else:
				if Show_Log == 1: print "| No Mechassault save folder found"
			if os.path.exists("E:/UDATA Backup/5553000c"):
				pDialog.update(30, '', 'Copying Splinter cell Save')
				shutil.copytree("E:/UDATA Backup/5553000c", "E:/UDATA/5553000c")
				if Show_Log == 1: print "| Copied Splinter cell save folder"
				time.sleep(2)
			else:
				if Show_Log == 1: print "| No Splinter cell save folder found"
			if os.path.exists("E:/UDATA Backup/41560017"):
				pDialog.update(45, '', 'Copying Splinter cell Save')
				shutil.copytree("E:/UDATA Backup/41560017", "E:/UDATA/41560017")
				if Show_Log == 1: print "| Copied Tony Hawks 4 save folder"
				time.sleep(2)
			else:
				if Show_Log == 1: print "| No Tony Hawks 4 save folder found"
			if os.path.exists("E:/UDATA Backup/21585554"):
				pDialog.update(60, '', 'Copying Softmod files Save')
				shutil.copytree("E:/UDATA Backup/21585554", "E:/UDATA/21585554")
				if Show_Log == 1: print "| Copied Softmod save folder"
				time.sleep(2)
			else:
				if Show_Log == 1: print "| No Softmod save folder found"
			if os.path.exists("E:/UDATA Backup/rescuedash"):
				pDialog.update(80, '', 'Copying Rescue Dashboard folder')
				shutil.copytree("E:/UDATA Backup/rescuedash", "E:/UDATA/rescuedash")
				if Show_Log == 1: print "| Copied Rescue Dashboard folder"
				time.sleep(2)
			else:
				if Show_Log == 1: print "| No Rescue Dashboard folder found"
				pDialog.update(99, 'Copying AdvancedSettings.xml')
				shutil.copy(Master_Profile_AdvancedSettings, Current_Profile_Directory)
				if Show_Log == 1: print "| Copied AdvancedSettings.xml"
				time.sleep(2)
			pDialog.update(100, '', 'Complete')
			pDialog.update(100, '', 'Done')
			time.sleep(1.0)
			pDialog.close()
###  Change user skin & skin settings names.
			dialog.ok("Notice","I need you to calibrate the screen to the size of your TV.","Move the top left and bottom right images to the corners","of your TV.")
			xbmc.executebuiltin("ReplaceWindow(11)")
			while True:
				time.sleep(1)
				if not xbmcgui.getCurrentWindowId() == 10011: break
			for line in fileinput.input(Current_Profile_GUISettings, inplace=1):
				line = line.replace('Manage Profiles Skin','Profile skin')
				print line,
			dialog.ok("That's everything setup","I need to restart XBMC","so that the changes take affect.")
			if not os.path.isdir('E:\\CACHE'): os.makedirs('E:\\CACHE')
			with open('E:\\CACHE\\tmp.bin','w') as tmp: tmp.write(' ')
			with open('Special://scripts/autoexec.py','w') as tmp: tmp.write("import os,xbmc\nif os.path.isfile('E:/CACHE/tmp.bin'):\n	xbmc.executebuiltin('LoadProfile("+Username+")')\n	os.remove('E:/CACHE/tmp.bin')")
			xbmc.executebuiltin("System.LogOff()")
			xbmc.executebuiltin("RestartApp")