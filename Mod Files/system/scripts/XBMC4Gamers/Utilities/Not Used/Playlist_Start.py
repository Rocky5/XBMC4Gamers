'''
	Script by Rocky5
	Used to start a playlist shuffled & fix shuddering of intro video on startup.
'''
import time, xbmc
print "loaded startup playlist script"
if xbmc.getCondVisibility('Skin.HasSetting(Use_Startup_Playback)') and not xbmc.getInfoLabel('currentwindow') == "1116":
	time.sleep(0.5)
	xbmc.executebuiltin('PlayMedia('+xbmc.getInfoLabel('Skin.String(Startup_Playback_Path)')+')')
	xbmc.PlayList(0).shuffle()
	xbmc.executebuiltin('playercontrol(RepeatAll)')