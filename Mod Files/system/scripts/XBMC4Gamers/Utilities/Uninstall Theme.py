# -*- coding: utf-8 -*-
import glob
import os
import shutil
import sys
import time
import xbmc
import xbmcgui

INCLUDES_CUSTOM_VIEWS_PATH = xbmc.translatePath('Special://skin/xml/Includes_Custom_Views.xml')
DEFAULT_FOLDER = xbmc.translatePath('Special://skin/xml/custom views/_global')
DEFAULT_PLAYLIST = 'Special://skin/extras/themes/playlists/default.m3u'
RANDOM_PLAYLIST = 'Special://profile/playlists/music/random.m3u'

def set_global_views():
	try:
		with open(INCLUDES_CUSTOM_VIEWS_PATH, 'w') as custom_xml:
			custom_xml.write('<includes>\n\t<include name="Custom Views">\n')
			for ID in range(80, 90):
				xbmc.executebuiltin('Skin.Reset(CustomViewtype_id_{})'.format(ID))
				xbmc.executebuiltin('Skin.Reset(CustomViewtype_id_{}_JPG)'.format(ID))
				xml_file = os.path.join(DEFAULT_FOLDER, "CustomViewtype_id_{}.xml".format(ID))
				jpg_file = os.path.join(DEFAULT_FOLDER, "CustomViewtype_id_{}.jpg".format(ID))
				if os.path.isfile(xml_file) and os.path.isfile(jpg_file):
					xbmc.executebuiltin('Skin.SetBool(CustomViewtype_id_{})'.format(ID))
					print "Added custom _global view ID: {}".format(ID)
					custom_xml.write('\t\t<include file="custom views\\_global\\CustomViewtype_id_{}.xml" condition="Skin.HasSetting(CustomViewtype_id_{})">custom_id_{}</include>\n'.format(ID, ID, ID))
			custom_xml.write('\t</include>\n</includes>')
	except Exception as error:
		print 'Error in "Check for custom _global views": {}'.format(error)

def set_default_playlist():
	try:
		if os.path.isfile(xbmc.translatePath(DEFAULT_PLAYLIST)):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(DEFAULT_PLAYLIST))
		elif os.path.isfile(xbmc.translatePath(RANDOM_PLAYLIST)):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(RANDOM_PLAYLIST))
		else:
			xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
	except Exception as error:
		print 'Error in "Set default playlist": {}'.format(error)

def uninstall_theme(theme):
	paths_to_remove = [
		'Special://skin/colors/{}.xml'.format(theme),
		'Special://skin/backgrounds/{}'.format(theme),
		'Special://skin/extras/themes/folder fanart/{}'.format(theme),
		'Special://skin/extras/themes/playlists/{}.m3u'.format(theme),
		'Special://skin/extras/themes/playlists/{}'.format(theme),
		'Special://skin/extras/themes/previews/{}.jpg'.format(theme),
		'Special://skin/extras/themes/splashes/{}.png'.format(theme),
		'Special://skin/extras/themes/splashes/thumbs/{}.jpg'.format(theme),
		'Special://skin/extras/themes/xmls/custom views/{}'.format(theme),
		'Special://skin/extras/themes/xmls/{}.xml'.format(theme),
		'Special://skin/extras/themes/xmls/{}_fonts.xml'.format(theme),
		'Special://skin/sounds/{}'.format(theme),
		'Special://skin/fonts/{}.ttf'.format(theme),
		'Special://skin/media/{}.xpr'.format(theme),
		'Special://skin/extras/urldownloader themes/previews/{}.jpg'.format(theme),
		'Special://skin/extras/urldownloader themes/XML files/{}.xml'.format(theme)
	]
	
	# Multiple font check
	font_files = glob.glob(os.path.join(xbmc.translatePath('Special://skin/fonts/'), '{}_*.ttf'.format(theme)))
	paths_to_remove.extend(font_files)
	
	try:
		for path in [xbmc.translatePath(path) for path in paths_to_remove]:
			if os.path.isfile(path):
				os.remove(path)
			elif os.path.isdir(path):
				shutil.rmtree(path)
	except OSError as error:
		time.sleep(2)
		uninstall_theme(theme)

	set_default_playlist()
	set_global_views()

def wait_for_condition(condition_func, timeout=5):
	start_time = time.time()
	while not condition_func() and (time.time() - start_time) < timeout:
		time.sleep(0.1)

if __name__ == "__main__":
	xbmc.executebuiltin("Skin.SetBool(SelectPreviewMode)")
	xbmc.executebuiltin('Dialog.Close(1100,true)')

	xpr_files = glob.glob(xbmc.translatePath('Special://skin/media/*.xpr'))
	if xpr_files:
		filter_xpr = sorted([os.path.basename(x.lower()) for x in xpr_files])
		filter_xpr = [x.lower().replace(".xpr", "").title() for x in filter_xpr if x not in ["textures.xpr", "night.xpr"]]
		theme_folder = xbmcgui.Dialog().select('Select Theme', filter_xpr, 10000)

		if theme_folder != -1:
			theme = filter_xpr[theme_folder]
			if xbmcgui.Dialog().yesno('Would you like to uninstall', '', theme.title(), '', xbmc.getLocalizedString(106), xbmc.getLocalizedString(107)):
				if xbmc.getCondVisibility('StringCompare(Skin.CurrentTheme,{})'.format(theme)):
					xbmc.executebuiltin('ActivateWindow(1100)')
					script_path = xbmc.translatePath('Special://scripts/XBMC4Gamers/Utilities/Apply Theme.py')
					xbmc.executebuiltin('RunScript({},toggle,default)'.format(script_path))
					wait_for_condition(lambda: xbmc.getInfoLabel("Skin.CurrentTheme") == "default", 120)
				uninstall_theme(theme)
				xbmcgui.Dialog().ok('Complete', '', '{} uninstalled.'.format(theme))
			else:
				xbmc.executebuiltin('ActivateWindow(1100)')
				time.sleep(1)
				xbmc.executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Uninstall Theme.py)')
	else:
		xbmcgui.Dialog().ok('ERROR', 'You have no themes installed.', 'You can download themes from the built-in downloader.')

	xbmc.executebuiltin("Skin.Reset(SelectPreviewMode)")