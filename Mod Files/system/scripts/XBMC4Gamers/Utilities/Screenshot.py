import datetime, os, xbmc, xbmcgui
folder		= 'Q:/system/screenshots/'
filename	= 'Screenshot-'+str(datetime.datetime.now()).replace(':','-').replace(' ','--')[:-7]+'.jpg'
flash		= 1
rotate		= 0
width		= xbmc.getInfoLabel('System.ScreenWidth')
height		= xbmc.getInfoLabel('System.ScreenHeight')
qaulity		= 100
if not os.path.exists(folder): os.mkdir(folder)
xbmc.executehttpapi('TakeScreenshot('+folder+filename+','+str(flash)+','+str(rotate)+','+str(width)+','+str(height)+','+str(qaulity)+')')