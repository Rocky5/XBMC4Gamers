import xbmcgui
class GUI(xbmcgui.WindowXMLDialog):
	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)
	def onInit(self):
		self.action_exitkeys_id = [10, 92]
	def onAction(self, action):
		if action in self.action_exitkeys_id:
			self.close()
	def onFocus(self, controlId):
		pass
	def onClick(self, controlId):
		pass