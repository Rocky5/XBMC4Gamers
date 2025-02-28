import xbmc
if xbmc.getCondVisibility('system.getbool(lookandfeel.enablerssfeeds)'):
	xbmc.executehttpapi('SetGUISetting(1;lookandfeel.enablerssfeeds;False)')
else:
	xbmc.executehttpapi('SetGUISetting(1;lookandfeel.enablerssfeeds;True)')