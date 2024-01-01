# -*- coding: utf-8 -*- 
'''
	Script by Rocky5
	Used to create items for the home screen
	Concept by Dom DXecutioner (Origins)
	
	Features:
		1. Random items pulled from your DB, if none of the XBMC4Gamers stuff is found it will use cached thumbs
		2. Last played items, this will display the last 10 items you have run.
	
'''
import datetime,os,sqlite3,sys,time,xbmc,xbmcgui
print "Loaded Home Screen Items.py"
myprograms6_db	= xbmc.translatePath("special://profile/database/MyPrograms6.db")
force64mbassets	= xbmc.executehttpapi('GetGUISetting(1;mygames.games128mbartwork)')
use128mbassets	= xbmc.getInfoLabel("System.memory(total)")
noblurredfanart	= xbmc.getInfoLabel("Skin.HasSetting(UseNoBlurredFanart)")

custom1_enabled, custom1_search, custom1_search_alt	= xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton1Enabled)"), xbmc.getInfoLabel("Skin.String(CustomHomeButton1Search)"), ""
custom2_enabled, custom2_search, custom2_search_alt	= xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton2Enabled)"), xbmc.getInfoLabel("Skin.String(CustomHomeButton2Search)"), ""
custom3_enabled, custom3_search, custom3_search_alt	= xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton3Enabled)"), xbmc.getInfoLabel("Skin.String(CustomHomeButton3Search)"), ""
custom4_enabled, custom4_search, custom4_search_alt	= xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton4Enabled)"), xbmc.getInfoLabel("Skin.String(CustomHomeButton4Search)"), ""

# Check custom string for multiple path lookup
if "," in custom1_search: custom1_search_alt, custom1_search = custom1_search.split(',')[1], custom1_search.split(',')[0]
if "," in custom2_search: custom2_search_alt, custom2_search = custom2_search.split(',')[1], custom2_search.split(',')[0]
if "," in custom3_search: custom3_search_alt, custom3_search = custom3_search.split(',')[1], custom3_search.split(',')[0]
if "," in custom4_search: custom4_search_alt, custom4_search = custom4_search.split(',')[1], custom4_search.split(',')[0]

class Main:
	homewindow	= xbmcgui.Window( 10000 )
	
	def __init__( self ):
		global version
		version = int("".join(str(x) for x in self.ParseDB('SELECT idVersion FROM version'))[1])
		
		try: arg1 = int(sys.argv[1:][0])
		except: arg1 = 0

		self.Games_Random()
		self.Homebrew_Random()
		self.Emulators_Random()
		self.Applications_Random()
		
		if arg1 > 0:
			self.Games_LastPlayed()
			self.Homebrew_LastPlayed()
			self.Emulators_LastPlayed()
			self.Applications_LastPlayed()
			if custom1_enabled and not custom1_search == "":
				self.Custom1_LastPlayed()
			if custom2_enabled and not custom2_search == "":
				self.Custom2_LastPlayed()
			if custom3_enabled and not custom3_search == "":
				self.Custom3_LastPlayed()
			if custom4_enabled and not custom4_search == "":
				self.Custom4_LastPlayed()
			if arg1 == 2:
				xbmc.executebuiltin('ActivateWindow(Home)')

		if custom1_enabled and not custom1_search == "":
			self.Custom1_Random()
		if custom2_enabled and not custom2_search == "":
			self.Custom2_Random()
		if custom3_enabled and not custom3_search == "":
			self.Custom3_Random()
		if custom4_enabled and not custom4_search == "":
			self.Custom4_Random()

	def ParseDB( self,var ):
		con = sqlite3.connect(myprograms6_db)
		cur = con.cursor()
		con.text_factory = str
		cur.execute(var)
		return cur.fetchall()
		
	def Artwork( self,var ):
		field = var[1]
		thumbcache = xbmc.getCacheThumbName( field )
		cachedthumb = 'Special://profile/Thumbnails/Programs/{}/{}'.format(thumbcache[0], thumbcache)
		field = "".join(str(x) for x in field).replace('default.xbe','_resources\\artwork')
		
		if version > 3 and os.path.isdir(str(var[23])):
			field = var[23]
			
		postercheck = os.path.join(field,"artwork\\poster.jpg")
		fanartcheck = os.path.join(field,"artwork\\fanart-blur.jpg")
		if noblurredfanart: fanartcheck = os.path.join(field,"artwork\\fanart.jpg")
		
		if not "64" in use128mbassets and "True" in force64mbassets: # (if not "64") for stellar if it adds over 128MB support
			poster = os.path.join(field,"synopsis.jpg")
			if not os.path.isfile(poster):
				poster = postercheck
				if not os.path.isfile(postercheck):
					poster = ""
					if os.path.isfile(cachedthumb):
						poster = cachedthumb
		else:
			poster = postercheck
			if not os.path.isfile(poster):
				poster = ""
				if os.path.isfile(cachedthumb):
					poster = cachedthumb

		fanart = fanartcheck
		if not os.path.isfile(fanart):
			fanart = "".join(str(x) for x in var[1]).replace('default.xbe','fanart.jpg')
			if not os.path.isfile(fanart):
				fanart = "no_fanart.jpg"

		return poster,fanart
		
	def ExtraInfo( self,var ):
		info = ""
		if not var[13] == "" and not "not" in var[13].lower(): info = var[13] + " · "
		if not var[17] == "": info = info + var[17] + " · "
		if not var[15] == "": info = info + var[15]
		return info

	def Custom1_Random(self):
		increment = 0
		xbmc.executebuiltin("Skin.Reset(RandomCustom1)")
		search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom1_search+'\\%" ORDER BY RANDOM() LIMIT 10'
		if not custom1_search_alt == "":
			search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom1_search+'\\%" OR strFileName LIKE "%:\\'+custom1_search_alt+'\\%" ORDER BY RANDOM() LIMIT 10'
		for field in self.ParseDB(search_perams):
			if os.path.isfile(field[1]):
				thumb = self.Artwork(field)
				if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
					increment += 1
					self.homewindow.setProperty('RandomCustom1.%d.Fanart'												% (increment,),thumb[1])
					self.homewindow.setProperty('RandomCustom1.%d.Thumb'												% (increment,),thumb[0])
					self.homewindow.setProperty('RandomCustom1.%d.Title'												% (increment,),field[8])
					if field[8] == "": self.homewindow.setProperty('RandomCustom1.%d.Title'								% (increment,),field[3])
					self.homewindow.setProperty('RandomCustom1.%d.XBEPath' 												% (increment,),"RunXBE("+field[1]+")")
					
					if version > 3:
						self.homewindow.setProperty('RandomCustom1.%d.Rating'											% (increment,),field[18])
						self.homewindow.setProperty('RandomCustom1.%d.Synopsis'											% (increment,),field[22])
						self.homewindow.setProperty('RandomCustom1.%d.ExtraInfo'										% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(RandomCustom1)")

	def Custom1_LastPlayed(self):
		datesfound = []
		increment = 0
		xbmc.executebuiltin("Skin.Reset(LastPlayedCustom1)")
		search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom1_search+'\\%"'
		if not custom1_search_alt == "":
			search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom1_search+'\\%" OR strFileName LIKE "%:\\'+custom1_search_alt+'\\%"'
		
		for field in self.ParseDB(search_perams):
			if field[0] != "":
				datesfound.append(field[0])
		for date in sorted(datesfound, key=None, reverse=1):
			for field in self.ParseDB('SELECT * FROM files WHERE last_played LIKE "%'+str(date)+'%" LIMIT 10'):
				if os.path.isfile(field[1]):
					thumb = self.Artwork(field)
					if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
						increment += 1
						self.homewindow.setProperty('LastPlayedCustom1.%d.Fanart'										% (increment,),thumb[1])
						self.homewindow.setProperty('LastPlayedCustom1.%d.Thumb'										% (increment,),thumb[0])
						self.homewindow.setProperty('LastPlayedCustom1.%d.Title'										% (increment,),field[8])
						if field[8] == "": self.homewindow.setProperty('LastPlayedCustom1.%d.Title'						% (increment,),field[3])
						self.homewindow.setProperty('LastPlayedCustom1.%d.XBEPath' 										% (increment,),"RunXBE("+field[1]+")")
						
						if version > 3:
							self.homewindow.setProperty('LastPlayedCustom1.%d.Rating'									% (increment,),field[18])
							self.homewindow.setProperty('LastPlayedCustom1.%d.Synopsis'									% (increment,),field[22])
							self.homewindow.setProperty('LastPlayedCustom1.%d.ExtraInfo'								% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(LastPlayedCustom1)")


	def Custom2_Random(self):
		increment = 0
		xbmc.executebuiltin("Skin.Reset(RandomCustom2)")
		search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom2_search+'\\%" ORDER BY RANDOM() LIMIT 10'
		if not custom2_search_alt == "":
			search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom2_search+'\\%" OR strFileName LIKE "%:\\'+custom2_search_alt+'\\%" ORDER BY RANDOM() LIMIT 10'
		for field in self.ParseDB(search_perams):
			if os.path.isfile(field[1]):
				thumb = self.Artwork(field)
				if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
					increment += 1
					self.homewindow.setProperty('RandomCustom2.%d.Fanart'												% (increment,),thumb[1])
					self.homewindow.setProperty('RandomCustom2.%d.Thumb'												% (increment,),thumb[0])
					self.homewindow.setProperty('RandomCustom2.%d.Title'												% (increment,),field[8])
					if field[8] == "": self.homewindow.setProperty('RandomCustom2.%d.Title'								% (increment,),field[3])
					self.homewindow.setProperty('RandomCustom2.%d.XBEPath' 												% (increment,),"RunXBE("+field[1]+")")
					
					if version > 3:
						self.homewindow.setProperty('RandomCustom2.%d.Rating'											% (increment,),field[18])
						self.homewindow.setProperty('RandomCustom2.%d.Synopsis'											% (increment,),field[22])
						self.homewindow.setProperty('RandomCustom2.%d.ExtraInfo'										% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(RandomCustom2)")

	def Custom2_LastPlayed(self):
		datesfound = []
		increment = 0
		xbmc.executebuiltin("Skin.Reset(LastPlayedCustom2)")
		search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom2_search+'\\%"'
		if not custom2_search_alt == "":
			search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom2_search+'\\%" OR strFileName LIKE "%:\\'+custom2_search_alt+'\\%"'
		for field in self.ParseDB(search_perams):
			if field[0] != "":
				datesfound.append(field[0])
		for date in sorted(datesfound, key=None, reverse=1):
			for field in self.ParseDB('SELECT * FROM files WHERE last_played LIKE "%'+str(date)+'%" LIMIT 10'):
				if os.path.isfile(field[1]):
					thumb = self.Artwork(field)
					if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
						increment += 1
						self.homewindow.setProperty('LastPlayedCustom2.%d.Fanart'										% (increment,),thumb[1])
						self.homewindow.setProperty('LastPlayedCustom2.%d.Thumb'										% (increment,),thumb[0])
						self.homewindow.setProperty('LastPlayedCustom2.%d.Title'										% (increment,),field[8])
						if field[8] == "": self.homewindow.setProperty('LastPlayedCustom2.%d.Title'						% (increment,),field[3])
						self.homewindow.setProperty('LastPlayedCustom2.%d.XBEPath' 										% (increment,),"RunXBE("+field[1]+")")
						
						if version > 3:
							self.homewindow.setProperty('LastPlayedCustom2.%d.Rating'									% (increment,),field[18])
							self.homewindow.setProperty('LastPlayedCustom2.%d.Synopsis'									% (increment,),field[22])
							self.homewindow.setProperty('LastPlayedCustom2.%d.ExtraInfo'								% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(LastPlayedCustom2)")
			

	def Custom3_Random(self):
		increment = 0
		xbmc.executebuiltin("Skin.Reset(RandomCustom3)")
		search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom3_search+'\\%" ORDER BY RANDOM() LIMIT 10'
		if not custom3_search_alt == "":
			search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom3_search+'\\%" OR strFileName LIKE "%:\\'+custom3_search_alt+'\\%" ORDER BY RANDOM() LIMIT 10'
		for field in self.ParseDB(search_perams):
			if os.path.isfile(field[1]):
				thumb = self.Artwork(field)
				if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
					increment += 1
					self.homewindow.setProperty('RandomCustom3.%d.Fanart'												% (increment,),thumb[1])
					self.homewindow.setProperty('RandomCustom3.%d.Thumb'												% (increment,),thumb[0])
					self.homewindow.setProperty('RandomCustom3.%d.Title'												% (increment,),field[8])
					if field[8] == "": self.homewindow.setProperty('RandomCustom3.%d.Title'								% (increment,),field[3])
					self.homewindow.setProperty('RandomCustom3.%d.XBEPath' 												% (increment,),"RunXBE("+field[1]+")")
					
					if version > 3:
						self.homewindow.setProperty('RandomCustom3.%d.Rating'											% (increment,),field[18])
						self.homewindow.setProperty('RandomCustom3.%d.Synopsis'											% (increment,),field[22])
						self.homewindow.setProperty('RandomCustom3.%d.ExtraInfo'										% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(RandomCustom3)")

	def Custom3_LastPlayed(self):
		datesfound = []
		increment = 0
		xbmc.executebuiltin("Skin.Reset(LastPlayedCustom3)")
		search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom3_search+'\\%"'
		if not custom3_search_alt == "":
			search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom3_search+'\\%" OR strFileName LIKE "%:\\'+custom3_search_alt+'\\%"'
		for field in self.ParseDB(search_perams):
			if field[0] != "":
				datesfound.append(field[0])
		for date in sorted(datesfound, key=None, reverse=1):
			for field in self.ParseDB('SELECT * FROM files WHERE last_played LIKE "%'+str(date)+'%" LIMIT 10'):
				if os.path.isfile(field[1]):
					thumb = self.Artwork(field)
					if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
						increment += 1
						self.homewindow.setProperty('LastPlayedCustom3.%d.Fanart'										% (increment,),thumb[1])
						self.homewindow.setProperty('LastPlayedCustom3.%d.Thumb'										% (increment,),thumb[0])
						self.homewindow.setProperty('LastPlayedCustom3.%d.Title'										% (increment,),field[8])
						if field[8] == "": self.homewindow.setProperty('LastPlayedCustom3.%d.Title'						% (increment,),field[3])
						self.homewindow.setProperty('LastPlayedCustom3.%d.XBEPath' 										% (increment,),"RunXBE("+field[1]+")")
						
						if version > 3:
							self.homewindow.setProperty('LastPlayedCustom3.%d.Rating'									% (increment,),field[18])
							self.homewindow.setProperty('LastPlayedCustom3.%d.Synopsis'									% (increment,),field[22])
							self.homewindow.setProperty('LastPlayedCustom3.%d.ExtraInfo'								% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(LastPlayedCustom3)")
			

	def Custom4_Random(self):
		increment = 0
		xbmc.executebuiltin("Skin.Reset(RandomCustom4)")
		search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom4_search+'\\%" ORDER BY RANDOM() LIMIT 10'
		if not custom4_search_alt == "":
			search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom4_search+'\\%" OR strFileName LIKE "%:\\'+custom4_search_alt+'\\%" ORDER BY RANDOM() LIMIT 10'
		for field in self.ParseDB(search_perams):
			if os.path.isfile(field[1]):
				thumb = self.Artwork(field)
				if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
					increment += 1
					self.homewindow.setProperty('RandomCustom4.%d.Fanart'												% (increment,),thumb[1])
					self.homewindow.setProperty('RandomCustom4.%d.Thumb'												% (increment,),thumb[0])
					self.homewindow.setProperty('RandomCustom4.%d.Title'												% (increment,),field[8])
					if field[8] == "": self.homewindow.setProperty('RandomCustom4.%d.Title'								% (increment,),field[3])
					self.homewindow.setProperty('RandomCustom4.%d.XBEPath' 												% (increment,),"RunXBE("+field[1]+")")
					
					if version > 3:
						self.homewindow.setProperty('RandomCustom4.%d.Rating'											% (increment,),field[18])
						self.homewindow.setProperty('RandomCustom4.%d.Synopsis'											% (increment,),field[22])
						self.homewindow.setProperty('RandomCustom4.%d.ExtraInfo'										% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(RandomCustom4)")

	def Custom4_LastPlayed(self):
		datesfound = []
		increment = 0
		xbmc.executebuiltin("Skin.Reset(LastPlayedCustom4)")
		search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom4_search+'\\%"'
		if not custom4_search_alt == "":
			search_perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+custom4_search+'\\%" OR strFileName LIKE "%:\\'+custom4_search_alt+'\\%"'
		for field in self.ParseDB(search_perams):
			if field[0] != "":
				datesfound.append(field[0])
		for date in sorted(datesfound, key=None, reverse=1):
			for field in self.ParseDB('SELECT * FROM files WHERE last_played LIKE "%'+str(date)+'%" LIMIT 10'):
				if os.path.isfile(field[1]):
					thumb = self.Artwork(field)
					if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
						increment += 1
						self.homewindow.setProperty('LastPlayedCustom4.%d.Fanart'										% (increment,),thumb[1])
						self.homewindow.setProperty('LastPlayedCustom4.%d.Thumb'										% (increment,),thumb[0])
						self.homewindow.setProperty('LastPlayedCustom4.%d.Title'										% (increment,),field[8])
						if field[8] == "": self.homewindow.setProperty('LastPlayedCustom4.%d.Title'						% (increment,),field[3])
						self.homewindow.setProperty('LastPlayedCustom4.%d.XBEPath' 										% (increment,),"RunXBE("+field[1]+")")
						
						if version > 3:
							self.homewindow.setProperty('LastPlayedCustom4.%d.Rating'									% (increment,),field[18])
							self.homewindow.setProperty('LastPlayedCustom4.%d.Synopsis'									% (increment,),field[22])
							self.homewindow.setProperty('LastPlayedCustom4.%d.ExtraInfo'								% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(LastPlayedCustom4)")

	def Applications_Random(self):
		increment = 0
		xbmc.executebuiltin("Skin.Reset(RandomApps)")
		for field in self.ParseDB('SELECT * FROM files WHERE strFileName LIKE "%:\Applications\%" OR strFileName LIKE "%:\Apps\%" ORDER BY RANDOM() LIMIT 10'):
			if os.path.isfile(field[1]):
				thumb = self.Artwork(field)
				if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
					increment += 1
					self.homewindow.setProperty('RandomApps.%d.Fanart'													% (increment,),thumb[1])
					self.homewindow.setProperty('RandomApps.%d.Thumb'													% (increment,),thumb[0])
					self.homewindow.setProperty('RandomApps.%d.Title'													% (increment,),field[8])
					if field[8] == "": self.homewindow.setProperty('RandomApps.%d.Title'								% (increment,),field[3])
					self.homewindow.setProperty('RandomApps.%d.XBEPath' 												% (increment,),"RunXBE("+field[1]+")")
					
					if version > 3:
						self.homewindow.setProperty('RandomApps.%d.Rating'												% (increment,),field[18])
						self.homewindow.setProperty('RandomApps.%d.Synopsis'											% (increment,),field[22])
						self.homewindow.setProperty('RandomApps.%d.ExtraInfo'											% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(RandomApps)")

	def Applications_LastPlayed(self):
		datesfound = []
		increment = 0
		xbmc.executebuiltin("Skin.Reset(LastPlayedApps)")
		for field in self.ParseDB('SELECT last_played FROM files WHERE strFileName LIKE "%:\Applications\%" OR strFileName LIKE "%:\Apps\%"'):
			if field[0] != "":
				datesfound.append(field[0])
		for date in sorted(datesfound, key=None, reverse=1):
			for field in self.ParseDB('SELECT * FROM files WHERE last_played LIKE "%'+str(date)+'%" LIMIT 10'):
				if os.path.isfile(field[1]):
					thumb = self.Artwork(field)
					if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
						increment += 1
						self.homewindow.setProperty('LastPlayedApps.%d.Fanart'											% (increment,),thumb[1])
						self.homewindow.setProperty('LastPlayedApps.%d.Thumb'											% (increment,),thumb[0])
						self.homewindow.setProperty('LastPlayedApps.%d.Title'											% (increment,),field[8])
						if field[8] == "": self.homewindow.setProperty('LastPlayedApps.%d.Title'						% (increment,),field[3])
						self.homewindow.setProperty('LastPlayedApps.%d.XBEPath' 										% (increment,),"RunXBE("+field[1]+")")
						
						if version > 3:
							self.homewindow.setProperty('LastPlayedApps.%d.Rating'										% (increment,),field[18])
							self.homewindow.setProperty('LastPlayedApps.%d.Synopsis'									% (increment,),field[22])
							self.homewindow.setProperty('LastPlayedApps.%d.ExtraInfo'									% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(LastPlayedApps)")

	def Emulators_Random(self):
		increment = 0
		xbmc.executebuiltin("Skin.Reset(RandomEmus)")
		for field in self.ParseDB('SELECT * FROM files WHERE strFileName LIKE "%:\Emulators\%" OR strFileName LIKE "%:\Emus\%" ORDER BY RANDOM() LIMIT 10'):
			if os.path.isfile(field[1]):
				thumb = self.Artwork(field)
				if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
					increment += 1
					self.homewindow.setProperty('RandomEmus.%d.Fanart'													% (increment,),thumb[1])
					self.homewindow.setProperty('RandomEmus.%d.Thumb'													% (increment,),thumb[0])
					self.homewindow.setProperty('RandomEmus.%d.Title'													% (increment,),field[8])
					if field[8] == "": self.homewindow.setProperty('RandomEmus.%d.Title'								% (increment,),field[3])
					self.homewindow.setProperty('RandomEmus.%d.XBEPath' 												% (increment,),"RunXBE("+field[1]+")")
					
					if version > 3:
						self.homewindow.setProperty('RandomEmus.%d.Rating'												% (increment,),field[18])
						self.homewindow.setProperty('RandomEmus.%d.Synopsis'											% (increment,),field[22])
						self.homewindow.setProperty('RandomEmus.%d.ExtraInfo'											% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(RandomEmus)")

	def Emulators_LastPlayed(self):
		datesfound = []
		increment = 0
		xbmc.executebuiltin("Skin.Reset(LastPlayedEmus)")
		for field in self.ParseDB('SELECT last_played FROM files WHERE strFileName LIKE "%:\Emulators\%" OR strFileName LIKE "%:\Emus\%"'):
			if field[0] != "":
				datesfound.append(field[0])
		for date in sorted(datesfound, key=None, reverse=1):
			for field in self.ParseDB('SELECT * FROM files WHERE last_played LIKE "%'+str(date)+'%" LIMIT 10'):
				if os.path.isfile(field[1]):
					thumb = self.Artwork(field)
					if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
						increment += 1
						self.homewindow.setProperty('LastPlayedEmus.%d.Fanart'											% (increment,),thumb[1])
						self.homewindow.setProperty('LastPlayedEmus.%d.Thumb'											% (increment,),thumb[0])
						self.homewindow.setProperty('LastPlayedEmus.%d.Title'											% (increment,),field[8])
						if field[8] == "": self.homewindow.setProperty('LastPlayedEmus.%d.Title'						% (increment,),field[3])
						self.homewindow.setProperty('LastPlayedEmus.%d.XBEPath' 										% (increment,),"RunXBE("+field[1]+")")
						
						if version > 3:
							self.homewindow.setProperty('LastPlayedEmus.%d.Rating'										% (increment,),field[18])
							self.homewindow.setProperty('LastPlayedEmus.%d.Synopsis'									% (increment,),field[22])
							self.homewindow.setProperty('LastPlayedEmus.%d.ExtraInfo'									% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(LastPlayedEmus)")

	def Games_Random(self):
		increment = 0
		xbmc.executebuiltin("Skin.Reset(RandomGames)")
		for field in self.ParseDB('SELECT * FROM files WHERE strFileName LIKE "%:\Games\%" ORDER BY RANDOM() LIMIT 10'):
			if os.path.isfile(field[1]):
				thumb = self.Artwork(field)
				if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
					increment += 1
					self.homewindow.setProperty('RandomGames.%d.Fanart'													% (increment,),thumb[1])
					self.homewindow.setProperty('RandomGames.%d.Thumb'													% (increment,),thumb[0])
					self.homewindow.setProperty('RandomGames.%d.Title'													% (increment,),field[8])
					if field[8] == "": self.homewindow.setProperty('RandomGames.%d.Title'								% (increment,),field[3])
					self.homewindow.setProperty('RandomGames.%d.XBEPath' 												% (increment,),"RunXBE("+field[1]+")")
					
					if version > 3:
						self.homewindow.setProperty('RandomGames.%d.Rating'												% (increment,),field[18])
						self.homewindow.setProperty('RandomGames.%d.Synopsis'											% (increment,),field[22])
						self.homewindow.setProperty('RandomGames.%d.ExtraInfo'											% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(RandomGames)")
	
	def Games_LastPlayed(self):
		datesfound = []
		increment = 0
		xbmc.executebuiltin("Skin.Reset(LastPlayedGames)")
		for field in self.ParseDB('SELECT last_played FROM files WHERE strFileName LIKE "%:\Games\%"'):
			if field[0] != "":
				datesfound.append(field[0])
		for date in sorted(datesfound, key=None, reverse=1):
			for field in self.ParseDB('SELECT * FROM files WHERE last_played LIKE "%'+str(date)+'%" LIMIT 10'):
				if os.path.isfile(field[1]):
					thumb = self.Artwork(field)
					if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
						increment += 1
						self.homewindow.setProperty('LastPlayedGames.%d.Fanart'											% (increment,),thumb[1])
						self.homewindow.setProperty('LastPlayedGames.%d.Thumb'											% (increment,),thumb[0])
						self.homewindow.setProperty('LastPlayedGames.%d.Title'											% (increment,),field[8])
						if field[8] == "": self.homewindow.setProperty('LastPlayedGames.%d.Title'						% (increment,),field[3])
						self.homewindow.setProperty('LastPlayedGames.%d.XBEPath' 										% (increment,),"RunXBE("+field[1]+")")
						
						if version > 3:
							self.homewindow.setProperty('LastPlayedGames.%d.Rating'										% (increment,),field[18])
							self.homewindow.setProperty('LastPlayedGames.%d.Synopsis'									% (increment,),field[22])
							self.homewindow.setProperty('LastPlayedGames.%d.ExtraInfo'									% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(LastPlayedGames)")

	def Homebrew_Random(self):
		increment = 0
		xbmc.executebuiltin("Skin.Reset(RandomBrews)")
		for field in self.ParseDB('SELECT * FROM files WHERE strFileName LIKE "%:\Homebrew\%" OR strFileName LIKE "%:\Ports\%" ORDER BY RANDOM() LIMIT 10'):
			if os.path.isfile(field[1]):
				thumb = self.Artwork(field)
				if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
					increment += 1
					self.homewindow.setProperty('RandomBrews.%d.Fanart'													% (increment,),thumb[1])
					self.homewindow.setProperty('RandomBrews.%d.Thumb'													% (increment,),thumb[0])
					self.homewindow.setProperty('RandomBrews.%d.Title'													% (increment,),field[8])
					if field[8] == "": self.homewindow.setProperty('RandomBrews.%d.Title'								% (increment,),field[3])
					self.homewindow.setProperty('RandomBrews.%d.XBEPath' 												% (increment,),"RunXBE("+field[1]+")")
					
					if version > 3:
						self.homewindow.setProperty('RandomBrews.%d.Rating'												% (increment,),field[18])
						self.homewindow.setProperty('RandomBrews.%d.Synopsis'											% (increment,),field[22])
						self.homewindow.setProperty('RandomBrews.%d.ExtraInfo'											% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(RandomBrews)")
	
	def Homebrew_LastPlayed(self):
		datesfound = []
		increment = 0
		xbmc.executebuiltin("Skin.Reset(LastPlayedBrews)")
		for field in self.ParseDB('SELECT last_played FROM files WHERE strFileName LIKE "%:\Homebrew\%" OR strFileName LIKE "%:\Ports\%"'):
			if field[0] != "":
				datesfound.append(field[0])
		for date in sorted(datesfound, key=None, reverse=1):
			for field in self.ParseDB('SELECT * FROM files WHERE last_played LIKE "%'+str(date)+'%" LIMIT 10'):
				if os.path.isfile(field[1]):
					thumb = self.Artwork(field)
					if ".jpg" in thumb[0] or ".tbn" in thumb[0]:
						increment += 1
						self.homewindow.setProperty('LastPlayedBrews.%d.Fanart'											% (increment,),thumb[1])
						self.homewindow.setProperty('LastPlayedBrews.%d.Thumb'											% (increment,),thumb[0])
						self.homewindow.setProperty('LastPlayedBrews.%d.Title'											% (increment,),field[8])
						if field[8] == "": self.homewindow.setProperty('LastPlayedBrews.%d.Title'						% (increment,),field[3])
						self.homewindow.setProperty('LastPlayedBrews.%d.XBEPath' 										% (increment,),"RunXBE("+field[1]+")")
						
						if version > 3:
							self.homewindow.setProperty('LastPlayedBrews.%d.Rating'										% (increment,),field[18])
							self.homewindow.setProperty('LastPlayedBrews.%d.Synopsis'									% (increment,),field[22])
							self.homewindow.setProperty('LastPlayedBrews.%d.ExtraInfo'									% (increment,),self.ExtraInfo(field) )
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool(LastPlayedBrews)")

if ( __name__ == "__main__" ):
	if os.path.isfile(myprograms6_db):
		start_time = time.time()
		Main()

print "Unloaded Home Screen Items.py - took %s seconds to complete" % int(round((time.time() - start_time)))