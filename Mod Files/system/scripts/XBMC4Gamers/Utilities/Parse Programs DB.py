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
import datetime
import os
import sqlite3
import sys
import time
import xbmc
import xbmcgui
import xml.etree.ElementTree as ET

dialog = xbmcgui.Dialog()
myprograms6_db	= xbmc.translatePath("special://profile/database/MyPrograms6.db")
theme_override	= xbmc.translatePath("special://skin/xml/Includes_Theme_Override.xml")
force64mbassets	= xbmc.executehttpapi('GetGUISetting(1;mygames.games128mbartwork)')
usecachedthumbs	= xbmc.getInfoLabel("Skin.HasSetting(UseCachedThumbs)")
use128mbassets	= xbmc.getInfoLabel("System.memory(total)")
noblurredfanart	= xbmc.getInfoLabel("Skin.HasSetting(UseNoBlurredFanart)")

class PopulateHome:
	homewindow = xbmcgui.Window(10000)
	programswindow = xbmcgui.Window(10001)

	def __init__(self):
		try:
			arg = sys.argv[1]
		except:
			arg = "refresh_randoms"
			
		# Default search parameters
		searches = {
			"games": "Games",
			"brews": "Homebrew,Ports",
			"emus": "Emulators,Emus",
			"apps": "Applications,Apps",
			"custom1": xbmc.getInfoLabel("Skin.String(CustomHomeButton1Search)"),
			"custom2": xbmc.getInfoLabel("Skin.String(CustomHomeButton2Search)"),
			"custom3": xbmc.getInfoLabel("Skin.String(CustomHomeButton3Search)"),
			"custom4": xbmc.getInfoLabel("Skin.String(CustomHomeButton4Search)")
		}
		enabled = {
			"games": not xbmc.getInfoLabel("Skin.HasSetting(DisableHome1)"),
			"brews": not xbmc.getInfoLabel("Skin.HasSetting(DisableHome2)"),
			"emus": not xbmc.getInfoLabel("Skin.HasSetting(DisableHome3)"),
			"apps": not xbmc.getInfoLabel("Skin.HasSetting(DisableHome4)"),
			"custom1": xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton1Enabled)"),
			"custom2": xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton2Enabled)"),
			"custom3": xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton3Enabled)"),
			"custom4": xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton4Enabled)")
		}
		
		self.source_focus = self.get_source_focus()
		self.lastplayed_total, self.randoms_total = self.ParseOverride(theme_override)
		if arg == "refresh_home_gotohome":
			self.memory_db = self.load_database(1)
		else: self.memory_db = self.load_database(0)

		try:
			if arg == "refresh_home_gotohome":
				self.populate_lastplayed(enabled, searches)
				self.populate_randoms(enabled, searches)
				self.populate_recents(searches)
				self.Check_For_HomeWindow()
			
			if arg == "refresh_home":
				self.populate_lastplayed(enabled, searches)
				self.populate_randoms(enabled, searches)
			
			if arg == "refresh_media":
				self.refresh_media_played(enabled, searches)
			
			if arg == "refresh_randoms":
				self.populate_randoms(enabled, searches)
			
			if arg == "refresh_recents":
				self.populate_recents(searches)
				self.Load_ProgramsWindow()
		
		except Exception as error:
			print error
			xbmc.executebuiltin("Dialog.Close(1100)")
			xbmc.executebuiltin("ActivateWindow(Programs)")
			xbmcgui.Dialog().ok("Parsing MyPrograms6.db Error",
'''Navigate to:
"Settings > XBMC4Xbox Setting > Debug > View Log Files"

Send me a picture of the last few lines of the latest log file.''')
	
	def get_source_focus(self):
		for control_id in range(100, 109):
			if xbmc.getCondVisibility('ControlGroup(1).HasFocus({})'.format(control_id)):
				return control_id
		return 0

	def load_database(self, var):
		if var:
			return self.database_to_memory(myprograms6_db)
		else:
			return myprograms6_db

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

	def populate_recents(self, searches):
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
		if xbmcgui.getCurrentWindowId() != 10000:
			xbmc.executebuiltin('ActivateWindow(Home)')

	def Load_ProgramsWindow( self ):
		xbmc.executebuiltin('ActivateWindow(Programs,{})'.format(xbmc.getInfoLabel("Skin.String(HomeWindow)")))

	def Random(self, var):
		increment = 0
		propertyvalue = var.split(',')[0]
		xbmc.executebuiltin("Skin.Reset(" + propertyvalue + ")")

		search_params = var.split(',')[1:]

		for i in range(len(search_params)):
			if ":\\" not in search_params[i]:
				search_params[i] = "%:\\{}".format(search_params[i])

		found_fields = set()
		valid_fields = []
		query_limit = 200

		while increment < self.randoms_total and len(valid_fields) < self.randoms_total:
			params = 'SELECT * FROM files WHERE ' + ' OR '.join(['strFileName LIKE "{}\\%"'.format(param) for param in search_params if param])
			params += ' ORDER BY RANDOM() LIMIT {}'.format(query_limit)

			results = self.ParseDB(self.memory_db, params)

			for field in results:
				if os.path.isfile(field['strFileName']) and field['strFileName'] not in found_fields:
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
				self.homewindow.setProperty(propertyvalue + '.%d.Title' % (index + 1), field['altname'] if 'altname' in field.keys() else 'Unknown Title')
				self.homewindow.setProperty(propertyvalue + '.%d.XBEPath' % (index + 1), "RunXBE(" + field['strFileName'] + ")")
				self.homewindow.setProperty(propertyvalue + '.%d.Rating' % (index + 1), field['rating'])
				self.homewindow.setProperty(propertyvalue + '.%d.ExtraInfo' % (index + 1), self.ExtraInfo(field))
				self.homewindow.setProperty(propertyvalue + '.%d.Synopsis' % (index + 1), truncate_with_ellipsis(field['synopsis'], 265))

		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(" + propertyvalue + ")")

	def LastPlayed(self, var):
		datesfound = []
		increment = 0
		propertyvalue = var.split(',')[0]
		xbmc.executebuiltin("Skin.Reset(" + propertyvalue + ")")

		for i in range(self.lastplayed_total):
			self.homewindow.setProperty(propertyvalue + '.%d.Title' % (i + 1), '')

		search_params = var.split(',')[1:]

		for i in range(len(search_params)):
			if ":\\" not in search_params[i]:
				search_params[i] = "%:\\{}".format(search_params[i])

		params = 'SELECT DISTINCT last_played FROM files WHERE ' + ' OR '.join(['strFileName LIKE "{}\\%"'.format(param) for param in search_params if param])
		params += ' ORDER BY last_played DESC LIMIT {}'.format(self.lastplayed_total)

		results = self.ParseDB(self.memory_db, params)
		datesfound = [field['last_played'] for field in results if field['last_played'] != ""]

		found_fields = set()
		valid_fields = []

		for date in datesfound:
			if increment >= self.lastplayed_total and len(valid_fields) >= self.lastplayed_total:
				break
			file_query = 'SELECT * FROM files WHERE last_played LIKE "%{}%"'.format(date)
			file_results = self.ParseDB(self.memory_db, file_query)

			for field in file_results:
				if os.path.isfile(field['strFileName']) and field['strFileName'] not in found_fields:
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
				self.homewindow.setProperty(propertyvalue + '.%d.Title' % (index + 1), field['altname'] if 'altname' in field.keys() else 'Unknown Title')
				self.homewindow.setProperty(propertyvalue + '.%d.XBEPath' % (index + 1), "RunXBE(" + field['strFileName'] + ")")
				self.homewindow.setProperty(propertyvalue + '.%d.Rating' % (index + 1), field['rating'])
				self.homewindow.setProperty(propertyvalue + '.%d.ExtraInfo' % (index + 1), self.ExtraInfo(field))
				self.homewindow.setProperty(propertyvalue + '.%d.Synopsis' % (index + 1), truncate_with_ellipsis(field['synopsis'], 365))

		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(" + propertyvalue + ")")

	def RecentPlayed(self, var):
		datesfound = []
		increment = 0
		total_limit = 10
		propertyvalue = var
		exclude_patterns = ["\\Media\\", "\\Movies\\", "\\TV Shows\\"]
		
		for i in range(total_limit):
			self.programswindow.setProperty(propertyvalue + '.%d.Title' % (i + 1), '')

		params = 'SELECT DISTINCT last_played FROM files ORDER BY last_played DESC'
		results = self.ParseDB(self.memory_db, params)
		datesfound = [field['last_played'] for field in results if field['last_played'] != ""]

		found_fields = set()
		valid_fields = []

		for date in datesfound:
			file_query = 'SELECT * FROM files WHERE last_played LIKE "%{}%"'.format(date)
			file_results = self.ParseDB(self.memory_db, file_query)

			for field in file_results:
				if (os.path.isfile(field['strFileName']) 
					and field['strFileName'] not in found_fields 
					and not any(pattern in field['strFileName'] for pattern in exclude_patterns)):
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
				self.programswindow.setProperty(propertyvalue + '.%d.Title' % (index + 1), field['altname'] if 'altname' in field.keys() else 'Unknown Title')
				self.programswindow.setProperty(propertyvalue + '.%d.XBEPath' % (index + 1), "RunXBE(" + field['strFileName'] + ")")

	def Artwork(self, var):
		field = var['strFileName']
		thumbcache = xbmc.getCacheThumbName(field)
		cachedthumb = 'Special://profile/Thumbnails/Programs/{}/{}'.format(thumbcache[0], thumbcache)
		field_path = "".join(str(x) for x in field).replace('default.xbe', '_resources\\artwork')

		field_path = var['resources']

		altfanartcheck = os.path.join(field_path, "artwork\\fanart_thumb.jpg")
		fanartcheck = os.path.join(field_path, "artwork\\fanart-blur.jpg")
		largepostercheck = os.path.join(field_path, "artwork\\synopsis.jpg")
		postercheck = os.path.join(field_path, "artwork\\poster.jpg")
		posterthumbcheck = os.path.join(field_path, "artwork\\thumb.jpg")

		if noblurredfanart:
			fanartcheck = os.path.join(field_path, "artwork\\fanart.jpg")
		
		if usecachedthumbs:
			if not os.path.isfile(cachedthumb):
				xbmc.executebuiltin("CacheThumbnail({},{})".format(postercheck, cachedthumb))
			poster = cachedthumb
		else:
			def get_poster_path(field_path, postercheck, cachedthumb):
				poster = largepostercheck if not "64" in use128mbassets and "True" in force64mbassets else postercheck
				return poster if os.path.isfile(poster) else cachedthumb if not os.path.isfile(postercheck) else postercheck
			poster = get_poster_path(field_path, postercheck, cachedthumb)

		posterthumb = posterthumbcheck if os.path.isfile(posterthumbcheck) else poster
		fanart = fanartcheck if os.path.isfile(fanartcheck) else os.path.join(os.path.dirname(field), 'fanart.jpg')
		fanart = fanart if os.path.isfile(fanart) else "no_fanart.jpg"
		fanartthumb = altfanartcheck if os.path.isfile(altfanartcheck) else poster
		largeposter = largepostercheck if os.path.isfile(largepostercheck) else poster

		return poster, posterthumb, fanartthumb, fanart, largeposter

	def ExtraInfo(self, var):
		parts = [var['features_online'], var['release_date'], var['esrb_descriptors']]
		info = " · ".join(filter(None, parts))
		return info

	def database_to_memory(self, var):
		disk_conn = sqlite3.connect(var)
		disk_conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
		mem_conn = sqlite3.connect(':memory:')
		mem_conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
		disk_cursor = disk_conn.cursor()
		mem_cursor = mem_conn.cursor()
		tables = disk_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
		
		for table in tables:
			table_name = table[0]
			create_table_query = disk_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?;", (table_name,)).fetchone()[0]
			mem_cursor.execute(create_table_query)
			rows = disk_cursor.execute("SELECT * FROM {};".format(table_name)).fetchall()
			if rows:
				placeholders = ", ".join("?" * len(rows[0]))
				for row in rows:
					try:
						mem_cursor.execute("INSERT INTO {} VALUES ({});".format(table_name, placeholders), row)
					except sqlite3.OperationalError as error:
						print "Error inserting row: {}, Error: {}".format(row, error)
						continue
						
		mem_conn.commit()
		disk_conn.close()
		return mem_conn

	def ParseDB(self, memory_db, var):
		if isinstance(memory_db, str):
			conn = sqlite3.connect(memory_db)
		else:
			conn = memory_db
		conn.row_factory = sqlite3.Row
		cur = conn.cursor()
		conn.text_factory = str
		cur.execute(var)
		results = cur.fetchall()
		if self.source_focus != 0:
			conn.close()
		return results

	def ParseOverride(self, var):
		self.lastplayed_total = 10
		self.randoms_total = 10
		
		if os.path.isfile(var):
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
	if os.path.isfile(myprograms6_db):
		print "Loaded Home Screen Items.py"
		start_time = time.time()
		
		try:
			PopulateHome()
			xbmc.executebuiltin("Dialog.Close(1100)")
		finally:
			if 'con' in locals():
				con.close()
		
		print "Unloaded Home Screen Items.py - took {} seconds to complete".format(int(round(time.time() - start_time)))
	else:
		xbmc.executebuiltin("ActivateWindow(Programs)")