'''	
	Script by Rocky5
	Used to grab source names for the quick changer toggles
'''
print "| Scripts\XBMC4Gamers\Utilities\Parse Sources.py loaded."
import os,sys,xbmc,xbmcgui
import xml.etree.cElementTree as etree
args = sys.argv[1:][0]
sourcesXML = "P:/Sources.xml"
names = []
tree = etree.parse(sourcesXML)
root = tree.getroot()
for name in root.findall('.//programs/source/[name]'):
	for found in [name.find('name')]:
		names.append(found.text)
choice = xbmcgui.Dialog().select('Select Source',names,10000)
if choice == -1:
	pass
else:
	xbmc.executebuiltin("Skin.SetString("+args+","+names[choice]+")")