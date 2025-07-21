import os, sys, glob
import xbmcgui, xbmcaddon
Addon = xbmcaddon.Addon('Run Artwork Installer')
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
	xbmc.executebuiltin('Skin.SetBool(ArtworkInstallerHeader)')
	# Close the script loading dialog
	xbmc.executebuiltin('Dialog.Close(1100,false)')
	ui.doModal()
	del ui
	xbmc.executebuiltin('Skin.Reset(ArtworkInstallerHeader)')