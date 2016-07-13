########################################################################################################################################
'''
	Script by Rocky5
	Extracts information from a file named default.xml located in the "_resources" folder.
'''
########################################################################################################################################


import os
import xbmcgui
import xbmc
import shutil
import glob
import fileinput
import time
from BeautifulSoup import *


########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XBMC4Kids\Synopsis\default.py loaded."
print "| ------------------------------------------------------------------------------"
	

########################################################################################################################################
# Sets paths & other crap.
########################################################################################################################################
Current_Window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
HasSetting_PreviewExtension = xbmc.getCondVisibility( 'Skin.HasSetting(PreviewExtension)' )
##
ThumbCache = xbmc.getCacheThumbName( xbmc.getInfoLabel('ListItem.FolderPath') )
CurProfileGuiSettings = xbmc.translatePath( 'special://profile/guisettings.xml' )
Video_Name = "Preview"
##
GameFolder = xbmc.getInfoLabel('ListItem.FolderName')
_Resources_Path = os.path.join( xbmc.getInfoLabel('ListItem.Path'), "_resources/default.xml" )
_Resources_Preview_Path = os.path.join( xbmc.getInfoLabel("ListItem.Path"), "_resources/media/" )


########################################################################################################################################
# Read XML & set
########################################################################################################################################
if os.path.isfile ( _Resources_Path ):
	Synopsis_XML = open( _Resources_Path, "r" ).read()
	Output = BeautifulSoup( Synopsis_XML )
	
	try: # Title
		Current_Window.setProperty( "Synopsis_title","[COLOR=synopsiscolour1]Title: [/COLOR][COLOR=synopsiscolour2]" + Output.title.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_title","[COLOR=synopsiscolour1]Title: [/COLOR]" )
	
	try: # Developer
		Current_Window.setProperty( "Synopsis_developer","[COLOR=synopsiscolour1]Developer: [/COLOR][COLOR=synopsiscolour2]" + Output.developer.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_developer","[COLOR=synopsiscolour1]Developer: [/COLOR]" )
	
	try: # Publisher
		Current_Window.setProperty( "Synopsis_publisher","[COLOR=synopsiscolour1]Publisher: [/COLOR][COLOR=synopsiscolour2]" + Output.publisher.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_publisher","[COLOR=synopsiscolour1]Publisher: [/COLOR]" )
	
	try: # Release Date
		Current_Window.setProperty( "Synopsis_release_date","[COLOR=synopsiscolour1]Release Date: [/COLOR][COLOR=synopsiscolour2]" + Output.release_date.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_release_date","[COLOR=synopsiscolour1]Release Date: [/COLOR]" )
		
	try: # Genre
		Current_Window.setProperty( "Synopsis_genre","[COLOR=synopsiscolour1]Genre: [/COLOR][COLOR=synopsiscolour2]" + Output.genre.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_genre","[COLOR=synopsiscolour1]Genre: [/COLOR]" )
	
	try: # Features General
		Current_Window.setProperty( "Synopsis_features_general","[COLOR=synopsiscolour1]General Features: [/COLOR][COLOR=synopsiscolour2]" + Output.features_general.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_features_general","[COLOR=synopsiscolour1]General Features: [/COLOR][COLOR=synopsiscolour2][/COLOR]" )
	
	try: #  Features Online
		Current_Window.setProperty( "Synopsis_features_online","[COLOR=synopsiscolour1]Online Features: [/COLOR][COLOR=synopsiscolour2]" + Output.features_online.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_features_online","[COLOR=synopsiscolour1]Online Features: [/COLOR]" )		
	
	try: # Exclusive
		Current_Window.setProperty( "Synopsis_exclusive","[COLOR=synopsiscolour1]Exclusive: [/COLOR][COLOR=synopsiscolour2]" + Output.exclusive.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_exclusive","[COLOR=synopsiscolour1]Exclusive: [/COLOR]" )

	try: # ESRB Rating
		Current_Window.setProperty( "Synopsis_esrb","[COLOR=synopsiscolour1]ESRB: [/COLOR][COLOR=synopsiscolour2]" + Output.esrb.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_esrb","[COLOR=synopsiscolour1]ESRB: [/COLOR]" )
	
	try: # ESRB Descriptors
		Current_Window.setProperty( "Synopsis_esrb_descriptors","[COLOR=synopsiscolour1]ESRB Descriptor: [/COLOR][COLOR=synopsiscolour2]" + Output.esrb_descriptors.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_esrb_descriptors","[COLOR=synopsiscolour1]ESRB Descriptor: [/COLOR]" )
		
	try: # Platform
		Current_Window.setProperty( "Synopsis_platform","[COLOR=synopsiscolour1]Platform: [/COLOR][COLOR=synopsiscolour2]" + Output.platform.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_platform","[COLOR=synopsiscolour1]Platform: [/COLOR]" )
			
	try: # Title ID
		Current_Window.setProperty( "Synopsis_titleid","[COLOR=synopsiscolour1]TitleId: [/COLOR][COLOR=synopsiscolour2]" + Output.titleid.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_titleid","[COLOR=synopsiscolour1]TitleId: [/COLOR]" )
	
	try: # Overview
		Current_Window.setProperty( "Synopsis_overview","[COLOR=synopsiscolour1]Overview: [/COLOR][COLOR=synopsiscolour2]" + Output.overview.string + "[/COLOR]" )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Synopsis_overview","[COLOR=synopsiscolour1]Overview: [/COLOR]" )

	try: # Thumb
		Current_Window.setProperty( "Synopsis_thumb", "special://profile/Thumbnails/Programs/%s/%s" % ( ThumbCache[0], ThumbCache, ) )
	except(TypeError, KeyError):
		Current_Window.setProperty( "Thumb", "" )

	xbmc.executebuiltin("SetFocus(9004)")
	print "================================================================================"
else:
	Current_Window.setProperty( "Synopsis_title","[COLOR=synopsiscolour1]Could not find:[/COLOR]" )
	Current_Window.setProperty( "Synopsis_developer","[COLOR=synopsiscolour2]" + GameFolder + "\\" + _Resources + "[/COLOR]" )
	Current_Window.setProperty( "Synopsis_publisher","" )
	Current_Window.setProperty( "Synopsis_platform","" )
	Current_Window.setProperty( "Synopsis_release_date","" )
	Current_Window.setProperty( "Synopsis_region","" )
	Current_Window.setProperty( "Synopsis_esrb","" )
	Current_Window.setProperty( "Synopsis_esrb_descriptors","" )
	Current_Window.setProperty( "Synopsis_genre","" )
	Current_Window.setProperty( "Synopsis_features_general","" )
	Current_Window.setProperty( "Synopsis_features_online","" )
	Current_Window.setProperty( "Synopsis_exclusive","" )
	Current_Window.setProperty( "Synopsis_mediatype","" )
	Current_Window.setProperty( "Synopsis_titleid","" )
	Current_Window.setProperty( "Synopsis_overview","" )
	Current_Window.setProperty( "Synopsis_overview","" )
	Current_Window.setProperty( "Synopsis_thumb", "special://profile/Thumbnails/Programs/%s/%s" % ( ThumbCache[0], ThumbCache, ) )
	xbmc.executebuiltin("SetFocus(9004)")
	print "================================================================================"

	
########################################################################################################################################
# Play Preview video
########################################################################################################################################
if HasSetting_PreviewExtension:
	Preview_File = _Resources_Preview_Path + Video_Name + "." + xbmc.getInfoLabel("Skin.String(PreviewFileExtension)")
	if os.path.isfile (Preview_File):
		print "| " + Preview_File
		Player = xbmc.Player( xbmc.PLAYER_CORE_MPLAYER )
		Player.play( Preview_File, "", True )
	else:
		print "| Not found: " + Preview_File
else:		
	Preview_File = _Resources_Preview_Path + Video_Name + ".xmv"
	if os.path.isfile (Preview_File):
		print "| " + Preview_File
		Player = xbmc.Player( xbmc.PLAYER_CORE_DVDPLAYER )
		Player.play( Preview_File, "", True )
	else:
		print "| Not found: " + Preview_File