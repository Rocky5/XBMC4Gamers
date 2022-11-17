import glob,os,shutil,sys,time,xbmc,xbmcgui

xbmc.executebuiltin("Skin.SetBool(SelectPreviewMode)") # This is set so the preview is shown in the skin settings menu when required.
xbmc.executebuiltin('Dialog.Close(1100,true)')
TMP_Theme_Path = 'Z:/temp/themes/'
if os.path.isdir(TMP_Theme_Path):
	shutil.rmtree(TMP_Theme_Path)
os.makedirs(TMP_Theme_Path)
XPR = os.listdir(xbmc.translatePath('Special://skin/media'))
Filter_XPR = [os.path.basename(r.lower()) for r in XPR if not "textures.xpr" in r.lower() and not "night.xpr" in r.lower()]


try:
	for fn in Filter_XPR:
		with open(os.path.join(TMP_Theme_Path,fn.upper()),"w") as ThemeFiles:
			ThemeFiles.write('')
except: pass


if len(os.listdir(TMP_Theme_Path)) > 0:
	XPR = sorted(os.listdir(TMP_Theme_Path))
	Filter_XPR = [os.path.basename(r[0:-4]) for r in XPR]
	ThemeFolder = xbmcgui.Dialog().select("Uninstall Theme",Filter_XPR)
	
	if ThemeFolder == -1:
		pass
	else:
		Theme = XPR[ThemeFolder][0:-4]
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
if os.path.isdir(TMP_Theme_Path): shutil.rmtree(TMP_Theme_Path)