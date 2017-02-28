'''
	Script by Rocky5
	Extracts information from a file named default.xml located in the '_resources' folder.
	
	Updated: 28 February 2017
	-- Added more logging info and cleaned the script up a tad.	
	
	Updated: 27 February 2017
	-- Fixed the launch game feature crashing XBMC.
	
	Updated: 26 February 2017
	-- Forgot to move all skin.SetStrings to setProperty.
	   Added a dialog argument that you add to the end of the RunScript string.
	   This will run the synopsis script window in dialog mode instead of windowed.
	   example: RunScript( Special://xbmc/scripts/XBMC4Kids Extras/Synopsis/default.py,dialog )
	
	Updated: 25 February 2017
	-- Moved the script to its own contained structure, so its separate from the skins now.
	   Added support for stopping playback and focusing when exiting the script.
	   There are still some things its dependent on.
	   Skin settings:
	    Skin.HasSetting(SynopsisMode) - Will show the synopsis window.
		Skin>Has Setting(Synopsis) - Will show the default view.
		Skin>Has Setting(Synopsis_alt_view) - Will show the alt view.
		Skin>Has Setting(Synopsis_Autoplay) - Will auto play the preview in the alt view only.
		
	   If Skin.HasSetting(SynopsisMode) is disbaled, it will default to the preview video window.
	
	Updated: 23 February 2017
	-- Added a few more lines of code for the likes of Rating and gamexbe path eg...
	   This was done for the new synopsis layout.
	   Updated the code to optimize reading of the default.xml
	   Reorganised the code.
	
	Updated: 18 February 2017
	-- Changed the video path code and added a new var for the names.
	   Added code to get the poster.jp, fanart.jpg and screenshots folder for the synopsis window.
	   Added code to get the preview video for the non synopsis mode.
	   
	Updated: 28 July 2016
	-- Rearranged the layout & now get the video file and pass it to the skin if found
	   also cleaned up some left over stuff.
	
	Updated: 15 July 2016
	-- Added a skin setting, to display info in the skin if there is a preview video found.
	   Disabled the video playback code, no done by press (A) when in the synopsis screen.
	
'''
import os, sys, xbmc, xbmcgui
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
#####	load window xml and check key presses/movement.
class GUI(windowdialog):
	
	def onInit(self):
		pass
	def onAction(self, action):
		if action.getButtonCode() == 257 or action.getButtonCode() == 275:
			if xbmc.getCondVisibility( 'Player.HasMedia' ): xbmc.executebuiltin('PlayerControl(stop)')
			self.close()
	def onClick(self, controlID):
		if (controlID == 10 and xbmc.getCondVisibility( 'Skin.HasSetting(SynopsisMode)' ) and xbmc.getCondVisibility( 'Skin.HasSetting(Synopsis)' ) ):
			self.close()
	def onFocus(self, controlID):
		# print 'onFocus(): control %i' % controlID
		pass
#####	Start of the scrip.
if (__name__ == '__main__'):
	#####	Start markings for the log file.
	print '================================================================================'
	print '| Scripts\XBMC4Kids Extras\Synopsis\default.py loaded.'
	print '| ------------------------------------------------------------------------------'
	#####	Sets paths & other crap.
	Current_Window					= xbmcgui.Window(xbmcgui.getCurrentWindowId())
	Preview_Video_Name				= 'Preview'
	GameName						= xbmc.getInfoLabel('ListItem.Label')
	GameFolder						= xbmc.getInfoLabel('ListItem.FolderName')
	GameXBE							= xbmc.getInfoLabel('listitem.FileNameAndPath')
	_Resources_Path					= xbmc.getInfoLabel('ListItem.Path') + '_resources'
	_Resources_Default_xml			= os.path.join(_Resources_Path, 'default.xml')
	_Resources_Screenshots			= os.path.join(_Resources_Path, 'screenshots')
	_Resources_Poster				= os.path.join(_Resources_Path, 'artwork\\poster.jpg')
	_Resources_Fanart				= os.path.join(_Resources_Path, 'artwork\\fanart.jpg')
	_Resources_Banner				= os.path.join(_Resources_Path, 'artwork\\banner.jpg')
	_Resources_Preview_Ext1			= os.path.join(_Resources_Path, 'media\\' + Preview_Video_Name + '.xmv')
	_Resources_Preview_Ext2 		= os.path.join(_Resources_Path, 'media\\' + Preview_Video_Name + '.mp4')
	_Resources_Preview_Ext3 		= os.path.join(_Resources_Path, 'media\\' + Preview_Video_Name + '.wmv')
	_Resources_Preview_Ext4 		= os.path.join(_Resources_Path, 'media\\' + Preview_Video_Name + '.mpg')
	Preview_default					= xbmc.getInfoLabel('ListItem.Path') + 'preview.xmv'
	Preview_ext						= xbmc.getInfoLabel('Skin.String(PreviewFileExtension)')
	Preview_alt						= xbmc.getInfoLabel('ListItem.Path') + Preview_Video_Name + '.' + Preview_ext
	CachedThumb						= xbmc.translatePath('special://profile/Thumbnails/Programs/%s/%s' % ( xbmc.getCacheThumbName(xbmc.getInfoLabel('ListItem.FolderPath'))[0], xbmc.getCacheThumbName(xbmc.getInfoLabel('ListItem.FolderPath')) ) )
	print '| ' + GameName
	if xbmc.getCondVisibility( 'Skin.HasSetting(SynopsisMode)' ) == 1:
		#####	Check for Preview file & set skin settings so they can be played.
		print '|  Scanning for preview video'
		if os.path.isfile( _Resources_Preview_Ext1 ):
			Current_Window.setProperty( 'Synopsis_Video_Preview_Path', _Resources_Preview_Ext1 )
			Current_Window.setProperty( 'Synopsis_Video_Preview_Name', Preview_Video_Name + '.xmv' )
			Current_Window.setProperty( 'Player_Type,DVDPlayer)' )
			print '|   Found ' + Preview_Video_Name + '.xmv' 
		elif os.path.exists( _Resources_Preview_Ext2 ):
			Current_Window.setProperty( 'Synopsis_Video_Preview_Path', _Resources_Preview_Ext2 )
			Current_Window.setProperty( 'Synopsis_Video_Preview_Name', Preview_Video_Name + '.mp4' )
			Current_Window.setProperty( 'Player_Type', 'MPlayer' )
			print '|   Found ' + Preview_Video_Name + '.mp4' 
		elif os.path.exists( _Resources_Preview_Ext3 ):
			Current_Window.setProperty( 'Synopsis_Video_Preview_Path', _Resources_Preview_Ext3)
			Current_Window.setProperty( 'Synopsis_Video_Preview_Name', Preview_Video_Name + '.wmv' )
			Current_Window.setProperty( 'Player_Type', 'MPlayer' )
			print '|   Found ' + Preview_Video_Name + '.wmv' 
		elif os.path.exists( _Resources_Preview_Ext4 ):
			Current_Window.setProperty( 'Synopsis_Video_Preview_Path', _Resources_Preview_Ext4 )
			Current_Window.setProperty( 'Synopsis_Video_Preview_Name', Preview_Video_Name + '.mpg' )
			Current_Window.setProperty( 'Player_Type', 'MPlayer' )
			print '|   Found ' + Preview_Video_Name + '.mpg' 
		else:
			Current_Window.setProperty( 'Synopsis_Video_Preview_Name', 'No Preview Video Found' )
			Current_Window.setProperty( 'Synopsis_Video_Preview_Path','' )
			print '|   No ' + Preview_Video_Name + ' video found'
		#####	Get _resources assets
		print '|  Scanning for assets'
		if os.path.isfile( _Resources_Banner ): # Banner
			Current_Window.setProperty( 'Synopsis_banner', _Resources_Banner )
			print '|   Found banner.jpg'
		else:
			Current_Window.setProperty( 'Synopsis_banner', '' )
		if os.path.isfile( _Resources_Fanart ): # Fanart
			Current_Window.setProperty( 'Synopsis_fanart', _Resources_Fanart )
			print '|   Found fanart.jpg'
		else:
			Current_Window.setProperty( 'Synopsis_fanart', '' )
		if os.path.isfile( _Resources_Poster): # Poster
			Current_Window.setProperty( 'Synopsis_poster', _Resources_Poster )
			print '|   Found poster.jpg'
		else:
			Current_Window.setProperty( 'Synopsis_poster', '' )
		if os.path.exists( _Resources_Screenshots ): # Screenshots
			Current_Window.setProperty( 'Synopsis_screenshots', _Resources_Screenshots )
			print '|   Found Screenshot folder'
		else:	
			Current_Window.setProperty( 'Synopsis_screenshots', '' )
		if os.path.isfile( GameXBE ): # GameXBE
			Current_Window.setProperty( 'Synopsis_xbe', GameXBE )
			print '|   Found default.xbe'
		else:
			Current_Window.setProperty( 'Synopsis_xbe', '' )
		if os.path.isfile( CachedThumb ): # Thumb
			Current_Window.setProperty( 'Synopsis_thumb', CachedThumb )
			print '|   Found Cached Thumb'
		else:
			Current_Window.setProperty( 'Synopsis_thumb', '' )
		#####	Read XML & set
		print '|  Scanning for default.xml'
		if os.path.isfile ( _Resources_Default_xml ):
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
			Current_Window.setProperty( 'Synopsis_developer','' + GameFolder + '/_resources/default.xml' )
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
				print '|   No ' + Preview_Video_Name + ' found'
				Current_Window.setProperty( 'Preview_default', '' )
		else:
			if os.path.isfile( Preview_alt ):
				print '|   Found ' + Preview_alt
				Current_Window.setProperty( 'Preview_alt', Preview_alt )
			else:
				Current_Window.setProperty( 'Synopsis_Video_Preview_Name', 'No Preview Video Found' )
				print '|   No ' + Preview_Video_Name + ' found'
				Current_Window.setProperty( 'Preview_alt', '' )
				
	xbmc.executebuiltin('dialog.close(1113,true)')
	print '================================================================================'
	#####	UI.
	ui = GUI( '_Script_Synopsis.xml', os.getcwd() )
	ui.doModal()
	del ui
	#####	Used to focus the games list when using the script in dialog mode
	if UseDialog == 'dialog': xbmc.executebuiltin('SetFocus(50)')