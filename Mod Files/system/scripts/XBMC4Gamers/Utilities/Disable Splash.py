'''
	Script by Rocky5
	Used to Disable the Splash
'''
import os, xbmc, xbmcgui

if str( xbmc.getCondVisibility( 'Skin.HasSetting(introenabled)' ) ) == "1":
	if os.path.isfile('Q:\\system\\toggles\\no splash.disabled'):
		os.rename('Q:\\system\\toggles\\no splash.disabled','Q:\\system\\toggles\\no splash.enabled')
	else:
		with open('Q:\\system\\toggles\\no splash.enabled', 'wb') as nosplash: nosplash.write( '' )
else:
	if os.path.isfile('Q:\\system\\toggles\\no splash.disabled'):
		pass
	else:
		if os.path.isfile('Q:\\system\\toggles\\no splash.enabled'): os.rename('Q:\\system\\toggles\\no splash.enabled','Q:\\system\\toggles\\no splash.disabled')