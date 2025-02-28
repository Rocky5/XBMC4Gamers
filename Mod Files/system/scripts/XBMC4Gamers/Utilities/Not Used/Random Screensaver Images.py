'''
	Script by Rocky5 (original idea DivideByZer0)
	Used to select a random directory from a folder of directories to use as the screenshot screensaver.
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
import random
import glob
import sys

def get_argument(index, default_value):
	try:
		return sys.argv[index]
	except IndexError:
		return default_value

def create_music_playlist(music_path, music_extension, playlist_path):
	if os.path.isdir(music_path):
		with open(playlist_path, "w") as playlist_file:
			playlist_file.write("#EXTM3U\n")
			music_files = glob.glob(os.path.join(music_path, "*.{}".format(music_extension)))
			for music_file in music_files:
				if os.path.isfile(music_file):
					file_ext = music_file.replace(music_path, "")
					line = '#EXTINF:0,{}\n{}\n'.format(file_ext[:-4], music_file)
					playlist_file.write(line)
		xbmc.executebuiltin("PlayMedia({})".format(playlist_path))
		xbmc.PlayList(0).shuffle()
		xbmc.executebuiltin("playercontrol(RepeatAll)")

def set_random_screensaver_path(pictures_path):
	list_root_directory = sorted(os.listdir(pictures_path))
	directory_name = os.path.join(pictures_path, random.choice(list_root_directory))
	
	xbmc.executehttpapi('SetGUISetting(3;screensaver.slideshowpath;{})'.format(directory_name))

def main():
	print "| Scripts/XBMC4Gamers/Utilities/Random Screensaver Images.py loaded."
	
	pictures_path = get_argument(1, "Z:/")
	music_playback = get_argument(2, "0")
	music_path = get_argument(3, "Z:/")
	music_extension = get_argument(4, "mp3")
	playlist_path = xbmc.translatePath("special://profile/playlists/music/random.m3u")
	
	if music_playback == "1":
		create_music_playlist(music_path, music_extension, playlist_path)
	
	set_random_screensaver_path(pictures_path)
	print "| New Path = {}".format(pictures_path)

if __name__ == "__main__":
	main()
