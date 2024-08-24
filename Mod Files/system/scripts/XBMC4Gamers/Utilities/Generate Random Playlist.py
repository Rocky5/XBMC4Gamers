'''
Script by Rocky5
Used to create a playlist from a specific directory.
'''

import os
import sys
import xbmc
import xbmcgui

dialog = xbmcgui.Dialog()

# Default music paths and extensions
default_music_paths = ["E:\\Music\\", "F:\\Music\\", "G:\\Music\\"]
default_music_extensions = ["mp3", "wma", "ogg", "m4a"]

# Get music paths and extensions from arguments or use defaults
music_paths = sys.argv[1].split(',') if len(sys.argv) > 1 else default_music_paths
music_extensions = sys.argv[2].split(',') if len(sys.argv) > 2 else default_music_extensions

# Playlist path
playlist_path = xbmc.translatePath("special://profile/playlists/music/random.m3u")

# Initialize error flags and file counter
errors = {path: False for path in music_paths}
file_counter = 0

# Create playlist
with open(playlist_path, "w") as playlist:
	playlist.write("#EXTM3U\n")
	for music_dir in music_paths:
		if os.path.isdir(music_dir):
			for root, _, files in os.walk(music_dir):
				for file in files:
					if file.split('.')[-1].lower() in music_extensions:
						file_path = os.path.join(root, file)
						line = '#EXTINF:0,{}\n{}\n'.format(file[:-4], file_path)
						playlist.write(line)
						file_counter += 1
		else:
			errors[music_dir] = True

# Shuffle the playlist and set repeat mode
xbmc.PlayList(0).shuffle()
xbmc.executebuiltin("PlayerControl(RepeatAll)")

# Check for errors and display appropriate message
if all(errors.values()):
	dialog.ok("Error", "", "No music folder found in the specified paths.")
else:
	dialog.ok("Success", "", "Startup playlist was created.[CR]Found {} files.".format(file_counter))
	xbmc.executebuiltin("Skin.SetString(Startup_Playback_Path,special://profile/playlists/music/random.m3u)")
