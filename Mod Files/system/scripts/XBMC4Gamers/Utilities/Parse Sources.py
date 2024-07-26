# Script by Rocky5
# Used to grab source names for the quick changer toggles

import os
import sys
import xbmc
import xbmcgui
import xml.etree.cElementTree as etree

def parse_sources(sources_xml):
	tree = etree.parse(sources_xml)
	root = tree.getroot()
	names = [name.find('name').text for name in root.findall('.//programs/source/[name]')]
	return names

def main():
	print "Parse Sources.py"
	arg = sys.argv[1:][0]
	sources_xml = "P:/Sources.xml"
	names = parse_sources(sources_xml)
	
	choice = xbmcgui.Dialog().select('Select Source', names, 10000)
	if choice != -1:
		xbmc.executebuiltin("Skin.SetString({}, {})".format(arg, names[choice]))
	else:
		xbmc.executebuiltin("Skin.Reset({}, {})".format(arg, names[choice]))

if __name__ == "__main__":
	main()