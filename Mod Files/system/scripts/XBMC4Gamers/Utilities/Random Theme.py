import fileinput
import os
import random
import time
import xbmc
import xbmcgui

def get_random_theme(file_list):
	if 'night.xpr' in file_list:
		file_list.remove('night.xpr')
	if 'Textures.xpr' in file_list:
		file_list.remove('Textures.xpr')
	if 'textures.xpr' in file_list:
		file_list.remove('textures.xpr')
	return random.choice(file_list)

def set_startup_playback_path(theme_file):
	if theme_file == "default":
		if os.path.isfile('Special://skin/extras/themes/playlists/default.m3u'):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/default.m3u)')
		elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
		else:
			xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
	else:
		if os.path.isfile('Special://skin/extras/themes/playlists/%s.m3u' % theme_file):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/%s.m3u)' % theme_file)
		elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
		else:
			xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')

def main():
	if xbmc.getCondVisibility('Skin.HasSetting(randomthemedl)'):
		file_list = os.listdir('Special://skin/media/')
		random_theme = get_random_theme(file_list)
	else:
		random_theme = random.choice(os.listdir('Special://skin/media/'))

	theme_file = 'default' if random_theme.lower() == "textures.xpr" else random_theme[:-4]
	theme_color_file = theme_file

	if xbmc.getCondVisibility('Skin.HasSetting(randomthemewallpaper)'):
		xbmc.executebuiltin('Skin.SetString(Background_Color,' + str(random.randint(1, 15)) + '.jpg)')
		xbmc.executebuiltin('Skin.Reset(Background_Image)')
		xbmc.executebuiltin('Skin.Reset(Background_Custom_Color)')

	theme_color_path = os.path.join(xbmc.translatePath('Special://skin/colors'), theme_color_file + ".xml")
	with open(theme_color_path) as test_theme:
		if "XBMC4Gamers v2.0+" in test_theme.read():
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;%s.xpr)' % theme_file)
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;%s.xml)' % theme_file)
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;default)')
			for line in fileinput.input(xbmc.translatePath('Special://skin/xml/Font.xml'),inplace=1):
				if '<filename>' in line and not '<filename>monofont' in line:
					line = line = '			<filename>%s.ttf</filename>\n' % theme_file
				print line,

			if xbmc.getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
				set_startup_playback_path(theme_file)
			else:
				if os.path.isfile('Special://profile/playlists/music/random.m3u'):
					xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
				else:
					xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')

			time.sleep(0.5)

			if not xbmc.getCondVisibility('Skin.HasSetting(introenabled)'):
				splash_path = 'Special://skin/extras/themes/splashes/%s.png' % theme_file
				if os.path.isfile(splash_path):
					xbmc.executebuiltin('ShowPicture(%s)' % splash_path)
					time.sleep(2)
				else:
					xbmc.executebuiltin('ShowPicture(Special://root/splash.png)')
					time.sleep(2)

			xbmc.executebuiltin('ReloadSkin')
			xbmc.executebuiltin('ReplaceWindow(2999)')
		else:
			print "| Didn't work, trying again. " + theme_file
			xbmc.executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Random Theme.py)')

if __name__ == "__main__":
	main()
