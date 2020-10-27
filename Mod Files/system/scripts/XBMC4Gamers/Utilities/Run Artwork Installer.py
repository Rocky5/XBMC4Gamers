import os,xbmc,xbmcgui
path_file = 'E:\\UDATA\\09999993\\location.bin'
dialog = xbmcgui.Dialog()
if os.path.isfile(path_file):
	with open(path_file,'r') as input:
		artwork_path = input.readline().strip()
		if os.path.isfile(artwork_path+'default.xbe'):
			xbmc.executebuiltin('RunScript('+artwork_path+'system\\scripts\\default.py,0,'+artwork_path+'settings.ini)')
		else:
			dialog.ok('uh-oh','','Please download and run the[CR]"Xbox Artwork Installer" application.','')
else:
	dialog.ok('uh-oh','','Please download and run the[CR]"Xbox Artwork Installer" application.','')