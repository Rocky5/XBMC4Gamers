# -*- coding: utf-8 -*-
'''
Mode:
	0 = change log.
	1 = Browse.
	2 = View logs.
'''
from os.path import basename, isdir, isfile, join
from os import listdir
from sys import argv
from xbmc import executebuiltin, log, LOGERROR
from xbmcgui import Dialog

LOG_PATH = 'E:/TDATA/Rocky5 needs these Logs/'

def view_file(file_path):
	if isfile(file_path):
		with open(file_path, "rb") as input_file:
			Dialog().textviewer(basename(file_path), input_file.read())
	else:
		Dialog().ok("Error", "Can't find changes.txt")

def browse_file():
	file_path = Dialog().browse(1, "Select file to view", 'files', '')
	if isfile(file_path):
		with open(file_path, "rb") as text_viewer:
			Dialog().textviewer(basename(file_path), text_viewer.read())

def view_logs():
	if not isdir(LOG_PATH):
		Dialog().ok("ERROR", "Log directory does not exist.")
		return

	try:
		select_root = Dialog().select("Select Dashboard", sorted(listdir(LOG_PATH)), 10000)
		if select_root == -1:
			return

		select_file = join(LOG_PATH, sorted(listdir(LOG_PATH))[select_root])
		if isdir(select_file) and listdir(select_file):
			select_root = Dialog().select("Select Log File", sorted(listdir(select_file)), 10000)
			select_file = join(select_file, sorted(listdir(select_file))[select_root])
		else:
			Dialog().ok("ERROR", "There are no logs to be viewed.", "", "This is a good thing.")
			return

		if select_root == -1 or select_file == -1:
			return

		if isfile(select_file):
			with open(select_file, "rb") as text_viewer:
				Dialog().textviewer(basename(select_file), text_viewer.read())
	except Exception as error:
		log("Failed to view logs: {}".format(error), LOGERROR)

def main():
	# Close the script loading dialog
	executebuiltin('Dialog.Close(1100,false)')
	mode = argv[1]
	file_path = argv[2] if len(argv) > 2 else ""

	if mode == '0':
		view_file(file_path)
	elif mode == '1':
		browse_file()
	elif mode == '2':
		view_logs()
	else:
		Dialog().ok("Error", "Invalid mode specified.")

if __name__ == "__main__":
	main()