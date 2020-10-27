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
		self.control_id_button_button1	= 3000
		self.control_id_button_button2	= 3001
		self.control_id_button_button3	= 3002
		self.control_id_button_button4	= 3003
		# translation ids
		self.translation_id_button1			= 3101
		self.translation_id_button1_info	= 3102
		self.translation_id_button2			= 3103
		self.translation_id_button3			= 3104
		self.translation_id_button4			= 3105
		# set actions
		self.button_button1 = self.getControl(self.control_id_button_button1)
		self.button_button2 = self.getControl(self.control_id_button_button2)
		self.button_button3 = self.getControl(self.control_id_button_button3)
		self.button_button3 = self.getControl(self.control_id_button_button4)
		# translate buttons
		self.button_button1.setLabel(getLocalizedString(self.translation_id_button1))
		self.button_button2.setLabel(getLocalizedString(self.translation_id_button2))
		self.button_button3.setLabel(getLocalizedString(self.translation_id_button3))
		self.button_button3.setLabel(getLocalizedString(self.translation_id_button4))
	def onAction(self, action):
		if action in self.action_exitkeys_id:
			self.close()
	def onFocus(self, controlId):
		pass
	def onClick(self, controlId):			
		if controlId == self.control_id_button_button1:
			xbmcgui.Dialog().ok(getLocalizedString(self.translation_id_button1),"",getLocalizedString(self.translation_id_button1_info))
		if controlId == self.control_id_button_button2:
			xbmc.executebuiltin("RunScript("+Working_Directory+"\\resources\\lib\\default.py)")
		elif controlId == self.control_id_button_button3:
			xbmc.executebuiltin("RunScript("+Working_Directory+"\\resources\\lib\\default.py,1,0)")
		elif controlId == self.control_id_button_button4:
			os.remove(xbmc.translatePath("special://profile/favourites.xml"))
			xbmcgui.Dialog().ok('Done','','Removed favourites.xml')