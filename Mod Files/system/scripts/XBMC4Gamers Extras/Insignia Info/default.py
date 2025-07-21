'''
	Script by Rocky5 to parse insignias data.
'''
from xbmc import executebuiltin
import xbmcaddon
import resources.lib.__init__ as addon_init

Addon = xbmcaddon.Addon('Insignia Info')
__scriptname__ = Addon.getAddonInfo('name')
__version__ = Addon.getAddonInfo('version')
__path__ = Addon.getAddonInfo('path')
print "[SCRIPT][{}] version {} initialized!".format(__scriptname__, __version__)

if __name__ == "__main__":
	ui = addon_init.GUI('%s.xml' % "main", __path__, xbmc.getSkinDir())
	# Close fake loading dialog
	executebuiltin('Dialog.Close(All, true)')
	ui.doModal()
	del ui