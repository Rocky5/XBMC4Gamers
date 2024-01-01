import os,re,xbmc,xbmcgui
path_file = 'E:\\UDATA\\09999993\\location.bin'
dialog = xbmcgui.Dialog()
arg1 = 0
arg2 = 0
arg3 = 0
if os.path.isfile(path_file):
	with open(path_file,'r') as input:
		artwork_path = input.readline().strip()
		if os.path.isfile(artwork_path+'default.xbe'):
			version = os.path.join(artwork_path+'skins/Default/language/English/strings.po')
			try:
				with open(version, "r") as strings:
					for lines in strings:
						if 'msgid "v' in lines.lower():
							int = re.findall(r'\d+', lines)
					if int >= 30: # version 3.0
						guisettings = os.path.join(artwork_path+'system/userdata/guisettings.xml')
						with open(guisettings, "r") as xml:
							for lines in xml:
								if 'default.skipgames">true<' in lines.lower():
									arg1 = 1
								if 'default.installfanart">true<' in lines.lower():
									arg2 = 1
								if 'default.installvideos">true<' in lines.lower():
									arg3 = 1
						xbmc.executebuiltin('RunScript('+artwork_path+'system\\scripts\\default.py,0,'+str(arg1)+','+str(arg2)+','+str(arg3)+')')
			except:
				dialog.ok('uh-oh','','Something wetn wrong[CR]corrupt file maybe.','')
		else:
			dialog.ok('uh-oh','','Please download and run the[CR]"Xbox Artwork Installer" application.','')
else:
	dialog.ok('uh-oh','','Please download and run the[CR]"Xbox Artwork Installer" application.','')