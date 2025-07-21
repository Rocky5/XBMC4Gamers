from datetime import datetime
from os.path import exists, join
from os import makedirs
from xbmc import executebuiltin, executehttpapi, getInfoLabel
import xbmcgui

folder = 'Q:/system/screenshots/'
filename = 'Screenshot-{}.png'.format(datetime.now().strftime("%Y-%m-%d--%H-%M-%S"))

flash = 1
rotate = 0
width = getInfoLabel('System.ScreenWidth')
height = getInfoLabel('System.ScreenHeight')
quality = 100

if not exists(folder):
	makedirs(folder)

executehttpapi('TakeScreenshot({}, {}, {}, {}, {}, {})'.format(join(folder, filename), flash, rotate, width, height, quality))

executebuiltin('Notification(Screenshot Saved, {})'.format(filename))