# -*- coding: utf-8 -*- 
'''
	Script by Rocky5
	Used to create items for the home screen
	Concept by Dom DXecutioner (Origins)
	
	Features:
		1. Random items pulled from your DB, if none of the XBMC4Gamers stuff is found it will use cached thumbs
		2. Last played items, this will display the last 10 items you have run.
		3. Refresh custom entries after being selected and home screen is returned to.
		4. 10 Recent items using the Y button when in the programs window.
	
'''
from os.path import isdir, dirname, isfile, join
from sys import argv
from xbmc import executebuiltin, executehttpapi, getCacheThumbName, getCondVisibility, getInfoLabel, translatePath
from xbmcgui import Dialog, getCurrentWindowId, Window
import sqlite3
import time
import xml.etree.ElementTree as ET

dialog = Dialog()
myprograms6_db	= translatePath("special://profile/database/MyPrograms6.db")
theme_override	= translatePath("special://skin/xml/Includes_Theme_Override.xml")
force64mbassets	= executehttpapi('GetGUISetting(1;mygames.games128mbartwork)')
usecachedthumbs	= getInfoLabel("Skin.HasSetting(UseCachedThumbs)")
use128mbassets	= getInfoLabel("System.memory(total)")
noblurredfanart	= getInfoLabel("Skin.HasSetting(UseNoBlurredFanart)")

class PopulateHome:
	homewindow = Window(10000)
	programswindow = Window(10001)

	def __init__(self):

		arg = argv[1] if len(argv) > 1 else "refresh_randoms"
			
		# Default search parameters
		searches = {
			"games": "Games",
			"brews": "Homebrew,Ports",
			"emus": "Emulators,Emus",
			"apps": "Applications,Apps",
			"custom1": getInfoLabel("Skin.String(CustomHomeButton1Search)") or getInfoLabel("Skin.String(CustomHomeButton1Name)"),
			"custom2": getInfoLabel("Skin.String(CustomHomeButton2Search)") or getInfoLabel("Skin.String(CustomHomeButton2Name)"),
			"custom3": getInfoLabel("Skin.String(CustomHomeButton3Search)") or getInfoLabel("Skin.String(CustomHomeButton3Name)"),
			"custom4": getInfoLabel("Skin.String(CustomHomeButton4Search)") or getInfoLabel("Skin.String(CustomHomeButton4Name)")
		}
		enabled = {
			"games": not getInfoLabel("Skin.HasSetting(DisableHome1)"),
			"brews": not getInfoLabel("Skin.HasSetting(DisableHome2)"),
			"emus": not getInfoLabel("Skin.HasSetting(DisableHome3)"),
			"apps": not getInfoLabel("Skin.HasSetting(DisableHome4)"),
			"custom1": getInfoLabel("Skin.HasSetting(CustomHomeButton1Enabled)"),
			"custom2": getInfoLabel("Skin.HasSetting(CustomHomeButton2Enabled)"),
			"custom3": getInfoLabel("Skin.HasSetting(CustomHomeButton3Enabled)"),
			"custom4": getInfoLabel("Skin.HasSetting(CustomHomeButton4Enabled)")
		}
		
		self.source_focus = self.get_source_focus()
		self.lastplayed_total, self.randoms_total = self.ParseOverride(theme_override)
		self.load_database()

		try:
			if arg == "refresh_home_gotohome":
				self.populate_lastplayed(enabled, searches)
				self.populate_randoms(enabled, searches)
				self.populate_recents()
				self.Check_For_HomeWindow()
			
			if arg == "refresh_home":
				self.populate_lastplayed(enabled, searches)
				self.populate_randoms(enabled, searches)
				self.populate_recents()
			
			if arg == "refresh_media":
				self.refresh_media_played(enabled, searches)
			
			if arg == "refresh_randoms":
				self.populate_randoms(enabled, searches)
			
			if arg == "refresh_recents":
				self.populate_recents()
				self.Load_ProgramsWindow()
		except Exception as error:
			print error
			executebuiltin("Dialog.Close(1100)")
			executebuiltin("ActivateWindow(Programs)")
			Dialog().ok("Parsing MyPrograms6.db Error",
'''Navigate to:
"Settings > XBMC4Xbox Setting > Debug > View Log Files"

Send me a picture of the last few lines of the latest log file.''')

	def get_source_focus(self):
		for control_id in range(100, 109):
			if getCondVisibility('ControlGroup(1).HasFocus({})'.format(control_id)):
				return control_id
		return 0

	def load_database(self):
		self.conn = sqlite3.connect(myprograms6_db)
		self.conn.row_factory = sqlite3.Row

	def populate_randoms(self, enabled, searches):
		if enabled["games"] and (self.source_focus == 100 or self.source_focus == 0):
			self.Random("RandomGames," + searches["games"])
		if enabled["brews"] and (self.source_focus == 101 or self.source_focus == 0):
			self.Random("RandomBrews," + searches["brews"])
		if enabled["emus"] and (self.source_focus == 102 or self.source_focus == 0):
			self.Random("RandomEmus," + searches["emus"])
		if enabled["apps"] and (self.source_focus == 103 or self.source_focus == 0):
			self.Random("RandomApps," + searches["apps"])
		if enabled["custom1"] and searches["custom1"] and (self.source_focus == 104 or self.source_focus == 0):
			self.Random("RandomCustom1," + searches["custom1"])
		if enabled["custom2"] and searches["custom2"] and (self.source_focus == 105 or self.source_focus == 0):
			self.Random("RandomCustom2," + searches["custom2"])
		if enabled["custom3"] and searches["custom3"] and (self.source_focus == 106 or self.source_focus == 0):
			self.Random("RandomCustom3," + searches["custom3"])
		if enabled["custom4"] and searches["custom4"] and (self.source_focus == 107 or self.source_focus == 0):
			self.Random("RandomCustom4," + searches["custom4"])

	def populate_lastplayed(self, enabled, searches):
		if enabled["games"]:
			self.LastPlayed("LastPlayedGames," + searches["games"])
		if enabled["brews"]:
			self.LastPlayed("LastPlayedBrews," + searches["brews"])
		if enabled["emus"]:
			self.LastPlayed("LastPlayedEmus," + searches["emus"])
		if enabled["apps"]:
			self.LastPlayed("LastPlayedApps," + searches["apps"])
		if enabled["custom1"] and searches["custom1"]:
			self.LastPlayed("LastPlayedCustom1," + searches["custom1"])
		if enabled["custom2"] and searches["custom2"]:
			self.LastPlayed("LastPlayedCustom2," + searches["custom2"])
		if enabled["custom3"] and searches["custom3"]:
			self.LastPlayed("LastPlayedCustom3," + searches["custom3"])
		if enabled["custom4"] and searches["custom4"]:
			self.LastPlayed("LastPlayedCustom4," + searches["custom4"])

	def populate_recents(self):
		self.RecentPlayed("RecentPlayed")

	def refresh_media_played(self, enabled, searches):
		if enabled["custom1"] and searches["custom1"] and self.source_focus == 104:
			self.LastPlayed("LastPlayedCustom1," + searches["custom1"])
		if enabled["custom2"] and searches["custom2"] and self.source_focus == 105:
			self.LastPlayed("LastPlayedCustom2," + searches["custom2"])
		if enabled["custom3"] and searches["custom3"] and self.source_focus == 106:
			self.LastPlayed("LastPlayedCustom3," + searches["custom3"])
		if enabled["custom4"] and searches["custom4"] and self.source_focus == 107:
			self.LastPlayed("LastPlayedCustom4," + searches["custom4"])

	def Check_For_HomeWindow( self ):
		if getCurrentWindowId() != 10000:
			executebuiltin('ActivateWindow(Home)')

	def Load_ProgramsWindow( self ):
		executebuiltin('ActivateWindow(Programs,{})'.format(getInfoLabel("Skin.String(HomeWindow)")))

	def Random(self, var):
		increment = 0
		propertyvalue = var.split(',')[0]
		executebuiltin("Skin.Reset(" + propertyvalue + ")")

		search_params = var.split(',')[1:]

		for i in range(len(search_params)):
			if ":\\" not in search_params[i]:
				search_params[i] = "%\\{}".format(search_params[i])

		found_fields = set()
		valid_fields = []
		query_limit = 200

		while increment < self.randoms_total and len(valid_fields) < self.randoms_total:
			params = 'SELECT * FROM files WHERE ' + ' OR '.join(['LOWER(strFileName) LIKE LOWER("{}\\%")'.format(param) for param in search_params if param])
			params += ' ORDER BY RANDOM() LIMIT {}'.format(query_limit)

			results = self.ParseDB(self.conn, params)

			for field in results:
				if isfile(field['strFileName']) and field['strFileName'] not in found_fields:
					valid_fields.append(field)
					found_fields.add(field['strFileName'])
					increment += 1
					if increment >= self.randoms_total:
						break

			if len(results) < query_limit:
				break

		for index, field in enumerate(valid_fields[:self.randoms_total]):
			artwork = self.Artwork(field)
			if artwork[0] != "":
				self.homewindow.setProperty(propertyvalue + '.%d.Poster' % (index + 1), artwork[0])
				self.homewindow.setProperty(propertyvalue + '.%d.PosterThumb' % (index + 1), artwork[1])
				self.homewindow.setProperty(propertyvalue + '.%d.FanartThumb' % (index + 1), artwork[2])
				self.homewindow.setProperty(propertyvalue + '.%d.Fanart' % (index + 1), artwork[3])
				self.homewindow.setProperty(propertyvalue + '.%d.LargePoster' % (index + 1), artwork[4])
				self.homewindow.setProperty(propertyvalue + '.%d.Title' % (index + 1), field['altname'] if 'altname' in field.keys() and field['altname'].strip() else field['xbedescription'])
				self.homewindow.setProperty(propertyvalue + '.%d.XBEPath' % (index + 1), "RunXBE({},{})".format(field['strFileName'], field['iRegion'] if 'iRegion' in field.keys() and field['iRegion'] != -1 else 0))
				self.homewindow.setProperty(propertyvalue + '.%d.Rating' % (index + 1), field['rating'])
				self.homewindow.setProperty(propertyvalue + '.%d.ExtraInfo' % (index + 1), self.ExtraInfo(field))
				self.homewindow.setProperty(propertyvalue + '.%d.Synopsis' % (index + 1), truncate_with_ellipsis(field['synopsis'], 265))

		if increment > 0:
			executebuiltin("Skin.SetBool(" + propertyvalue + ")")

	def LastPlayed(self, var):
		datesfound = []
		increment = 0
		propertyvalue = var.split(',')[0]
		executebuiltin("Skin.Reset(" + propertyvalue + ")")

		for i in range(self.lastplayed_total):
			self.homewindow.setProperty(propertyvalue + '.%d.Title' % (i + 1), '')

		search_params = var.split(',')[1:]

		for i in range(len(search_params)):
			if ":\\" not in search_params[i]:
				search_params[i] = "%\\{}".format(search_params[i])

		params = 'SELECT DISTINCT last_played FROM files WHERE ' + ' OR '.join(['LOWER(strFileName) LIKE LOWER("{}\\%")'.format(param) for param in search_params if param])
		params += ' ORDER BY last_played DESC LIMIT {}'.format(self.lastplayed_total)

		results = self.ParseDB(self.conn, params)
		datesfound = [field['last_played'] for field in results if field['last_played'] != ""]

		found_fields = set()
		valid_fields = []

		for date in datesfound:
			if increment >= self.lastplayed_total and len(valid_fields) >= self.lastplayed_total:
				break
			file_query = 'SELECT * FROM files WHERE last_played LIKE "%{}%"'.format(date)
			file_results = self.ParseDB(self.conn, file_query)

			for field in file_results:
				if isfile(field['strFileName']) and field['strFileName'] not in found_fields:
					valid_fields.append(field)
					found_fields.add(field['strFileName'])
					increment += 1
					if increment >= self.lastplayed_total:
						break

		for index, field in enumerate(valid_fields[:self.lastplayed_total]):
			artwork = self.Artwork(field)
			if artwork[0] != "":
				self.homewindow.setProperty(propertyvalue + '.%d.Poster' % (index + 1), artwork[0])
				self.homewindow.setProperty(propertyvalue + '.%d.PosterThumb' % (index + 1), artwork[1])
				self.homewindow.setProperty(propertyvalue + '.%d.FanartThumb' % (index + 1), artwork[2])
				self.homewindow.setProperty(propertyvalue + '.%d.Fanart' % (index + 1), artwork[3])
				self.homewindow.setProperty(propertyvalue + '.%d.LargePoster' % (index + 1), artwork[4])
				self.homewindow.setProperty(propertyvalue + '.%d.Title' % (index + 1), field['altname'] if 'altname' in field.keys() and field['altname'].strip() else field['xbedescription'])
				self.homewindow.setProperty(propertyvalue + '.%d.XBEPath' % (index + 1), "RunXBE({},{})".format(field['strFileName'], field['iRegion'] if 'iRegion' in field.keys() and field['iRegion'] != -1 else 0))
				self.homewindow.setProperty(propertyvalue + '.%d.Rating' % (index + 1), field['rating'])
				self.homewindow.setProperty(propertyvalue + '.%d.ExtraInfo' % (index + 1), self.ExtraInfo(field))
				self.homewindow.setProperty(propertyvalue + '.%d.Synopsis' % (index + 1), truncate_with_ellipsis(field['synopsis'], 365))

		if increment > 0:
			executebuiltin("Skin.SetBool(" + propertyvalue + ")")

	def RecentPlayed(self, propertyvalue):
		datesfound = []
		increment = 0
		total_limit = 10
		exclude_patterns = ['4C464456'] # 4C464456 (VDFL) int 1279673430
		
		for i in range(total_limit):
			self.programswindow.setProperty(propertyvalue + '.%d.Title' % (i + 1), '')

		params = 'SELECT DISTINCT last_played FROM files ORDER BY last_played DESC'
		results = self.ParseDB(self.conn, params)
		datesfound = [field['last_played'] for field in results if field['last_played'] != ""]

		found_fields = set()
		valid_fields = []

		for date in datesfound:
			file_query = 'SELECT * FROM files WHERE last_played LIKE "%{}%"'.format(date)
			file_results = self.ParseDB(self.conn, file_query)

			for field in file_results:
				titleid_str = "%08X" % field['titleid']
				if (isfile(field['strFileName']) and field['strFileName'] not in found_fields and titleid_str not in exclude_patterns):
					valid_fields.append(field)
					found_fields.add(field['strFileName'])
					increment += 1
					if increment >= total_limit:
						break

			if len(valid_fields) >= total_limit:
				break

		for index, field in enumerate(valid_fields[:total_limit]):
			artwork = self.Artwork(field)
			if artwork[0] != "":
				self.programswindow.setProperty(propertyvalue + '.%d.Poster' % (index + 1), artwork[0])
				self.programswindow.setProperty(propertyvalue + '.%d.Title' % (index + 1), field['altname'] if 'altname' in field.keys() and field['altname'].strip() else field['xbedescription'])
				self.programswindow.setProperty(propertyvalue + '.%d.XBEPath' % (index + 1), "RunXBE({},{})".format(field['strFileName'], field['iRegion'] if 'iRegion' in field.keys() and field['iRegion'] != -1 else 0))

	def Artwork(self, var):
		field_xbe_path = var['strFileName']
		field_resources_path = var['resources']
		artwork_files = {
			"fanart_thumb": join(field_resources_path, "artwork/fanart_thumb.jpg"),
			"fanart_blur": join(field_resources_path, "artwork/fanart-blur.jpg"),
			"synopsis": join(field_resources_path, "artwork/synopsis.jpg"),
			"poster": join(field_resources_path, "artwork/poster.jpg"),
			"thumb": join(field_resources_path, "artwork/thumb.jpg"),
			"fanart": join(field_resources_path, "artwork/fanart.jpg")
		}
		file_exists = {key: isfile(path) for key, path in artwork_files.items()}
		
		thumbcache = getCacheThumbName(field_xbe_path)
		cachedthumb = 'Special://profile/Thumbnails/Programs/{}/{}'.format(thumbcache[0], thumbcache)

		if noblurredfanart:
			artwork_files["fanart_blur"] = artwork_files["fanart"]
		
		if usecachedthumbs and not isfile(cachedthumb):
			executebuiltin('CacheThumbnail("{}", "{}")'.format(artwork_files["poster"], cachedthumb))
			poster = cachedthumb
		else:
			poster = artwork_files["synopsis"] if not "64" in use128mbassets and "True" in force64mbassets else artwork_files["poster"]
			poster = poster if file_exists.get(poster) else cachedthumb if not file_exists["poster"] else artwork_files["poster"]

		posterthumb = artwork_files["thumb"] if file_exists["thumb"] else poster
		fanartthumb = artwork_files["fanart_thumb"] if file_exists["fanart_thumb"] else poster
		fanart = artwork_files["fanart_blur"] if file_exists["fanart_blur"] else join(dirname(field_xbe_path), 'fanart.jpg')
		fanart = fanart if isfile(fanart) else "no_fanart.jpg"
		largeposter = artwork_files["synopsis"] if file_exists["synopsis"] else poster

		return poster, posterthumb, fanartthumb, fanart, largeposter

	def ExtraInfo(self, var):
		parts = [var['features_online'], var['release_date'], var['esrb_descriptors']]
		info = " · ".join(filter(None, parts))
		return info

	def ParseDB(self, conn, var):
		conn.text_factory = str
		cur = conn.cursor()
		cur.execute(var)
		results = cur.fetchall()
		cur.close()
		return results

	def ParseOverride(self, var):
		self.lastplayed_total = 10
		self.randoms_total = 10
		
		if isfile(var):
			elements = ET.parse(var).getroot().iter()
			for lines_checked, element in enumerate(elements, start=1):
				if element.tag.lower() == 'parse_lastplayed_total' and element.text:
					self.lastplayed_total = int(element.text)
				elif element.tag.lower() == 'parse_randoms_total' and element.text:
					self.randoms_total = int(element.text)
				if self.lastplayed_total != 10 and self.randoms_total != 10:
					break
				if lines_checked >= 20:
					break
					
		return self.lastplayed_total, self.randoms_total

def truncate_with_ellipsis(text, max_length):
	text = ' '.join(text.split()).strip()
	if len(text) <= max_length:
		return text
	else:
		last_space_index = text.rfind(' ', 0, max_length)
		if last_space_index == -1:
			return text[:max_length]
		else:
			return text[:last_space_index] + "..."

if __name__ == "__main__":
	if isfile(myprograms6_db):
		print "Loaded Parse Programs DB.py"
		start_time = time.time()
		
		try:
			PopulateHome()
			executebuiltin("Dialog.Close(1100)")
		finally:
			if 'conn' in locals():
				conn.close()
		
		print "Unloaded Parse Programs DB.py - took {} seconds to complete".format(int(round(time.time() - start_time)))
	else:
		executebuiltin("ActivateWindow(Programs)")