'''
	Script by Rocky5 (original idea headphone)
	Used to create a favourites.xml from all your games.
	
	Update: 21 August 2016
	-- Updated the progress bars code & also fixed any issue of the script failing if no Games directory is found when reading the db.

	Enabled if you want the games directory (ie, E:\Games\, F:\Games\, or G:\Games\) to be used to build the xml.
 		You can also enabled the TBN option, this will use the default.tbn files, instead of the cached versions XBMC has made. 
			Use Games + default.tbn	= RunScript( Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py,1,1 )
			Use Games + cached tbn	= RunScript( Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py,1,0 )
 			Use MyPrograms6.db		= RunScript( Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py,0,0 )
			Use MyPrograms6.db		= RunScript( Special://xbmc/scripts/XBMC4Gamers/Utilities/Generate Favourites.py )
'''

import glob, operator, os, sqlite3, string, struct, time, xbmc, xbmcgui

#####	Start markings for the log file.
print "================================================================================"
print "| Scripts\XBMC4Gamers Extras\Generate Favourites\resources\lib\default.py loaded."
print "| ------------------------------------------------------------------------------"


try:
	Use_Game_Directory = sys.argv[1]
except:
	Use_Game_Directory = "0"
try:
	Use_Game_Directory_TBN = sys.argv[2]
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

		
Current_Profile_Directory	= xbmc.translatePath( 'special://profile/' )
Game_Directories			= [ "E:\\Games\\", "F:\\Games\\", "G:\\Games\\" ]
Favourites_XML				= xbmc.translatePath( "special://Profile/favourites.xml")
MyPrograms6_db				= xbmc.translatePath( "special://Profile/Database/MyPrograms6.db" )
pDialog						= xbmcgui.DialogProgress()
dialog						= xbmcgui.Dialog()
CountList					= 1
pDialog.update( 0 )


if os.path.isfile( MyPrograms6_db ):

	if os.path.isfile(Favourites_XML) == 1: os.remove(Favourites_XML)
	f	=	open(Favourites_XML,"w")
	f.write("<favourites>\n")

	if Use_Game_Directory == "1":
		pDialog.create('Building Favourites.xml','','Using the Games directory to build the favourites.xml')
		time.sleep(1)
		print "| Games Directory Used."
		try:
			for Game_Directories in Game_Directories :
				if os.path.isdir( Game_Directories ):
					for Items in sorted( os.listdir( Game_Directories ) ):
						if os.path.isdir(os.path.join( Game_Directories, Items)):
							Game_Directory = os.path.join( Game_Directories, Items )
							if os.path.isdir( Game_Directory ) :
								XBEFiles = glob.glob( os.path.join( Game_Directory, "default.xbe" ) )
								for Path in XBEFiles:
									XBETitle = XbeInfo( Path )
									ThumbCache = xbmc.getCacheThumbName( Path )
									PathXBE = Path.replace("\\","\\\\")
									PathTBN = Path.replace("xbe","tbn")
									pDialog.update( ( CountList * 100 ) / len( sorted( os.listdir( Game_Directories ) ) ),"Scanning Games",Items )
									CountList = CountList + 1
									if Use_Game_Directory_TBN == "1":
										if os.path.isfile( PathTBN ):
											line='<favourite name="' + XBETitle.encode(encoding='UTF-8') + '\" thumb=\"' + PathTBN + '">RunXBE(&quot;' + PathXBE.encode(encoding='UTF-8') + '&quot;)</favourite>\n'
											f.write(line)
										else:
											line='<favourite name="' + XBETitle.encode(encoding='UTF-8') + '\" thumb=\"' + Current_Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache + '">RunXBE(&quot;' + Path.encode(encoding='UTF-8') + '&quot;)</favourite>\n'
											f.write(line)
									else:
										line='<favourite name="' + XBETitle.encode(encoding='UTF-8') + '\" thumb=\"' + Current_Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache + '">RunXBE(&quot;' + Path.encode(encoding='UTF-8') + '&quot;)</favourite>\n'
										f.write(line)
									time.sleep(0.05)
			f.write("</favourites>")
			f.close()
			pDialog.update(100, 'Please wait')
			pDialog.close()
			dialog.ok('Building Favourites.xml','','Done.')
		except:
			f.close()
			pDialog.close()
			dialog.ok( "Error","","Something went wrong.","Are there any Games folders?" )
	else:
		try:
			pDialog.create('Building Favourites.xml','','Using MyPrograms6.db to build the favourites.xml')
			time.sleep(1)
			print "| XBMC MyPrograms6.db Used."
			cursor = sqlite3.connect( MyPrograms6_db ).cursor()
			sql = "SELECT * FROM files"
			cursor.execute(sql)
			rows = cursor.fetchall()
			for row in rows:
				title = row[3]
				xbe_path = row[1].replace('\\','\\\\')
				ThumbCache = xbmc.getCacheThumbName( row[1] )
				if os.path.isdir( row[1][:9] ):
					if os.path.isfile( row[1] ):
						pDialog.update( ( CountList * 100 ) / len( os.listdir( row[1][:9] ) ),"Scanning Games",title )
						line='<favourite name="' + title.encode(encoding='UTF-8') + '\" thumb=\"' + Current_Profile_Directory + "Thumbnails\\Programs\\" + ThumbCache[0] + "\\" + ThumbCache + '">RunXBE(&quot;' + xbe_path.encode(encoding='UTF-8') + '&quot;)</favourite>\n'
						f.write(line)
						CountList = CountList + 1
						time.sleep(0.05)
			f.write("</favourites>")
			f.close()
			pDialog.update(100, 'Please wait')
			pDialog.close()
			dialog.ok('Building Favourites.xml','','Done.')
		except:
			f.close()
			pDialog.close()
			dialog.ok( "Error","","Something went wrong.","MyPrograms6.db could be empty." )		
else:
	dialog.ok( "Error","","MyPrograms6.db is missing." )
print "================================================================================"