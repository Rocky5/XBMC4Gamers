import os,random,shutil,sys,xbmc,xbmcgui
'''
 arguments 1:
	toggle
	select
	random
 arguments 2:
	theme name (not including extension)
'''
arg1 = sys.argv[1:][0]
arg2 = sys.argv[2:][0]
if arg1 == 'toggle':
	if xbmc.getCondVisibility('StringCompare(Skin.CurrentTheme,night)'):
		ThemeFile = "default"
	else:
		ThemeFile = arg2
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;%s.xpr)'%ThemeFile)
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;%s.xml)'%ThemeFile)
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;%s.ttf)'%ThemeFile)
	if xbmc.getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
		if ThemeFile == "default":
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
	xbmc.executebuiltin("Skin.SetBool(SelectPreviewMode)") # This is set so the preview is shown in the skin settings menu when required.
	Theme_Path = xbmc.translatePath('Special://skin/media')
	Sorted_Theme_Path = [f for f in sorted(os.listdir(Theme_Path)) if f.endswith('.xpr')]
	Sorted_Theme_Path_Files = [os.path.splitext(x)[0].lower().replace('textures','default') for x in Sorted_Theme_Path]
	ThemeFolder = xbmcgui.Dialog().select("Select Theme",Sorted_Theme_Path_Files,10000)
	if ThemeFolder == -1:
		pass
	else:
		ThemeFile = sorted(os.listdir(Theme_Path))[ThemeFolder]
		ThemeFile_NoExt = ThemeFile[:-4]
		if ThemeFile_NoExt.lower() == "textures": ThemeFile_NoExt = "default"
		xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;%s.xpr)'%ThemeFile_NoExt)
		xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;%s.xml)'%ThemeFile_NoExt)
		xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;%s.ttf)'%ThemeFile_NoExt)
		if xbmc.getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
			if ThemeFile_NoExt == "default":
				if os.path.isfile('Special://skin/extras/themes/playlists/default.m3u'):
					xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/default.m3u)')
				elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
					xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
				else:
					xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
			else:
				if os.path.isfile('Special://skin/extras/themes/playlists/'+ThemeFile_NoExt+'.m3u'): xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/'+ThemeFile_NoExt+'.m3u)')
		else:
			if os.path.isfile('Special://profile/playlists/music/random.m3u'):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
			else:
				xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
		xbmc.executebuiltin('ReloadSkin')
	xbmc.executebuiltin("Skin.Reset(SelectPreviewMode)") # This is reset so the preview isn't shown in the skin settings menu when not required.
if arg1 == 'random':
	Random_Theme = random.choice(os.listdir('Special://skin/media/'))
	if Random_Theme.lower() == "textures.xpr":
		ThemeFile = 'default'
	else:
		ThemeFile = Random_Theme[:-4]
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;%s.xpr)'%ThemeFile)
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;%s.xml)'%ThemeFile)
	xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;%s.ttf)'%ThemeFile)
	if xbmc.getCondVisibility('Skin.HasSetting(usethemeplaylist)'):
		if ThemeFile == "default":
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