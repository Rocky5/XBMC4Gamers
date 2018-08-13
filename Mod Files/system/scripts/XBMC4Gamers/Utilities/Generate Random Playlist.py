'''
	Script by Rocky5
	Used to create a playlist from a specific directory.

'''

import glob, os, xbmc, xbmcgui
dialog	= xbmcgui.Dialog()

error1 = 0
error2 = 0
error3 = 0

try:
	Music_Path = sys.argv[1]
except:
	Music_Path = [ "E:\\Music\\","F:\\Music\\","G:\\Music\\" ]
try:
	Music_Extension = sys.argv[2][3][4]
except:
	Music_Extension = [ "mp3","wma","ogg","m4a" ]
	
Playlist = xbmc.translatePath( "special://Profile/playlists/music/random.m3u" )

with open( Playlist,"w" ) as fin:
	for Music_Dir in Music_Path:
		if os.path.isdir( Music_Dir ):
			for dirName, subdirList, fileList in os.walk( Music_Dir ):
				for files in fileList:
					if files.endswith(tuple(Music_Extension)):
						with open( Playlist,"a" ) as fin:
							fin.write( "#EXTM3U\n" )
							line = '#EXTINF:0,' + files[:-4] + '\n' + os.path.join( dirName,files ) + '\n'
							fin.write(line)
			xbmc.PlayList( 0 ).shuffle()
			xbmc.executebuiltin( "playercontrol(RepeatAll)" )
		else:
			error = "Error: " + Music_Dir + " path not found."
			if error == "Error: E:\Music\ path not found.": error1 = "1"
			if error == "Error: F:\Music\ path not found.": error2 = "1"
			if error == "Error: G:\Music\ path not found.": error3 = "1"
		
if error1 == "1" and error2 == "1" and error3 == "1":
	dialog.ok("Error","","No music folder found in E, F or G.")
else:
	dialog.ok("Success","","Startup playlist was created.")
	xbmc.executebuiltin( "Skin.SetString(Startup_Playback_Path,special://profile/playlists/music/random.m3u)" )
