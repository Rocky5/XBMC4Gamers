import glob
import os
import shutil
import sys
import time
import xbmc
import xbmcgui

def main():
	xbmc.executebuiltin("Skin.SetBool(SelectPreviewMode)")
	xbmc.executebuiltin('Dialog.Close(1100,true)')

	xpr_files = glob.glob(xbmc.translatePath('Special://skin/media/*.xpr'))
	if xpr_files:
		filter_xpr = sorted([os.path.basename(x.lower()) for x in xpr_files])
		filter_xpr = [x.replace(".xpr", "").title() for x in filter_xpr if x not in ["textures.xpr", "night.xpr"]]
		theme_folder = xbmcgui.Dialog().select('Select Theme', filter_xpr, 10000)

		if theme_folder != -1:
			theme = filter_xpr[theme_folder]
			if xbmcgui.Dialog().yesno('Would you like to uninstall', theme.upper(), '', '',xbmc.getLocalizedString(106),xbmc.getLocalizedString(107)):
				uninstall_theme(theme)
				xbmcgui.Dialog().ok(	'Complete',
										'{} uninstalled.'.format(theme),
										''	)
			else:
				xbmc.executebuiltin('ActivateWindow(1100)')
				time.sleep(1)
				xbmc.executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Uninstall Theme.py)')
	else:
		xbmcgui.Dialog().ok(	'ERROR',
								'You have no themes installed.',
								'You can download themes from the built-in downloader.'	)

	xbmc.executebuiltin("Skin.Reset(SelectPreviewMode)")

def uninstall_theme(theme):
	if xbmc.getCondVisibility('StringCompare(Skin.CurrentTheme,{})'.format(theme)):
		if os.path.isfile('Special://skin/xml/Includes_Theme_Override.xml'):
			os.remove('Special://skin/xml/Includes_Theme_Override.xml')
		xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty("MyScript.ExternalRunning", "True")
		xbmc.executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Apply Theme.py,toggle,default)')
		while xbmcgui.Window(xbmcgui.getCurrentWindowId()).getProperty("MyScript.ExternalRunning") == "True":
			time.sleep(3)

	paths_to_remove = [
		'Special://skin/colors/{}.xml'.format(theme),
		'Special://skin/backgrounds/{}'.format(theme),
		'Special://skin/extras/themes/playlists/{}.m3u'.format(theme),
		'Special://skin/extras/themes/playlists/{}'.format(theme),
		'Special://skin/extras/themes/previews/{}.jpg'.format(theme),
		'Special://skin/extras/themes/splashes/{}.png'.format(theme),
		'Special://skin/extras/themes/splashes/thumbs/{}.jpg'.format(theme),
		'Special://skin/extras/themes/xmls/{}.xml'.format(theme),
		'Special://skin/extras/themes/xmls/{}_fonts.xml'.format(theme),
		'Special://skin/fonts/{}.ttf'.format(theme),
		'Special://skin/media/{}.xpr'.format(theme),
		'Special://skin/extras/urldownloader themes/previews/{}.jpg'.format(theme),
		'Special://skin/extras/urldownloader themes/XML files/{}.xml'.format(theme)
	]
	# multi font check
	font_files = glob.glob(os.path.join('Special://skin/fonts/', '{}_*.ttf'.format(theme)))
	for font_file in font_files:
		font_name = os.path.basename(font_file)
		paths_to_remove.append('Special://skin/fonts/{}'.format(font_name))

	for path in [xbmc.translatePath(path) for path in paths_to_remove]:
		if os.path.isfile(path):
			# print "File: {}".format(path)
			os.remove(path)
		elif os.path.isdir(path):
			# print "Folder: {}".format(path)
			shutil.rmtree(path)

	set_theme_playlist()

def set_theme_playlist():
	if os.path.isfile('Special://skin/extras/themes/playlists/default.m3u'):
		xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/default.m3u)')
	elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
		xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
	else:
		xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')

if __name__ == "__main__":
	main()
