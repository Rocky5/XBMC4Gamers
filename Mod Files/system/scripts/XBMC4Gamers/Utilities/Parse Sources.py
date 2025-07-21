# -*- coding: utf-8 -*-
from sys import argv
from xbmc import executebuiltin, log, LOGERROR
from xbmcgui import Dialog
import xml.etree.cElementTree as etree

SOURCES_XML_PATH = "P:/Sources.xml"

def parse_sources(sources_xml):
	try:
		tree = etree.parse(sources_xml)
		root = tree.getroot()
		names = [name.find('name').text for name in root.findall('.//programs/source/[name]')]
		return names
	except Exception as error:
		log("Failed to parse sources XML: {}".format(error), LOGERROR)
		return []

def main():
	print "Parse Sources.py"
	if len(argv) < 2:
		log("Argument missing: The script requires one argument.", LOGERROR)
		return

	arg = argv[1]
	names = parse_sources(SOURCES_XML_PATH)

	if names:
		choice = Dialog().select('Select Source', names, 10000)
		if choice != -1:
			executebuiltin("Skin.SetString({}, {})".format(arg, names[choice]))
		else:
			executebuiltin("Skin.Reset({})".format(arg))
	else:
		log("No sources found in the XML.", LOGERROR)

if __name__ == "__main__":
	# Close the script loading dialog
	executebuiltin('Dialog.Close(1100,true)')
	main()