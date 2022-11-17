'''
	Script by Rocky5
	Extracts information from a file named default.xml located in the '_resources' folder.
'''
import fileinput,glob,os,shutil,socket,sys,time,xbmc,xbmcgui
from BeautifulSoup import *
windowdialog = xbmcgui.WindowXMLDialog
#windowdialog = xbmcgui.WindowXML
# Check if audio is playing when entering synopsis and store if true.
if xbmc.getCondVisibility('Player.HasAudio'):
	Music_Playing = 1
else:
	Music_Playing = 0
#####	Sets paths & other crap.
Current_Window					= xbmcgui.Window(xbmcgui.getCurrentWindowId())
Working_Directory				= os.getcwd()+'\\resources\\'
GetInfoPath						= xbmc.getInfoLabel('ListItem.Path')
GameName						= xbmc.getInfoLabel('ListItem.Label')
GameXBE							= xbmc.getInfoLabel('listitem.FileNameAndPath')
_Resources_Path					= GetInfoPath+'_resources'
_Resources_Default_xml			= os.path.join(_Resources_Path, 'default.xml')
_Resources_Screenshots			= os.path.join(_Resources_Path, 'screenshots')
_Resources_Preview				= os.path.join(_Resources_Path, 'media')
_Resources_Artwork				= os.path.join(_Resources_Path, 'artwork')
Preview_default					= GetInfoPath+'preview.xmv'
Preview_ext						= xbmc.getInfoLabel('Skin.String(PreviewFileExtension)')
Preview_alt						= GetInfoPath+'Preview.'+Preview_ext
Video_Played					= 0
CachedThumb						= xbmc.translatePath('special://profile/Thumbnails/Programs/%s/%s' % (xbmc.getCacheThumbName(xbmc.getInfoLabel('ListItem.FolderPath'))[0], xbmc.getCacheThumbName(xbmc.getInfoLabel('ListItem.FolderPath'))))
Font_Path1						= xbmc.translatePath('Special://skin/1080i/Font.xml')
Font_Path2						= xbmc.translatePath('Special://skin/xml/Font.xml')
Font_Path3						= xbmc.translatePath('Special://skin/NTSC/Font.xml')
Font_Path4						= xbmc.translatePath('Special://skin/NTSC 16x9/Font.xml')
Font_Path5						= xbmc.translatePath('Special://skin/PAL/Font.xml')
Font_Path6						= xbmc.translatePath('Special://skin/PAL 16x9/Font.xml')
def synopsis_mode_video():
	#####	Check for Preview files.
	PreviewFile = "0"
	for root, dirs, files in os.walk(_Resources_Preview):
		for filename in files:
			PreviewFile = root+'\\'+filename
			Current_Window.setProperty('Synopsis_Video_Preview_Path', PreviewFile)
			Current_Window.setProperty('Synopsis_Video_Preview_Name', "Found "+filename)
	if PreviewFile == "0":
		xbmc.executebuiltin('Skin.Reset(SynopsisPreviewThere)')
	else:
		if PreviewFile.endswith('.xmv'):
			Current_Window.setProperty('Player_Type','DVDPlayer')
			xbmc.executebuiltin('Skin.SetBool(SynopsisPreviewThere)')
		elif PreviewFile.endswith('.strm'):
			try:
				socket.setdefaulttimeout(3.0)
				socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
				Current_Window.setProperty('Player_Type','MPlayer')
				xbmc.executebuiltin('Skin.SetBool(SynopsisPreviewThere)')
			except socket.error as ex:
				xbmc.executebuiltin('Skin.Reset(SynopsisPreviewThere)')
		else:
			Current_Window.setProperty('Player_Type','MPlayer')
			xbmc.executebuiltin('Skin.SetBool(SynopsisPreviewThere)')
def synopsis_mode_images():
	#####	Check for assets files.
	if os.path.isfile(os.path.join(_Resources_Artwork,'alt_synopsis.jpg')):
		Current_Window.setProperty('Alt_Synopsis_icon', os.path.join(_Resources_Artwork,'alt_synopsis.jpg'))
	else:
		Current_Window.setProperty('Alt_Synopsis_icon', os.path.join(_Resources_Artwork,'poster.jpg'))
	if os.path.isfile(os.path.join(_Resources_Artwork,'banner.png')):
		Current_Window.setProperty('Synopsis_banner', os.path.join(_Resources_Artwork,'banner.png'))
	if os.path.isfile(os.path.join(_Resources_Artwork,'cd.png')):
		Current_Window.setProperty('Synopsis_disc', os.path.join(_Resources_Artwork,'cd.png'))
	if os.path.isfile(os.path.join(_Resources_Artwork,'fanart.jpg')):
		Current_Window.setProperty('Synopsis_fanart', os.path.join(_Resources_Artwork,'fanart.jpg'))
	if os.path.isfile(os.path.join(_Resources_Artwork,'fanart-blur.jpg')):
		Current_Window.setProperty('Synopsis_fanart_blur', os.path.join(_Resources_Artwork,'fanart-blur.jpg'))
	if os.path.isfile(os.path.join(_Resources_Artwork,'fog.jpg')):
		Current_Window.setProperty('Synopsis_fog', os.path.join(_Resources_Artwork,'fog.jpg'))
	if os.path.isfile(os.path.join(_Resources_Artwork,'poster.jpg')):
		Current_Window.setProperty('Synopsis_poster', os.path.join(_Resources_Artwork,'poster.jpg'))
	if os.path.isfile(os.path.join(_Resources_Artwork,'poster_small_blurred.jpg')):
		Current_Window.setProperty('Synopsis_poster_small', os.path.join(_Resources_Artwork,'poster_small_blurred.jpg'))
	elif os.path.isfile(os.path.join(_Resources_Artwork,'poster_small.jpg')):
		Current_Window.setProperty('Synopsis_poster_small', os.path.join(_Resources_Artwork,'poster_small.jpg'))
	else:
		Current_Window.setProperty('Synopsis_poster_small', os.path.join(_Resources_Artwork,'poster.jpg'))
	if os.path.isfile(os.path.join(_Resources_Artwork,'synopsis.png')):
		Current_Window.setProperty('Synopsis_icon', os.path.join(_Resources_Artwork,'synopsis.png'))
	#####	Get screenshots, xbe and cached thumb	
	Current_Window.setProperty('Synopsis_screenshots', _Resources_Screenshots)
	Current_Window.setProperty('Synopsis_xbe', GameXBE)
	Current_Window.setProperty('Synopsis_thumb', CachedThumb)
def synopsis_mode_text():
	#####	Read XML & set
	if os.path.isfile(_Resources_Default_xml):
		xbmc.executebuiltin('Skin.Reset(nodefaultxml)')
		Synopsis_XML = open(_Resources_Default_xml, 'r').read()
		Output = BeautifulSoup(Synopsis_XML)
		try: # Title
			Current_Window.setProperty('Synopsis_title', Output.title.string.replace('&amp;','&'))
			Current_Window.setProperty('Synopsis_title_alt', Output.title.string.replace('&amp;','&'))
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Developer
			Current_Window.setProperty('Synopsis_developer', Output.developer.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Publisher
			Current_Window.setProperty('Synopsis_publisher', Output.publisher.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Features General
			Current_Window.setProperty('Synopsis_features_general', Output.features_general.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: #  Features Online
			Current_Window.setProperty('Synopsis_features_online', Output.features_online.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # ESRB Rating
			Current_Window.setProperty('Synopsis_esrb', Output.esrb.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # ESRB Descriptors
			Current_Window.setProperty('Synopsis_esrb_descriptors', Output.esrb_descriptors.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Genre
			Current_Window.setProperty('Synopsis_genre', Output.genre.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Release Date
			Current_Window.setProperty('Synopsis_release_date', Output.release_date.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # GameRating
			Current_Window.setProperty('Synopsis_rating', Output.rating.string)
			if "0" <= Output.rating.string < "1":
				Current_Window.setProperty('Synopsis_rating_alt', "0")
			if "1" <= Output.rating.string < "2":
				Current_Window.setProperty('Synopsis_rating_alt', "1")
			if "2" <= Output.rating.string < "3":
				Current_Window.setProperty('Synopsis_rating_alt', "2")
			if "3" <= Output.rating.string < "4":
				Current_Window.setProperty('Synopsis_rating_alt', "3")
			if "4" <= Output.rating.string < "5":
				Current_Window.setProperty('Synopsis_rating_alt', "4")
			if "5" <= Output.rating.string < "6":
				Current_Window.setProperty('Synopsis_rating_alt', "5")
			if "6" <= Output.rating.string < "7":
				Current_Window.setProperty('Synopsis_rating_alt', "6")
			if "7" <= Output.rating.string < "8":
				Current_Window.setProperty('Synopsis_rating_alt', "7")
			if "8" <= Output.rating.string < "9":
				Current_Window.setProperty('Synopsis_rating_alt', "8")
			if "9" <= Output.rating.string <= "9.9":
				Current_Window.setProperty('Synopsis_rating_alt', "9")
			if "10" <= Output.rating.string <= "10.9":
				Current_Window.setProperty('Synopsis_rating_alt', "10")
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Platform
			Current_Window.setProperty('Synopsis_platform', Output.platform.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Exclusive
			Current_Window.setProperty('Synopsis_exclusive', Output.exclusive.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Title ID
			Current_Window.setProperty('Synopsis_titleid', Output.titleid.string)
			Current_Window.setProperty('Synopsis_titleid_alt', Output.titleid.string)
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Overview
			Current_Window.setProperty('Synopsis_overview', Output.overview.string)
			Current_Window.setProperty('Synopsis_overview_alt', Output.overview.string)
		except(TypeError, KeyError, AttributeError):
			pass
	else:
		xbmc.executebuiltin('Skin.SetBool(nodefaultxml)')
		Current_Window.setProperty('Synopsis_title','Could not find:')
		Current_Window.setProperty('Synopsis_title_alt',GameName)
		Current_Window.setProperty('Synopsis_developer',''+_Resources_Default_xml)
		Current_Window.setProperty('Synopsis_titleid_alt','')
		Current_Window.setProperty('Synopsis_overview_alt','No synopsis information found.')
def clear_properties():
	#####	default.xml
	Current_Window.setProperty('Synopsis_title','')
	Current_Window.setProperty('Synopsis_title_alt','')
	Current_Window.setProperty('Synopsis_developer','')
	Current_Window.setProperty('Synopsis_publisher','')
	Current_Window.setProperty('Synopsis_features_general','')
	Current_Window.setProperty('Synopsis_features_online','')	
	Current_Window.setProperty('Synopsis_esrb','')
	Current_Window.setProperty('Synopsis_esrb_descriptors','')
	Current_Window.setProperty('Synopsis_genre','')
	Current_Window.setProperty('Synopsis_release_date','')
	Current_Window.setProperty('Synopsis_rating','')
	Current_Window.setProperty('Synopsis_rating_alt', '')
	Current_Window.setProperty('Synopsis_platform','')
	Current_Window.setProperty('Synopsis_exclusive','')
	Current_Window.setProperty('Synopsis_titleid','')
	Current_Window.setProperty('Synopsis_titleid_alt','')
	Current_Window.setProperty('Synopsis_overview','')
	Current_Window.setProperty('Synopsis_overview_alt','')
	#####	assets (videos, images eg...)
	Current_Window.setProperty('Synopsis_banner', '')
	Current_Window.setProperty('Synopsis_fanart', '')
	Current_Window.setProperty('Synopsis_fanart_blur', '')
	Current_Window.setProperty('Synopsis_fog', '')
	Current_Window.setProperty('Synopsis_poster', '')
	Current_Window.setProperty('Synopsis_poster_small', '')
	Current_Window.setProperty('Synopsis_icon', '')
	Current_Window.setProperty('Alt_Synopsis_icon', '')
	Current_Window.setProperty('Synopsis_disc', '')
	Current_Window.setProperty('Synopsis_screenshots', '')
	Current_Window.setProperty('Synopsis_xbe', '')
	Current_Window.setProperty('Synopsis_thumb', '')
	Current_Window.setProperty('Synopsis_Video_Preview_Name', 'No Preview Video Found')
	Current_Window.setProperty('Synopsis_Video_Preview_Path','')
	Current_Window.setProperty('Preview_default', '')
	Current_Window.setProperty('Preview_alt', '')			
	#####	colours.xml
	Current_Window.setProperty('Synopsis_colour_1','FF399EDA')
	Current_Window.setProperty('Synopsis_colour_2','FF969696')
	Current_Window.setProperty('Synopsis_colour_3','FFCCCCCC')
	Current_Window.setProperty('Synopsis_colour_4','FFFFFFFF')
	Current_Window.setProperty('Synopsis_colour_5','FF333333')
	#####	labels.xml
	Current_Window.setProperty('Synopsis_label_1','Title ID:')
	Current_Window.setProperty('Synopsis_label_2','Synopsis')
	Current_Window.setProperty('Synopsis_label_3','Game Rating')
	Current_Window.setProperty('Synopsis_label_4','/ 5')
	Current_Window.setProperty('Synopsis_label_5','Title:')
	Current_Window.setProperty('Synopsis_label_6','Developer:')
	Current_Window.setProperty('Synopsis_label_7','Publisher:')
	Current_Window.setProperty('Synopsis_label_8','General Features:')
	Current_Window.setProperty('Synopsis_label_9','Online Features:')
	Current_Window.setProperty('Synopsis_label_10','ESRB:')
	Current_Window.setProperty('Synopsis_label_11','ESRB Descriptor:')
	Current_Window.setProperty('Synopsis_label_12','Genre:')
	Current_Window.setProperty('Synopsis_label_13','Release Date:')
	Current_Window.setProperty('Synopsis_label_14','Rating:')
	Current_Window.setProperty('Synopsis_label_15','Platform:')
	Current_Window.setProperty('Synopsis_label_16','Exclusive:')
	Current_Window.setProperty('Synopsis_label_17','Title ID:')
	Current_Window.setProperty('Synopsis_label_18','Synopsis:')
	Current_Window.setProperty('Synopsis_label_19','Year:')
	Current_Window.setProperty('Synopsis_label_20','')
	Current_Window.setProperty('Synopsis_label_21','')
	Current_Window.setProperty('Synopsis_label_22','')
	Current_Window.setProperty('Synopsis_label_23','')
	Current_Window.setProperty('Synopsis_label_24','')
	Current_Window.setProperty('Synopsis_label_25','')
	Current_Window.setProperty('Synopsis_label_26','')
	Current_Window.setProperty('Synopsis_label_27','')
	Current_Window.setProperty('Synopsis_label_28','')
	Current_Window.setProperty('Synopsis_label_29','')
	Current_Window.setProperty('Synopsis_label_30','')
#####	load window xml and check key presses/movement.
class GUI(windowdialog):
	def onInit(self):
		if xbmc.getCondVisibility('!Skin.HasSetting(Synopsis_First_Run)'):
			xbmc.executebuiltin('SetFocus(100)')
	def onClick(self, controlID):
		if (controlID == 100):
			time.sleep(1)
			self.close()
		if (controlID == 101):
			time.sleep(1)
			self.close()
		if (controlID == 10):
			self.close()
			time.sleep(0.7)
			xbmc.executebuiltin('RunXBE('+xbmc.getInfoLabel('Window(MyPrograms).Property(Synopsis_xbe)')+')')
		if (controlID == 13):
			if xbmc.getCondVisibility('Skin.HasSetting(SynopsisPreviewThere)'):
				global Video_Played
				Video_Played = 1
				xbmc.executebuiltin('PlayWith('+xbmc.getInfoLabel('Window(MyPrograms).Property(Player_Type)')+')')
				xbmc.executebuiltin('Playmedia('+xbmc.getInfoLabel('Window(MyPrograms).Property(Synopsis_Video_Preview_Path)')+',1,noresume)')
				xbmc.executebuiltin('playercontrol(RepeatOff)')
				xbmcgui.DialogProgress().update(0,"")
	def onAction(self, action):
		if action.getButtonCode() == 257 or action.getButtonCode() == 275:
			if xbmc.getCondVisibility('Player.HasVideo'):
				xbmc.executebuiltin('PlayerControl(stop)')
				self.close()
				if Music_Playing == 1 and xbmc.getCondVisibility('Skin.HasSetting(Use_Startup_Playback)') and Video_Played == 1:
					time.sleep(0.1)
					xbmc.executebuiltin('PlayMedia('+xbmc.getInfoLabel('Skin.String(Startup_Playback_Path)')+')')
					xbmc.executebuiltin('playercontrol(RepeatAll)')
			else:
				self.close()
	def onFocus(self, controlID):
		pass
if (__name__ == '__main__'):
	clear_properties()
	synopsis_mode_video()
	synopsis_mode_images()
	synopsis_mode_text()
	#####	UI.
	xbmc.executebuiltin('dialog.close(1100,true)')
	GUI = GUI('_Script_Synopsis.xml', os.getcwd())
	GUI.doModal()
	del GUI
	xbmcgui.DialogProgress().update(0,"") # stops urldownloader or other progress dialogs showing 100%