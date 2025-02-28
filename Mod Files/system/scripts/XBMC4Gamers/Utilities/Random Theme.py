# -*- coding: utf-8 -*-
import os
import random
import sys
import time
import xbmc
import xbmcgui

sys.path.append(xbmc.translatePath('Special://scripts/XBMC4Gamers/Utilities/libs'))
from theme_version import THEME_VERSION

EXCLUDE_FILES = ['night.xpr', 'Textures.xpr', 'textures.xpr']
THEME_DIR = 'Special://skin/media/'
SPLASH_DIR = 'Special://skin/extras/themes/splashes/'

def get_random_theme(file_list):
	file_list = [file for file in file_list if file not in EXCLUDE_FILES]
	try:
		return random.choice(file_list)
	except IndexError:
		xbmc.log("No valid theme files found.", xbmc.LOGWARNING)
		return None

def wait_for_condition(condition_func, timeout=5):
	start_time = time.time()
	while not condition_func() and (time.time() - start_time) < timeout:
		time.sleep(0.1)

def apply_theme(theme_file):
	try:
		wait_for_condition(lambda: xbmcgui.getCurrentWindowId() != 12007, 10)
		if not xbmc.getCondVisibility('Skin.HasSetting(introenabled)'):
			custom_splash_path = xbmc.translatePath('Special://root/custom_splash.png')
			default_splash_path = xbmc.executebuiltin('Special://root/splash.png')
			splash_path = os.path.join(xbmc.translatePath(SPLASH_DIR), '{}.png'.format(theme_file))
			
			if os.path.isfile(custom_splash_path):
				xbmc.executebuiltin('ShowPicture({})'.format(custom_splash_path))
			elif os.path.isfile(splash_path):
				xbmc.executebuiltin('ShowPicture({})'.format(splash_path))
			else:
				xbmc.executebuiltin('ShowPicture({})'.format(default_splash_path))
			time.sleep(1)

		window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
		window.setProperty("MyScript.ExternalRunning", "True")
		xbmc.executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Apply Theme.py,startup,{})'.format(theme_file))
		wait_for_condition(lambda: window.getProperty("MyScript.ExternalRunning") == "False", 60)

		xbmc.executebuiltin('ReloadSkin')
		xbmc.executebuiltin('ReplaceWindow(2999)')
		return True

	except Exception as e:
		xbmc.log("Failed to apply theme: {}".format(e), xbmc.LOGERROR)
		return False

def main():
	retries = 3
	success = False
	default_theme = 'default'

	try:
		if xbmc.getCondVisibility('Skin.HasSetting(randomthemedl)'):
			file_list = os.listdir(xbmc.translatePath(THEME_DIR))
			random_theme = get_random_theme(file_list)
		else:
			random_theme = random.choice(os.listdir(xbmc.translatePath(THEME_DIR)))

		theme_file = 'default' if random_theme and random_theme.lower() == "textures.xpr" else random_theme[:-4]
		theme_color_file = 'defaults' if theme_file.lower() == 'default' else theme_file

		if xbmc.getCondVisibility('Skin.HasSetting(randomthemewallpaper)'):
			xbmc.executebuiltin('Skin.SetString(Background_Color, {}.jpg)'.format(random.randint(1, 15)))
			xbmc.executebuiltin('Skin.Reset(Background_Image)')
			xbmc.executebuiltin('Skin.Reset(Background_Custom_Color)')

		while retries > 0 and not success:
			theme_color_path = os.path.join(xbmc.translatePath('Special://skin/colors'), theme_color_file + ".xml")
			if os.path.isfile(theme_color_path):
				with open(theme_color_path) as test_theme:
					if THEME_VERSION in test_theme.read():
						success = apply_theme(theme_file)
					else:
						xbmc.log("Didn't work, trying again. {}".format(theme_file), xbmc.LOGINFO)
						retries -= 1
						random_theme = get_random_theme(file_list)
						theme_file = random_theme[:-4] if random_theme else 'default'
						theme_color_file = theme_file
			else:
				xbmc.log("Theme color file does not exist. Using default theme.", xbmc.LOGINFO)
				retries = 0

		if not success:
			apply_theme(default_theme)

	except Exception as e:
		xbmc.log("An error occurred: {}".format(e), xbmc.LOGERROR)

if __name__ == "__main__":
	main()