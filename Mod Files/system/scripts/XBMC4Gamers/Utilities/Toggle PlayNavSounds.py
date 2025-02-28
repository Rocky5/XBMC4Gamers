import xbmc
if xbmc.getCondVisibility('system.getbool(lookandfeel.soundsduringplayback)'):
	xbmc.executehttpapi('SetGUISetting(1;lookandfeel.soundsduringplayback;False)')
else:
	xbmc.executehttpapi('SetGUISetting(1;lookandfeel.soundsduringplayback;True)')