import glob,os,shutil,sys,time,xbmc,xbmcgui
xbmc.executebuiltin("Skin.SetBool(SelectPreviewMode)") # This is set so the preview is shown in the skin settings menu when required.
TMP_Theme_Path = 'Z:/temp/themes/'
XPR = glob.glob('Q:/skins/profile skin/media/*.xpr')
Filter_XPR = [os.path.basename(r.lower()) for r in XPR if not "textures.xpr" in r.lower() and not "night.xpr" in r.lower()]
if not os.path.isdir(TMP_Theme_Path): os.makedirs(TMP_Theme_Path)
try:
	for fn in Filter_XPR:
		with open(os.path.join(TMP_Theme_Path,fn),"w") as ThemeFiles:
			ThemeFiles.write('')
except: pass
if len(os.listdir(TMP_Theme_Path)) > 0:
	XPR = glob.glob(TMP_Theme_Path+'\\*.xpr')
	Filter_XPR = [os.path.basename(r[0:-4]) for r in XPR]
	ThemeFolder = xbmcgui.Dialog().select("Uninstall Theme",Filter_XPR,10000)
	if ThemeFolder == -1:
		pass
	else:
		Theme = sorted(os.listdir(TMP_Theme_Path))[ThemeFolder][0:-4]
		if xbmc.getCondVisibility('StringCompare(Skin.CurrentTheme,'+Theme+')'):
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skintheme;default.xpr)')
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.skincolors;default.xml)')
			xbmc.executehttpapi('SetGUISetting(3;lookandfeel.font;default.ttf)')
			xbmcgui.Dialog().ok('Done','Theme Uninstalled.','')
			xbmc.executebuiltin('ReloadSkin')
			time.sleep(2)
		else:
			xbmcgui.Dialog().ok('Done','Theme Uninstalled.','')
		## Colour.xml
		if os.path.isfile('Q:/skins/profile skin/colors/'+Theme+'.xml'): os.remove('Q:/skins/profile skin/colors/'+Theme+'.xml')
		## Playlist
		if os.path.isfile('Q:/skins/profile skin/extras/themes/playlists/'+Theme+'.m3u'): os.remove('Q:/skins/profile skin/extras/themes/playlists/'+Theme+'.m3u')
		if os.path.isdir('Q:/skins/profile skin/extras/themes/playlists/'+Theme):
			xbmc.Player().stop()
			shutil.rmtree('Q:/skins/profile skin/extras/themes/playlists/'+Theme)
		## Preview
		if os.path.isfile('Q:/skins/profile skin/extras/themes/previews/'+Theme+'.jpg'): os.remove('Q:/skins/profile skin/extras/themes/previews/'+Theme+'.jpg')
		## Splash
		if os.path.isfile('Q:/skins/profile skin/extras/themes/splashes/'+Theme+'.png'): os.remove('Q:/skins/profile skin/extras/themes/splashes/'+Theme+'.png')
		## Font
		if os.path.isfile('Q:/skins/profile skin/fonts/'+Theme+'.ttf'): os.remove('Q:/skins/profile skin/fonts/'+Theme+'.ttf')
		## XPR
		if os.path.isfile('Q:/skins/profile skin/media/'+Theme+'.xpr'): os.remove('Q:/skins/profile skin/media/'+Theme+'.xpr')
		## URLDownloader stuff
		if os.path.isfile('Q:/skins/profile skin/extras/urldownloader themes/previews/'+Theme+'.jpg'): os.remove('Q:/skins/profile skin/extras/urldownloader themes/previews/'+Theme+'.jpg')
		if os.path.isfile('Q:/skins/profile skin/extras/urldownloader themes/XML files/'+Theme+'.xml'): os.remove('Q:/skins/profile skin/extras/urldownloader themes/XML files/'+Theme+'.xml')
		## Set theme playlist or reset to random.
		if os.path.isfile('Special://skin/extras/themes/playlists/default.m3u'):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://skin/extras/themes/playlists/default.m3u)')
		elif os.path.isfile('Special://profile/playlists/music/random.m3u'):
			xbmc.executebuiltin('Skin.SetString(Startup_Playback_Path,Special://profile/playlists/music/random.m3u)')
		else:
			xbmc.executebuiltin('Skin.Reset(Startup_Playback_Path)')
else:
	xbmcgui.Dialog().ok('ERROR','You have no themes installed.','You can download themes from the built in downloader.')
xbmc.executebuiltin("Skin.Reset(SelectPreviewMode)") # This is reset so the preview isn't shown in the skin settings menu when not required.
if os.path.isdir(TMP_Theme_Path): shutil.rmtree(TMP_Theme_Path)