'''
	Script by Rocky5
	Extracts information from a file named default.xml located in the '_resources' folder.
	
'''

import fileinput, glob, os, shutil, sys, time, xbmc, xbmcgui
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
Font_Path1						= xbmc.translatePath('Special://skin/1080i/Font.xml')
Font_Path2						= xbmc.translatePath('Special://skin/720p/Font.xml')
Font_Path3						= xbmc.translatePath('Special://skin/NTSC/Font.xml')
Font_Path4						= xbmc.translatePath('Special://skin/NTSC 16x9/Font.xml')
Font_Path5						= xbmc.translatePath('Special://skin/PAL/Font.xml')
Font_Path6						= xbmc.translatePath('Special://skin/PAL 16x9/Font.xml')
Fonts = '<synopsis_fonts>Installed</synopsis_fonts>\n\
<font>\n\
	<name>synopsis_font17</name>\n\
	<filename>arial.ttf</filename>\n\
	<size>17</size>\n\
</font>\n\
<font>\n\
	<name>synopsis_font18</name>\n\
	<filename>arial.ttf</filename>\n\
	<size>18</size>\n\
</font>\n\
<font>\n\
	<name>synopsis_font20</name>\n\
	<filename>arial.ttf</filename>\n\
	<size>20</size>\n\
</font>\n\
<font>\n\
	<name>synopsis_font21</name>\n\
	<filename>arial.ttf</filename>\n\
	<size>21</size>\n\
</font>\n\
<font>\n\
	<name>synopsis_font28</name>\n\
	<filename>arial.ttf</filename>\n\
	<size>28</size>\n\
</font>\n\
<font>\n\
	<name>synopsis_font35</name>\n\
	<filename>arial.ttf</filename>\n\
	<size>35</size>\n\
</font>'

def log( input ):
	if logging: print "%s" % str( input )

def synopsis_mode_video():
	#####	Check for Preview files.
	PreviewFile = "0"
	for root, dirs, files in os.walk( _Resources_Preview ):
		for filename in files:
			PreviewFile = root + '\\' + filename
			Current_Window.setProperty( 'Synopsis_Video_Preview_Path', PreviewFile )
			Current_Window.setProperty( 'Synopsis_Video_Preview_Name', filename )
	if PreviewFile == "0":
		log('|   No preview video found')
		xbmc.executebuiltin('Skin.Reset(SynopsisPreviewThere)')
	else:
		if PreviewFile.endswith('.xmv'):
			Current_Window.setProperty( 'Player_Type','DVDPlayer' )
			xbmc.executebuiltin('Skin.SetBool(SynopsisPreviewThere)')
		else:
			Current_Window.setProperty( 'Player_Type','MPlayer' )
			xbmc.executebuiltin('Skin.SetBool(SynopsisPreviewThere)')
		log('|   Found ' + PreviewFile)
		
def synopsis_mode_images():
	#####	Check for assets files.
	for root, dirs, files in os.walk( _Resources_Artwork ):
		for filename in files:
			if filename.startswith('banner'):
				Current_Window.setProperty( 'Synopsis_banner', root + '\\' + filename )
				log('|   Found ' + filename)
			if filename.startswith('fanart'):
				Current_Window.setProperty( 'Synopsis_fanart', root + '\\' + filename )
				log('|   Found ' + filename)
			if filename.startswith('poster'):
				Current_Window.setProperty( 'Synopsis_poster', root + '\\' + filename )
				log('|   Found ' + filename)
	
	#####	Get screenshots, xbe and cached thumb	
	Current_Window.setProperty( 'Synopsis_screenshots', _Resources_Screenshots )
	if os.path.exists( _Resources_Screenshots ): log('|   Found Screenshot folder')
	Current_Window.setProperty( 'Synopsis_xbe', GameXBE )
	if os.path.isfile( GameXBE ): log('|   Found default.xbe')
	Current_Window.setProperty( 'Synopsis_thumb', CachedThumb )
	if os.path.isfile( CachedThumb ): log('|   Found Cached Thumb')
	
def synopsis_mode_text():
	#####	Read XML & set
	if os.path.isfile( _Resources_Default_xml ):
		log('|   Found default.xml')
		xbmc.executebuiltin('Skin.Reset(nodefaultxml)')
		Synopsis_XML = open( _Resources_Default_xml, 'r' ).read()
		Output = BeautifulSoup( Synopsis_XML )
		try: # Title
			Current_Window.setProperty( 'Synopsis_title', Output.title.string )
			Current_Window.setProperty( 'Synopsis_title_alt', Output.title.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Developer
			Current_Window.setProperty( 'Synopsis_developer', Output.developer.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Publisher
			Current_Window.setProperty( 'Synopsis_publisher', Output.publisher.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Features General
			Current_Window.setProperty( 'Synopsis_features_general', Output.features_general.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: #  Features Online
			Current_Window.setProperty( 'Synopsis_features_online', Output.features_online.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # ESRB Rating
			Current_Window.setProperty( 'Synopsis_esrb', Output.esrb.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # ESRB Descriptors
			Current_Window.setProperty( 'Synopsis_esrb_descriptors', Output.esrb_descriptors.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Genre
			Current_Window.setProperty( 'Synopsis_genre', Output.genre.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Release Date
			Current_Window.setProperty( 'Synopsis_release_date', Output.release_date.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # GameRating
			Current_Window.setProperty( 'Synopsis_rating', Output.rating.string )
			if "0" <= Output.rating.string < "1":
				Current_Window.setProperty( 'Synopsis_rating_alt', "0" )
			if "1" <= Output.rating.string < "2":
				Current_Window.setProperty( 'Synopsis_rating_alt', "1" )
			if "2" <= Output.rating.string < "3":
				Current_Window.setProperty( 'Synopsis_rating_alt', "2" )
			if "3" <= Output.rating.string < "4":
				Current_Window.setProperty( 'Synopsis_rating_alt', "3" )
			if "4" <= Output.rating.string < "5":
				Current_Window.setProperty( 'Synopsis_rating_alt', "4" )
			if "5" <= Output.rating.string < "6":
				Current_Window.setProperty( 'Synopsis_rating_alt', "5" )
			if "6" <= Output.rating.string < "7":
				Current_Window.setProperty( 'Synopsis_rating_alt', "6" )
			if "7" <= Output.rating.string < "8":
				Current_Window.setProperty( 'Synopsis_rating_alt', "7" )
			if "8" <= Output.rating.string < "9":
				Current_Window.setProperty( 'Synopsis_rating_alt', "8" )
			if "9" <= Output.rating.string <= "9.9":
				Current_Window.setProperty( 'Synopsis_rating_alt', "9" )
			if "10" <= Output.rating.string <= "10.9":
				Current_Window.setProperty( 'Synopsis_rating_alt', "10" )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Platform
			Current_Window.setProperty( 'Synopsis_platform', Output.platform.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Exclusive
			Current_Window.setProperty( 'Synopsis_exclusive', Output.exclusive.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Title ID
			Current_Window.setProperty( 'Synopsis_titleid', Output.titleid.string )
			Current_Window.setProperty( 'Synopsis_titleid_alt', Output.titleid.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Overview
			Current_Window.setProperty( 'Synopsis_overview', Output.overview.string )
			Current_Window.setProperty( 'Synopsis_overview_alt', Output.overview.string )
		except(TypeError, KeyError, AttributeError):
			pass
	else:
		log('|   No default.xml found')
		xbmc.executebuiltin('Skin.SetBool(nodefaultxml)')
		Current_Window.setProperty( 'Synopsis_title','Could not find:' )
		Current_Window.setProperty( 'Synopsis_title_alt',GameName )
		Current_Window.setProperty( 'Synopsis_developer','' + _Resources_Default_xml )
		Current_Window.setProperty( 'Synopsis_titleid_alt','Null' )
		Current_Window.setProperty( 'Synopsis_overview_alt','No synopsis information found.' )

def preview_mode():
	log('|  Looking for preview video')
	if xbmc.getCondVisibility( 'Skin.HasSetting(PreviewExtension)' ) == 0:
		if os.path.isfile( Preview_default ):
			log('|   Found ' + Preview_default)
			Current_Window.setProperty( 'Preview_default', Preview_default )
		else:
			log('|   No preview video found')
	else:
		if os.path.isfile( Preview_alt ):
			log('|   Found ' + Preview_alt)
			Current_Window.setProperty( 'Preview_alt', Preview_alt )
		else:
			log('|   No preview video found')

def colours():
	#####	Read colour XML & set
	if os.path.isfile ( Colour_xml ):
		log('|   Parsing colours.xml')
		xbmc.executebuiltin('Skin.Reset(nodefaultxml)')
		Colour_XML = open( Colour_xml, 'r' ).read()
		Output = BeautifulSoup( Colour_XML )
		try: # Colour 1
			Current_Window.setProperty( 'Synopsis_colour_1', Output.colour_1.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Colour 2
			Current_Window.setProperty( 'Synopsis_colour_2', Output.colour_2.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Colour 3
			Current_Window.setProperty( 'Synopsis_colour_3', Output.colour_3.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Colour 4
			Current_Window.setProperty( 'Synopsis_colour_4', Output.colour_4.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # Colour 5
			Current_Window.setProperty( 'Synopsis_colour_5', Output.colour_5.string )
		except(TypeError, KeyError, AttributeError):
			pass
	else:
		log('|   No colour.xml found')

def labels():
	#####	Read labels XML & set
	if os.path.isfile ( Labels_xml ):
		log('|   Parsing labels.xml')
		xbmc.executebuiltin('Skin.Reset(nodefaultxml)')
		Labels_XML = open( Labels_xml, 'r' ).read()
		Output = BeautifulSoup( Labels_XML )
		try: # label 1
			Current_Window.setProperty( 'Synopsis_label_1', Output.label_1.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 2
			Current_Window.setProperty( 'Synopsis_label_2', Output.label_2.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 3
			Current_Window.setProperty( 'Synopsis_label_3', Output.label_3.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 4
			Current_Window.setProperty( 'Synopsis_label_4', Output.label_4.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 5
			Current_Window.setProperty( 'Synopsis_label_5', Output.label_5.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 6
			Current_Window.setProperty( 'Synopsis_label_6', Output.label_6.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 7
			Current_Window.setProperty( 'Synopsis_label_7', Output.label_7.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 8
			Current_Window.setProperty( 'Synopsis_label_8', Output.label_8.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 9
			Current_Window.setProperty( 'Synopsis_label_9', Output.label_9.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 10
			Current_Window.setProperty( 'Synopsis_label_10', Output.label_10.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 11
			Current_Window.setProperty( 'Synopsis_label_11', Output.label_11.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 12
			Current_Window.setProperty( 'Synopsis_label_12', Output.label_12.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 13
			Current_Window.setProperty( 'Synopsis_label_13', Output.label_13.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 14
			Current_Window.setProperty( 'Synopsis_label_14', Output.label_14.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 15
			Current_Window.setProperty( 'Synopsis_label_15', Output.label_15.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 16
			Current_Window.setProperty( 'Synopsis_label_16', Output.label_16.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 17
			Current_Window.setProperty( 'Synopsis_label_17', Output.label_17.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 18
			Current_Window.setProperty( 'Synopsis_label_18', Output.label_18.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 19
			Current_Window.setProperty( 'Synopsis_label_19', Output.label_19.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 20
			Current_Window.setProperty( 'Synopsis_label_20', Output.label_20.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 21
			Current_Window.setProperty( 'Synopsis_label_21', Output.label_21.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 22
			Current_Window.setProperty( 'Synopsis_label_22', Output.label_22.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 23
			Current_Window.setProperty( 'Synopsis_label_23', Output.label_23.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 24
			Current_Window.setProperty( 'Synopsis_label_24', Output.label_24.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 25
			Current_Window.setProperty( 'Synopsis_label_25', Output.label_25.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 26
			Current_Window.setProperty( 'Synopsis_label_26', Output.label_26.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 27
			Current_Window.setProperty( 'Synopsis_label_27', Output.label_27.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 28
			Current_Window.setProperty( 'Synopsis_label_28', Output.label_28.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 29
			Current_Window.setProperty( 'Synopsis_label_29', Output.label_29.string )
		except(TypeError, KeyError, AttributeError):
			pass
		try: # label 30
			Current_Window.setProperty( 'Synopsis_label_30', Output.label_30.string )
		except(TypeError, KeyError, AttributeError):
			pass
	else:
		log('|   No label.xml found')

def pars_font_xml(Font_Path):
	global fonts_installed
	if os.path.isfile( Font_Path ):
		Font_XML = BeautifulSoup( open( Font_Path, 'r' ).read() )
		try:
			log('|   Synopsis Fonts ' + Font_XML.synopsis_fonts.string)
		except(TypeError, KeyError, AttributeError):
			shutil.copyfile(Font_Path, Font_Path + '_backup')
			for line in fileinput.FileInput(Font_Path,inplace=1):
				if '<fontset' in line:
					line = line.replace(line,line+Fonts)
				print line,
				fonts_installed = 1
	
def check_fonts():
	#####	I could have used os.walk, but it took to long to search for the files, this way is far quicker
	global fonts_installed
	fonts_installed = 0
	Font_Path = Font_Path1
	pars_font_xml(Font_Path)
	Font_Path = Font_Path2
	pars_font_xml(Font_Path)
	Font_Path = Font_Path3
	pars_font_xml(Font_Path)
	Font_Path = Font_Path4
	pars_font_xml(Font_Path)
	Font_Path = Font_Path5
	pars_font_xml(Font_Path)
	Font_Path = Font_Path6
	pars_font_xml(Font_Path)
	if fonts_installed:
		xbmc.executebuiltin('dialog.close(all,true)')
		xbmcgui.Dialog().ok("Font install Complete","","Synopsis fonts added to the Font.xml","I will need to reload the skin to finish.")
		xbmc.executebuiltin('ReloadSkin')
		log('|   Synopsis Fonts written to Font.xml')
	
def clear_properties():
	#####	default.xml
	Current_Window.setProperty( 'Synopsis_title','' )
	Current_Window.setProperty( 'Synopsis_title_alt','' )
	Current_Window.setProperty( 'Synopsis_developer','' )
	Current_Window.setProperty( 'Synopsis_publisher','' )
	Current_Window.setProperty( 'Synopsis_features_general','' )
	Current_Window.setProperty( 'Synopsis_features_online','' )	
	Current_Window.setProperty( 'Synopsis_esrb','' )
	Current_Window.setProperty( 'Synopsis_esrb_descriptors','' )
	Current_Window.setProperty( 'Synopsis_genre','' )
	Current_Window.setProperty( 'Synopsis_release_date','' )
	Current_Window.setProperty( 'Synopsis_rating','' )
	Current_Window.setProperty( 'Synopsis_rating_alt', '' )
	Current_Window.setProperty( 'Synopsis_platform','' )
	Current_Window.setProperty( 'Synopsis_exclusive','' )
	Current_Window.setProperty( 'Synopsis_titleid','' )
	Current_Window.setProperty( 'Synopsis_titleid_alt','' )
	Current_Window.setProperty( 'Synopsis_overview','' )
	Current_Window.setProperty( 'Synopsis_overview_alt','' )
	#####	assets ( videos, images eg... )
	Current_Window.setProperty( 'Synopsis_banner', '' )
	Current_Window.setProperty( 'Synopsis_fanart', '' )
	Current_Window.setProperty( 'Synopsis_poster', '' )
	Current_Window.setProperty( 'Synopsis_screenshots', '' )
	Current_Window.setProperty( 'Synopsis_xbe', '' )
	Current_Window.setProperty( 'Synopsis_thumb', '' )
	Current_Window.setProperty( 'Synopsis_Video_Preview_Name', 'No Preview Video Found' )
	Current_Window.setProperty( 'Synopsis_Video_Preview_Path','' )
	Current_Window.setProperty( 'Preview_default', '' )
	Current_Window.setProperty( 'Preview_alt', '' )			
	#####	colours.xml
	Current_Window.setProperty( 'Synopsis_colour_1','FF399EDA' )
	Current_Window.setProperty( 'Synopsis_colour_2','FF969696' )
	Current_Window.setProperty( 'Synopsis_colour_3','FF969696' )
	Current_Window.setProperty( 'Synopsis_colour_4','FF969696' )
	Current_Window.setProperty( 'Synopsis_colour_5','FF969696' )
	#####	labels.xml
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
	
#####	load window xml and check key presses/movement.
class GUI(windowdialog):
	def onInit(self):
		log('|-------------------------------------------------------------------------------')
		if xbmc.getCondVisibility( 'Skin.HasSetting(SynopsisMode)' ):
			log('|  Scanning for assets')
			log('|-------------------------------------------------------------------------------')
			synopsis_mode_text()
			synopsis_mode_images()
			synopsis_mode_video()
			if xbmc.getCondVisibility( 'Skin.HasSetting(Synopsis_alt_view)' ) and xbmc.getCondVisibility( 'Skin.HasSetting(Synopsis_Autoplay)' ): time.sleep(1)
			xbmc.executebuiltin('SetFocus(10)')
		else:
			preview_mode()
			time.sleep(1)
			xbmc.executebuiltin('SetFocus(10)')
		log('|===============================================================================')
		
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
		
if (__name__ == '__main__'):
	logging = ""
	#####	Start markings for the log file.
	log('|===============================================================================')
	log('| Scripts\XBMC4Kids Extras\Synopsis\default.py loaded.')
	log('|-------------------------------------------------------------------------------')
	log('|  Initializing')
	log('|-------------------------------------------------------------------------------')
	check_fonts()
	clear_properties()
	colours()
	labels()
	xbmc.executebuiltin('dialog.close(all,true)')
	#####	UI.
	if not fonts_installed:
		ui = GUI( '_Script_Synopsis.xml', os.getcwd() )
		ui.doModal()
		del ui
	
	#####	Used to focus the games list when using the script in dialog mode
	if UseDialog == 'dialog': xbmc.executebuiltin('SetFocus(50)')