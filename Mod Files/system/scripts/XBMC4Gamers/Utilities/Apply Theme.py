'''
 arguments 1:
	toggle
	select
	random
 arguments 2:
	theme name (not including extension)
'''
import glob,os,random,shutil,sys,xbmc,xbmcgui
dialog = xbmcgui.Dialog()
arg1 = sys.argv[1:][0]
arg2 = sys.argv[2:][0]


if arg1 == 'toggle':
	if xbmc.getCondVisibility('StringCompare(Skin.CurrentTheme,night)'):
		ThemeFile = 'default'
	else:
		ThemeFile = arg2
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;%s.xpr)'%ThemeFile)
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;%s.xml)'%ThemeFile)
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;%s.ttf)'%ThemeFile)
	if xbmc.getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
		if ThemeFile == 'default':
			if os.path.isfile('Special://skin/extras/themes/playlists/default.m3u'):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/default.m3u)')
			elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
			else:
				xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
		else:	
			if os.path.isfile('Special://skin/extras/themes/playlists/'+ThemeFile+'.m3u'):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/'+ThemeFile+'.m3u)')
			elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
			else:
				xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
	else:
		if os.path.isfile('Special://profile/playlists/music/random.m3u'):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
		else:
			xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
	xbmc.executebuiltin('ReloadSkin')


if arg1 == 'select':
	xbmc.executebuiltin('Skin.SetBool(SelectPreviewMode)') # This is set so the preview is shown in the skin settings menu when required.

	Filter_XPR = sorted([x.lower().replace('textures','Default') for x in glob.glob(xbmc.translatePath('Special://skin/media/*.xpr'))], key=None, reverse=0)
	Filter_XPR = [os.path.basename(x.replace(".xpr","").title()) for x in Filter_XPR]
	ThemeFolder = dialog.select('Select Theme',Filter_XPR,10000)
	
	if ThemeFolder == -1:
		pass
	else:
		SelectedTheme = Filter_XPR[ThemeFolder]
		if SelectedTheme.lower() == 'default':
			ThemeFile = 'default'
			ThemeColorFile = 'defaults'
		else:
			ThemeFile = SelectedTheme
			ThemeColorFile= ThemeFile
		# Check if it's a v2.0+ Gamers theme.
		with open(os.path.join(xbmc.translatePath('Special://skin/colors'),ThemeColorFile+'.xml')) as test_theme:
			if 'XBMC4Gamers v2.0+' in test_theme.read() and os.path.isfile(os.path.join(xbmc.translatePath('Special://skin/backgrounds/'),ThemeFile+'/0.jpg')):
				xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;%s.xpr)'%ThemeFile)
				xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;%s.xml)'%ThemeFile)
				xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;%s.ttf)'%ThemeFile)
				if xbmc.getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
					if ThemeFile == 'default':
						if os.path.isfile('Special://skin/extras/themes/playlists/default.m3u'):
							xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/default.m3u)')
						elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
							xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
						else:
							xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
					else:
						if os.path.isfile('Special://skin/extras/themes/playlists/'+ThemeFile+'.m3u'): xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/'+ThemeFile+'.m3u)')
				else:
					if os.path.isfile('Special://profile/playlists/music/random.m3u'):
						xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
					else:
						xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
				xbmc.executebuiltin('ReloadSkin')
			else:
				dialog.ok('ERROR','This theme is not compatible with this version of','XBMC4Gamers.','[CR]Try redownloading the theme.')
	xbmc.executebuiltin('Skin.Reset(SelectPreviewMode)') # This is reset so the preview isn't shown in the skin settings menu when not required.


if arg1 == 'random':
	Random_Theme = random.choice(os.listdir('Special://skin/media/'))
	if Random_Theme.lower() == 'textures.xpr':
		ThemeFile = 'default'
		ThemeColorFile = 'defaults'
	else:
		ThemeFile = Random_Theme[:-4]
		ThemeColorFile= ThemeFile
	# Check if it's a v2.0+ Gamers theme.
	with open(os.path.join(xbmc.translatePath('Special://skin/colors'),ThemeColorFile+'.xml')) as test_theme:
		if 'XBMC4Gamers v2.0+' in test_theme.read() and os.path.isfile(os.path.join(xbmc.translatePath('Special://skin/backgrounds/'),ThemeFile+'/0.jpg')):
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;%s.xpr)'%ThemeFile)
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;%s.xml)'%ThemeFile)
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;%s.ttf)'%ThemeFile)
			if xbmc.getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
				if ThemeFile == 'default':
					if os.path.isfile('Special://skin/extras/themes/playlists/default.m3u'):
						xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/default.m3u)')
					elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
						xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
					else:
						xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
				else:	
					if os.path.isfile('Special://skin/extras/themes/playlists/'+ThemeFile+'.m3u'):
						xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/'+ThemeFile+'.m3u)')
					elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
						xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
					else:
						xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
			else:
				if os.path.isfile('Special://profile/playlists/music/random.m3u'):
					xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
				else:
					xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
			xbmc.executebuiltin('ReloadSkin')
		else:
			# Rerun till we find a working theme.
			xbmc.executebuiltin('RunScript(Special://root/system/scripts/XBMC4Gamers/Utilities/Apply Theme.py,random,nothing)')