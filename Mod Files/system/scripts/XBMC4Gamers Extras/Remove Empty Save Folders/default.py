'''
	Script by Rocky5
	Removes empty directories from TDATA and UDATA.
'''
import os
import xbmcgui
import shutil

def clean_save_folders(save_directories):
	pDialog = xbmcgui.DialogProgress()
	pDialog.update(0)
	pDialog.create("Cleaning Save Folders")

	for save_directory in save_directories:
		CountList = 1
		if os.path.isdir(save_directory):
			for save_dir in sorted(os.listdir(save_directory)):
				save_path = os.path.join(save_directory, save_dir)
				if os.path.isdir(save_path):
					pDialog.update((CountList * 100) / len(os.listdir(save_directory)), "Processing", save_path)
					try:
						subdirectories = next(os.walk(save_path))[1]
						if subdirectories:
							print save_path + " - skipping"
						else:
							files = os.listdir(save_path)
							if any(not fname.endswith('.xbx') for fname in files):
								print save_path + " - skipping"
							else:
								shutil.rmtree(save_path)
								print save_path + " - removed"
						CountList += 1
					except StopIteration:
						print save_path + " is write protected?"
		else:
			print save_directory + " does not exist."

	pDialog.close()
	xbmcgui.Dialog().ok("Cleaning Save Folders", "", "Process Complete")

if __name__ == "__main__":
	Save_Directories = ["E:\\TDATA\\", "E:\\UDATA\\"]
	clean_save_folders(Save_Directories)
