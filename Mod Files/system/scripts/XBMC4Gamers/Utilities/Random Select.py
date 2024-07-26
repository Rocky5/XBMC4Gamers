from random import randrange
import xbmc
import xbmcgui

def wait_for_window_ready():
	while True:
		current_window_id = xbmcgui.getCurrentWindowId()
		if current_window_id not in [10101, 10138]:
			break

def select_random_game():
	try:
		ID = xbmc.getInfoLabel('Container.Viewmode').split('view')[1]
		item_count = int(xbmc.getInfoLabel('Container(' + ID + ').NumItems'))
		random_index = str(randrange(0, item_count, 1))
		
		if xbmc.getCondVisibility('Window.IsVisible(1)') or item_count >= 10:
			xbmc.executebuiltin('SetFocus(' + ID + ',' + random_index + ')')
	except:
		pass

if __name__ == "__main__":
	# if xbmc.getInfoLabel('Skin.HasSetting(Random_Game)') and xbmc.getInfoLabel('Skin.HasSetting(run_random_script)'):
		# wait_for_window_ready()
	select_random_game()
	xbmc.executebuiltin('Skin.SetBool(run_random_script,false)')
