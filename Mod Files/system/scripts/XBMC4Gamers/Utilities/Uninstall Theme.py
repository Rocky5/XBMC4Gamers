import glob,os,shutil,sys,time,xbmc,xbmcgui

xbmc.executebuiltin("Skin.SetBool(SelectPreviewMode)") # This is set so the preview is shown in the skin settings menu when required.
xbmc.executebuiltin('Dialog.Close(1100,true)')

if len(glob.glob(xbmc.translatePath('Special://skin/media/*.xpr'))) > 0:
	Filter_XPR = sorted([os.path.basename(x.lower()) for x in glob.glob(xbmc.translatePath('Special://skin/media/*.xpr'))], key=None, reverse=0)
	Filter_XPR.remove("textures.xpr")
	Filter_XPR.remove("night.xpr")
	Filter_XPR = [os.path.basename(x.replace(".xpr","").title()) for x in Filter_XPR]
	ThemeFolder = xbmcgui.Dialog().select('Select Theme',Filter_XPR,10000)
	
	if ThemeFolder == -1:
		pass
	else:
		Theme = Filter_XPR[ThemeFolder]
		if xbmcgui.Dialog().yesno('Would you like to uninstall',Theme.upper(),'','','No','Yes'):
			
			# Check if current theme is the one you want to uninstall and change to the default theme
			if xbmc.getCondVisibility('StringCompare(Skin.CurrentTheme,'+Theme+')'):
				xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;default.xpr)')
				xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;default.xml)')
				xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;default.ttf)')
				xbmc.executebuiltin('ReloadSkin')
				time.sleep(2)
			
			# Colour.xml
			if os.path.isfile('Q:/skins/profile skin/colors/'+Theme+'.xml'):
				os.remove('Q:/skins/profile skin/colors/'+Theme+'.xml')
			
			# Backgrounds
			if os.path.isdir('Q:/skins/profile skin/backgrounds/'+Theme+''):
				shutil.rmtree('Q:/skins/profile skin/backgrounds/'+Theme+'')
			
			# Playlist
			if os.path.isfile('Q:/skins/profile skin/extras/themes/playlists/'+Theme+'.m3u'):
				os.remove('Q:/skins/profile skin/extras/themes/playlists/'+Theme+'.m3u')
			
			if os.path.isdir('Q:/skins/profile skin/extras/themes/playlists/'+Theme):
				xbmc.Player().stop()
				shutil.rmtree('Q:/skins/profile skin/extras/themes/playlists/'+Theme)
			
			# Preview
			if os.path.isfile('Q:/skins/profile skin/extras/themes/previews/'+Theme+'.jpg'):
				os.remove('Q:/skins/profile skin/extras/themes/previews/'+Theme+'.jpg')
			
			# Splash
			if os.path.isfile('Q:/skins/profile skin/extras/themes/splashes/'+Theme+'.png'):
				os.remove('Q:/skins/profile skin/extras/themes/splashes/'+Theme+'.png')
			if os.path.isfile('Q:/skins/profile skin/extras/themes/splashes/thumbs/'+Theme+'.png'):
				os.remove('Q:/skins/profile skin/extras/themes/splashes/thumbs/'+Theme+'.png')
			
			# Font
			if os.path.isfile('Q:/skins/profile skin/fonts/'+Theme+'.ttf'):
				os.remove('Q:/skins/profile skin/fonts/'+Theme+'.ttf')
			
			# XPR
			if os.path.isfile('Q:/skins/profile skin/media/'+Theme+'.xpr'):
				os.remove('Q:/skins/profile skin/media/'+Theme+'.xpr')
			
			# URLDownloader stuff
			if os.path.isfile('Q:/skins/profile skin/extras/urldownloader themes/previews/'+Theme+'.jpg'):
				os.remove('Q:/skins/profile skin/extras/urldownloader themes/previews/'+Theme+'.jpg')
			
			if os.path.isfile('Q:/skins/profile skin/extras/urldownloader themes/XML files/'+Theme+'.xml'):
				os.remove('Q:/skins/profile skin/extras/urldownloader themes/XML files/'+Theme+'.xml')
			
			# Set theme playlist or reset to random
			if os.path.isfile('Special://skin/extras/themes/playlists/default.m3u'):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/default.m3u)')
			elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
				xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
			else:
				xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
				
			xbmcgui.Dialog().ok('Complete','',Theme+' uninstalled.','')

		else:
			xbmc.executebuiltin('ActivateWindow(1100)')
			time.sleep(1)
			xbmc.executebuiltin('RunScript(Special://root/system/scripts/XBMC4Gamers/Utilities/Uninstall Theme.py)')
else:
	xbmcgui.Dialog().ok('ERROR','You have no themes installed.','You can download themes from the built in downloader.')


xbmc.executebuiltin("Skin.Reset(SelectPreviewMode)") # This is reset so the preview isn't shown in the skin settings menu when not required.