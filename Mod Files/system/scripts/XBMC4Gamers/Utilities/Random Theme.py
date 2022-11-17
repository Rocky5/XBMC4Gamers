import os,random,time,xbmc,xbmcgui

if xbmc.getCondVisibility('Skin.HasSetting(randomthemedl)'):
	File_List = os.listdir('Special://skin/media/')
	if 'night.xpr' in File_List: File_List.remove('night.xpr')
	if 'Textures.xpr' in File_List: File_List.remove('Textures.xpr')
	if 'textures.xpr' in File_List: File_List.remove('textures.xpr')
	Random_Theme = random.choice(File_List)
else:
	Random_Theme = random.choice(os.listdir('Special://skin/media/'))

if Random_Theme.lower() == "textures.xpr":
	ThemeFile = 'default'
	ThemeColorFile = "defaults"
else:
	ThemeFile = Random_Theme[:-4]
	ThemeColorFile= ThemeFile

# Randomise the wallpaper for the theme.
if xbmc.getCondVisibility('Skin.HasSetting(randomthemewallpaper)'):
	xbmc.executebuiltin('Skin.SetString(Background_Color,backgrounds/'+str(random.randint(1,15))+'.jpg)')
	xbmc.executebuiltin('Skin.Reset(Background_Image)')
	xbmc.executebuiltin('Skin.Reset(Background_Custom_Color)')

# Check if it's a v1.4_ Gamers theme.
with open(os.path.join(xbmc.translatePath('Special://skin/colors'),ThemeColorFile+".xml")) as test_theme:
	if "XBMC4Gamers v1.4+" in test_theme.read():
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
				if os.path.isfile('Special://skin/extras/themes/playlists/%s.m3u'%ThemeFile):
					xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/%s.m3u)'%ThemeFile)
				elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
					xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
				else:
					xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
		else:
			if os.path.isfile('Special://profile/playlists/music/random.m3u'):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
			else:
				xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
		
		# This is used to show the splash and reload the skin.
		time.sleep(.5) # Delay so the splash window has time to load up
		
		if not xbmc.getCondVisibility('Skin.HasSetting(introenabled)'):
			if os.path.isfile('Special://skin/extras/themes/splashes/%s.png'%ThemeFile):
				xbmc.executebuiltin('ShowPicture(Special://skin/extras/themes/splashes/%s.png)'%ThemeFile)
				time.sleep(3)
			else:
				xbmc.executebuiltin('ShowPicture(Special://root/splash.png)')
				time.sleep(3)
				
		xbmc.executebuiltin('ReloadSkin')
		xbmc.executebuiltin('ActivateWindow(2999)')
	else:
		# Rerun till we find a working theme.
		print "| Didn't work, trying again. " + ThemeFile
		xbmc.executebuiltin('RunScript(Special://root/system/scripts/XBMC4Gamers/Utilities/Random Theme.py)')