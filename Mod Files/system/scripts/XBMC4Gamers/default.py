### Script by Rocky
import glob, os, re, shutil, time, xbmcgui, xbmc
dialog = xbmcgui.Dialog()
print "Loaded default.py"
start_time = time.time()
#  Sets paths, for profiles names & locations.
kioskmode_Enabler = xbmc.translatePath("special://xbmc/system/keymaps/Enabled")
Username = xbmc.getInfoLabel('system.profilename')
Current_Profile_Setup = xbmc.translatePath('special://profile/setup.bin')
# This sleep is so the fade animation plays out
time.sleep(1.01)
#  Check if kioskmode is enabled
if os.path.isfile(kioskmode_Enabler):
	xbmc.executebuiltin('Skin.SetBool(kioskmode)')
	xbmc.executebuiltin('Skin.reset(AdultProfile)') # Enabled adult mode when kiosk mode is disabled
else:
	xbmc.executebuiltin('Skin.reset(kioskmode)')
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
else:
	# Check if the skin is set correctly
	if xbmc.getSkinDir() == "Manage Profiles Skin":
		dialog.ok("ERROR","Something has gone wrong, your GUISettings have been","reset. This could be due to corruption by the system","powering off during a write.")
		xbmc.setSkin("Profile Skin")
		xbmc.executebuiltin("LoadProfile("+Username+")")
	else:
		# Check for custom views 
		try:
			Path=xbmc.translatePath('Special://skin/xml/custom views/')
			ID=80
			for _ in range(10):
				xbmc.executebuiltin('Skin.Reset(CustomViewtype_id_'+str(ID)+')')
				if os.path.isfile(os.path.join(Path,"CustomViewtype_id_"+str(ID)+".xml")) and os.path.isfile(os.path.join(Path,"CustomViewtype_id_"+str(ID)+".jpg")):
					xbmc.executebuiltin('Skin.SetBool(CustomViewtype_id_'+str(ID)+')')
					print "Added custom view ID: " + str(ID)
				ID+=1
		except: print 'Error in "Check for custom views"'
		#  Get current profile from UDATA folder and store its name.
		try:
			if os.path.isdir('E:/UDATA/09999990/'):
				loop = 0
				while True:
					shutil.rmtree('E:/UDATA/09999990/')
					time.sleep(1)
					loop = loop+1
					if loop == 5 or not os.path.isdir('E:/UDATA/09999990'): break
			for TMPProfile in glob.glob(r'E:\UDATA\*.profile'):
				dirname, TMPProfile = os.path.split(TMPProfile)
				Profile_Name, fileExtension = os.path.splitext(TMPProfile)
				Profile_Directory = ('E:/UDATA '+Profile_Name)
				Profile_Profile = ('E:/UDATA/'+Profile_Name+'.profile')
				#  If user created folder rename to UDATA user and rename UDATA Backup to UDATA.
				if os.path.isfile(Profile_Profile) and os.path.isdir('E:/UDATA Backup'):
					loop = 0
					while True:
						os.rename('E:/UDATA' , Profile_Directory)
						if os.path.isdir('E:/UDATA Backup'): os.rename('E:/UDATA Backup' , 'E:/UDATA')
						time.sleep(1)
						loop = loop+1
						if loop == 5 or os.path.isdir(Profile_Directory): break
		except: print 'Error in "Get current profile" area'
# Load next window
xbmc.executebuiltin("ActivateWindow(1114)")
print "Unloaded default.py - took %s seconds to complete" % int(round((time.time() - start_time)))