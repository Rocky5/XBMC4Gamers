'''
	Script by Rocky5
'''
import binascii, io, os, shutil, struct, sys, time, xbmcgui, zipfile, glob
from shutil import copyfile
from struct import unpack
from xbe import *
from xbeinfo import *

print "| Scripts\XBMC4Gamers Extras\\480p Game Loaders\resources\\lib\uninstall.py loaded."

def cleanup_game_directory(Game_Path):
	files_to_remove = [
		"default.xbe",
		"evox.ini",
		"loader_default.xbe",
	]

	for filename in files_to_remove:
		file_path = os.path.join(Game_Path, filename)
		if os.path.isfile(file_path):
			os.remove(file_path)

	# Remove specific directories
	for dir_name in ["480loadr", "skin"]:
		dir_path = os.path.join(Game_Path, dir_name)
		if os.path.isdir(dir_path):
			shutil.rmtree(dir_path)

	# Rename game_default.xbe to default.xbe if both files exist
	game_default_path = os.path.join(Game_Path, "game_default.xbe")
	default_path = os.path.join(Game_Path, "default.xbe")
	if os.path.isfile(game_default_path) and not os.path.isfile(default_path):
		os.rename(game_default_path, default_path)

Working_Directory	= os.getcwd()+"\\"
pDialog				= xbmcgui.DialogProgress()
dialog				= xbmcgui.Dialog()
Cleaned	= ""
Cancelled = ""

try:
	Select		= sys.argv[1]
	RollBack	= 1
except:
	Select		= 0
	RollBack	= 0
	
if Select == 0:
	Select = dialog.yesno("Uninstaller","Note:","Auto Uninstaller uninstalls loaders from [CR]E:\Games\, F:\Games\ & G:\Games","","Manual","Auto")

pDialog.update(0)

if Select:
	Game_Directories 	= [ "E:\\Games\\", "F:\\Games\\", "G:\\Games\\" ]
	for Game_Directories in Game_Directories:
		CountList = 1
		pDialog.create("Uninstaller","","Please wait...")
		if os.path.isdir(Game_Directories):
			for Items in sorted(os.listdir(Game_Directories)):
				if not pDialog.iscanceled():
					if os.path.isdir(os.path.join(Game_Directories, Items)):
						Game_Path = os.path.join(Game_Directories, Items)+"\\"
						XBEFiles = glob.glob(os.path.join(Game_Path, "default.xbe"))
						try:
							pDialog.update((CountList * 100) / len(os.listdir(Game_Directories)),"Checking for Game loaders",Items)
							CountList = CountList+1
							if os.path.isfile(os.path.join(Game_Path, "default.xbe")) and os.path.isfile(os.path.join(Game_Path, "game_default.xbe")):
								if RollBack == 1:
									pDialog.update((CountList * 100) / len(os.listdir(Game_Directories)),"Rolling back",Items)
									time.sleep(0.5)
								else:
									pDialog.update((CountList * 100) / len(os.listdir(Game_Directories)),"Uninstalling loader",Items)
									time.sleep(0.5)
								Cleaned = "True"
								cleanup_game_directory(Game_Path)
							else:
								if os.path.isfile(os.path.join(Game_Path, "loader_default.xbe")):
									os.remove(os.path.join(Game_Path, "loader_default.xbe"))
						except:
							pass
				else:
					Cancelled = "True"
					pass
else:
	Game_Path	= dialog.browse(0,"Select a folder","files")
	CountList = 1
	if not Game_Path == "":
		if os.path.isdir(Game_Path):
			try:
				if os.path.isfile(os.path.join(Game_Path, "default.xbe")) and os.path.isfile(os.path.join(Game_Path, "game_default.xbe")):
					Game_Title	= XBE(os.path.join(Game_Path, "game_default.xbe")).Get_title()
					if CountList == 1:
						pDialog.create("Uninstaller","","Please wait...")
					pDialog.update((CountList * 100) / len(os.listdir(Game_Path)),"Uninstalling loader")
					CountList = CountList+1
					Cleaned = "True"
					cleanup_game_directory(Game_Path)
				elif os.path.isfile(os.path.join(Game_Path, "loader_default.xbe")):
					os.remove(os.path.join(Game_Path, "loader_default.xbe"))
			except:
				pass
pDialog.close()										
if Cleaned == "True" and Cancelled == "":
	if Select == 1:
		dialog.ok("Uninstaller","","All loaders have been uninstalled.")
	else:
		dialog.ok("Uninstaller","","Loader for [B]"+Game_Title+"[/B] uninstalled.")

if Cancelled == "True":
	if Select == 1:
		dialog.ok("Uninstaller","","Uninstall cancelled.")
	elif RollBack == 1:
		dialog.ok("Uninstaller","","Roll back cancelled.")

if Cancelled == "" and RollBack == 1:
	dialog.ok("Uninstaller","","Roll back complete.")

if Cleaned == "" and Cancelled == "":
	dialog.ok("Error","","No games needed cleaned.")
