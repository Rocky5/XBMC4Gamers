import os
import glob
import xbmcgui

def remove_media_files(sub_folder):
	media_folder = os.path.join(sub_folder, '_resources\\media\\')
	file_patterns = ['*.xmv', '*.strm']
	
	for pattern in file_patterns:
		for file_path in glob.iglob(os.path.join(media_folder, pattern)):
			print(file_path)
			os.remove(file_path)

def main():
	dialog = xbmcgui.Dialog()
	root_folder = dialog.browse(0, "Select a game folder", "files")
	
	for folder in sorted(os.listdir(root_folder)):
		sub_folder = os.path.join(root_folder, folder)
		remove_media_files(sub_folder)
	
	dialog.ok("", "Done")

if __name__ == "__main__":
	main()
