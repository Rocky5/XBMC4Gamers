# -*- coding: utf-8 -*-
'''
Mode:
	0 = change log.
	1 = Browse.
	2 = View logs.
'''
import os
import sys
import xbmc
import xbmcgui

LOG_PATH = 'E:/TDATA/Rocky5 needs these Logs/'

def view_file(file_path):
	if os.path.isfile(file_path):
		with open(file_path, "rb") as input_file:
			xbmcgui.Dialog().textviewer(os.path.basename(file_path), input_file.read())
	else:
		xbmcgui.Dialog().ok("Error", "Can't find changes.txt")

def browse_file():
	file_path = xbmcgui.Dialog().browse(1, "Select file to view", 'files', '')
	if os.path.isfile(file_path):
		with open(file_path, "rb") as text_viewer:
			xbmcgui.Dialog().textviewer(os.path.basename(file_path), text_viewer.read())

def view_logs():
	if not os.path.isdir(LOG_PATH):
		xbmcgui.Dialog().ok("ERROR", "Log directory does not exist.")
		return

	try:
		select_root = xbmcgui.Dialog().select("Select Dashboard", sorted(os.listdir(LOG_PATH)), 10000)
		if select_root == -1:
			return

		select_file = os.path.join(LOG_PATH, sorted(os.listdir(LOG_PATH))[select_root])
		if os.path.isdir(select_file) and os.listdir(select_file):
			select_root = xbmcgui.Dialog().select("Select Log File", sorted(os.listdir(select_file)), 10000)
			select_file = os.path.join(select_file, sorted(os.listdir(select_file))[select_root])
		else:
			xbmcgui.Dialog().ok("ERROR", "There are no logs to be viewed.", "", "This is a good thing.")
			return

		if select_root == -1 or select_file == -1:
			return

		if os.path.isfile(select_file):
			with open(select_file, "rb") as text_viewer:
				xbmcgui.Dialog().textviewer(os.path.basename(select_file), text_viewer.read())
	except Exception as e:
		xbmc.log("Failed to view logs: {}".format(e), xbmc.LOGERROR)

def main():
	mode = sys.argv[1]
	file_path = sys.argv[2] if len(sys.argv) > 2 else ""

	if mode == '0':
		view_file(file_path)
	elif mode == '1':
		browse_file()
	elif mode == '2':
		view_logs()
	else:
		xbmcgui.Dialog().ok("Error", "Invalid mode specified.")

if __name__ == "__main__":
	main()