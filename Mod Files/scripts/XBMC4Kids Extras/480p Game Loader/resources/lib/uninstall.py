'''
	Script by Rocky5
'''


import binascii, io, os, shutil, struct, sys, time, xbmcgui, zipfile, glob
from shutil import copyfile
from struct import unpack
from xbe import *
from xbeinfo import *
			
			
#####	Start markings for the log file.
print "================================================================================"
print "| Scripts\\480p Game Loader\resources\\lib\uninstall.py loaded."
print "| ------------------------------------------------------------------------------"

		
Working_Directory	= os.getcwd() + "\\"
pDialog				= xbmcgui.DialogProgress()
dialog				= xbmcgui.Dialog()
pDialog.update( 0 )


try:
	Select		= sys.argv[1]
	RollBack	= 1
except:
	Select		= 0
	RollBack	= 0

if Select == 0:
	Select = dialog.yesno( "Unisntaller","","Would you like to use the Auto Uninstall?","Note: Auto mode uninstalls loaders from E,F & G:\Games" )
Cleaned	= ""
Install	= ""

if Select:
	Game_Directories 	= [ "E:\\Games\\", "F:\\Games\\", "G:\\Games\\" ]
	for Game_Directories in Game_Directories:
		CountList = 1
		if os.path.isdir( Game_Directories ):
			for Items in sorted( os.listdir( Game_Directories ) ):
				if os.path.isdir(os.path.join( Game_Directories, Items)):
					Game_Path = os.path.join( Game_Directories, Items ) + "\\"
					if os.path.isdir( Game_Path ):
						XBEFiles = glob.glob( os.path.join( Game_Path, "default.xbe" ) )
						for Default in XBEFiles:
							if os.path.isfile( Default ):
								try:
									if os.path.isfile( Game_Path + "game_default.xbe" ):
										if CountList == 1: pDialog.create( "Unisntaller","","Please wait..." )
										if RollBack == 1:
											pDialog.update( ( CountList * 100 ) / len( os.listdir( Game_Directories ) ),"","Rolling back changes." )
										else:
											pDialog.update( ( CountList * 100 ) / len( os.listdir( Game_Directories ) ),"Uninstalling Game loaders",Items )
										CountList = CountList + 1
										Cleaned = "True"
										if os.path.isdir( Game_Path + "cdxmedia" ): shutil.rmtree( Game_Path + "cdxmedia" )
										if os.path.isdir( Game_Path + "skin" ): shutil.rmtree( Game_Path + "skin" )
										if os.path.isfile( Game_Path + "default.tbn" ): os.remove( Game_Path + "default.tbn" )
										if os.path.isfile( Game_Path + "icon.png" ): os.remove( Game_Path + "icon.png" )
										if os.path.isfile( Game_Path + "default.xbe" ): os.remove( Game_Path + "default.xbe" )
										if os.path.isfile( Game_Path + "evox.ini" ): os.remove( Game_Path + "evox.ini" )
										if os.path.isfile( Game_Path + "cdxmedia_cdx.xsb" ): os.remove( Game_Path + "cdxmedia_cdx.xsb" ) 
										if os.path.isfile( Game_Path + "cdxmedia_cdx.xpr" ): os.remove( Game_Path + "cdxmedia_cdx.xpr" )
										if os.path.isfile( Game_Path + "cdxmedia_cdx.inx" ): os.remove( Game_Path + "cdxmedia_cdx.inx" ) 
										if os.path.isfile( Game_Path + "cdxmedia_ArialUni.ttf" ): os.remove( Game_Path + "cdxmedia_ArialUni.ttf" )
										if os.path.isfile( Game_Path + "loader_default.xbe" ): os.remove( Game_Path + "loader_default.xbe" )
										os.rename( Game_Path + "game_default.xbe",Game_Path + "default.xbe" )
									elif os.path.isfile( Game_Path + "loader_default.xbe" ): 
										if os.path.isfile( Game_Path + "loader_default.xbe" ): os.remove( Game_Path + "loader_default.xbe" )
								except:
									pass
else:
	Game_Path	= dialog.browse( 0,"Select a folder","files" )
	CountList = 1
	if not Game_Path == "":
		if os.path.isdir( Game_Path ):
			try:
				if os.path.isfile( Game_Path + "game_default.xbe" ):
					Game_Title	= XBE( Game_Path + "game_default.xbe" ).Get_title()
					if CountList == 1: pDialog.create( "Unisntaller","","Please wait..." )
					pDialog.update( ( CountList * 100 ) / len( os.listdir( Game_Path ) ),"Uninstalling Game loaders",Items )
					CountList = CountList + 1
					Cleaned = "True"
					if os.path.isdir( Game_Path + "cdxmedia" ): shutil.rmtree( Game_Path + "cdxmedia" )
					if os.path.isdir( Game_Path + "skin" ): shutil.rmtree( Game_Path + "skin" )
					if os.path.isfile( Game_Path + "default.tbn" ): os.remove( Game_Path + "default.tbn" )
					if os.path.isfile( Game_Path + "icon.png" ): os.remove( Game_Path + "icon.png" )
					if os.path.isfile( Game_Path + "default.xbe" ): os.remove( Game_Path + "default.xbe" )
					if os.path.isfile( Game_Path + "evox.ini" ): os.remove( Game_Path + "evox.ini" )
					if os.path.isfile( Game_Path + "cdxmedia_cdx.xsb" ): os.remove( Game_Path + "cdxmedia_cdx.xsb" ) 
					if os.path.isfile( Game_Path + "cdxmedia_cdx.xpr" ): os.remove( Game_Path + "cdxmedia_cdx.xpr" )
					if os.path.isfile( Game_Path + "cdxmedia_cdx.inx" ): os.remove( Game_Path + "cdxmedia_cdx.inx" ) 
					if os.path.isfile( Game_Path + "cdxmedia_ArialUni.ttf" ): os.remove( Game_Path + "cdxmedia_ArialUni.ttf" )
					if os.path.isfile( Game_Path + "loader_default.xbe" ): os.remove( Game_Path + "loader_default.xbe" )
					os.rename( Game_Path + "game_default.xbe",Game_Path + "default.xbe" )
				elif os.path.isfile( Game_Path + "loader_default.xbe" ): 
					if os.path.isfile( Game_Path + "loader_default.xbe" ): os.remove( Game_Path + "loader_default.xbe" )
			except:
				pass

pDialog.close()										
if Cleaned == "True" and Select == 1: dialog.ok( "Unisntaller","","All loaders have been uninstalled." )
if Cleaned == "True" and Select == 0: dialog.ok( "Unisntaller","","Loader for [B]" + Game_Title + "[/B] uninstalled." )
if Install == "" and Cleaned == "" and not Game_Path == "": dialog.ok( "Error","","No games needing cleaned." )

print "================================================================================"