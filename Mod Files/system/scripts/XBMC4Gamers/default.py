'''
	Script by Rocky5
	Used to switch between save directories.
'''
import glob, os, shutil, time, xbmcgui, xbmc
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()

#  Start markings for the log file.
print "| Scripts\XBMC4Gamers\default.py loaded."

#  Sets paths, for profiles names & locations.
EditMode_Enabler = xbmc.translatePath("special://xbmc/system/keymaps/Enabled")
Username = xbmc.getInfoLabel('system.profilename')
Current_Profile_Name = (Username+'.profile')
Current_Profile_Save_Profile = ('E:/UDATA/'+Current_Profile_Name)
Current_Profile_Save_Directory = ('E:/UDATA '+Username)
Current_Profile_Save_Profile_Alt = ('E:/UDATA '+Username+'/'+Current_Profile_Name)
Current_Profile_Setup = xbmc.translatePath('special://profile/setup.bin')
LaunchMenuLoader = "ActivateWindow(1114)"
Use_Individual_Profile_Saves = 0
if 'Manage Profiles Skin.useprofiles">true<' in open(xbmc.translatePath('special://UserData/guisettings.xml')).read(): Use_Individual_Profile_Saves = 1
	
#  Check if editmode is enabled
if os.path.isfile(EditMode_Enabler):
	xbmc.executebuiltin('Skin.SetBool(editmode)')
else:
	xbmc.executebuiltin('Skin.reset(editmode)')

#  Check to see if the current profile loaded is the Manage Profiles & do nothing.
if Username == "Manage Profiles":
	if os.path.isfile(Current_Profile_Setup):
		os.remove(Current_Profile_Setup)
		dialog.ok("Welcome to XBMC4Gamers","I need you to calibrate the screen to the size of your TV.","Move the top left and bottom right images to the corners","of your TV & make the disc circular.")
		xbmc.executebuiltin("ReplaceWindow(11)")
		time.sleep(1)
		while True:
			time.sleep(1)
			if not xbmcgui.getCurrentWindowId() == 10011: break
	xbmc.executebuiltin(LaunchMenuLoader)
else:

	#  Check if for Cache folder
	if not os.path.isdir("E:\\CACHE"): os.mkdir("E:\\CACHE")											 

	#  If the script is disabled in the Manage Profiles profile settings, edit current skin & log out.
	if Use_Individual_Profile_Saves == 0:

		#  Removes XBMC save folder, so I can rename UDATA.
		try:
			if os.path.isdir('E:/UDATA/09999990/'):
				loop = 0
				while True:
					shutil.rmtree('E:/UDATA/09999990/')
					time.sleep(1)
					loop = loop+1
					if loop == 5 or not os.path.isdir('E:/UDATA/09999990'): break
		except: pass

		#  Get current profile from UDATA folder and store its name.
		for TMPProfile in glob.glob(r'E:\UDATA\*.profile'):
			dirname, TMPProfile = os.path.split(TMPProfile)
			Previous_Profile_Save_Name, fileExtension = os.path.splitext(TMPProfile)
			Previous_Profile_Save_Directory = ('E:/UDATA '+Previous_Profile_Save_Name)
			Previous_Profile_Save_Profile = ('E:/UDATA/'+Previous_Profile_Save_Name+'.profile')

			#  If user created folder rename to UDATA user and rename UDATA Backup to UDATA.
			if os.path.isfile(Previous_Profile_Save_Profile) and os.path.isdir('E:/UDATA Backup'):
				loop = 0
				while True:
					os.rename('E:/UDATA' , Previous_Profile_Save_Directory)
					if os.path.isdir('E:/UDATA Backup'): os.rename('E:/UDATA Backup' , 'E:/UDATA')
					time.sleep(1)
					loop = loop+1
					if loop == 5 or os.path.isdir(Previous_Profile_Save_Directory): break
		xbmc.executebuiltin(LaunchMenuLoader)
	
	if Use_Individual_Profile_Saves == 1:

		#  Check if UDATA exist if not make one.
		if not os.path.exists("E:/UDATA"): os.mkdir("E:/UDATA")

		#  Removes XBMC save folder, so I can rename UDATA.
		try:
			if os.path.isdir('E:/UDATA/09999990/'):
				loop = 0
				while True:
					shutil.rmtree('E:/UDATA/09999990/')
					time.sleep(1)
					loop = loop+1
					if loop == 5 or not os.path.isdir('E:/UDATA/09999990'): break
		except: pass

		#  Check if Backup.profile exist if not make one.
		if not os.path.exists("E:/UDATA Backup"):
			with open("E:\UDATA\Backup.profile","w") as profile: profile.write(" ")

		#  Get current profile from UDATA folder and store its name.
		for TMPProfile in glob.glob(r'E:\UDATA\*.profile'):
			dirname, TMPProfile = os.path.split(TMPProfile)
			Previous_Profile_Save_Name, fileExtension = os.path.splitext(TMPProfile)
			Previous_Profile_Save_Directory = ('E:/UDATA '+Previous_Profile_Save_Name)
			Previous_Profile_Save_Profile = ('E:/UDATA/'+Previous_Profile_Save_Name+'.profile')

		#  Check to see if the current user is the current save folder.
		if os.path.isfile(Previous_Profile_Save_Profile) and os.path.isfile(Current_Profile_Save_Profile):
			xbmc.executebuiltin(LaunchMenuLoader)

		#  If user created folder rename to UDATA, if not then create folder.
		elif os.path.isfile(Current_Profile_Save_Profile_Alt) and os.path.isfile(Previous_Profile_Save_Profile):
			loop = 0
			while True:
				os.rename('E:/UDATA' , Previous_Profile_Save_Directory)
				os.rename(Current_Profile_Save_Directory , 'E:/UDATA')
				time.sleep(1)
				loop = loop+1
				if loop == 5 or os.path.isdir(Previous_Profile_Save_Directory): break
			xbmc.executebuiltin(LaunchMenuLoader)

		#  Checks for the presence of the user UDATA folder & if not present creates it.
		elif not os.path.isfile(Current_Profile_Save_Profile_Alt):
			pDialog.create('Preping save directory for '+Username)
			pDialog.update(0, '', 'Please wait')
			time.sleep(1.0)
			os.mkdir("E:/UDATA "+Username)
			with open(Current_Profile_Save_Profile_Alt,"w") as profile: profile.write(" ")
			os.rename('E:/UDATA' , Previous_Profile_Save_Directory)
			os.rename(Current_Profile_Save_Directory , 'E:/UDATA')

			#  Prepare the new users save directory & copy a few saves/tools if they exist.
			if os.path.exists("E:/UDATA Backup/4541000d"):
				pDialog.update(5, '', 'Copying 007 Save')
				shutil.copytree("E:/UDATA Backup/4541000d", "E:/UDATA/4541000d")
			if os.path.exists("E:/UDATA Backup/4d530017"):
				pDialog.update(15, '', 'Copying Mechassault Save.')
				shutil.copytree("E:/UDATA Backup/4d530017", "E:/UDATA/4d530017")
			if os.path.exists("E:/UDATA Backup/5553000c"):
				pDialog.update(30, '', 'Copying Splinter cell Save')
				shutil.copytree("E:/UDATA Backup/5553000c", "E:/UDATA/5553000c")
			if os.path.exists("E:/UDATA Backup/41560017"):
				pDialog.update(45, '', 'Copying Splinter cell Save')
				shutil.copytree("E:/UDATA Backup/41560017", "E:/UDATA/41560017")
			if os.path.exists("E:/UDATA Backup/21585554"):
				pDialog.update(60, '', 'Copying Softmod files Save')
				shutil.copytree("E:/UDATA Backup/21585554", "E:/UDATA/21585554")
			if os.path.exists("E:/UDATA Backup/rescuedash"):
				pDialog.update(80, '', 'Copying Rescue Dashboard folder')
				shutil.copytree("E:/UDATA Backup/rescuedash", "E:/UDATA/rescuedash")
			
			pDialog.update(100, '', 'Complete')
			pDialog.update(0, '', 'Done')
			time.sleep(1)
			pDialog.close()

			xbmc.executebuiltin(LaunchMenuLoader)