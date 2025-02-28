# -*- coding: utf-8 -*-
import os
import sys
import xbmc
import xbmcgui
import xml.etree.cElementTree as etree

SOURCES_XML_PATH = "P:/Sources.xml"

def parse_sources(sources_xml):
	try:
		tree = etree.parse(sources_xml)
		root = tree.getroot()
		names = [name.find('name').text for name in root.findall('.//programs/source/[name]')]
		return names
	except Exception as error:
		xbmc.log("Failed to parse sources XML: {}".format(error), xbmc.LOGERROR)
		return []

def main():
	print "Parse Sources.py"
	if len(sys.argv) < 2:
		xbmc.log("Argument missing: The script requires one argument.", xbmc.LOGERROR)
		return

	arg = sys.argv[1]
	names = parse_sources(SOURCES_XML_PATH)

	if names:
		choice = xbmcgui.Dialog().select('Select Source', names, 10000)
		if choice != -1:
			xbmc.executebuiltin("Skin.SetString({}, {})".format(arg, names[choice]))
		else:
			xbmc.executebuiltin("Skin.Reset({})".format(arg))
	else:
		xbmc.log("No sources found in the XML.", xbmc.LOGERROR)

if __name__ == "__main__":
	main()