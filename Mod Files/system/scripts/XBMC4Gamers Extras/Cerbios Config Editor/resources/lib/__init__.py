from xbmc import executebuiltin, getCondVisibility, getInfoLabel
import xbmcgui
class GUI(xbmcgui.WindowXMLDialog):
	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)
	def onInit(self):
		self.PREVIOUS_MENU = [10]
		self.ACTION_NAV_BACK = [92]
	def onAction(self, action):
		if action in self.PREVIOUS_MENU:
			self.close()
		if action in self.ACTION_NAV_BACK:
			self.close()
	def onFocus(self, controlId):
		pass
	def onClick(self, controlId):
		pass