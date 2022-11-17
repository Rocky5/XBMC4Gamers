import os,random,shutil,sys,xbmc,xbmcgui
'''
 arguments 1:
	toggle
	select
	random
 arguments 2:
	theme name (not including extension)
'''
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
	
	TMP_Theme_Path = 'Z:/temp/themes/'
	if os.path.isdir(TMP_Theme_Path):
		shutil.rmtree(TMP_Theme_Path)
	os.makedirs(TMP_Theme_Path)
	XPR = os.listdir(xbmc.translatePath('Special://skin/media'))
	XPR = [x.lower().replace('textures',' default') for x in XPR]
	
	try:
		for fn in XPR:
			with open(os.path.join(TMP_Theme_Path,fn.upper()),"w") as ThemeFiles:
				ThemeFiles.write('')
	except: pass
	
	XPR = sorted(os.listdir(TMP_Theme_Path))
	Filter_XPR = [os.path.basename(r[0:-4]) for r in XPR]
	Filter_XPR = [x.replace(' D','D') for x in Filter_XPR]
	ThemeFolder = xbmcgui.Dialog().select('Select Theme',Filter_XPR,10000)
	
	if ThemeFolder == -1:
		pass
	else:
		SelectedTheme = XPR[ThemeFolder]
		if SelectedTheme.lower() == ' default.xpr':
			ThemeFile = 'default'
			ThemeColorFile = 'defaults'
		else:
			ThemeFile = SelectedTheme[:-4]
			ThemeColorFile= ThemeFile
		# Check if it's a v1.4+ Gamers theme.
		with open(os.path.join(xbmc.translatePath('Special://skin/colors'),ThemeColorFile+'.xml')) as test_theme:
			if 'XBMC4Gamers v1.4+' in test_theme.read():
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
				dialog.ok('ERROR','','This theme is not compatible with this version[CR]of XBMC4Gamers.','')
	xbmc.executebuiltin('Skin.Reset(SelectPreviewMode)') # This is reset so the preview isn't shown in the skin settings menu when not required.


if arg1 == 'random':
	Random_Theme = random.choice(os.listdir('Special://skin/media/'))
	if Random_Theme.lower() == 'textures.xpr':
		ThemeFile = 'default'
		ThemeColorFile = 'defaults'
	else:
		ThemeFile = Random_Theme[:-4]
		ThemeColorFile= ThemeFile
	# Check if it's a v1.4+ Gamers theme.
	with open(os.path.join(xbmc.translatePath('Special://skin/colors'),ThemeColorFile+'.xml')) as test_theme:
		if 'XBMC4Gamers v1.4+' in test_theme.read():
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