import os, time, xbmc, xbmcgui

## Updated by Rocky5 to add dynamic extensions and other stuff

filename	= xbmc.getInfoLabel( 'Skin.String(selectedintrofile)' )
Extensions	= [ "avi","mp4","wmv","xmv" ]
intro_found = 0

if filename.endswith(tuple(Extensions)):
	isplayed = xbmc.getInfoLabel( "Window(Home).Property(intro.isplayed)" ).lower() == "true"
	winPrograms = xbmc.getCondVisibility( 'Window.IsVisible(Programs)' )

	if not isplayed or winPrograms:
		ReplaceWindowHome = not winPrograms
		print "XBMC Intro Movie"

		if filename.endswith("xmv") or filename.endswith("mp4"):
			print "dvdplayer"
			player = xbmc.Player( xbmc.PLAYER_CORE_DVDPLAYER )
		else:
			print "mplayer"
			player = xbmc.Player( xbmc.PLAYER_CORE_MPLAYER )
		player.play( filename )
		xbmcgui.Window( 10000 ).setProperty( "intro.isplayed", "true" )

		if ReplaceWindowHome:
			xbmc.sleep( 500 )

			while player.isPlaying():
				#continue
				time.sleep( .2 )

			xbmc.executebuiltin( "RunScript( Special://xbmc/system/scripts/XBMC4Gamers/Utilities/Update Checker.py )" )

			xbmc.sleep( 1000 )
			intro_found = 1
			if str(  xbmc.getCondVisibility( 'Skin.HasSetting(Use_Startup_Playback)' ) ) == "1":
				print "worked"
				xbmc.executebuiltin( 'PlayMedia(' + xbmc.getInfoLabel( 'Skin.String(Startup_Playback_Path)' ) + ')' )
		
if not intro_found: xbmc.executebuiltin( "RunScript( Special://xbmc/system/scripts/XBMC4Gamers/Utilities/Update Checker.py )" )



'''
Original script from here: https://web.archive.org/web/20140712122422/http://passion-xbmc.org/addons/?Page=View&ID=script.xbmc.intro.movie
'''