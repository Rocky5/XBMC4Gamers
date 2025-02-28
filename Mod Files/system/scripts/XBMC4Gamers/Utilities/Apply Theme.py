# -*- coding: utf-8 -*- 
'''
Arguments 1:
	toggle
	select
	random
Arguments 2:
	theme name (not including extension)
'''

import fileinput
import glob
import os
import random
import shutil
import sys
import time
import xbmc
import xbmcgui
import xml.etree.ElementTree as ET

sys.path.append(xbmc.translatePath('Special://scripts/XBMC4Gamers/Utilities/libs'))
from custom_views import custom_views_update_programs as check_custom_views
from theme_version import THEME_VERSION

THEME_DIR = 'Special://skin/media/'
SPLASH_DIR = 'Special://skin/extras/themes/splashes/'
FONT_PATH = xbmc.translatePath('Special://skin/xml/Font.xml')

def update_fontXML(ThemeFile):
	theme_xml_path = xbmc.translatePath('Special://skin/extras/themes/xmls/{}_fonts.xml'.format(ThemeFile))
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;{}.xpr)'.format(ThemeFile))
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;{}.xml)'.format(ThemeFile))
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;default)')
																					
	if os.path.isfile(theme_xml_path):
		with open(theme_xml_path, 'r') as file1, open(FONT_PATH, 'r') as file2:
			file1_lines = file1.readlines()
			file2_lines = file2.readlines()
		
		updated_lines = []
		for line1, line2 in zip(file1_lines, file2_lines):
			if line1 != line2 and '<filename>monofont-' not in line1 and '<filename>home.ttf' not in line1:
				updated_lines.append(line1)
			else:
				updated_lines.append(line2)
		
		with open(FONT_PATH, 'w') as output_file:
			output_file.writelines(updated_lines)
	else:
		for line in fileinput.input(FONT_PATH, inplace=True):
			if '<filename>' in line and '<filename>monofont-' not in line and '<filename>home.ttf' not in line:
				line = '            <filename>{}.ttf</filename>\n'.format(ThemeFile)
			print line,

def handle_theme_files(ThemeFile):
	global reload_home
	reload_home = 0
	theme_xml_path = xbmc.translatePath('Special://skin/extras/themes/xmls/{}.xml'.format(ThemeFile))
	override_xml_path = xbmc.translatePath('Special://skin/xml/Includes_Theme_Override.xml')
	
	if os.path.isfile(theme_xml_path):
		if os.path.isfile(override_xml_path):
			if check_for_tags(override_xml_path):
				reload_home = 1
			os.remove(override_xml_path)
		shutil.copyfile(theme_xml_path, override_xml_path)
		if check_for_tags(override_xml_path):
			reload_home = 1
	elif os.path.isfile(override_xml_path):
		if check_for_tags(override_xml_path):
			reload_home = 1
		os.remove(override_xml_path)

	theme_custom_view_path = xbmc.translatePath('Special://skin/extras/themes/xmls/custom views/{}'.format(ThemeFile))
	custom_view_path = xbmc.translatePath('Special://skin/xml/custom views')
	custom_view_theme_path = xbmc.translatePath('Special://skin/xml/custom views/{}'.format(ThemeFile))
	try:
		for folder in os.listdir(custom_view_path):
			folder_path = os.path.join(custom_view_path, folder)
			if folder.lower() != '_global' and os.path.isdir(folder_path):
				shutil.rmtree(folder_path)
	except IOError as error:
		xbmc.log('Removal of "{}" folder from "{}"'.format(error, custom_view_path), xbmc.LOGERROR)
	
	if os.path.isdir(theme_custom_view_path):
		if os.path.isdir(custom_view_theme_path):
			shutil.rmtree(custom_view_theme_path)
		shutil.copytree(theme_custom_view_path, custom_view_theme_path)

def check_for_tags(theme_xml_path):
	lastplayed_exists = 0
	randoms_exists = 0

	if os.path.isfile(theme_xml_path):
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
	playlist_path = xbmc.translatePath('Special://profile/playlists/music/random.m3u')
	if xbmc.getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
		if ThemeFile == 'default':
			default_playlist = xbmc.translatePath('Special://skin/extras/themes/playlists/default.m3u')
			if os.path.isfile(default_playlist):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(default_playlist))
			elif os.path.isfile(playlist_path):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(playlist_path))
			else:
				xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
		else:
			theme_playlist = xbmc.translatePath('Special://skin/extras/themes/playlists/{}.m3u'.format(ThemeFile))
			if os.path.isfile(theme_playlist):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(theme_playlist))
			elif os.path.isfile(playlist_path):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(playlist_path))
			else:
				xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
	else:
		if os.path.isfile(playlist_path):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(playlist_path))
		else:
			xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')

def handle_folder_fanart(ThemeFile):
	xbmc.executebuiltin('Skin.SetString(FolderFanartPath,{})'.format(xbmc.translatePath('Special://skin/extras/folder fanart/default')))
	folder_fanart = xbmc.translatePath('Special://skin/extras/folder fanart/{}'.format(ThemeFile))
	if len(os.listdir(folder_fanart)) > 0:
		xbmc.executebuiltin('Skin.SetString(FolderFanartPath,{})'.format(folder_fanart))

def check_custom_sounds(ThemeFile):
	try:
		theme_sound_xml = xbmc.translatePath('Special://skin/sounds/{}/sounds.xml'.format(ThemeFile))
		if os.path.isfile(theme_sound_xml) and not xbmc.getCondVisibility('Skin.HasSetting(disablethemesounds)'):
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.soundskin;{})'.format(ThemeFile))
		else:
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.soundskin;default)')
	except Exception as error:
		xbmc.log('Error in "Check for custom sounds": {}'.format(error), xbmc.LOGERROR)

def process_theme(ThemeFile):
		handle_folder_fanart(ThemeFile)
		update_fontXML(ThemeFile)
		handle_theme_files(ThemeFile)
		handle_playlist(ThemeFile)
		check_custom_views(ThemeFile)
		check_custom_sounds(ThemeFile)

if __name__ == "__main__":
	global reload_home
	reload_home = 0
	dialog = xbmcgui.Dialog()
	xbmc.executebuiltin('Dialog.Close(1100,false)')
	wait_delay = 2
	arg1 = sys.argv[1]
	arg2 = sys.argv[2]

	if arg1 == 'toggle':
		ThemeFile = 'default' if xbmc.getCondVisibility('StringCompare(Skin.CurrentTheme,night)') else arg2.lower()
		process_theme(ThemeFile)
		xbmc.executebuiltin('ReloadSkin')

	elif arg1 == 'select':
		xbmc.executebuiltin('Skin.SetBool(SelectPreviewMode)')
		Filter_XPR = sorted([x.lower().replace('textures', 'Default') for x in glob.glob(xbmc.translatePath('Special://skin/media/*.xpr'))])
		Filter_XPR = [os.path.basename(x.replace(".xpr", "").title()) for x in Filter_XPR]
		ThemeFolder = dialog.select('Select Theme', Filter_XPR, 10000)
		
		if ThemeFolder != -1:
			SelectedTheme = Filter_XPR[ThemeFolder]
			ThemeFile = 'default' if SelectedTheme.lower() == 'default' else SelectedTheme.lower()
			ThemeColorFile = 'defaults' if SelectedTheme.lower() == 'default' else ThemeFile
			
			with open(os.path.join(xbmc.translatePath('Special://skin/colors'), ThemeColorFile + '.xml')) as test_theme:
				if THEME_VERSION in test_theme.read() and os.path.isfile(os.path.join(xbmc.translatePath('Special://skin/backgrounds/'), '{}/0.jpg'.format(ThemeFile))):
					process_theme(ThemeFile)
					xbmc.executebuiltin('ReloadSkin')
				else:
					dialog.ok('ERROR', '', 'This theme is not compatible with this version of XBMC4Gamers.', '[CR]Redownloading the theme.')

		xbmc.executebuiltin('Skin.Reset(SelectPreviewMode)')

	elif arg1 == 'random':
		while True:
			Random_Theme = random.choice(os.listdir(xbmc.translatePath('Special://skin/media/')))
			ThemeFile = 'default' if Random_Theme.lower() == 'textures.xpr' else Random_Theme[:-4].lower()
			ThemeColorFile = 'defaults' if Random_Theme.lower() == 'textures.xpr' else ThemeFile
			
			with open(os.path.join(xbmc.translatePath('Special://skin/colors'), ThemeColorFile + '.xml')) as test_theme:
				if THEME_VERSION in test_theme.read() and os.path.isfile(os.path.join(xbmc.translatePath('Special://skin/backgrounds/'), '{}/0.jpg'.format(ThemeFile))):
					process_theme(ThemeFile)
					xbmc.executebuiltin('ReloadSkin')
					break
				else:
					dialog.ok('ERROR', '', 'This theme is not compatible with this version of XBMC4Gamers.', '[CR]Redownloading the theme.')
					xbmc.executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Apply Theme.py,random,nothing)')

	elif arg1 == 'startup':
		wait_delay = 0
		ThemeFile = arg2.lower()
		process_theme(ThemeFile)
		xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty("MyScript.ExternalRunning", "False")

	time.sleep(wait_delay)

	if reload_home and xbmc.getCondVisibility('StringCompare(Skin.String(HomeWindowSource),Home)'):
		xbmc.executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Home Screen Items.py,1)')
		if xbmc.getCondVisibility('Window.IsActive(1111)'):
			xbmc.executebuiltin('RunScript(Special://Scripts/XBMC4Gamers/Utilities/Dialogs.py,"","ok","$LOCALIZE[31600]","","$LOCALIZE[31611]","","","")')