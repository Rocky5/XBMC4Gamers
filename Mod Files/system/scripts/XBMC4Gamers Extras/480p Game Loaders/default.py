'''
	Script by Rocky5
	This is used to add a workaround to stubborn games that will not display properly in 480p on v1.6 Xbox.
'''
import os, sys
import xbmcgui, xbmcaddon
import zipfile
#####	Modules required
limpp	= xbmc.translatePath("special://xbmc/system/scripts/_modules/script.module.limpp")
xbeinfo	= xbmc.translatePath("special://xbmc/system/scripts/_modules/script.module.xbeinfo")
Addon = xbmcaddon.Addon('480p Game Loaders')
#####	Script constants
__scriptname__ = Addon.getAddonInfo('name')
__id__ = Addon.getAddonInfo('id')
__author__ = Addon.getAddonInfo('author')
__version__ = Addon.getAddonInfo('version')
__path__ = Addon.getAddonInfo('path')
getLocalizedString = Addon.getLocalizedString
getSetting = Addon.getSetting
print '[SCRIPT][%s] version %s initialized!' % (__scriptname__, __version__)
#####	Check for modules I need and error if not found.
# Close the script loading dialog
xbmc.executebuiltin('Dialog.Close(1100,false)')
if os.path.isdir(limpp):
	if os.path.isdir(xbeinfo):
		#####	Extract the loaders.zip on first run.
		if os.path.isfile(__path__+"\\resources\\lib\\loaders.zip"): 
			xbmcgui.Dialog().ok("Set-up","","I need to extract the loader xbe files before I can do anything.","This only happens once.")
			with zipfile.ZipFile(__path__+"\\resources\\lib\\loaders.zip") as zf:
				zf.extractall(__path__+"\\resources\\lib\\")
			os.remove(__path__+"\\resources\\lib\\loaders.zip")
		#####	Main section.
		if os.path.isdir(__path__+"\\resources\\lib\\loaders"): 
			if (__name__ == "__main__"):
				import resources.lib.__init__ as __init__
				ui = __init__.GUI('%s.xml' % "main", __path__, 'default')
				ui.doModal()
				del ui
		else:
			xbmcgui.Dialog().ok("Error","","The loaders folder is missing, please reinstall this script.")
	else:
		xbmcgui.Dialog().ok("Error","","Module is missing.","[B]script.module.xbeinfo[/B]")
else:
	xbmcgui.Dialog().ok("Error","","Module is missing.","[B]script.module.limpp[/B]")