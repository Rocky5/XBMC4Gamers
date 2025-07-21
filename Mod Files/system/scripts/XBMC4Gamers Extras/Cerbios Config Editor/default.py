import os, sys, glob
import xbmcgui, xbmcaddon

Addon = xbmcaddon.Addon('Cerbios Config Editor')
ini_file = "E:\\Cerbios\\cerbios.ini"

__scriptname__ = Addon.getAddonInfo('name')
__id__ = Addon.getAddonInfo('id')
__author__ = Addon.getAddonInfo('author')
__version__ = Addon.getAddonInfo('version')
__path__ = Addon.getAddonInfo('path')

print '[SCRIPT][%s] version %s initialized!' % (__scriptname__, __version__)

if __name__ == "__main__":
	import resources.lib.__init__ as __init__
	ui = __init__.GUI('%s.xml' % "main", __path__, 'default')

	execfile(os.path.join(__path__, "resources", "lib", "config_edit.py"))

	if os.path.isfile(ini_file):
		ui.doModal()
		del ui