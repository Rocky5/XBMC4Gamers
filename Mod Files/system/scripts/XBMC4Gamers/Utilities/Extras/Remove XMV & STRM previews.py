import os, glob, xbmcgui
dialog = xbmcgui.Dialog()
root_folder = dialog.browse(0,"Select a game folder","files")
for folder in sorted(os.listdir(root_folder)):
	sub_folder = os.path.join(root_folder,folder)
	for _resources in sorted(os.listdir(sub_folder)):
		for xmv in glob.iglob(os.path.join(sub_folder,'_resources\\media\\') + '\\*.xmv'):
			print os.path.join(sub_folder,'_resources\\media\\',xmv)
			os.remove(os.path.join(sub_folder,'_resources\\media\\',xmv))
		for xmv in glob.iglob(os.path.join(sub_folder,'_resources\\media\\') + '\\*.strm'):
			print os.path.join(sub_folder,'_resources\\media\\',xmv)
			os.remove(os.path.join(sub_folder,'_resources\\media\\',xmv))
