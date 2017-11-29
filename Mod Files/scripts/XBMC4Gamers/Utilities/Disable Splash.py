'''
	Script by Rocky5
	Used to Disable the Splash
'''
import os, xbmc, xbmcgui

if str( xbmc.getCondVisibility( 'Skin.HasSetting(introenabled)' ) ) == "1":
	with open('Q:\\nosplash.bin', 'w') as nosplash: nosplash.write( '' )
else:
	if os.path.isfile('Q:\\nosplash.bin'): os.remove('Q:\\nosplash.bin')