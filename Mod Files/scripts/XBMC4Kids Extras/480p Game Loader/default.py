'''
	Script by Rocky5
	This is used to add a workaround to stubborn games that will not display properly in 480p on v1.6 Xbox.
	
	Update: 03 September 2016
	-- New front end for the scripts, it's a nice little menu for Auto Install, Manual Install or Unisntall.
	   Also updated the error logging and the all round functionality.
	   Added Tony Hawks 3.
'''


import os, sys
import xbmcgui, xbmcaddon
import zipfile


Addon = xbmcaddon.Addon('480p Game Loader')

#####	Script constants
__scriptname__ = Addon.getAddonInfo('name')
__id__ = Addon.getAddonInfo('id')
__author__ = Addon.getAddonInfo('author')
__version__ = Addon.getAddonInfo('version')
__path__ = Addon.getAddonInfo('path')

getLocalizedString = Addon.getLocalizedString
getSetting = Addon.getSetting

print '[SCRIPT][%s] version %s initialized!' % (__scriptname__, __version__)


#####	extract the loaders.zip on first run.
if os.path.isfile( __path__ + "\\resources\\lib\\loaders.zip" ): 
	xbmcgui.Dialog().ok( "Set-up","","I need to extract the loader xbe files before I can do anything.","This only happens once." )
	with zipfile.ZipFile( __path__ + "\\resources\\lib\\loaders.zip" ) as zf:
		zf.extractall( __path__ + "\\resources\\lib\\" )
	os.remove( __path__ + "\\resources\\lib\\loaders.zip" )
	
if os.path.isdir( __path__ + "\\resources\\lib\\loaders" ): 
	if (__name__ == "__main__"):
		import resources.lib.__init__ as __init__
		ui = __init__.GUI('%s.xml' % "main", __path__, 'default')
		ui.doModal()
		print '[SCRIPT][%s] version %s exited!' % (__scriptname__, __version__)
		del ui
else:
	xbmcgui.Dialog().ok( "Error","","The loaders folder is missing, please reinstall this script." )


sys.modules.clear()