'''
	Script by Rocky5
	Used to create a playlist from a specific directory.

'''
				
				
import glob, os, time, xbmc, xbmcgui
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
	Music_Extension = [ "mp3","wma","ogg" ]
	
Playlist = xbmc.translatePath( "special://Profile/playlists/music/random.m3u" )

for Music_Dir in Music_Path:
	if os.path.isdir( Music_Dir ):
		f=open( Playlist,"w" )
		for Music_Extension in Music_Extension:
			Music_Files = glob.glob( os.path.join( Music_Dir, "*." + Music_Extension ) )
			for Files in Music_Files:
				if os.path.isfile( Files ):
					f.write( "#EXTM3U\n" )
					FileExt = Files.replace( Music_Dir,"" )
					line = '#EXTINF:0,' + FileExt[:-4] + '\n' + Files + '\n'
					f.write(line)
		f.close()
		xbmc.PlayList( 0 ).shuffle()
		xbmc.executebuiltin( "playercontrol(RepeatAll)" )
	else:
		error = "Error: " + Music_Dir + " path not found."
		if error == "Error: E:\Music\ path not found.": error1 = "1"
		if error == "Error: F:\Music\ path not found.": error2 = "1"
		if error == "Error: G:\Music\ path not found.": error3 = "1"
		
if error1 == "1" and error2 == "1" and error3 == "1":
	dialog.ok("Error","", "No music folder found in E, F or G.")
else:
	dialog.ok("Playlist Created","", "Complete.")
