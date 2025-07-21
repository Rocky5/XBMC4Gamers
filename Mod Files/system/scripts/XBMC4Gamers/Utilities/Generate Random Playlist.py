'''
Script by Rocky5
Creating a playlist from specific directory(s).
'''

import os
import sys
import xbmc
import xbmcgui

DEFAULT_MUSIC_PATHS = ["E:\\Music\\", "F:\\Music\\", "G:\\Music\\"]
DEFAULT_MUSIC_EXTENSIONS = ["mp3", "wma", "ogg", "m4a"]

def add_skin_music_path(default_paths):
	additional_paths = xbmc.getInfoLabel('Skin.String(MusicPaths)')
	if additional_paths:
		additional_paths = [path.strip() for path in additional_paths.split(',')]
		additional_paths = [path if path.endswith('\\') else path + '\\' for path in additional_paths]
		default_paths += additional_paths
	return default_paths

def add_skin_music_extensions(default_extensions):
	additional_extensions = xbmc.getInfoLabel('Skin.String(MusicExtPaths)')
	if additional_extensions:
		additional_extensions = [ext.strip().lower() for ext in additional_extensions.split(',')]
		default_extensions += additional_extensions
	return default_extensions

def get_music_paths_and_extensions():
	music_paths = add_skin_music_path(DEFAULT_MUSIC_PATHS)
	music_paths = sys.argv[1].split(',') if len(sys.argv) > 1 else music_paths

	music_extensions = add_skin_music_extensions(DEFAULT_MUSIC_EXTENSIONS)
	music_extensions = sys.argv[2].split(',') if len(sys.argv) > 2 else music_extensions

	return music_paths, music_extensions

def calculate_total_files(music_paths, music_extensions):
	return sum(len(files) for music_dir in music_paths if os.path.isdir(music_dir)
			   for _, _, files in os.walk(music_dir)
			   if any(file.split('.')[-1].lower() in music_extensions for file in files))

def create_playlist(playlist_path, music_paths, music_extensions):
	file_counter = 0
	pDialog = xbmcgui.DialogProgress()
	pDialog.create("Generating Playlist", "", "Please wait...")

	try:
		total_files = calculate_total_files(music_paths, music_extensions)
		if total_files == 0:
			pDialog.update(100, "No files found.")
			xbmcgui.Dialog().ok("Error", "", "No music files found in the following paths:\n{}".format(", ".join(music_paths)))
			return

		pDialog.update(0, "")

		with open(playlist_path, "w") as playlist:
			playlist.write("#EXTM3U\n")
			for music_dir in music_paths:
				if os.path.isdir(music_dir):
					for root, _, files in os.walk(music_dir):
						for file in files:
							if file.split('.')[-1].lower() in music_extensions:
								file_path = os.path.join(root, file)
								line = "#EXTINF:0,%s\n%s\n" % (file[:-4], file_path)
								playlist.write(line)
								file_counter += 1
								progress = int((file_counter * 100) / total_files)
								pDialog.update(progress, "", "Processing files: %d found" % file_counter)

		pDialog.update(100, "Playlist built!")
		xbmcgui.Dialog().ok(
			"Generating Playlist", 
			"", 
			"Playlist created successfully!", 
			"Found %d audio files." % file_counter
		)
	finally:
		pDialog.close()

def main():
	music_paths, music_extensions = get_music_paths_and_extensions()
	playlist_path = xbmc.translatePath("special://profile/playlists/music/random.m3u")

	create_playlist(playlist_path, music_paths, music_extensions)

	xbmc.PlayList(0).shuffle()
	xbmc.executebuiltin("PlayerControl(RepeatAll)")
	xbmc.executebuiltin("Skin.SetString(Startup_Playback_Path,special://profile/playlists/music/random.m3u)")

if __name__ == "__main__":
	# Close the script loading dialog
	xbmc.executebuiltin('Dialog.Close(1100,false)')
	main()