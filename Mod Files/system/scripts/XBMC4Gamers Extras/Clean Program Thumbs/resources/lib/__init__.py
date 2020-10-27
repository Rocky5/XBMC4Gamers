import os, sys
import xbmc, xbmcgui
Working_Directory	= os.getcwd()+"\\"
getLocalizedString = sys.modules['__main__'].getLocalizedString
class GUI(xbmcgui.WindowXMLDialog):
	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)
	def onInit(self):
		self.action_exitkeys_id = [10, 92]
		# get control ids
		self.control_id_button_button1 = 3000
		self.control_id_button_button2 = 3001
		self.control_id_button_button3 = 3002
		# translation ids
		self.translation_id_button1 = 3101
		self.translation_id_button2 = 3102
		self.translation_id_button3 = 3103
		# set actions
		self.button_button1 = self.getControl(self.control_id_button_button1)
		self.button_button2 = self.getControl(self.control_id_button_button2)
		self.button_button3 = self.getControl(self.control_id_button_button3)
		# translate buttons
		self.button_button1.setLabel(getLocalizedString(self.translation_id_button1))
		self.button_button2.setLabel(getLocalizedString(self.translation_id_button2))
		self.button_button3.setLabel(getLocalizedString(self.translation_id_button3))
	def onAction(self, action):
		if action in self.action_exitkeys_id:
			self.close()
	def onFocus(self, controlId):
		pass
	def onClick(self, controlId):
		if controlId == self.control_id_button_button1:
			auto()
		elif controlId == self.control_id_button_button2:
			manual()
		elif controlId == self.control_id_button_button3:
			uninstall()
def auto():
	xbmc.executebuiltin("RunScript("+Working_Directory+"\\resources\\lib\\default.py)")
def manual():
	xbmc.executebuiltin("RunScript("+Working_Directory+"\\resources\\lib\\default.py,1,0)")
def uninstall():
	xbmc.executebuiltin("RunScript("+Working_Directory+"\\resources\\lib\\default.py,0,1)")