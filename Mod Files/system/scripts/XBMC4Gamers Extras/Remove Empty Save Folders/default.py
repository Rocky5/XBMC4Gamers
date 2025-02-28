'''
	Script by Rocky5
	Removes empty directories from TDATA and UDATA.
'''
import os
import xbmcgui
import shutil

def clean_save_folders(save_directories):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create("Cleaning Save Folders")
	
	for save_directory in save_directories:
		if os.path.isdir(save_directory):
			save_dirs = sorted(os.listdir(save_directory))
			total_dirs = len(save_dirs)

			for count, save_dir in enumerate(save_dirs, start=1):
				save_path = os.path.join(save_directory, save_dir)
				process = ''
				
				if os.path.isdir(save_path):
					try:
						subdirectories = next(os.walk(save_path))[1]
						if subdirectories:
							process = 'Not empty, skipping'
						else:
							files = os.listdir(save_path)
							if any(not fname.endswith('.xbx') for fname in files):
								process = 'Not empty, skipping'
							else:
								shutil.rmtree(save_path)
								process = 'Found empty folder, removing'
					except (StopIteration, OSError):
						process = 'Cannot remove folder, write protected?'
					
					print('{} - {}'.format(save_path, process))
					progress = (count * 100) // total_dirs
					pDialog.update(progress, "Processing", '{}[CR]{}'.format(save_path, process))
		else:
			print(save_directory + " does not exist.")

	pDialog.close()
	xbmcgui.Dialog().ok("Cleaning Save Folders", "", "Process Complete")

if __name__ == "__main__":
	Save_Directories = ["E:\\TDATA\\", "E:\\UDATA\\"]
	clean_save_folders(Save_Directories)
