import glob
import os
import shutil
import xbmc
import xbmcgui

def main():
	dialog = xbmcgui.Dialog()
	file_out = 'Q:/custom_splash.png'

	xbmc.executebuiltin('Skin.SetBool(SelectPreviewMode)')
	xbmc.executebuiltin('Skin.SetBool(SelectSplash)')

	filter_xpr = sorted([x.lower() for x in glob.glob(xbmc.translatePath('Special://skin/media/*.xpr'))])
	filter_xpr = ['Select image file'] + filter_xpr
	if os.path.isfile(file_out):
		filter_xpr = ['Remove custom splash'] + filter_xpr
	filter_xpr = [os.path.basename(x.replace(".xpr", "").title()) for x in filter_xpr]
	filter_xpr.remove('Textures')
	theme_folder = dialog.select('Select Override Splash', filter_xpr, 10000)

	if theme_folder == -1:
		return

	selected_theme = filter_xpr[theme_folder]
	file_in = xbmc.translatePath('Special://skin/extras/themes/splashes/') + selected_theme + '.png'
	thumb_in = xbmc.translatePath('Special://skin/extras/themes/splashes/thumbs/') + selected_theme + '.jpg'
	thumb_out = xbmc.translatePath('Special://skin/extras/themes/splashes/thumbs/Remove custom splash.jpg')

	if selected_theme.lower() == 'remove custom splash':
		label = "remove the custom_splash.png file."
		label2 = ""
	else:
		label = "overwrite the existing custom_splash.png file."
		label2 = " Theme Splash"

	if selected_theme.lower() == 'select image file':
		theme_image = dialog.browse(2, 'Select your image', "files")
		thumb_in = theme_image
		if theme_image:
			if os.path.isfile(file_out):
				if dialog.yesno(os.path.basename(theme_image), "This will " + label,'','',xbmc.getLocalizedString(106),xbmc.getLocalizedString(107)):
					shutil.copyfile(theme_image, file_out)
					try:
						shutil.copyfile(thumb_in, thumb_out)
					except: pass
			else:
				shutil.copyfile(theme_image, file_out)
				try:
					shutil.copyfile(thumb_in, thumb_out)
				except: pass
	else:
		if os.path.isfile(file_out):
			if dialog.yesno(selected_theme + label2, "This will " + label,'','',xbmc.getLocalizedString(106),xbmc.getLocalizedString(107)):
				if selected_theme.lower() == 'remove custom splash':
					os.remove(file_out)
					try:
						os.remove(thumb_out)
					except: pass
				elif os.path.isfile(file_in):
					shutil.copyfile(file_in, file_out)
					try:
						shutil.copyfile(thumb_in, thumb_out)
					except: pass
		elif os.path.isfile(file_in):
			shutil.copyfile(file_in, file_out)
			try:
				shutil.copyfile(thumb_in, thumb_out)
			except: pass

	xbmc.executebuiltin('Skin.Reset(SelectSplash)')
	xbmc.executebuiltin('Skin.Reset(SelectPreviewMode)')

if __name__ == "__main__":
	main()
