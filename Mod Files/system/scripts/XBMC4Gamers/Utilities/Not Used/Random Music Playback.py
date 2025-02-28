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

import glob
import os
import sys
import xbmc

def create_playlist(music_paths, music_extensions, playlist_path):
	with open(playlist_path, "w") as playlist_file:
		for music_dir in music_paths:
			if os.path.isdir(music_dir):
				for extension in music_extensions:
					music_files = glob.glob(os.path.join(music_dir, "*.{}".format(extension)))
					for music_file in music_files:
						if os.path.isfile(music_file):
							playlist_file.write("#EXTM3U\n")
							file_ext = music_file.replace(music_dir, "")
							line = '#EXTINF:0,{}\n{}\n'.format(file_ext[:-4], music_file)
							playlist_file.write(line)
				xbmc.executebuiltin("PlayMedia({})".format(playlist_path))
				xbmc.PlayList(0).shuffle()
				xbmc.executebuiltin("playercontrol(RepeatAll)")
			else:
				print("Error: {} path not found.".format(music_dir))

def main():
	try:
		music_path = sys.argv[1].split(',')
	except IndexError:
		music_path = ["E:\\Music\\", "F:\\Music\\", "G:\\Music\\"]

	try:
		music_extension = sys.argv[2].split(',')
	except IndexError:
		music_extension = ["mp3", "wma", "ogg"]

	playlist = xbmc.translatePath("special://Profile/playlists/music/random.m3u")
	create_playlist(music_path, music_extension, playlist)

if __name__ == "__main__":
	main()