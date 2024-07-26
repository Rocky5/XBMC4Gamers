'''
Script by Rocky5
Used to create a playlist from a specific directory.
'''

import glob
import os
import sys
import xbmc
import xbmcgui

dialog = xbmcgui.Dialog()

# Default music paths and extensions
default_music_paths = ["E:\\Music\\", "F:\\Music\\", "G:\\Music\\"]
default_music_extensions = ["mp3", "wma", "ogg", "m4a"]

# Get music paths and extensions from arguments or use defaults
music_paths = sys.argv[1] if len(sys.argv) > 1 else default_music_paths
music_extensions = sys.argv[2] if len(sys.argv) > 2 else default_music_extensions

# Playlist path
playlist_path = xbmc.translatePath("special://Profile/playlists/music/random.m3u")

# Initialize error flags
errors = {path: False for path in default_music_paths}

# Create playlist
with open(playlist_path, "w") as playlist:
	playlist.write("#EXTM3U\n")
	for music_dir in music_paths:
		if os.path.isdir(music_dir):
			for dir_name, subdir_list, file_list in os.walk(music_dir):
				for file in file_list:
					if file.endswith(tuple(music_extensions)):
						line = '#EXTINF:0,{}\n{}\n'.format(file[:-4], os.path.join(dir_name, file))
						playlist.write(line)
			xbmc.PlayList(0).shuffle()
			xbmc.executebuiltin("playercontrol(RepeatAll)")
		else:
			errors[music_dir] = True

# Check for errors and display appropriate message
if all(errors.values()):
	dialog.ok(	"Error",
				"",
				"No music folder found in E, F, or G."	)
else:
	dialog.ok(	"Success",
				"",
				"Startup playlist was created."	)
	xbmc.executebuiltin("Skin.SetString(Startup_Playback_Path,special://profile/playlists/music/random.m3u)")
