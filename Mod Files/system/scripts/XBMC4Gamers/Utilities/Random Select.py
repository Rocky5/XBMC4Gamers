import xbmc
import xbmcgui

def wait_for_window_ready():
	while True:
		current_window_id = xbmcgui.getCurrentWindowId()
		if current_window_id not in [10101, 10138]:
			break

if __name__ == "__main__":
	# if xbmc.getInfoLabel('Skin.HasSetting(Random_Game)') and xbmc.getInfoLabel('Skin.HasSetting(run_random_script)'):
	wait_for_window_ready()
	xbmc.executebuiltin('RandomSelect()')
	xbmc.executebuiltin('Skin.SetBool(run_random_script,false)')
