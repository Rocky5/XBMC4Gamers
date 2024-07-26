import glob
import os
import shutil
import time
import xbmcgui
import xbmc

def check_kioskmode():
	kioskmode_enabler = xbmc.translatePath("special://xbmc/system/keymaps/Enabled")
	if os.path.isfile(kioskmode_enabler):
		xbmc.executebuiltin('Skin.SetBool(kioskmode)')
		xbmc.executebuiltin('Skin.reset(AdultProfile)')
	else:
		xbmc.executebuiltin('Skin.reset(kioskmode)')

def manage_profiles_setup():
	current_profile_setup = xbmc.translatePath('special://profile/setup.bin')
	if os.path.isfile(current_profile_setup):
		os.remove(current_profile_setup)
		dialog.ok(	"Welcome to XBMC4Gamers",
'''I need you to calibrate the screen to the size of your TV.

Move the top left and bottom right images to the corners of your TV
(no red visible) & make the disc as circular as you can.'''	)
		xbmc.executebuiltin("ReplaceWindow(11)")
		time.sleep(1)
		while xbmcgui.getCurrentWindowId() == 10011:
			time.sleep(1)

def check_skin(username):
	if xbmc.getSkinDir() == "Manage Profiles":
		dialog.ok(	"ERROR", 
'''Something has gone wrong, your GUISettings have been reset.

This could be due to corruption by the system powering off during
a write.'''	)
		xbmc.setSkin("Profile")
		xbmc.executebuiltin("LoadProfile({})".format(username))

def check_custom_views():
	try:
		path = xbmc.translatePath('Special://skin/xml/custom views/')
		for ID in range(80, 90):
			xbmc.executebuiltin('Skin.Reset(CustomViewtype_id_{})'.format(ID))
			xml_file = os.path.join(path, "CustomViewtype_id_{}.xml".format(ID))
			jpg_file = os.path.join(path, "CustomViewtype_id_{}.jpg".format(ID))
			if os.path.isfile(xml_file) and os.path.isfile(jpg_file):
				xbmc.executebuiltin('Skin.SetBool(CustomViewtype_id_{})'.format(ID))
				print "Added custom view ID: {}".format(ID)
	except Exception as error:
		print 'Error in "Check for custom views": {}'.format(error)

def restore_udata_backup():
	try:
		for tmp_profile in glob.glob(r'E:\UDATA\*.profile'):
			profile_name = os.path.splitext(os.path.basename(tmp_profile))[0]
			profile_directory = 'E:/UDATA {}'.format(profile_name)
			profile_profile = 'E:/UDATA/{}.profile'.format(profile_name)
			save_directory = 'E:/UDATA/09999990'
			udata_directory = 'E:/UDATA'
			if os.path.isdir(save_directory):
				for _ in range(5):
					shutil.rmtree(save_directory)
					time.sleep(1)
					if not os.path.isdir(save_directory):
						break
			if os.path.isfile(profile_profile) and os.path.isdir('E:/UDATA Backup'):
				for _ in range(5):
					os.rename(udata_directory, profile_directory)
					if os.path.isdir('E:/UDATA Backup'):
						os.rename('E:/UDATA Backup', udata_directory)
					time.sleep(1)
					if os.path.isdir(profile_directory) and os.path.isdir(udata_directory):
						break
	except Exception as error:
		print 'Error in "Get current profile from UDATA and restore UDATA backup": {}'.format(error)

def main():
	time.sleep(1.01) # this is so the fade animation plays out.
	check_kioskmode()
	username = xbmc.getInfoLabel('system.profilename')
	if username == "Manage Profiles":
		manage_profiles_setup()
	else:
		check_skin(username)
		check_custom_views()
		restore_udata_backup()

	xbmc.executebuiltin("ActivateWindow(1114)")

if __name__ == "__main__":
	dialog = xbmcgui.Dialog()
	print "Loaded XBMC4Gamers\default.py"
	start_time = time.time()
	main()
	print "Unloaded XBMC4Gamers\default.py - took {} seconds to complete".format(int(round((time.time() - start_time))))

