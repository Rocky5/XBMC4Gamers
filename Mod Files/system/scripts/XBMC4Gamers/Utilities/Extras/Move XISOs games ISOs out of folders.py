import os
import shutil
import glob
import xbmcgui

def move_iso_files(sub_folder, destination_folder):
	for iso in glob.iglob(os.path.join(sub_folder, '*.iso')):
		print(iso)
		if not os.path.isdir(destination_folder):
			os.makedirs(destination_folder)
		else:
			shutil.move(iso, destination_folder)

def main():
	root_folder = xbmcgui.Dialog().browse(0, "Select folder containing ISO games", 'files', '')
	if root_folder:
		destination_folder = xbmcgui.Dialog().browse(0, "Select destination folder", 'files', '')
		if destination_folder:
			print root_folder
			print destination_folder
			for folder in sorted(os.listdir(root_folder)):
				sub_folder = os.path.join(root_folder, folder)
				move_iso_files(sub_folder, destination_folder)
			
			print("Done")

if __name__ == "__main__":
	main()