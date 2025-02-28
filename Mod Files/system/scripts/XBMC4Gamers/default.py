# -*- coding: utf-8 -*-
import glob
import os
import shutil
import sys
import time
import xbmcgui
import xbmc

sys.path.append('Q:/system/scripts/XBMC4Gamers/Utilities/libs')
from custom_views import custom_views_update_programs as check_custom_views

MASTER_PROFILE_NAME = "Add User"
MASTER_PROFILE_SKIN = "Add User"

def check_kioskmode():
	kioskmode_enabler = xbmc.translatePath("special://xbmc/system/keymaps/Enabled")
	if os.path.isfile(kioskmode_enabler):
		xbmc.executebuiltin('Skin.SetBool(kioskmode)')
		xbmc.executebuiltin('Skin.Reset(AdultProfile)')
	else:
		xbmc.executebuiltin('Skin.Reset(kioskmode)')

def manage_profiles_setup():
	current_profile_setup = xbmc.translatePath('special://profile/setup.bin')
	if os.path.isfile(current_profile_setup):
		os.remove(current_profile_setup)
		xbmc.executebuiltin("ReplaceWindow(11)")
		xbmcgui.Dialog().ok("Welcome to XBMC4Gamers", "[CR]Please calibrate the screen to fit your TV.[CR]Move the top left and bottom right chevrons to the corners of your TV[CR](no red visible) and adjust the disc to be as circular as possible.")
		wait_for_condition(lambda: xbmcgui.getCurrentWindowId() != 10011, 120)

def check_skin(username):
	if xbmc.getSkinDir() == MASTER_PROFILE_SKIN:
		xbmc.setSkin("Profile")
		# xbmcgui.Dialog().ok("Error", "[CR]Oops! Something went wrong and your settings might have been[CR]corrupted. This could have been due to a power-off during a write[CR]operation.")
		print 'Error with profile {}: Settings might have been corrupted, reset skin and reloaded skin.'.format(username)
		xbmc.executebuiltin("ReloadSkin")
		return False
	else:
		return True

def restore_udata_backup():
	try:
		udata_backup_path = 'E:/UDATA Backup'
		save_directory = 'E:/UDATA/09999990'
		for tmp_profile in glob.glob(r'E:\UDATA\*.profile'):
			profile_name = os.path.splitext(os.path.basename(tmp_profile))[0]
			profile_directory = 'E:/UDATA {}'.format(profile_name)
			profile_profile = 'E:/UDATA/{}.profile'.format(profile_name)
			udata_directory = 'E:/UDATA'
			if os.path.isfile(profile_profile) and os.path.isdir(udata_backup_path):
				if os.path.isdir(save_directory):
					for _ in range(5):
						shutil.rmtree(save_directory)
						wait_for_condition(lambda: not os.path.isdir(save_directory))
						if not os.path.isdir(save_directory):
							break
				for _ in range(5):
					os.rename(udata_directory, profile_directory)
					if os.path.isdir(udata_backup_path):
						os.rename(udata_backup_path, udata_directory)
					wait_for_condition(lambda: os.path.isdir(profile_directory) and os.path.isdir(udata_directory))
					if os.path.isdir(profile_directory) and os.path.isdir(udata_directory):
						break
	except Exception as error:
		print 'Error in "Get current profile from UDATA and restore UDATA backup": {}'.format(error)

def wait_for_condition(condition_func, timeout=5):
	start_time = time.time()
	while not condition_func() and (time.time() - start_time) < timeout:
		time.sleep(0.1)

def main(username):
	if not xbmc.getCondVisibility('Skin.HasSetting(loginfade)'):
		time.sleep(1.5) # This is so the fade animation plays out fully
	check_kioskmode()
	if username == MASTER_PROFILE_NAME:
		manage_profiles_setup()
		xbmc.executebuiltin('Skin.Reset(UpdateDB)')
	else:
		restore_udata_backup()
		reload = check_custom_views(xbmc.getInfoLabel('Skin.CurrentTheme'))
		return reload

if __name__ == "__main__":
	reload = 0
	run_main = True
	username = xbmc.getInfoLabel('system.profilename')
	
	if username != MASTER_PROFILE_NAME:
		run_main = check_skin(username)
	
	# Run main part of the script
	if run_main:
		print "Loaded XBMC4Gamers\\default.py"
		start_time = time.time()
		reload = main(username)		
		print "Unloaded XBMC4Gamers\\default.py - took {} seconds to complete".format(int(round(time.time() - start_time)))
		
		# Run maintenance script or load menu loader window
		if xbmc.getCondVisibility('Skin.HasSetting(UpdateDB)') and not xbmc.getCondVisibility('Skin.HasSetting(AdultProfile)'):
			xbmc.executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Database Maintenance.py)')
		else:
			xbmc.executebuiltin("ActivateWindow(1114)")
			if reload:
				print "Reloaded Skin as it's required to load found custom views"
				xbmc.executebuiltin("ReloadSkin")