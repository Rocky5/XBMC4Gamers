'''
 arguments 1:
	toggle
	select
	random
 arguments 2:
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


def update_fontXML(ThemeFile):
	theme_xml_path = 'Special://skin/extras/themes/xmls/{}_fonts.xml'.format(ThemeFile)
	font_path = xbmc.translatePath('Special://skin/xml/Font.xml')
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;{}.xpr)'.format(ThemeFile))
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;{}.xml)'.format(ThemeFile))
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;default)')
	# if theme_fonts.xml is found its used to set fonts. Else default to normal method.
	if os.path.isfile(theme_xml_path):
		with open(theme_xml_path, 'r') as file1:
			file1_lines = file1.readlines()
		with open(font_path, 'r') as file2:
			file2_lines = file2.readlines()
		updated_lines = []
		for line1, line2 in zip(file1_lines, file2_lines):
			if line1 != line2 and not '<filename>monofont-' in line1 and not '<filename>home.ttf' in line1:
				updated_lines.append(line1)
			else:
				updated_lines.append(line2)
		with open(font_path, 'w') as output_file:
			output_file.writelines(updated_lines)
	else:
		for line in fileinput.input(font_path,inplace=1):
			if '<filename>' in line and not '<filename>monofont-' in line and not '<filename>home.ttf' in line:
				line = line = '			<filename>{}.ttf</filename>\n'.format(ThemeFile)
			print line,

def handle_theme_file(ThemeFile):
	theme_xml_path = 'Special://skin/extras/themes/xmls/{}.xml'.format(ThemeFile)
	override_xml_path = 'Special://skin/xml/Includes_Theme_Override.xml'
	if os.path.isfile(theme_xml_path):
		shutil.copyfile(theme_xml_path, override_xml_path)
	elif os.path.isfile(override_xml_path):
		try:
			os.remove(override_xml_path)
		except: pass

def handle_playlist(ThemeFile):
	if xbmc.getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
		if ThemeFile == 'default':
			playlist_path = 'Special://skin/extras/themes/playlists/default.m3u'
			random_playlist_path = 'Special://profile/playlists/music/random.m3u'
			if os.path.isfile(playlist_path):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(playlist_path))
			elif os.path.isfile(random_playlist_path):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(random_playlist_path))
			else:
				xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
		else:
			playlist_path = 'Special://skin/extras/themes/playlists/{}.m3u'.format(ThemeFile)
			random_playlist_path = 'Special://profile/playlists/music/random.m3u'
			if os.path.isfile(playlist_path):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(playlist_path))
			elif os.path.isfile(random_playlist_path):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(random_playlist_path))
			else:
				xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
	else:
		random_playlist_path = 'Special://profile/playlists/music/random.m3u'
		if os.path.isfile(random_playlist_path):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,{})'.format(random_playlist_path))
		else:
			xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')

def handle_folder_fanart(ThemeFile):
	xbmc.executebuiltin('Skin.SetString(FolderFanartPath,{})'.format(xbmc.translatePath('Special://skin/extras/folder fanart/default')))
	folder_fanart = xbmc.translatePath('Special://skin/extras/folder fanart/{}'.format(ThemeFile))
	if len(os.listdir(folder_fanart)) > 0:
		xbmc.executebuiltin('Skin.SetString(FolderFanartPath,{})'.format(folder_fanart))

def main():
	dialog = xbmcgui.Dialog()
	arg1 = sys.argv[1:][0]
	arg2 = sys.argv[2:][0]

	if arg1 == 'toggle':
		ThemeFile = 'default' if xbmc.getCondVisibility('StringCompare(Skin.CurrentTheme,night)') else arg2
		handle_folder_fanart(ThemeFile)
		update_fontXML(ThemeFile)
		handle_theme_file(ThemeFile)
		handle_playlist(ThemeFile)
		xbmc.executebuiltin('ReloadSkin')

	elif arg1 == 'select':
		xbmc.executebuiltin('Skin.SetBool(SelectPreviewMode)')
		Filter_XPR = sorted([x.lower().replace('textures', 'Default') for x in glob.glob(xbmc.translatePath('Special://skin/media/*.xpr'))])
		Filter_XPR = [os.path.basename(x.replace(".xpr", "").title()) for x in Filter_XPR]
		ThemeFolder = dialog.select('Select Theme', Filter_XPR, 10000)
		
		if ThemeFolder != -1:
			SelectedTheme = Filter_XPR[ThemeFolder]
			ThemeFile = 'default' if SelectedTheme.lower() == 'default' else SelectedTheme
			ThemeColorFile = 'defaults' if SelectedTheme.lower() == 'default' else ThemeFile
			
			with open(os.path.join(xbmc.translatePath('Special://skin/colors'), ThemeColorFile + '.xml')) as test_theme:
				if 'XBMC4Gamers v2.1+ 002' in test_theme.read() and os.path.isfile(os.path.join(xbmc.translatePath('Special://skin/backgrounds/'), ThemeFile + '/0.jpg')):
					handle_folder_fanart(ThemeFile)
					update_fontXML(ThemeFile)
					handle_theme_file(ThemeFile)
					handle_playlist(ThemeFile)
					xbmc.executebuiltin('ReloadSkin')
				else:
					dialog.ok(	'ERROR',
								'This theme is not compatible with this version of',
								'XBMC4Gamers.',
								'[CR]Try redownloading the theme.'	)
		xbmc.executebuiltin('Skin.Reset(SelectPreviewMode)')

	elif arg1 == 'random':
		while True:
			Random_Theme = random.choice(os.listdir('Special://skin/media/'))
			ThemeFile = 'default' if Random_Theme.lower() == 'textures.xpr' else Random_Theme[:-4]
			ThemeColorFile = 'defaults' if Random_Theme.lower() == 'textures.xpr' else ThemeFile
			
			with open(os.path.join(xbmc.translatePath('Special://skin/colors'), ThemeColorFile + '.xml')) as test_theme:
				if 'XBMC4Gamers v2.1+ 002' in test_theme.read() and os.path.isfile(os.path.join(xbmc.translatePath('Special://skin/backgrounds/'), ThemeFile + '/0.jpg')):
					handle_folder_fanart(ThemeFile)
					update_fontXML(ThemeFile)
					handle_theme_file(ThemeFile)
					handle_playlist(ThemeFile)
					xbmc.executebuiltin('ReloadSkin')
					break
				else:
					dialog.ok(	'ERROR',
								'This theme is not compatible with this version of',
								'XBMC4Gamers.',
								'[CR]Try redownloading the theme.'	)
					xbmc.executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Apply Theme.py,random,nothing)')

	time.sleep(2)
	xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty("MyScript.ExternalRunning", "False")

if __name__ == "__main__":
	main()
