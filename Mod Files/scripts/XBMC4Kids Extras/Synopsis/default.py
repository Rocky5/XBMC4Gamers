'''
	Script by Rocky5
	Extracts information from a file named default.xml located in the '_resources' folder.
	
'''


import os, sys, time, xbmc, xbmcgui, glob
from BeautifulSoup import *


#####	Check args for dialog and set the window output.
try:
	UseDialog = sys.argv[1]
except:
	UseDialog = 'window'
if UseDialog == 'dialog':
	windowdialog = xbmcgui.WindowXMLDialog
else:
	windowdialog = xbmcgui.WindowXML
	
	
#####	Sets paths & other crap.
Current_Window					= xbmcgui.Window(xbmcgui.getCurrentWindowId())
Working_Directory				= os.getcwd() + '\\resources\\'
GetInfoPath						= xbmc.getInfoLabel('ListItem.Path')
Colour_xml						= os.path.join(Working_Directory, 'colours.xml')
Labels_xml						= os.path.join(Working_Directory, 'labels.xml')
GameName						= xbmc.getInfoLabel('ListItem.Label')
GameXBE							= xbmc.getInfoLabel('listitem.FileNameAndPath')
_Resources_Path					= GetInfoPath + '_resources'
_Resources_Default_xml			= os.path.join(_Resources_Path, 'default.xml')
_Resources_Screenshots			= os.path.join(_Resources_Path, 'screenshots')
_Resources_Preview				= os.path.join(_Resources_Path, 'media' )
_Resources_Artwork				= os.path.join(_Resources_Path, 'artwork' )
Preview_default					= GetInfoPath + 'preview.xmv'
Preview_ext						= xbmc.getInfoLabel('Skin.String(PreviewFileExtension)')
Preview_alt						= GetInfoPath + 'Preview.' + Preview_ext
CachedThumb						= xbmc.translatePath('special://profile/Thumbnails/Programs/%s/%s' % ( xbmc.getCacheThumbName(xbmc.getInfoLabel('ListItem.FolderPath'))[0], xbmc.getCacheThumbName(xbmc.getInfoLabel('ListItem.FolderPath')) ) )


def colours():
	#####	Read colour XML & set
	if os.path.isfile ( Colour_xml ):
		print '|   Parsing colours.xml'
		xbmc.executebuiltin('Skin.Reset(nodefaultxml)')
		Colour_XML = open( Colour_xml, 'r' ).read()
		Output = BeautifulSoup( Colour_XML )
		try: # Colour 1
			Current_Window.setProperty( 'Synopsis_colour_1', Output.colour_1.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_colour_1','FF399EDA' )
		try: # Colour 2
			Current_Window.setProperty( 'Synopsis_colour_2', Output.colour_2.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_colour_2','FF969696' )
		try: # Colour 3
			Current_Window.setProperty( 'Synopsis_colour_3', Output.colour_3.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_colour_3','FF969696' )
		try: # Colour 4
			Current_Window.setProperty( 'Synopsis_colour_4', Output.colour_4.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_colour_4','FF969696' )
		try: # Colour 5
			Current_Window.setProperty( 'Synopsis_colour_5', Output.colour_5.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_colour_5','FF969696' )
	else:
		print '|   No colour.xml found'
		Current_Window.setProperty( 'Synopsis_colour_1','FF399EDA' )
		Current_Window.setProperty( 'Synopsis_colour_2','FF399EDA' )	
		Current_Window.setProperty( 'Synopsis_colour_3','FF399EDA' )	
		Current_Window.setProperty( 'Synopsis_colour_4','FF399EDA' )	
		Current_Window.setProperty( 'Synopsis_colour_5','FF399EDA' )	


def labels():
	#####	Read labels XML & set
	if os.path.isfile ( Labels_xml ):
		print '|   Parsing labels.xml'
		xbmc.executebuiltin('Skin.Reset(nodefaultxml)')
		Labels_XML = open( Labels_xml, 'r' ).read()
		Output = BeautifulSoup( Labels_XML )
		try: # label 1
			Current_Window.setProperty( 'Synopsis_label_1', Output.label_1.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_1','Title ID:' )
		try: # label 2
			Current_Window.setProperty( 'Synopsis_label_2', Output.label_2.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_2','Synopsis' )
		try: # label 3
			Current_Window.setProperty( 'Synopsis_label_3', Output.label_3.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_3','Game Rating' )
		try: # label 4
			Current_Window.setProperty( 'Synopsis_label_4', Output.label_4.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_4','/ 5' )
		try: # label 5
			Current_Window.setProperty( 'Synopsis_label_5', Output.label_5.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_5','Title:' )
		try: # label 6
			Current_Window.setProperty( 'Synopsis_label_6', Output.label_6.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_6','Developer:' )
		try: # label 7
			Current_Window.setProperty( 'Synopsis_label_7', Output.label_7.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_7','Publisher:' )
		try: # label 8
			Current_Window.setProperty( 'Synopsis_label_8', Output.label_8.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_8','General Features:' )
		try: # label 9
			Current_Window.setProperty( 'Synopsis_label_9', Output.label_9.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_9','Online Features:' )
		try: # label 10
			Current_Window.setProperty( 'Synopsis_label_10', Output.label_10.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_10','ESRB:' )
		try: # label 11
			Current_Window.setProperty( 'Synopsis_label_11', Output.label_11.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_11','ESRB Descriptor:' )
		try: # label 12
			Current_Window.setProperty( 'Synopsis_label_12', Output.label_12.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_12','Genre:' )
		try: # label 13
			Current_Window.setProperty( 'Synopsis_label_13', Output.label_13.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_13','Release Date:' )
		try: # label 14
			Current_Window.setProperty( 'Synopsis_label_14', Output.label_14.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_14','Rating:' )
		try: # label 15
			Current_Window.setProperty( 'Synopsis_label_15', Output.label_15.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_15','Platform:' )
		try: # label 16
			Current_Window.setProperty( 'Synopsis_label_16', Output.label_16.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_16','Exclusive:' )
		try: # label 17
			Current_Window.setProperty( 'Synopsis_label_17', Output.label_17.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_17','Title ID:' )
		try: # label 18
			Current_Window.setProperty( 'Synopsis_label_18', Output.label_18.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_18','Overview:' )
		try: # label 19
			Current_Window.setProperty( 'Synopsis_label_19', Output.label_19.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_19','No Poster Found' )
		try: # label 20
			Current_Window.setProperty( 'Synopsis_label_20', Output.label_20.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_20','No Screenshots Found' )
		try: # label 21
			Current_Window.setProperty( 'Synopsis_label_21', Output.label_21.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_21','[B]Example[/B][CR]Halo\Preview.' )
		try: # label 22
			Current_Window.setProperty( 'Synopsis_label_22', Output.label_22.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_22','[CR]This option works separate from the [B]Synopsis mode[/B].[CR]Synopsis mode gets the video extension dynamical.' )
		try: # label 23
			Current_Window.setProperty( 'Synopsis_label_23', Output.label_23.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_23','Synopsis Mode' )
		try: # label 24
			Current_Window.setProperty( 'Synopsis_label_24', Output.label_24.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_24','Default layout' )
		try: # label 25
			Current_Window.setProperty( 'Synopsis_label_25', Output.label_25.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_25','Alternative layout' )
		try: # label 26
			Current_Window.setProperty( 'Synopsis_label_26', Output.label_26.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_26','Autoplay preview video' )
		try: # label 27
			Current_Window.setProperty( 'Synopsis_label_27', Output.label_27.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_27','' )
		try: # label 28
			Current_Window.setProperty( 'Synopsis_label_28', Output.label_28.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_28','' )
		try: # label 29
			Current_Window.setProperty( 'Synopsis_label_29', Output.label_29.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_29','' )
		try: # label 30
			Current_Window.setProperty( 'Synopsis_label_30', Output.label_30.string )
		except(TypeError, KeyError, AttributeError):
			Current_Window.setProperty( 'Synopsis_label_30','' )
	else:
		print '|   No label.xml found'
		Current_Window.setProperty( 'Synopsis_label_1','Title ID:' )
		Current_Window.setProperty( 'Synopsis_label_2','Synopsis' )
		Current_Window.setProperty( 'Synopsis_label_3','Game Rating' )
		Current_Window.setProperty( 'Synopsis_label_4','/ 5' )
		Current_Window.setProperty( 'Synopsis_label_5','Title:' )
		Current_Window.setProperty( 'Synopsis_label_6','Developer:' )
		Current_Window.setProperty( 'Synopsis_label_7','Publisher:' )
		Current_Window.setProperty( 'Synopsis_label_8','General Features:' )
		Current_Window.setProperty( 'Synopsis_label_9','Online Features:' )
		Current_Window.setProperty( 'Synopsis_label_10','ESRB:' )
		Current_Window.setProperty( 'Synopsis_label_11','ESRB Descriptor:' )
		Current_Window.setProperty( 'Synopsis_label_12','Genre:' )
		Current_Window.setProperty( 'Synopsis_label_13','Release Date:' )
		Current_Window.setProperty( 'Synopsis_label_14','Rating:' )
		Current_Window.setProperty( 'Synopsis_label_15','Platform:' )
		Current_Window.setProperty( 'Synopsis_label_16','Exclusive:' )
		Current_Window.setProperty( 'Synopsis_label_17','Title ID:' )
		Current_Window.setProperty( 'Synopsis_label_18','Overview:' )
		Current_Window.setProperty( 'Synopsis_label_19','No Poster Found' )
		Current_Window.setProperty( 'Synopsis_label_20','No Screenshots Found' )
		Current_Window.setProperty( 'Synopsis_label_21','[B]Example[/B][CR]Halo\Preview.' )
		Current_Window.setProperty( 'Synopsis_label_22','[CR]This option works separate from the [B]Synopsis mode[/B].[CR]Synopsis mode gets the video extension dynamical.' )
		Current_Window.setProperty( 'Synopsis_label_23','Synopsis Mode' )
		Current_Window.setProperty( 'Synopsis_label_24','Default layout' )
		Current_Window.setProperty( 'Synopsis_label_25','Alternative layout' )
		Current_Window.setProperty( 'Synopsis_label_26','Autoplay preview video' )
		Current_Window.setProperty( 'Synopsis_label_27','' )
		Current_Window.setProperty( 'Synopsis_label_28','' )
		Current_Window.setProperty( 'Synopsis_label_29','' )
		Current_Window.setProperty( 'Synopsis_label_30','' )
	print '================================================================================'


#####	load window xml and check key presses/movement.
class GUI(windowdialog):
	def onInit(self):
		pass

		
	def onAction(self, action):
		if action.getButtonCode() == 257 or action.getButtonCode() == 275:
			if xbmc.getCondVisibility( 'Player.HasMedia' ): xbmc.executebuiltin('PlayerControl(stop)')
			self.close()
		if action.getButtonCode() == 260:
			if xbmc.getCondVisibility( 'Player.HasMedia' ): xbmc.executebuiltin('PlayerControl(stop)')
			xbmc.executebuiltin('ActivateWindow(1102)')
			if UseDialog == 'dialog': self.close()
			
	def onClick(self, controlID):
		if (controlID == 10 and xbmc.getCondVisibility( 'Skin.HasSetting(SynopsisMode)' ) and xbmc.getCondVisibility( 'Skin.HasSetting(Synopsis)' ) ):
			self.close()

			
	def onFocus(self, controlID):
		pass

		
#####	Start of the scrip.
if (__name__ == '__main__'):
	
	
	#####	Start markings for the log file.
	print '================================================================================'
	print '| Scripts\XBMC4Kids Extras\Synopsis\default.py loaded.'
	print '| ------------------------------------------------------------------------------'
	print '| ' + GameName
		
	
	if xbmc.getCondVisibility( 'Skin.HasSetting(SynopsisMode)' ) == 1:
		
		
		#####	Check for Preview files.
		print '|  Scanning for assets'
		PreviewFile = "0"
		for root, dirs, files in os.walk( _Resources_Preview ):
			for filename in files:
				PreviewFile = root + '\\' + filename
				Current_Window.setProperty( 'Synopsis_Video_Preview_Path', PreviewFile )
				Current_Window.setProperty( 'Synopsis_Video_Preview_Name', filename )
		if PreviewFile == "0":
			Current_Window.setProperty( 'Synopsis_Video_Preview_Name', 'No Preview Video Found' )
			Current_Window.setProperty( 'Synopsis_Video_Preview_Path','' )
			xbmc.executebuiltin('Skin.Reset(SynopsisPreviewThere)')
			print '|   No preview video found'
		else:
			if PreviewFile.endswith('.xmv'):
				Current_Window.setProperty( 'Player_Type','DVDPlayer' )
				xbmc.executebuiltin('Skin.SetBool(SynopsisPreviewThere)')
			else:
				Current_Window.setProperty( 'Player_Type','MPlayer' )
				xbmc.executebuiltin('Skin.SetBool(SynopsisPreviewThere)')
			print '|   Found ' + PreviewFile
		
		
		#####	Check for assets files.
		for root, dirs, files in os.walk( _Resources_Artwork ):
			Current_Window.setProperty( 'Synopsis_banner', '' )
			Current_Window.setProperty( 'Synopsis_fanart', '' )
			Current_Window.setProperty( 'Synopsis_poster', '' )
			for filename in files:
				if filename.startswith('banner'):
					Current_Window.setProperty( 'Synopsis_banner', root + '\\' + filename )
					print '|   Found ' + filename
				if filename.startswith('fanart'):
					Current_Window.setProperty( 'Synopsis_fanart', root + '\\' + filename )
					print '|   Found ' + filename
				if filename.startswith('poster'):
					Current_Window.setProperty( 'Synopsis_poster', root + '\\' + filename )
					print '|   Found ' + filename
		
		
		#####	Get screenshots, xbe and cached thumb
		Current_Window.setProperty( 'Synopsis_screenshots', '' )		
		Current_Window.setProperty( 'Synopsis_screenshots', _Resources_Screenshots )
		if os.path.exists( _Resources_Screenshots ): print '|   Found Screenshot folder'
		Current_Window.setProperty( 'Synopsis_xbe', '' )
		Current_Window.setProperty( 'Synopsis_xbe', GameXBE )
		if os.path.isfile( GameXBE ): print '|   Found default.xbe'
		Current_Window.setProperty( 'Synopsis_thumb', '' )
		Current_Window.setProperty( 'Synopsis_thumb', CachedThumb )
		if os.path.isfile( CachedThumb ): print '|   Found Cached Thumb'
		
		
		#####	Read XML & set
		print '|  Scanning for default.xml'
		if os.path.isfile( _Resources_Default_xml ):
			print '|   Parsing ' + _Resources_Default_xml
			xbmc.executebuiltin('Skin.Reset(nodefaultxml)')
			Synopsis_XML = open( _Resources_Default_xml, 'r' ).read()
			Output = BeautifulSoup( Synopsis_XML )
			try: # Title
				Current_Window.setProperty( 'Synopsis_title', Output.title.string )
				Current_Window.setProperty( 'Synopsis_title_alt', Output.title.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_title','' )
				Current_Window.setProperty( 'Synopsis_title_alt','' )
			try: # Developer
				Current_Window.setProperty( 'Synopsis_developer', Output.developer.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_developer','' )
			try: # Publisher
				Current_Window.setProperty( 'Synopsis_publisher', Output.publisher.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_publisher','' )
			try: # Features General
				Current_Window.setProperty( 'Synopsis_features_general', Output.features_general.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_features_general','' )
			try: #  Features Online
				Current_Window.setProperty( 'Synopsis_features_online', Output.features_online.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_features_online','' )		
			try: # ESRB Rating
				Current_Window.setProperty( 'Synopsis_esrb', Output.esrb.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_esrb','' )
			try: # ESRB Descriptors
				Current_Window.setProperty( 'Synopsis_esrb_descriptors', Output.esrb_descriptors.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_esrb_descriptors','' )
			try: # Genre
				Current_Window.setProperty( 'Synopsis_genre', Output.genre.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_genre','' )
			try: # Release Date
				Current_Window.setProperty( 'Synopsis_release_date', Output.release_date.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_release_date','' )
			try: # GameRating
				Current_Window.setProperty( 'Synopsis_rating', Output.rating.string )
				Current_Window.setProperty( 'Synopsis_rating_alt', Output.rating.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_rating','' )
				Current_Window.setProperty( 'Synopsis_rating_alt', '0' )
			try: # Platform
				Current_Window.setProperty( 'Synopsis_platform', Output.platform.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_platform','' )
			try: # Exclusive
				Current_Window.setProperty( 'Synopsis_exclusive', Output.exclusive.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_exclusive','' )
			try: # Title ID
				Current_Window.setProperty( 'Synopsis_titleid', Output.titleid.string )
				Current_Window.setProperty( 'Synopsis_titleid_alt', Output.titleid.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_titleid','' )
				Current_Window.setProperty( 'Synopsis_titleid_alt','' )
			try: # Overview
				Current_Window.setProperty( 'Synopsis_overview', Output.overview.string )
				Current_Window.setProperty( 'Synopsis_overview_alt', Output.overview.string )
			except(TypeError, KeyError, AttributeError):
				Current_Window.setProperty( 'Synopsis_overview','' )
				Current_Window.setProperty( 'Synopsis_overview_alt','' )
			print '|   Parsing complete'
		else:
			print '|   No default.xml found'
			xbmc.executebuiltin('Skin.SetBool(nodefaultxml)')
			Current_Window.setProperty( 'Synopsis_title','Could not find:' )
			Current_Window.setProperty( 'Synopsis_title_alt',GameName )
			Current_Window.setProperty( 'Synopsis_developer','' + _Resources_Default_xml )
			Current_Window.setProperty( 'Synopsis_publisher','' )
			Current_Window.setProperty( 'Synopsis_features_general','' )
			Current_Window.setProperty( 'Synopsis_features_online','' )
			Current_Window.setProperty( 'Synopsis_esrb','' )
			Current_Window.setProperty( 'Synopsis_esrb_descriptors','' )
			Current_Window.setProperty( 'Synopsis_release_date','' )
			Current_Window.setProperty( 'Synopsis_rating','' )
			Current_Window.setProperty( 'Synopsis_rating_alt','0' )
			Current_Window.setProperty( 'Synopsis_genre','' )
			Current_Window.setProperty( 'Synopsis_platform','' )
			Current_Window.setProperty( 'Synopsis_exclusive','' )
			Current_Window.setProperty( 'Synopsis_titleid','' )
			Current_Window.setProperty( 'Synopsis_titleid_alt','Null' )
			Current_Window.setProperty( 'Synopsis_overview','' )
			Current_Window.setProperty( 'Synopsis_overview_alt','No synopsis information found.' )
	else:
		print '|  Looking for preview video'
		if xbmc.getCondVisibility( 'Skin.HasSetting(PreviewExtension)' ) == 0:
			if os.path.isfile( Preview_default ):
				print '|   Found ' + Preview_default
				Current_Window.setProperty( 'Preview_default', Preview_default )
			else:
				Current_Window.setProperty( 'Synopsis_Video_Preview_Name', 'No Preview Video Found' )
				print '|   No preview video found'
				Current_Window.setProperty( 'Preview_default', '' )
		else:
			if os.path.isfile( Preview_alt ):
				print '|   Found ' + Preview_alt
				Current_Window.setProperty( 'Preview_alt', Preview_alt )
			else:
				Current_Window.setProperty( 'Synopsis_Video_Preview_Name', 'No Preview Video Found' )
				print '|   No preview video found'
				Current_Window.setProperty( 'Preview_alt', '' )
	
	
	xbmc.executebuiltin('dialog.close(all,true)')
	print '================================================================================'
	
	
	#####	UI.
	colours()
	labels()
	ui = GUI( '_Script_Synopsis.xml', os.getcwd() )
	ui.doModal()
	del ui
	
	
	#####	Used to focus the games list when using the script in dialog mode
	if UseDialog == 'dialog': xbmc.executebuiltin('SetFocus(50)')