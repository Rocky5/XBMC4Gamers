import datetime
import os
import xbmc
import xbmcgui

folder = 'Q:/system/screenshots/'
filename = 'Screenshot-{}.png'.format(datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S"))

flash = 1
rotate = 0
width = xbmc.getInfoLabel('System.ScreenWidth')
height = xbmc.getInfoLabel('System.ScreenHeight')
quality = 100

if not os.path.exists(folder):
	os.makedirs(folder)

xbmc.executehttpapi('TakeScreenshot({}, {}, {}, {}, {}, {})'.format(os.path.join(folder, filename), flash, rotate, width, height, quality))

xbmc.executebuiltin('Notification(Screenshot Saved, {})'.format(filename))