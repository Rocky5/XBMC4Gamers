'''
	Script by Rocky5
	Use to clean the programs thumbnails. This is handy for updating thumbnails without having to do it manually.
'''
import os, sys
import xbmcgui, xbmcaddon
Addon = xbmcaddon.Addon('Clean Program Thumbs')
#####	Script constants
__scriptname__ = Addon.getAddonInfo('name')
__id__ = Addon.getAddonInfo('id')
__author__ = Addon.getAddonInfo('author')
__version__ = Addon.getAddonInfo('version')
__path__ = Addon.getAddonInfo('path')
getLocalizedString = Addon.getLocalizedString
getSetting = Addon.getSetting
print '[SCRIPT][%s] version %s initialized!' % (__scriptname__, __version__)
if (__name__ == "__main__"):
	import resources.lib.__init__ as __init__
	ui = __init__.GUI('%s.xml' %  "main",__path__, 'default')
	ui.doModal()
	print '[SCRIPT][%s] version %s exited!' % (__scriptname__, __version__)
	del ui
sys.modules.clear()