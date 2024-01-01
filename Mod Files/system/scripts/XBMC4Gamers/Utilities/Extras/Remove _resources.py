import os, shutil, xbmcgui
dialog = xbmcgui.Dialog()
root_folder = dialog.browse(0,"Select a folder","files")
for folder in sorted(os.listdir(root_folder)):
	sub_folder = os.path.join(root_folder,folder)
	for _resources in sorted(os.listdir(sub_folder)):
		if os.path.isdir(os.path.join(sub_folder,'_resources\\artwork')):
			shutil.rmtree(os.path.join(sub_folder,'_resources\\artwork'))
		if os.path.isdir(os.path.join(sub_folder,'_resources\\screenshots')):
			shutil.rmtree(os.path.join(sub_folder,'_resources\\screenshots'))
		if os.path.isfile(os.path.join(sub_folder,'_resources\\default.xml')):
			os.remove(os.path.join(sub_folder,'_resources\\default.xml'))
		if os.path.isfile(os.path.join(sub_folder,'default.tbn')):
			os.remove(os.path.join(sub_folder,'default.tbn'))
		if os.path.isfile(os.path.join(sub_folder,'fanart.jpg')):
			os.remove(os.path.join(sub_folder,'fanart.jpg'))
		if os.path.isfile(os.path.join(sub_folder,'icon.jpg')):
			os.remove(os.path.join(sub_folder,'icon.jpg'))
		if os.path.isfile(os.path.join(sub_folder,'icon.png')):
			os.remove(os.path.join(sub_folder,'icon.png'))
dialog.ok("","Done")