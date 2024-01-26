import glob,os,shutil,xbmc,xbmcgui
dialog = xbmcgui.Dialog()
FileOut = 'Q:/custom_splash.png'

xbmc.executebuiltin('Skin.SetBool(SelectPreviewMode)') # This is set so the preview is shown in the skin settings menu when required.
xbmc.executebuiltin('Skin.SetBool(SelectSplash)')

Filter_XPR = sorted([x.lower() for x in glob.glob(xbmc.translatePath('Special://skin/media/*.xpr'))], key=None, reverse=0)
Filter_XPR = ['Select image file']+Filter_XPR
if os.path.isfile(FileOut): Filter_XPR = ['Remove custom splash']+Filter_XPR
Filter_XPR = [os.path.basename(x.replace(".xpr","").title()) for x in Filter_XPR]
Filter_XPR.remove('Textures')
ThemeFolder = dialog.select('Select Override Splash',Filter_XPR,10000)

if ThemeFolder == -1:
	pass
else:
	SelectedTheme = Filter_XPR[ThemeFolder]
	FileIn = xbmc.translatePath('Special://skin/extras/themes/splashes/')+SelectedTheme+'.png'

	if SelectedTheme.lower() == 'remove custom splash':
		Label = "remove the custom_splash.png file."
	else:
		Label = "overwrite the existing custom_splash.png file."

	if SelectedTheme.lower() == 'select image file':
		ThemeImage = dialog.browse(2, 'Select your image', "files")
		if not ThemeImage == "":
			
			if os.path.isfile('Q:/custom_splash.png'): 
				if dialog.yesno(os.path.basename(ThemeImage),"This will "+Label):
					shutil.copy2(ThemeImage,FileOut)
			else:
				shutil.copy2(ThemeImage,FileOut)
	
	
	else:
		if os.path.isfile(FileOut):
			if dialog.yesno(SelectedTheme+" Theme Splash","This will "+Label):
				if SelectedTheme.lower() == 'remove custom splash':
					os.remove(FileOut)
				else:
					if os.path.isfile(FileIn):
						shutil.copy2(FileIn,FileOut)
		else:
			if os.path.isfile(FileIn):
				shutil.copy2(FileIn,FileOut)

xbmc.executebuiltin('Skin.Reset(SelectSplash)')
xbmc.executebuiltin('Skin.Reset(SelectPreviewMode)') # This is reset so the preview isn't shown in the skin settings menu when not required.