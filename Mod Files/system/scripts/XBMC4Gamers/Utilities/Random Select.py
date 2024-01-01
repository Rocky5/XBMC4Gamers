from random import randrange
from xbmc import executebuiltin, getCondVisibility, getInfoLabel
# from xbmcgui import getCurrentWindowId
# from time import sleep
# used for random selection of a game on boot, waits till the window is ready.
# if getInfoLabel('Skin.HasSetting(Random_Game)') and getInfoLabel('Skin.HasSetting(run_random_script)') :
	# while True:
		# if not getCurrentWindowId() == 10101 and not getCurrentWindowId() == 10138:
			# break
	
# main part that does the selection
try:
	ID	= getInfoLabel('Container.Viewmode').split('view')[1]
	Get_Item_Count	= int(getInfoLabel('Container(' + ID + ').NumItems'))
	Random 			= str(randrange(0,Get_Item_Count,1))
	if getCondVisibility('Window.IsVisible(1)'):
		executebuiltin('SetFocus('+ID+','+Random+')')
	else:
		if Get_Item_Count >= 10:
			executebuiltin('SetFocus('+ID+','+Random+')')
except:
	pass

executebuiltin('Skin.SetBool(run_random_script,false)')