import os, xbmc, xbmcgui
dialog	= xbmcgui.Dialog()

Mode = sys.argv[1:][0]
File = sys.argv[2:][0]
if Mode == '0':
	if os.path.isfile(File):
		with open(File,"rb") as input:
			xbmcgui.Dialog().textviewer(os.path.basename(File), input.read())
	else:
		dialog.ok("Error","Cant find changelog.txt")