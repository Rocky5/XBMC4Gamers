# -*- coding: utf-8 -*-
import glob
import os
import shutil
import xbmc
import xbmcgui

FILE_OUT = 'Q:/custom_splash.png'
SKIN_PATH = xbmc.translatePath
SELECT_IMAGE_PROMPT = 'Select your image'
OVERRIDE_SPLASH_PROMPT = 'Select Override Splash'
REMOVE_CUSTOM_SPLASH = 'Remove custom splash'
SELECT_IMAGE_FILE = 'Select image file'

def main():
	dialog = xbmcgui.Dialog()
	
	xbmc.executebuiltin('Skin.SetBool(SelectPreviewMode)')
	xbmc.executebuiltin('Skin.SetBool(SelectSplash)')

	filter_xpr = sorted([x.lower() for x in glob.glob(SKIN_PATH('Special://skin/media/*.xpr'))])
	filter_xpr = [SELECT_IMAGE_FILE] + filter_xpr

	if os.path.isfile(FILE_OUT):
		filter_xpr = [REMOVE_CUSTOM_SPLASH] + filter_xpr

	filter_xpr = [os.path.basename(x).replace(".xpr", "").title() for x in filter_xpr]
	filter_xpr.remove('Textures')

	theme_folder = dialog.select(OVERRIDE_SPLASH_PROMPT, filter_xpr, 10000)

	if theme_folder == -1:
		return

	selected_theme = filter_xpr[theme_folder]
	file_in = os.path.join(SKIN_PATH('Special://skin/extras/themes/splashes/'), selected_theme + '.png')
	thumb_in = os.path.join(SKIN_PATH('Special://skin/extras/themes/splashes/thumbs/'), selected_theme + '.jpg')
	thumb_out = os.path.join(SKIN_PATH('Special://skin/extras/themes/splashes/thumbs/'), REMOVE_CUSTOM_SPLASH + '.jpg')

	if selected_theme.lower() == REMOVE_CUSTOM_SPLASH.lower():
		label = "remove the custom_splash.png file."
		label2 = ""
	else:
		label = "overwrite the existing custom_splash.png file."
		label2 = " Theme Splash"

	if selected_theme.lower() == SELECT_IMAGE_FILE.lower():
		theme_image = dialog.browse(2, SELECT_IMAGE_PROMPT, "files")
		thumb_in = theme_image
		if theme_image:
			copy_files(theme_image, FILE_OUT, thumb_in, thumb_out, dialog, label)
	else:
		if os.path.isfile(FILE_OUT):
			if dialog.yesno(selected_theme + label2, "This will " + label, '', '', xbmc.getLocalizedString(106), xbmc.getLocalizedString(107)):
				if selected_theme.lower() == REMOVE_CUSTOM_SPLASH.lower():
					remove_files(FILE_OUT, thumb_out)
				elif os.path.isfile(file_in):
					copy_files(file_in, FILE_OUT, thumb_in, thumb_out)
		elif os.path.isfile(file_in):
			copy_files(file_in, FILE_OUT, thumb_in, thumb_out)

	xbmc.executebuiltin('Skin.Reset(SelectSplash)')
	xbmc.executebuiltin('Skin.Reset(SelectPreviewMode)')

def copy_files(src, dst, thumb_src, thumb_dst, dialog=None, label=None):
	try:
		if os.path.isfile(dst):
			if dialog and label:
				if dialog.yesno(os.path.basename(src), "This will " + label, '', '', xbmc.getLocalizedString(106), xbmc.getLocalizedString(107)):
					shutil.copyfile(src, dst)
					try:
						shutil.copyfile(thumb_src, thumb_dst)
					except:
						pass
			else:
				shutil.copyfile(src, dst)
				try:
					shutil.copyfile(thumb_src, thumb_dst)
				except:
					pass
		else:
			shutil.copyfile(src, dst)
			try:
				shutil.copyfile(thumb_src, thumb_dst)
			except:
				pass
	except Exception as error:
		xbmc.log("Failed to copy files: {}".format(error), xbmc.LOGERROR)

def remove_files(file_out, thumb_out):
	try:
		os.remove(file_out)
		try:
			os.remove(thumb_out)
		except:
			pass
	except Exception as error:
		xbmc.log("Failed to remove files: {}".format(error), xbmc.LOGERROR)

if __name__ == "__main__":
	xbmc.executebuiltin('Dialog.Close(1100,false)')
	main()