import hashlib
import os
import xbmc
import xbmcgui

def calculate_sha256(file_path):
	global Not_Cancelled
	filesize = os.path.getsize(file_path)
	hash = hashlib.sha256()
	read_buffer = 1024 * 1024 * 5
	percent = 0
	current_data = 0
	pDialog.create("Calculating sha256", "This can take some time, please be patient.")

	with open(file_path, "rb", buffering=read_buffer) as f:
		while True:
			if not pDialog.iscanceled():
				data = f.read(read_buffer)
				hash.update(data)
				current_data += len(data)
				pDialog.update( (100 * current_data / filesize),os.path.basename(file_path),"This can take some time, please be patient." )
				if not data:
					break
			else:
				Not_Cancelled = 0
				break
	
	return hash.hexdigest()

def main():
	select_file = Dialog.browse(1, "Select file to hash", 'files', '')
	
	if select_file:
		hash_value = calculate_sha256(select_file)
		
		if Not_Cancelled:
			with open("E:\\sha256hash.txt", "w") as output:
				output.write(hash_value)
			
			Dialog.ok("", "Hash:", hash_value)

if __name__ == "__main__":
	Dialog = xbmcgui.Dialog()
	pDialog = xbmcgui.DialogProgress()
	Not_Cancelled = 1
	main()
