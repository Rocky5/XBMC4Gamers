import os, xbmc, xbmcgui
show_dialog = 0
try:
	title	= sys.argv[1:][0]
except:
	title	= ""
try:
	line1	= sys.argv[2:][0]
except:
	line1	= ""
try:
	line2	= sys.argv[3:][0]
except:
	line2	= ""
try:
	line3	= sys.argv[4:][0]
except:
	line3	= ""

xbmcgui.Dialog().ok(title,line1,line2,line3)