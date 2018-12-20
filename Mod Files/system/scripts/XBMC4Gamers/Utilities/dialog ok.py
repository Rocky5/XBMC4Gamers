'''
	Script by Rocky5
	Used to display a dialog ok window for giving information on some toggle
'''
import os, xbmc, xbmcgui
#####	Start markings for the log file.
print "| dialog_ok.py loaded."
show_dialog = 0
try:
	setting	= sys.argv[1:][0]
except:
	setting	= ""
try:
	title	= sys.argv[2:][0]
except:
	title	= ""
try:
	line1	= sys.argv[3:][0]
except:
	line1	= ""
try:
	line2	= sys.argv[4:][0]
except:
	line2	= ""
try:
	line3	= sys.argv[5:][0]
except:
	line3	= ""
show_dialog = setting.split('-')[1]
if setting.startswith("show_enabled"):
	if xbmc.getCondVisibility('Skin.HasSetting('+show_dialog+')'):
		xbmcgui.Dialog().ok( title,line1,line2,line3 )
elif setting.startswith("show_disabled"):
	if not xbmc.getCondVisibility('Skin.HasSetting('+show_dialog+')'):
		xbmcgui.Dialog().ok( title,line1,line2,line3 )
elif setting.startswith("show_both"):
	xbmcgui.Dialog().ok( title,line1,line2,line3 )

