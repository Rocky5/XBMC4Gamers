import os
import shutil
import xbmcgui

def remove_files_and_folders(sub_folder):
	paths_to_remove = [
		'_resources',
		# '_resources\\artwork',
		#'_resources\\media',
		# '_resources\\screenshots',
		# '_resources\\default.xml',
		'default.tbn',
		'fanart.jpg',
		'icon.jpg',
		'icon.png'
	]
	
	for path in paths_to_remove:
		full_path = os.path.join(sub_folder, path)
		if os.path.isdir(full_path):
			shutil.rmtree(full_path)
		elif os.path.isfile(full_path):
			os.remove(full_path)

def main():
	dialog = xbmcgui.Dialog()
	root_folder = dialog.browse(0, "Select a folder", "files")
	
	for folder in sorted(os.listdir(root_folder)):
		sub_folder = os.path.join(root_folder, folder)
		remove_files_and_folders(sub_folder)
	
	dialog.ok("", "Done")

if __name__ == "__main__":
	main()
