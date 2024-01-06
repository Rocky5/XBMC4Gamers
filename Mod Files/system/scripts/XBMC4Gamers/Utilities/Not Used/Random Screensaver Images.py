'''
	Script by Rocky5 (original idea DivideByZer0)
	Used to select a random directory from a folder of directories, to use as the screenshot screensaver.
	Usage:
		This script uses arguments, so to use it you add characters/paths to the end of the RunScript command.
		Random Image Directory for the screensaver.
			<onclick>RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Random Screensaver Images.py,C:\Images\Backgrounds\)</onclick>
		Below will select a random directory for the screensaver and then build a playlist using the path and extension, in this case mp3.
			<onclick>RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Random Screensaver Images.py,C:\Images\Backgrounds\,1,G:\Music\My Music\,mp3)</onclick>
		Same as above but music playback is disabled.
			<onclick>RunScript(Special://xbmc/scripts/XBMC4Gamers/Utilities/Random Screensaver Images.py,C:\Images\Backgrounds\,0,G:\Music\My Music\,mp3)</onclick>
'''
import os
import xbmc
import fileinput
import random
import glob
import time
try:
	Pictures_Path = sys.argv[1]
except:
	Pictures_Path = "Z:/"
try:
	Music_Playback = sys.argv[2]
except:
	Music_Playback = "0"
try:
	Music_Path = sys.argv[3]
except:
	Music_Path = "Z:/"
try:
	Music_Extension = sys.argv[4]
except:
	Music_Extension = ".mp3"
Playlist = xbmc.translatePath("special://Profile/playlists/music/random.m3u")
print "| Scripts\XBMC4Gamers\Utilities\Random Screensaver Images.py loaded."
#####	Play random music file
if Music_Playback == "1":
	if os.path.isdir(Music_Path):
		f=open(Playlist,"w")
		f.write("#EXTM3U\n")
		Music_Files = glob.glob(os.path.join(Music_Path, "*."+Music_Extension))
		list = os.listdir(Music_Path)
		for Files in Music_Files:
			FileExt = Files.replace(Music_Path,"")
			line = '#EXTINF:0,'+FileExt[:-4]+'\n'+Files+'\n'
			f.write(line)
	f.close()
	xbmc.executebuiltin("PlayMedia("+Playlist+")")
	xbmc.PlayList(0).shuffle()
else:
	pass
#####	Get a random subdirectory of Pictures_Path.
List_Root_Directory = sorted(os.listdir(Pictures_Path))
Directory_Name = random.choice(List_Root_Directory)
New_Path = '<slideshowpath pathversion="1">'+Pictures_Path+Directory_Name+'/</slideshowpath>\n'
GUISettings_Path = fileinput.input(xbmc.translatePath('special://profile/guisettings.xml'), inplace=1)
for line in GUISettings_Path:
	if "slideshowpath" in line:
		line = New_Path
	sys.stdout.write(line)
print ("| New Path = "+Pictures_Path+Directory_Name+"/")