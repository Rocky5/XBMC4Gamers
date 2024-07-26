import os
import shutil
import glob

def move_iso_files(sub_folder, destination_folder):
	for iso in glob.iglob(os.path.join(sub_folder, '*.iso')):
		print(iso)
		if not os.path.isdir(destination_folder):
			os.makedirs(destination_folder)
		else:
			shutil.move(iso, destination_folder)

def main():
	root_folder = 'F:\\Games ISOs\\'
	destination_folder = 'F:\\Test\\'
	
	for folder in sorted(os.listdir(root_folder)):
		sub_folder = os.path.join(root_folder, folder)
		move_iso_files(sub_folder, destination_folder)
	
	print("Done")

if __name__ == "__main__":
	main()
