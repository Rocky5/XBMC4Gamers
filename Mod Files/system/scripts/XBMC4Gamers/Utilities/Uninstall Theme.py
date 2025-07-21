# -*- coding: utf-8 -*-
from glob import glob
from os.path import basename, isdir, isfile, join
from os import remove
from shutil import rmtree
import time
from xbmc import executebuiltin, getCondVisibility, getInfoLabel, getLocalizedString, translatePath
from xbmcgui import Dialog

INCLUDES_CUSTOM_VIEWS_PATH = translatePath('Special://skin/xml/Includes_Custom_Views.xml')
DEFAULT_FOLDER = translatePath('Special://skin/xml/custom views/_global')
DEFAULT_PLAYLIST = 'Special://skin/extras/themes/playlists/default.m3u'
RANDOM_PLAYLIST = 'Special://profile/playlists/music/random.m3u'

def set_global_views():
	try:
		with open(INCLUDES_CUSTOM_VIEWS_PATH, 'w') as custom_xml:
			custom_xml.write('<includes>\n\t<include name="Custom Views">\n')
			for ID in range(80, 90):
				executebuiltin('Skin.Reset(CustomViewtype_id_{})'.format(ID))
				executebuiltin('Skin.Reset(CustomViewtype_id_{}_JPG)'.format(ID))
				xml_file = join(DEFAULT_FOLDER, "CustomViewtype_id_{}.xml".format(ID))
				jpg_file = join(DEFAULT_FOLDER, "CustomViewtype_id_{}.jpg".format(ID))
				if isfile(xml_file) and isfile(jpg_file):
					executebuiltin('Skin.SetBool(CustomViewtype_id_{})'.format(ID))
					print "Added custom _global view ID: {}".format(ID)
					custom_xml.write('\t\t<include file="custom views\\_global\\CustomViewtype_id_{}.xml" condition="Skin.HasSetting(CustomViewtype_id_{})">custom_id_{}</include>\n'.format(ID, ID, ID))
			custom_xml.write('\t</include>\n</includes>')
	except Exception as error:
		print 'Error in "Check for custom _global views": {}'.format(error)

def set_default_playlist():
	try:
		if isfile(translatePath(DEFAULT_PLAYLIST)):
			executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(DEFAULT_PLAYLIST))
		elif isfile(translatePath(RANDOM_PLAYLIST)):
			executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(RANDOM_PLAYLIST))
		else:
			executebuiltin('Skin.Reset(Startup_Playback_Path)')
	except Exception as error:
		print 'Error in "Set default playlist": {}'.format(error)

def uninstall_theme(theme):
	paths_to_remove = [
		'Special://skin/colors/{}.xml'.format(theme),
		'Special://skin/backgrounds/{}'.format(theme),
		'Special://skin/extras/folder fanart/{}'.format(theme),
		'Special://skin/extras/themes/playlists/{}.m3u'.format(theme),
		'Special://skin/extras/themes/playlists/{}'.format(theme),
		'Special://skin/extras/themes/previews/{}.jpg'.format(theme),
		'Special://skin/extras/themes/splashes/{}.png'.format(theme),
		'Special://skin/extras/themes/splashes/thumbs/{}.jpg'.format(theme),
		'Special://skin/extras/themes/xmls/custom views/{}'.format(theme),
		'Special://skin/extras/themes/xmls/{}.xml'.format(theme),
		'Special://skin/extras/themes/xmls/{}_fonts.xml'.format(theme),
		'Special://skin/extras/themes/scripts/{}'.format(theme),
		'Special://skin/extras/urldownloader themes/previews/{}.jpg'.format(theme),
		'Special://skin/extras/urldownloader themes/XML files/{}.xml'.format(theme),
		'Special://skin/extras/user icons/{}'.format(theme),
		'Special://skin/sounds/{}'.format(theme),
		'Special://skin/fonts/{}.ttf'.format(theme),
		'Special://skin/media/{}.xpr'.format(theme)
	]
	
	# Multiple font check
	font_files = glob(join(translatePath('Special://skin/fonts/'), '{}_*.ttf'.format(theme)))
	paths_to_remove.extend(font_files)
	
	try:
		for path in [translatePath(path) for path in paths_to_remove]:
			if isfile(path):
				remove(path)
			elif isdir(path):
				rmtree(path)
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
	executebuiltin("Skin.SetBool(SelectPreviewMode)")
	executebuiltin('Dialog.Close(1100,true)')

	xpr_files = glob(translatePath('Special://skin/media/*.xpr'))
	if xpr_files:
		filter_xpr = sorted([basename(x.lower()) for x in xpr_files])
		filter_xpr = [x.lower().replace(".xpr", "").upper() for x in filter_xpr if x not in ["textures.xpr", "night.xpr"]]
		theme_folder = Dialog().select('Select Theme', filter_xpr, 10000)

		if theme_folder != -1:
			theme = filter_xpr[theme_folder]
			if Dialog().yesno('Would you like to uninstall', '', theme.upper(), '', getLocalizedString(106), getLocalizedString(107)):
				if getCondVisibility('StringCompare(Skin.CurrentTheme,{})'.format(theme)):
					executebuiltin('ActivateWindow(1100)')
					script_path = translatePath('Special://scripts/XBMC4Gamers/Utilities/Apply Theme.py')
					executebuiltin('RunScript({},toggle,default)'.format(script_path))
					wait_for_condition(lambda: getInfoLabel("Skin.CurrentTheme") == "default", 120)
				uninstall_theme(theme)
				Dialog().ok('Complete', '', '{} uninstalled.'.format(theme))
			else:
				executebuiltin('ActivateWindow(1100)')
				time.sleep(1)
				executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Uninstall Theme.py)')
	else:
		Dialog().ok('ERROR', 'You have no themes installed.', 'You can download themes from the built-in downloader.')

	executebuiltin("Skin.Reset(SelectPreviewMode)")