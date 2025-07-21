# -*- coding: utf-8 -*- 
'''
Arguments 1:
	toggle
	select
	random
Arguments 2:
	theme name (not including extension)
'''

from filecmp import cmp as compare_file
from fileinput import input as fileinput
from glob import glob
from os.path import basename, isdir, isfile, join
from os import listdir, remove
from random import choice
from shutil import copyfile, copytree, rmtree
from sys import argv
from time import sleep
from xbmc import executebuiltin, executehttpapi, getCondVisibility, getInfoLabel, log, LOGERROR, translatePath
import xbmcgui
import xml.etree.ElementTree as ET

sys.path.append(translatePath('Special://scripts/XBMC4Gamers/Utilities/libs'))
from custom_views import custom_views_update_programs as check_custom_views
from theme_version import THEME_VERSION

THEME_DIR = 'Special://skin/media/'
SPLASH_DIR = 'Special://skin/extras/themes/splashes/'
FONT_PATH = translatePath('Special://skin/xml/Font.xml')
MASTER_PROFILE_SKIN = "Add User"

def update_fontXML(ThemeFile):
	backup_xml = translatePath('Special://root/skins/{}/xml/Font.xml'.format(MASTER_PROFILE_SKIN))
	theme_xml = translatePath('Special://skin/extras/themes/xmls/{}_fonts.xml'.format(ThemeFile))
	theme_fonts_installed = translatePath('Special://skin/xml/Fonts_Custom_Installed.xml')
	executehttpapi('SetGUISetting(3;lookandfeel.skintheme;{}.xpr)'.format(ThemeFile))
	executehttpapi('SetGUISetting(3;lookandfeel.skincolors;{}.xml)'.format(ThemeFile))
	executehttpapi('SetGUISetting(3;lookandfeel.font;default)')
																					
	if isfile(theme_xml):
		if not compare_file(theme_xml, FONT_PATH, shallow=False):
			copyfile(theme_xml, FONT_PATH)
			with open(theme_fonts_installed, "w") as installed:
				installed.write("")
	else:
		if isfile(theme_fonts_installed):
			remove(theme_fonts_installed)
		copyfile(backup_xml, FONT_PATH)

		for line in fileinput(FONT_PATH, inplace=True):
			if '<filename>' in line and '<filename>monofont-' not in line and '<filename>home.ttf' not in line:
				line = '            <filename>{}.ttf</filename>\n'.format(ThemeFile)
			print line,

def handle_theme_files(ThemeFile):
	reload_home = 0
	theme_xml_path = translatePath('Special://skin/extras/themes/xmls/{}.xml'.format(ThemeFile))
	override_xml_path = translatePath('Special://skin/xml/Includes_Theme_Override.xml')
	
	if isfile(theme_xml_path):
		if isfile(override_xml_path):
			if check_for_tags(override_xml_path):
				reload_home = 1
			remove(override_xml_path)
		copyfile(theme_xml_path, override_xml_path)
		if check_for_tags(override_xml_path):
			reload_home = 1
	elif isfile(override_xml_path):
		if check_for_tags(override_xml_path):
			reload_home = 1
		remove(override_xml_path)

	theme_custom_view_path = translatePath('Special://skin/extras/themes/xmls/custom views/{}'.format(ThemeFile))
	custom_view_path = translatePath('Special://skin/xml/custom views')
	custom_view_theme_path = translatePath('Special://skin/xml/custom views/{}'.format(ThemeFile))
	try:
		for folder in listdir(custom_view_path):
			folder_path = join(custom_view_path, folder)
			if folder.lower() != '_global' and isdir(folder_path):
				rmtree(folder_path)
	except IOError as error:
		log('Removal of "{}" folder from "{}"'.format(error, custom_view_path), LOGERROR)
	
	if isdir(theme_custom_view_path):
		if isdir(custom_view_theme_path):
			rmtree(custom_view_theme_path)
		copytree(theme_custom_view_path, custom_view_theme_path)
		
	check_custom_views(ThemeFile)

	return reload_home

def handle_walls(ThemeFile):
	if not getCondVisibility('Skin.HasSetting(custom_wallpaper_set)'):
		executebuiltin(
			'SetWallpaper(Background_Image, {}, {}, {}, Q:\\skins\\Profile\\backgrounds\\{}\\0.jpg)'.format(
				getInfoLabel('Skin.String(WallpaperWidth)'),
				getInfoLabel('Skin.String(WallpaperHeight)'),
				getInfoLabel('Skin.String(WallpaperQuality)'),
				ThemeFile
		))
	
def check_for_tags(theme_xml_path):
	lastplayed_exists = 0
	randoms_exists = 0

	if isfile(theme_xml_path):
		elements = ET.parse(theme_xml_path).getroot().iter()
		for lines_checked, element in enumerate(elements, start=1):
			if element.tag.lower() == 'parse_lastplayed_total':
				lastplayed_exists = 1
			elif element.tag.lower() == 'parse_randoms_total':
				randoms_exists = 1
			if lastplayed_exists or randoms_exists:
				return 1
			if lines_checked >= 20:
				break

	return 0

def handle_playlist(ThemeFile):
	playlist_path = translatePath('Special://profile/playlists/music/random.m3u')
	if getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
		if ThemeFile == 'default':
			default_playlist = translatePath('Special://skin/extras/themes/playlists/default.m3u')
			if isfile(default_playlist):
				executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(default_playlist))
			elif isfile(playlist_path):
				executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(playlist_path))
			else:
				executebuiltin('Skin.Reset(Startup_Playback_Path)')
		else:
			theme_playlist = translatePath('Special://skin/extras/themes/playlists/{}.m3u'.format(ThemeFile))
			if isfile(theme_playlist):
				executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(theme_playlist))
			elif isfile(playlist_path):
				executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(playlist_path))
			else:
				executebuiltin('Skin.Reset(Startup_Playback_Path)')
	else:
		if isfile(playlist_path):
			executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(playlist_path))
		else:
			executebuiltin('Skin.Reset(Startup_Playback_Path)')

def handle_folder_fanart(ThemeFile):
	executebuiltin('Skin.SetString(FolderFanartPath,{})'.format(translatePath('Special://skin/extras/folder fanart/default')))
	folder_fanart = translatePath('Special://skin/extras/folder fanart/{}'.format(ThemeFile))
	if len(listdir(folder_fanart)) > 0:
		executebuiltin('Skin.SetString(FolderFanartPath,{})'.format(folder_fanart))

def check_custom_sounds(ThemeFile):
	try:
		theme_sound_xml = translatePath('Special://skin/sounds/{}/sounds.xml'.format(ThemeFile))
		if isfile(theme_sound_xml) and not getCondVisibility('Skin.HasSetting(disablethemesounds)'):
			executehttpapi('SetGUISetting(3;lookandfeel.soundskin;{})'.format(ThemeFile))
		else:
			executehttpapi('SetGUISetting(3;lookandfeel.soundskin;default)')
	except Exception as error:
		log('Error in "Check for custom sounds": {}'.format(error), LOGERROR)

def process_theme(ThemeFile):
	handle_folder_fanart(ThemeFile)
	update_fontXML(ThemeFile)
	handle_playlist(ThemeFile)
	check_custom_sounds(ThemeFile)
	handle_walls(ThemeFile)
	
	return handle_theme_files(ThemeFile)

if __name__ == "__main__":
	dialog = xbmcgui.Dialog()
	reload_skin = False
	reload_home = 0
	arg1 = argv[1]
	arg2 = argv[2]

	if arg1 == 'toggle':
		executebuiltin('Dialog.Close(1100,true)')
		ThemeFile = 'default' if getCondVisibility('StringCompare(Skin.CurrentTheme,night)') else arg2.lower()
		reload_home = process_theme(ThemeFile)
		reload_skin = True

	elif arg1 == 'select':
		executebuiltin('Dialog.Close(1100,true)')
		executebuiltin('Skin.SetBool(SelectPreviewMode)')
		Filter_XPR = sorted([x.lower().replace('textures', 'Default') for x in glob(translatePath('Special://skin/media/*.xpr'))])
		Filter_XPR = [basename(x.replace(".xpr", "").upper()) for x in Filter_XPR]
		ThemeFolder = dialog.select('Select Theme', Filter_XPR, 10000)
		
		if ThemeFolder != -1:
			SelectedTheme = Filter_XPR[ThemeFolder]
			ThemeFile = 'default' if SelectedTheme.lower() == 'default' else SelectedTheme.lower()
			ThemeColorFile = 'defaults' if SelectedTheme.lower() == 'default' else ThemeFile
			
			with open(join(translatePath('Special://skin/colors'), ThemeColorFile + '.xml')) as test_theme:
				if THEME_VERSION in test_theme.read() and isfile(join(translatePath('Special://skin/backgrounds/'), '{}/0.jpg'.format(ThemeFile))):
					reload_home = process_theme(ThemeFile)
					reload_skin = True
				else:
					dialog.ok('ERROR', '', 'This theme is not compatible with this version of XBMC4Gamers.', '[CR]Redownloading the theme.')

		executebuiltin('Skin.Reset(SelectPreviewMode)')

	elif arg1 == 'random':
		executebuiltin('Dialog.Close(1100,true)')
		while True:
			Random_Theme = choice(listdir(translatePath('Special://skin/media/')))
			ThemeFile = 'default' if Random_Theme.lower() == 'textures.xpr' else Random_Theme[:-4].lower()
			ThemeColorFile = 'defaults' if Random_Theme.lower() == 'textures.xpr' else ThemeFile
			
			with open(join(translatePath('Special://skin/colors'), ThemeColorFile + '.xml')) as test_theme:
				if THEME_VERSION in test_theme.read() and isfile(join(translatePath('Special://skin/backgrounds/'), '{}/0.jpg'.format(ThemeFile))):
					reload_home = process_theme(ThemeFile)
					reload_skin = True
					break
				else:
					dialog.ok('ERROR', '', 'This theme is not compatible with this version of XBMC4Gamers.', '[CR]Redownloading the theme.')
					executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Apply Theme.py,random,nothing)')
		
	if reload_skin:
		executebuiltin('ReloadSkin')

	if reload_home and getCondVisibility('StringCompare(Skin.String(HomeWindowSource),Home)'):
		sleep(1)
		if getCondVisibility('Window.IsActive(1111)'):
			executebuiltin('RunScript(Special://Scripts/XBMC4Gamers/Utilities/Dialogs.py,"","ok","$LOCALIZE[31600]","","$LOCALIZE[31611]","","","")')
		executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Parse Programs DB.py,refresh_home)')