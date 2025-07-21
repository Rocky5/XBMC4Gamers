import os
import shutil
import xbmcgui

dialog = xbmcgui.Dialog()
progress_dialog = xbmcgui.DialogProgress()

PARTITIONS = ["C:\\", "E:\\", "F:\\", "G:\\"]
FOLDERS = ["Applications", "Apps", "Games", "Emulators", "Emus", "Homebrew", "Ports"]
BACKUP_DIR = os.path.join(os.getcwd(), "\\Backup")
MAX_DEPTH = 2 # go 2 sub folders down from FOLDER entry

### Only default.tbn
FILES_TO_BACKUP = ["default.tbn"]

# If using these set MAX_DEPTH to 4 This is so it backs up all files if you for example have your games in F:\Games\J-M\Game name\
### Full resource takes up a lot of space
# FILES_TO_BACKUP = ["default.tbn", "default.xml", "alt_synopsis.jpg", "banner.png", "cd.png", "cd_small.jpg", "cdposter.png", "dual3d.png", "fanart.jpg", "fanart_thumb.jpg", "fanart-blur.jpg", "fog.jpg", "icon.png", "opencase.png", "poster.jpg", "poster_small.jpg", "poster_small_blurred.jpg", "synopsis.jpg", "thumb.jpg", "preview.mp4", "Screenshot-1.jpg", "Screenshot-2.jpg", "Screenshot-3.jpg"]
### No videos takes up less space
# FILES_TO_BACKUP = ["default.tbn", "default.xml", "alt_synopsis.jpg", "banner.png", "cd.png", "cd_small.jpg", "cdposter.png", "dual3d.png", "fanart.jpg", "fanart_thumb.jpg", "fanart-blur.jpg", "fog.jpg", "icon.png", "opencase.png", "poster.jpg", "poster_small.jpg", "poster_small_blurred.jpg", "synopsis.jpg", "thumb.jpg", "Screenshot-1.jpg", "Screenshot-2.jpg", "Screenshot-3.jpg"]

def copy_file(source, base_folder, destination):
	relative_path = os.path.relpath(source, base_folder)
	dest_path = os.path.join(destination, relative_path)
	dest_folder = os.path.dirname(dest_path)
	if not os.path.exists(dest_folder): os.makedirs(dest_folder)
	shutil.copy2(source, dest_path)

def process_files(action, partitions, folders, backup, files_to_backup):
	if not os.path.exists(BACKUP_DIR):
		os.makedirs(BACKUP_DIR)
	progress_dialog.create("{} in Progress".format(action), "Starting {}...".format(action.lower()))
	progress_dialog.update(0, "")
	total = sum(1 for p in partitions if os.path.exists(p) for f in folders if os.path.exists(os.path.join(p, f)))
	count = 0

	for partition in partitions:
		if os.path.exists(partition):
			partition_name = os.path.splitdrive(partition)[0].replace(":", "")
			partition_backup = os.path.join(backup, partition_name)
			partition_folder_created = False

			for folder in folders:
				if action == "Restore":
					target_path = os.path.join(partition, folder)
					if not os.path.exists(target_path):
						continue
					current_path = os.path.join(partition_backup, folder)
				else:
					current_path = os.path.join(partition, folder)

				if os.path.isdir(current_path):
					base_depth = current_path.rstrip("\\").count("\\")
					print base_depth
					for root, dirs, files in os.walk(current_path):
						current_depth = root.rstrip("\\").count("\\")
						if current_depth - base_depth > MAX_DEPTH:
							dirs[:] = []
							continue
						for file in files:
							if file.lower() in files_to_backup:
								file_path = os.path.join(root, file)
								
								if action == "Backup" and not partition_folder_created:
									if not os.path.exists(partition_backup):
										os.makedirs(partition_backup)
									partition_folder_created = True
								
								if action == "Backup":
									dest_path = os.path.join(partition_backup, os.path.relpath(file_path, partition))
								elif action == "Restore":
									dest_path = os.path.join(partition, os.path.relpath(file_path, partition_backup))

								dest_folder = os.path.dirname(dest_path)
								if not os.path.exists(dest_folder):
									os.makedirs(dest_folder)

								shutil.copy2(file_path, dest_path)

								count += 1
								progress_dialog.update((count * 100) // total, "Processing File:", os.path.basename(root))
								if progress_dialog.iscanceled():
									progress_dialog.close()
									return False
	progress_dialog.close()
	return True

if __name__ == "__main__":
	xbmc.executebuiltin("Skin.SetString(DisableCancel,)")

	if dialog.yesno("Backup Files", "", "Do you want to create a backup or restore?", "", "Backup", "Restore"):
		if dialog.yesno("Restore Mode", "", "This will restore the mirror backup.[CR]Start the process?", "", "Cancel", "Start"):
			if process_files("Restore", PARTITIONS, FOLDERS, BACKUP_DIR, [f.lower() for f in FILES_TO_BACKUP]):
				dialog.ok("Restore Completed", "", "Files have been restored.")
			else:
				dialog.ok("Restore Cancelled", "", "Restore was partially complete.")
	else:
		if dialog.yesno("Backup Mode", "", "This will create a mirror backup.[CR]Start the process?", "", "Cancel", "Start"):
			if process_files("Backup", PARTITIONS, FOLDERS, BACKUP_DIR, [f.lower() for f in FILES_TO_BACKUP]):
				dialog.ok("Backup Completed", "", "Files have been backed up.")
			else:
				dialog.ok("Backup Cancelled", "", "Backup was partially complete.")