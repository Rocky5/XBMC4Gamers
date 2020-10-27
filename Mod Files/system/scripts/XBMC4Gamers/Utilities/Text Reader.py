import os, xbmc, xbmcgui
dialog	= xbmcgui.Dialog()
'''
Mode:
0 = change log.
1 = Browse.
2 = View logs.
'''
Mode = sys.argv[1:][0]
File = sys.argv[2:][0]
if Mode == '0':
	if os.path.isfile(File):
		with open(File,"rb") as input:
			xbmcgui.Dialog().textviewer(os.path.basename(File), input.read())
	else:
		dialog.ok("Error","Cant find changes.txt")
if Mode == '1':
	File = dialog.browse(1,"Select file to view",'files','' )
	Input = os.path.basename(File)
	if os.path.isfile(File):
		with open(File,"rb") as text_viewer:
			xbmcgui.Dialog().textviewer(Input, text_viewer.read())
if Mode == '2':
	Log_Path = 'E:/TDATA/Rocky5 needs these Logs/'
	Select_Root = dialog.select( "Select Log File",sorted(os.listdir(Log_Path)),10000 )
	if Select_Root == -1:
		pass
	else:
		Select_File = os.path.join(Log_Path,sorted(os.listdir(Log_Path))[Select_Root])
		if os.path.isdir(Select_File) and len(os.listdir(Select_File)) > 0:
			Select_Root = dialog.select( "Select Log File",sorted(os.listdir(Select_File)),10000 )
			Select_File = os.path.join(Select_File,sorted(os.listdir(Select_File))[Select_Root])
		else:
			xbmcgui.Dialog().ok("ERROR","There are no logs to be viewed.","","This is a good thing.")
		if Select_Root == -1 or Select_File == -1:
			pass
		else:
			File = Select_File
			Input = os.path.basename(File)
			if os.path.isfile(File):
				with open(File,"rb") as text_viewer:
					xbmcgui.Dialog().textviewer(Input, text_viewer.read())
