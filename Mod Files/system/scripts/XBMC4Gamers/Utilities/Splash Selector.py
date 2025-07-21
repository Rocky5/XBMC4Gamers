# -*- coding: utf-8 -*-
from glob import glob
from os.path import basename, isfile, join
from os import remove
from shutil import copyfile
from xbmc import executebuiltin, getLocalizedString, translatePath
from xbmcgui import Dialog

FILE_OUT = 'Q:/custom_splash.png'
SPLASH_PATH = translatePath('Special://skin/extras/themes/splashes/')
SELECT_IMAGE_PROMPT = 'Select your image'
OVERRIDE_SPLASH_PROMPT = 'Select Override Splash'
REMOVE_CUSTOM_SPLASH = 'Remove custom splash'
SELECT_IMAGE_FILE = 'Select image file'

def main():
	dialog = Dialog()
	
	executebuiltin('Skin.SetBool(SelectPreviewMode)')
	executebuiltin('Skin.SetBool(SelectSplash)')

	filter_xpr = sorted([x.lower() for x in glob(translatePath('Special://skin/media/*.xpr'))])
	filter_xpr = [SELECT_IMAGE_FILE] + filter_xpr

	if isfile(FILE_OUT):
		filter_xpr = [REMOVE_CUSTOM_SPLASH] + filter_xpr

	filter_xpr = [basename(x).replace(".xpr", "").upper() for x in filter_xpr]
	filter_xpr.remove('TEXTURES')

	theme_folder = dialog.select(OVERRIDE_SPLASH_PROMPT, filter_xpr, 10000)

	if theme_folder == -1:
		return

	selected_theme = filter_xpr[theme_folder]
	file_in = join(SPLASH_PATH, selected_theme + '.png')
	thumb_in = join(SPLASH_PATH, 'thumbs', selected_theme + '.jpg')
	thumb_out = join(SPLASH_PATH, 'thumbs', REMOVE_CUSTOM_SPLASH + '.jpg')

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
		if isfile(FILE_OUT):
			if dialog.yesno(selected_theme + label2, '', "This will " + label, '', getLocalizedString(106), getLocalizedString(107)):
				if selected_theme.lower() == REMOVE_CUSTOM_SPLASH.lower():
					remove_files(FILE_OUT, thumb_out)
				elif isfile(file_in):
					copy_files(file_in, FILE_OUT, thumb_in, thumb_out)
		elif isfile(file_in):
			copy_files(file_in, FILE_OUT, thumb_in, thumb_out)

	executebuiltin('Skin.Reset(SelectSplash)')
	executebuiltin('Skin.Reset(SelectPreviewMode)')

def copy_files(src, dst, thumb_src, thumb_dst, dialog=None, label=None):
	try:
		if isfile(dst):
			if dialog and label:
				if dialog.yesno(basename(src), '', "This will " + label, '', getLocalizedString(106), getLocalizedString(107)):
					copyfile(src, dst)
					try:
						copyfile(thumb_src, thumb_dst)
					except:
						pass
			else:
				copyfile(src, dst)
				try:
					copyfile(thumb_src, thumb_dst)
				except:
					pass
		else:
			copyfile(src, dst)
			try:
				copyfile(thumb_src, thumb_dst)
			except:
				pass
	except Exception as error:
		print "Failed to copy files: {}".format(error)

def remove_files(file_out, thumb_out):
	try:
		remove(file_out)
		try:
			remove(thumb_out)
		except:
			pass
	except Exception as error:
		print "Failed to remove files: {}".format(error)

if __name__ == "__main__":
	# Close the script loading dialog
	executebuiltin('Dialog.Close(1100,true)')
	main()