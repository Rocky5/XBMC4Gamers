'''
	Script by Rocky5
'''
import binascii, io, os, shutil, struct, sys, time, xbmcgui, zipfile, glob
from shutil import copyfile
from struct import unpack
from xbe import *
from xbeinfo import *
print "| Scripts\XBMC4Gamers Extras\\480p Game Loaders\resources\\lib\uninstall.py loaded."
Working_Directory	= os.getcwd()+"\\"
pDialog				= xbmcgui.DialogProgress()
dialog				= xbmcgui.Dialog()
pDialog.update(0)
try:
	Select		= sys.argv[1]
	RollBack	= 1
except:
	Select		= 0
	RollBack	= 0
if Select == 0:
	Select = dialog.yesno("Uninstaller","Note:","Auto Uninstaller uninstalls loaders from [CR]E:\Games\, F:\Games\ & G:\Games","","Manual","Auto")
Cleaned	= ""
Install	= ""
if Select:
	Game_Directories 	= [ "E:\\Games\\", "F:\\Games\\", "G:\\Games\\" ]
	for Game_Directories in Game_Directories:
		CountList = 1
		if os.path.isdir(Game_Directories):
			for Items in sorted(os.listdir(Game_Directories)):
				if os.path.isdir(os.path.join(Game_Directories, Items)):
					Game_Path = os.path.join(Game_Directories, Items)+"\\"
					if os.path.isdir(Game_Path):
						XBEFiles = glob.glob(os.path.join(Game_Path, "default.xbe"))
						for Default in XBEFiles:
							if os.path.isfile(Default):
								try:
									if os.path.isfile(os.path.join(Game_Path, "default.xbe")) and os.path.isfile(os.path.join(Game_Path, "game_default.xbe")):
										if CountList == 1: pDialog.create("Uninstaller","","Please wait...")
										if RollBack == 1:
											pDialog.update((CountList * 100) / len(os.listdir(Game_Directories)),"","Rolling back changes.")
										else:
											pDialog.update((CountList * 100) / len(os.listdir(Game_Directories)),"Uninstalling Game loaders",Items)
										CountList = CountList+1
										Cleaned = "True"
										if os.path.isdir(os.path.join(Game_Path, "480loadr")): shutil.rmtree(os.path.join(Game_Path, "480loadr"))
										if os.path.isdir(os.path.join(Game_Path, "skin")): shutil.rmtree(os.path.join(Game_Path, "skin"))
										if os.path.isfile(os.path.join(Game_Path, "evox.ini")): os.remove(os.path.join(Game_Path, "evox.ini"))
										if os.path.isfile(os.path.join(Game_Path, "default.xbe")): os.remove(os.path.join(Game_Path, "default.xbe"))
										if os.path.isfile(os.path.join(Game_Path, "loader_default.xbe")): os.remove(os.path.join(Game_Path, "loader_default.xbe"))
										os.rename(os.path.join(Game_Path, "game_default.xbe"), os.path.join(Game_Path, "default.xbe"))
									elif os.path.isfile(os.path.join(Game_Path, "loader_default.xbe")): 
										os.remove(os.path.join(Game_Path, "loader_default.xbe"))
								except:
									pass
else:
	Game_Path	= dialog.browse(0,"Select a folder","files")
	CountList = 1
	if not Game_Path == "":
		if os.path.isdir(Game_Path):
			try:
				if os.path.isfile(os.path.join(Game_Path, "default.xbe")) and os.path.isfile(os.path.join(Game_Path, "game_default.xbe")):
					Game_Title	= XBE(os.path.join(Game_Path, "game_default.xbe")).Get_title()
					if CountList == 1: pDialog.create("Uninstaller","","Please wait...")
					pDialog.update((CountList * 100) / len(os.listdir(Game_Path)),"Uninstalling Game loader")
					CountList = CountList+1
					Cleaned = "True"
					if os.path.isdir(os.path.join(Game_Path, "480loadr")): shutil.rmtree(os.path.join(Game_Path, "480loadr"))
					if os.path.isdir(os.path.join(Game_Path, "skin")): shutil.rmtree(os.path.join(Game_Path, "skin"))
					if os.path.isfile(os.path.join(Game_Path, "evox.ini")): os.remove(os.path.join(Game_Path, "evox.ini"))
					if os.path.isfile(os.path.join(Game_Path, "default.xbe")): os.remove(os.path.join(Game_Path, "default.xbe"))
					if os.path.isfile(os.path.join(Game_Path, "loader_default.xbe")): os.remove(os.path.join(Game_Path, "loader_default.xbe"))
					os.rename(os.path.join(Game_Path, "game_default.xbe"), os.path.join(Game_Path, "default.xbe"))
				elif os.path.isfile(os.path.join(Game_Path, "loader_default.xbe")): 
					os.remove(os.path.join(Game_Path, "loader_default.xbe"))
			except:
				pass
pDialog.close()										
if Cleaned == "True" and Select == 1: dialog.ok("Uninstaller","","All loaders have been uninstalled.")
if Cleaned == "True" and Select == 0: dialog.ok("Uninstaller","","Loader for [B]"+Game_Title+"[/B] uninstalled.")
if RollBack == 1: dialog.ok("Uninstaller","","Roll back complete.")
if Install == "" and Cleaned == "" and not Game_Path == "": dialog.ok("Error","","No games needing cleaned.")