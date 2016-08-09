########################################################################################################################################
'''
	Script by Rocky5 (original idea headphone)
	Used to create a favourites.xml from all your games.
'''
########################################################################################################################################


import xbmc
import xbmcgui
import time
import os
import sqlite3
import re
import glob
import struct
import operator
import string


########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\Utilities\Generate Favourites.py loaded."
print "| ------------------------------------------------------------------------------"


# Enabled if you want the games directory (ie, E:\Games\, F:\Games\, or G:\Games\) to be used to build the xml.
# You can also enabled the TBN option, this will use the default.tbn files, instead of the cached versions XBMC has made. 
# Use Games + default.tbn	= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Generate Favourites.py,1,1 )
# Use Games + cached tbn	= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Generate Favourites.py,1,0 )
# Disabled					= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Generate Favourites.py,0,0 )
# Disabled					= RunScript( Special://xbmc/scripts/XBMC4Kids/Utilities/Generate Favourites.py )
try:
	Use_Game_Directory = sys.argv[1][0]
except:
	Use_Game_Directory = "0"
try:
	Use_Game_Directory_TBN = sys.argv[2][0]
except:
	Use_Game_Directory_TBN = "0"


def XbeInfo(FileName): # Modified by me. Original by chunk_1970 - http://forum.kodi.tv/showthread.php?tid=24666&pid=125356#pid125356
    try :
        XbeDta          =   {}
        if os.path.isfile(FileName) and FileName.endswith('.xbe')   :
            xbe         =   open(FileName,'rb')
            ## Get XbeId Data ##
            xbe.seek(0x104)
            tLoadAddr   =   xbe.read(4)
            xbe.seek(0x118)
            tCertLoc    =   xbe.read(4)
            LoadAddr    =   struct.unpack('L',tLoadAddr)
            CertLoc     =   struct.unpack('L',tCertLoc)
            CertBase    =   CertLoc[0] - LoadAddr[0]
            CertBase    +=  8
            IdStart     =   xbe.seek(CertBase)
            tIdData     =   xbe.read(4)
            IdData      =   struct.unpack('L',tIdData)
            ## Get Xbe Title ##
            XbeTitle    =   ''
            for dta in struct.unpack(operator.repeat('H',40),xbe.read(0x0050)):
                try     :
                    if dta != 00:	XbeTitle += str(unichr(dta))
                except  :   pass
            XbeDta    =   str(XbeTitle)
            #XbeDta['Title']     =   str(XbeTitle)
            #XbeDta['Id']        =   str(hex(IdData[0])[2:-1]).lower().rjust(8,'0')
            #XbeDta['Path']      =   str(FileName)
            xbe.close()
        return XbeDta
    except  :
        xbe.close()
        return {}

		
Current_Profile_Directory = xbmc.translatePath( 'special://profile/' )
Game_Directories = [ "E:\\Games\\", "F:\\Games\\", "G:\\Games\\" ]
Favourites_XML = xbmc.translatePath( "special://Profile/favourites.xml")
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
progress = 0
pDialog.update( 0 )


if os.path.isfile(Favourites_XML) == 1: os.remove(Favourites_XML)
f=open(Favourites_XML,"w")
f.write("<favourites>\n")


if Use_Game_Directory == "1":
	pDialog.create('Building Favourites.xml','','Using the Games directory to build the favourites.xml')
	time.sleep(2)
	print "| Games Directory Used."
	for Game_Directories in Game_Directories :
		for Items in sorted( os.listdir( Game_Directories ) ):
			if os.path.isdir(os.path.join( Game_Directories, Items)):
				Game_Directory = os.path.join( Game_Directories, Items )
				progress += 1
				if progress == 1:	pDialog.update( 0,"Scanning Games","Processing." )
				if os.path.isdir( Game_Directory ) :
					XBEFiles = glob.glob( os.path.join( Game_Directory, "default.xbe" ) )
					TBNFiles = glob.glob( os.path.join( Game_Directory, "default.tbn" ) )
					for TBN in TBNFiles:
						for Path in XBEFiles:
							XBETitle = XbeInfo( Path )
							ThumbCache = xbmc.getCacheThumbName( Path )
							Path = Path.replace("\\","\\\\")
							pDialog.update( int ( progress / float( len ( sorted( os.listdir( Game_Directories ) ) ) ) *100 ),"Scanning Games",Items )
							if Use_Game_Directory_TBN == "1":
								line='<favourite name="' + XBETitle.encode(encoding='UTF-8') + '\" thumb=\"' + TBN + '">RunXBE(&quot;' + Path.encode(encoding='UTF-8') + '&quot;)</favourite>\n'
								f.write(line)
							else:
								line='<favourite name="' + XBETitle.encode(encoding='UTF-8') + '\" thumb=\"' + Current_Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache + '">RunXBE(&quot;' + Path.encode(encoding='UTF-8') + '&quot;)</favourite>\n'
								f.write(line)
	f.write("</favourites>")
	f.close()
else:
	pDialog.create('Building Favourites.xml','','Using MyPrograms6.db to build the favourites.xml')
	time.sleep(2)
	print "| XBMC MyPrograms6.db Used."
	cursor = sqlite3.connect(xbmc.translatePath( "special://Profile/Database/MyPrograms6.db" )).cursor()
	sql = "SELECT * FROM files"
	cursor.execute(sql)
	rows = cursor.fetchall()
	for row in rows:
		progress += 1
		if progress == 1:	pDialog.update( 0,"Scanning Games","Processing." )
		title = row[3]
		xbe_path = row[1].replace('\\','\\\\')
		ThumbCache = xbmc.getCacheThumbName( row[1] )
		pDialog.update( int ( progress / float( len ( os.listdir( row[1][:9] ) ) ) *100 ),"Scanning Games",title )
		line='<favourite name="' + title.encode(encoding='UTF-8') + '\" thumb=\"' + Current_Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache + '">RunXBE(&quot;' + xbe_path.encode(encoding='UTF-8') + '&quot;)</favourite>\n'
		f.write(line)
	f.write("</favourites>")
	f.close()

pDialog.update(100, 'Please wait')
pDialog.close()
dialog.ok('Building Favourites.xml','','Done.')
print "================================================================================"