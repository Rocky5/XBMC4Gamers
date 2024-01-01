'''
	Script by Rocky5
	Removes empty directories from TDATA and UDATA.
'''
import os, xbmcgui, shutil
Save_Directories		= [ "E:\\TDATA\\", "E:\\UDATA\\" ]
pDialog					= xbmcgui.DialogProgress()
dialog					= xbmcgui.Dialog()
skip					= 0
pDialog.update(0)
pDialog.create("Cleaning Save Folders")
print "| Scripts\XBMC4Gamers Extras\Remove Empty Save Folders\default.py loaded."
for Save_Directories in Save_Directories:
	CountList = 1
	if os.path.isdir(Save_Directories):
		for Save_Dir in sorted(os.listdir(Save_Directories)):
			Save_Path = os.path.join(Save_Directories, Save_Dir)
			if os.path.isdir(Save_Path):
				pDialog.update((CountList * 100) / len(os.listdir(Save_Directories)),"Processing",Save_Directories,Save_Dir)
				try:
					if os.walk(Save_Path).next()[1]:
						print Save_Path+"\\ - skipping"
					else:
						if len(Save_Path) > 0:
							for fname in os.listdir(Save_Path):
								if not fname.endswith('.xbx'):
									print Save_Path+"\\ - skipping"
									skip = 1
									break
						if not skip:
							shutil.rmtree(Save_Path)
							print Save_Path+"\\ - removed"
						else:
							skip = 0
					CountList = CountList+1
				except:
					print Save_Path+"\\ is write protected?"
pDialog.close()
dialog.ok("Cleaning Save Folders","","Process Complete")