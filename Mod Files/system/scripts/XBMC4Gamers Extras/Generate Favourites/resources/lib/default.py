# -*- coding: utf-8 -*- 
'''
	Script by Rocky5 (original idea headphone)
	Used to create a favourites.xml from all your games.
	Enabled if you want the games directory (ie, E:\Games\, F:\Games\, or G:\Games\) to be used to build the xml.
		You can also enabled the TBN option, this will use the default.tbn files, instead of the cached versions XBMC has made. 
			Use Games+default.tbn	= RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py,1,1)
			Use Games+cached tbn	= RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py,1,0)
			Use MyPrograms6.db		= RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py,0,0)
			Use MyPrograms6.db		= RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py)
'''
import glob
import operator
import os
import sqlite3
import struct
import time
import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
from xml.dom import minidom

def XbeInfo(FileName):
	try:
		XbeDta = {}
		if os.path.isfile(FileName) and FileName.endswith('.xbe'):
			xbe = open(FileName, 'rb')
			# Get XbeId Data
			xbe.seek(0x104)
			tLoadAddr = xbe.read(4)
			xbe.seek(0x118)
			tCertLoc = xbe.read(4)
			LoadAddr = struct.unpack('L', tLoadAddr)
			CertLoc = struct.unpack('L', tCertLoc)
			CertBase = CertLoc[0] - LoadAddr[0] + 8
			xbe.seek(CertBase)
			tIdData = xbe.read(4)
			IdData = struct.unpack('L', tIdData)
			# Get Xbe Title
			XbeTitle = ''
			for dta in struct.unpack(operator.repeat('H', 40), xbe.read(0x0050)):
				try:
					if dta != 0:
						XbeTitle += str(unichr(dta))
				except:
					pass
			XbeDta = str(XbeTitle)
			xbe.close()
		return XbeDta
	except:
		xbe.close()
		return {}

def custom_text_factory(data):
    return data.decode('utf-8', 'ignore')  # Ignore decoding errors

try:
	Use_Game_Directory = sys.argv[1]
except:
	Use_Game_Directory = "0"
try:
	Use_Game_Directory_TBN = sys.argv[2]
except:
	Use_Game_Directory_TBN = "0"

# Constants and variables...
Current_Profile_Directory = xbmc.translatePath('special://profile/')
Game_Directories = ["E:\\Games\\", "F:\\Games\\", "G:\\Games\\"]
Favourites_XML = xbmc.translatePath("special://Profile/favourites.xml")
MyPrograms6_db = xbmc.translatePath("special://Profile/Database/MyPrograms6.db")
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
pDialog.update(0)
CountList = 1


# Check if MyPrograms6.db exists
if os.path.isfile(MyPrograms6_db):
	if os.path.isfile(Favourites_XML):
		os.remove(Favourites_XML)

	root = ET.Element("favourites")

	if Use_Game_Directory == "1":
		# Use game directories...
		pDialog.create('Building Favourites.xml','','Using the Games directory to build the favourites.xml')
		for Game_Directories in Game_Directories:
			if os.path.isdir(Game_Directories):
				for Items in sorted(os.listdir(Game_Directories)):
					if os.path.isdir(os.path.join(Game_Directories, Items)):
						Game_Directory = os.path.join(Game_Directories, Items)
						if os.path.isdir(Game_Directory):
							for Path in glob.glob(os.path.join(Game_Directory, "default.xbe")):
								pDialog.update((CountList * 100) / len(sorted(os.listdir(Game_Directories))),"Scanning Games",Items)
								XBETitle = XbeInfo(Path)
								ThumbCache = xbmc.getCacheThumbName(Path)
								PathXBE = Path.replace("\\", "\\\\")
								PathTBN = Path.replace("xbe", "tbn")
								favourite = ET.SubElement(root, "favourite")
								favourite.set("name", XBETitle if XBETitle != "" else Items)
								favourite.set("thumb", PathTBN if Use_Game_Directory_TBN == "1" else Current_Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache)
								favourite.text = "RunXBE(\"" + PathXBE + "\")"
								CountList = CountList+1
	else:
		# Use MyPrograms6.db...
		pDialog.create('Building Favourites.xml','','Using MyPrograms6.db to build the favourites.xml')
		con = sqlite3.connect(MyPrograms6_db)
		cur = con.cursor()
		con.text_factory = custom_text_factory
		sql = "SELECT * FROM files"
		cur.execute(sql)
		rows = cur.fetchall()
		for row in sorted(rows):
			title, xbe_path = row[3], row[1].replace('\\', '\\\\')
			ThumbCache = xbmc.getCacheThumbName(row[1])
			if os.path.isdir(row[1][:9]) and os.path.isfile(row[1]):
				pDialog.update((CountList * 100) / len(os.listdir(row[1][:9])),"Scanning Games",title)
				favourite = ET.SubElement(root, "favourite")
				favourite.set("name", title)
				favourite.set("thumb", Current_Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache)
				favourite.text = "RunXBE(\"" + xbe_path + "\")"
				CountList = CountList+1
	
	tree = ET.ElementTree(root)
	tree_str = ET.tostring(root)
	pretty_xml = minidom.parseString(tree_str).toprettyxml(indent="  ")

	with open(Favourites_XML, 'w') as f:
		f.write(pretty_xml.encode('ascii', 'ignore').decode('ascii'))

	pDialog.update(100, 'Please wait')
	pDialog.close()
	dialog.ok('Building Favourites.xml', '', 'Done.')
else:
	dialog.ok("Error", "", "MyPrograms6.db is missing.")
