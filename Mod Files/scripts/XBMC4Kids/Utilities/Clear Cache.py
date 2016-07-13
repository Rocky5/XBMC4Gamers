###################################################################
#
#   my_wipecache v0.0.0
#   by AMaNO
#   A simple cache file and drive clearing system
#
#	Added to by Rocky5
#
#	Added progress dialogue
#
###################################################################

import os
import xbmcgui
import xbmc
import time
from os.path import join

pDialog = xbmcgui.DialogProgress()
pDialog.create('Clearing Cache', 'Please wait.')

for root, dirs, files in os.walk("E:\\Cache\\", topdown=False):
	for name in files:
		os.remove(join(root, name))
	for name in dirs:
		os.rmdir(join(root, name))

pDialog.update(10, 'Clearing E:\Cache\\')
time.sleep(0.2)

for root, dirs, files in os.walk("X:\\", topdown=False):
	for name in files:
		os.remove(join(root, name))
	for name in dirs:
		os.rmdir(join(root, name))

pDialog.update(40, 'Clearing X:\\')
time.sleep(0.2)

for root, dirs, files in os.walk("Y:\\", topdown=False):
	for name in files:
		os.remove(join(root, name))
	for name in dirs:
		os.rmdir(join(root, name))

pDialog.update(60, 'Clearing Y:\\')
time.sleep(0.2)
		
for root, dirs, files in os.walk("Z:\\", topdown=False):
	for name in files:
		os.remove(join(root, name))
	for name in dirs:
		os.rmdir(join(root, name))

pDialog.update(80, 'Clearing Z:\\')
time.sleep(0.2)
pDialog.update(100, 'Done')
time.sleep(2)