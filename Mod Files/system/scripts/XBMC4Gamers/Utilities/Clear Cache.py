'''
   A simple cache cleaning script
'''

import os
import xbmcgui
import xbmc
import time
from os.path import join

def clear_cache(drive, progress, update_value):
	try:
		for root, dirs, files in os.walk(drive, topdown=False):
			for name in files:
				os.remove(join(root, name))
			for name in dirs:
				os.rmdir(join(root, name))
		progress.update(update_value, '', 'Clearing {}'.format(drive))
		time.sleep(0.1)
	except:
		pass

def main():
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Clearing Cache', '', 'Please wait.')
	pDialog.update(0)

	drives = ["E:\\Cache\\", "X:\\", "Y:\\", "Z:\\"]
	update_values = [25, 50, 75, 100]

	for drive, update_value in zip(drives, update_values):
		clear_cache(drive, pDialog, update_value)

	pDialog.update(100, '', 'Done')
	time.sleep(1)
	pDialog.close()

if __name__ == "__main__":
	# Close the script loading dialog
	xbmc.executebuiltin('Dialog.Close(1100,false)')
	main()
