from xbmc import executebuiltin, getCondVisibility, getInfoLabel
import xbmcgui
class GUI(xbmcgui.WindowXMLDialog):
	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)
	def onInit(self):
		self.PREVIOUS_MENU = [10]
		self.ACTION_NAV_BACK = [92]
		self.ACTION_SELECT_ITEM = [7]
	def onAction(self, action):
		if action in self.PREVIOUS_MENU:
			self.close()
		if action in self.ACTION_NAV_BACK:
			if getCondVisibility('Control.HasFocus(9210)'):
				self.close()
		if action in self.ACTION_SELECT_ITEM:
			pass
		if action.getButtonCode() == 259:
			if getCondVisibility('Control.HasFocus(9201)'):
				self.close()
				executebuiltin('ActivateWindow(1100)')
				executebuiltin('Dialog.Close(3000, false)')
				executebuiltin('RunScript(Special://scripts/XBMC4Gamers Extras/Insignia Info/resources/lib/update icons.py)')
	def onFocus(self, controlId):
		pass
	def onClick(self, controlId):
		pass