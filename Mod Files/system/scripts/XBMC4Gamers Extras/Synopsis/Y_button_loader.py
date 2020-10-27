import os,xbmc,xbmcgui
if os.path.isfile(xbmc.getInfoLabel('ListItem.FolderPath')):
	xbmc.executebuiltin('RunScript(Special://xbmc/system/scripts/XBMC4Gamers Extras/Synopsis/default.py)')
	xbmc.executebuiltin('ActivateWindow(1100)')
	# xbmc.executebuiltin('Skin.Reset(synopsis_first_run)')