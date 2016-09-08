'''
	Script by Rocky5
	Removes empty directories from TDATA and UDATA.
'''

import os, xbmcgui, shutil

Save_Directories		= [ "E:\\TDATA\\", "E:\\UDATA\\" ]
pDialog					= xbmcgui.DialogProgress()
dialog					= xbmcgui.Dialog()
pDialog.update( 0 )
pDialog.create( "Cleaning Save Folders" )

#####	Start markings for the log file.
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\Remove Empty Save Folders.py loaded."
print "| ------------------------------------------------------------------------------"

for Save_Directories in Save_Directories:
	CountList = 1
	if os.path.isdir( Save_Directories ):
		for Save_Dir in sorted( os.listdir( Save_Directories ) ):
			Save_Path = os.path.join( Save_Directories, Save_Dir )
			if os.path.isdir( Save_Path ):
				pDialog.update( ( CountList * 100 ) / len( os.listdir( Save_Directories ) ),"Processing",Save_Directories,Save_Dir )
				try:
					if not os.walk( Save_Path ).next()[1]:
						shutil.rmtree( Save_Path )
						print "Removed " + Save_Path
					else:
						print Save_Path + " is not empty"
						CountList = CountList + 1
				except:
					pass
				
pDialog.close()
dialog.ok( "Cleaning Save Folders","","Process Complete" )
print "================================================================================"