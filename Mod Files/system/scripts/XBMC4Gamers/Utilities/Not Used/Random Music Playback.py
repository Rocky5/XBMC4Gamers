'''
	Script by Rocky5
	Used to create a playlist from a specific directory and play it back shuffled and repeated.
		Usage:
			This script uses arguments, so to use it you add characters/paths to the end of the RunScript command.
			Below will build a playlist using the path and extension, in this case using 3 custom extensions.
				<onclick>RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Random Screensaver Images.py,G:\Music\My Music\,aac,wav,flac)</onclick>
			Same as above but uses default values for getting files.
				<onclick>RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Random Screensaver Images.py)</onclick>
'''
import glob, os, time, xbmc
try:
	Music_Path = sys.argv[1]
except:
	Music_Path = [ "E:\\Music\\","F:\\Music\\","G:\\Music\\" ]
try:
	Music_Extension = sys.argv[2][3][4]
except:
	Music_Extension = [ "mp3","wma","ogg" ]
Playlist = xbmc.translatePath("special://Profile/playlists/music/random.m3u")
for Music_Dir in Music_Path:
	if os.path.isdir(Music_Dir):
		f=open(Playlist,"w")
		for Music_Extension in Music_Extension:
			Music_Files = glob.glob(os.path.join(Music_Dir, "*."+Music_Extension))
			for Files in Music_Files:
				if os.path.isfile(Files):
					f.write("#EXTM3U\n")
					FileExt = Files.replace(Music_Dir,"")
					line = '#EXTINF:0,'+FileExt[:-4]+'\n'+Files+'\n'
					f.write(line)
		f.close()
		xbmc.executebuiltin("PlayMedia("+Playlist+")")
		xbmc.PlayList(0).shuffle()
		xbmc.executebuiltin("playercontrol(RepeatAll)")
	else:
		print "Error: "+Music_Dir+" path not found."