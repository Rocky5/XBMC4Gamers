# -*- coding: utf-8 -*-
'''
	Script by Rocky5 (original idea headphone)
	Used to create a favourites.xml from all your games.
	Enabled if you want the games directory (ie, E:\Games\, F:\Games\, or G:\Games\) to be used to build the xml.
	You can also enabled the TBN option, this will use the default.tbn files, instead of the cached versions XBMC has made. 
		Use Games+default.tbn  = RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py,1,1)
		Use Games+cached tbn   = RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py,1,0)
		Use MyPrograms6.db     = RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py,0,0)
		Use MyPrograms6.db     = RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py)
'''
import glob
import operator
import os
import sqlite3
import struct
import sys
import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
from xml.dom import minidom

def XbeInfo(FileName):
	try:
		if os.path.isfile(FileName) and FileName.endswith('.xbe'):
			with open(FileName, 'rb') as xbe:
				xbe.seek(0x104)
				LoadAddr = struct.unpack('L', xbe.read(4))
				xbe.seek(0x118)
				CertLoc = struct.unpack('L', xbe.read(4))
				CertBase = CertLoc[0] - LoadAddr[0] + 8
				xbe.seek(CertBase)
				IdData = struct.unpack('L', xbe.read(4))
				XbeTitle = ''.join([unichr(dta) for dta in struct.unpack('40H', xbe.read(0x0050)) if dta != 0])
			return str(XbeTitle)
		return {}
	except Exception as e:
		print("Error reading XBE: {}".format(e))
		return {}

def custom_text_factory(data):
	return data.decode('utf-8', 'ignore')  # Ignore decoding errors

def create_favourites_xml():
	try:
		Use_Game_Directory = sys.argv[1] if len(sys.argv) > 1 else "0"
		Use_Game_Directory_TBN = sys.argv[2] if len(sys.argv) > 2 else "0"

		# Constants and variables...
		Current_Profile_Directory = xbmc.translatePath('special://profile/')
		Game_Directories = ["E:\\Games\\", "F:\\Games\\", "G:\\Games\\"]
		Favourites_XML = xbmc.translatePath("special://profile/favourites.xml")
		MyPrograms6_db = xbmc.translatePath("special://profile/Database/MyPrograms6.db")
		pDialog = xbmcgui.DialogProgress()
		dialog = xbmcgui.Dialog()
		CountList = 0

		# Check if MyPrograms6.db exists
		if os.path.isfile(MyPrograms6_db):
			if os.path.isfile(Favourites_XML):
				os.remove(Favourites_XML)

			root = ET.Element("favourites")

			if Use_Game_Directory == "1":
				# Use game directories...
				pDialog.create('Building Favourites.xml', '', 'Using the Games directory to build the favourites.xml')
				total_games = sum(len(os.listdir(Game_Directory)) for Game_Directory in Game_Directories if os.path.isdir(Game_Directory))
				processed_games = 0

				for Game_Directory in Game_Directories:
					if os.path.isdir(Game_Directory):
						for Items in sorted(os.listdir(Game_Directory)):
							Game_Path = os.path.join(Game_Directory, Items)
							if os.path.isdir(Game_Path):
								for Path in glob.glob(os.path.join(Game_Path, "default.xbe")):
									processed_games += 1
									pDialog.update((processed_games * 100) // total_games, "Scanning Games", Items)
									XBETitle = XbeInfo(Path)
									ThumbCache = xbmc.getCacheThumbName(Path)
									PathXBE = Path.replace("\\", "\\\\")
									PathTBN = Path.replace("xbe", "tbn")
									favourite = ET.SubElement(root, "favourite")
									favourite.set("name", XBETitle if XBETitle else Items)
									favourite.set("thumb", PathTBN if Use_Game_Directory_TBN == "1" else Current_Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache)
									favourite.text = 'RunXBE("{}")'.format(PathXBE)
									CountList += 1
			else:
				# Use MyPrograms6.db...
				pDialog.create('Building Favourites.xml', '', 'Using MyPrograms6.db to build the favourites.xml')
				con = sqlite3.connect(MyPrograms6_db)
				con.text_factory = custom_text_factory
				cur = con.cursor()
				cur.execute("SELECT * FROM files ORDER BY title COLLATE NOCASE")
				rows = cur.fetchall()
				total_rows = len(rows)

				for row_count, row in enumerate(rows, start=1):
					title, xbe_path = row[3], row[1].replace('\\', '\\\\')
					ThumbCache = xbmc.getCacheThumbName(row[1])
					if os.path.isdir(row[1][:9]) and os.path.isfile(row[1]):
						pDialog.update((row_count * 100) // total_rows, "Scanning Games", title)
						favourite = ET.SubElement(root, "favourite")
						favourite.set("name", title)
						favourite.set("thumb", Current_Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache)
						favourite.text = 'RunXBE("{}")'.format(xbe_path)
						CountList += 1

			tree_str = ET.tostring(root)
			pretty_xml = minidom.parseString(tree_str).toprettyxml(indent="  ")

			with open(Favourites_XML, 'w') as f:
				f.write(pretty_xml.encode('ascii', 'ignore').decode('ascii'))

			pDialog.update(100, 'Please wait')
			pDialog.close()
			dialog.ok('Building Favourites.xml', '', 'Done.')
		else:
			dialog.ok("Error", "", "MyPrograms6.db is missing.")
	except Exception as e:
		print("Error: {}".format(e))
		dialog.ok("Error", "", "An unexpected error occurred.")

if __name__ == "__main__":
	create_favourites_xml()
