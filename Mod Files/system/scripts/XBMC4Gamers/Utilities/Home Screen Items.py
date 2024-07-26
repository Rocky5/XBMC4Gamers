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
myprograms6_db	= xbmc.translatePath("special://profile/database/MyPrograms6.db")
force64mbassets	= xbmc.executehttpapi('GetGUISetting(1;mygames.games128mbartwork)')
use128mbassets	= xbmc.getInfoLabel("System.memory(total)")
noblurredfanart	= xbmc.getInfoLabel("Skin.HasSetting(UseNoBlurredFanart)")

class PopulateHome:
	homewindow	= xbmcgui.Window( 10000 )
	
	def __init__( self ):
		global version
		version = int("".join(str(x) for x in self.ParseDB('SELECT idVersion FROM version'))[1])
		try: arg = int(sys.argv[1:][0])
		except: arg = 0
		# These are the default search permas to search the DB. They are folder names, so Games will search Games, Games 1, Games 2, Games that are cool etc....
		Search_Games	= "Games"
		Search_Brews	= "Homebrew,Ports"
		Search_Emus		= "Emulators,Emus"
		Search_Apps		= "Applications,Apps"
		custom1_enabled, custom1_search	= xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton1Enabled)"), xbmc.getInfoLabel("Skin.String(CustomHomeButton1Search)")
		custom2_enabled, custom2_search	= xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton2Enabled)"), xbmc.getInfoLabel("Skin.String(CustomHomeButton2Search)")
		custom3_enabled, custom3_search	= xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton3Enabled)"), xbmc.getInfoLabel("Skin.String(CustomHomeButton3Search)")
		custom4_enabled, custom4_search	= xbmc.getInfoLabel("Skin.HasSetting(CustomHomeButton4Enabled)"), xbmc.getInfoLabel("Skin.String(CustomHomeButton4Search)")
		try:
			# First part is the skin property value, don't change this unless you want to edit the home.xml
			self.Random("RandomGames,"+Search_Games)
			self.Random("RandomBrews,"+Search_Brews)
			self.Random("RandomEmus,"+Search_Emus)
			self.Random("RandomApps,"+Search_Apps)
			if arg > 0:
				self.LastPlayed("LastPlayedGames,"+Search_Games)
				self.LastPlayed("LastPlayedBrews,"+Search_Brews)
				self.LastPlayed("LastPlayedEmus,"+Search_Emus)
				self.LastPlayed("LastPlayedApps,"+Search_Apps)
				if custom1_enabled and not custom1_search == "": self.LastPlayed("LastPlayedCustom1,"+custom1_search)
				if custom2_enabled and not custom2_search == "": self.LastPlayed("LastPlayedCustom2,"+custom2_search)
				if custom3_enabled and not custom3_search == "": self.LastPlayed("LastPlayedCustom3,"+custom3_search)
				if custom4_enabled and not custom4_search == "": self.LastPlayed("LastPlayedCustom4,"+custom4_search)
				if arg == 2:
					xbmc.executebuiltin('ActivateWindow(Home)')
			if custom1_enabled and not custom1_search == "": self.Random("RandomCustom1,"+custom1_search)
			if custom2_enabled and not custom2_search == "": self.Random("RandomCustom2,"+custom2_search)
			if custom3_enabled and not custom3_search == "": self.Random("RandomCustom3,"+custom3_search)
			if custom4_enabled and not custom4_search == "": self.Random("RandomCustom4,"+custom4_search)
		except:
			xbmc.executebuiltin('ActivateWindow(Home)')

	def Random(self,var):
		increment = 0
		propertyvalue = var.split(',')[0]
		xbmc.executebuiltin("Skin.Reset("+propertyvalue+")")
		
		search_peram_alt = ""
		if var.count(',') > 1: search_peram_alt, search_peram = var.split(',')[2], var.split(',')[1]
		else: search_peram = var.split(',')[1]
		
		perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+search_peram+'\\%" ORDER BY RANDOM() LIMIT 10'
		if not search_peram_alt == "": perams = 'SELECT * FROM files WHERE strFileName LIKE "%:\\'+search_peram+'\\%" OR strFileName LIKE "%:\\'+search_peram_alt+'\\%" ORDER BY RANDOM() LIMIT 10'
		
		for field in self.ParseDB(perams):
			
			if os.path.isfile(field[1]):
				thumb = self.Artwork(field)
				
				if not thumb[0] == "":
					increment += 1
					self.homewindow.setProperty(propertyvalue+'.%d.Fanart' % (increment,),thumb[1])
					self.homewindow.setProperty(propertyvalue+'.%d.Thumb' % (increment,),thumb[0])
					self.homewindow.setProperty(propertyvalue+'.%d.Title' % (increment,),truncate_with_ellipsis(field[8], 40))
					if field[8] == "":
						self.homewindow.setProperty(propertyvalue+'.%d.Title' % (increment,),field[3])
					self.homewindow.setProperty(propertyvalue+'.%d.XBEPath' % (increment,),"RunXBE("+field[1]+")")
					
					if version > 3:
						# self.homewindow.setProperty(propertyvalue+'.%d.Rating' % (increment,),field[18])
						self.homewindow.setProperty(propertyvalue+'.%d.Synopsis' % (increment,),truncate_with_ellipsis(field[22], 265))
						# self.homewindow.setProperty(propertyvalue+'.%d.ExtraInfo' % (increment,),self.ExtraInfo(field) )
		
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool("+propertyvalue+")")
	
	def LastPlayed(self,var):
		datesfound = []
		increment = 0
		propertyvalue = var.split(',')[0]
		xbmc.executebuiltin("Skin.Reset("+propertyvalue+")")
		
		search_peram_alt = ""
		if var.count(',') > 1: search_peram_alt, search_peram = var.split(',')[2], var.split(',')[1]
		else: search_peram = var.split(',')[1]
		
		perams = 'SELECT last_played FROM files WHERE strFileName LIKE "%:\\'+search_peram+'\\%"'
		if not search_peram_alt == "": perams = 'SELECT last_played FROM files WHERE strFileName LIKE "%:\\'+search_peram+'\\%" OR strFileName LIKE "%:\\'+search_peram_alt+'\\%"'
		
		for field in self.ParseDB(perams):
			if field[0] != "": datesfound.append(field[0])
		
		for date in sorted(datesfound, key=None, reverse=1):
			
			for field in self.ParseDB('SELECT * FROM files WHERE last_played LIKE "%'+str(date)+'%" LIMIT 10'):
				
				if os.path.isfile(field[1]):
					thumbcache = xbmc.getCacheThumbName(field[1])
					thumb = self.Artwork(field)
					
					if not thumb[0] == "":
						increment += 1
						self.homewindow.setProperty(propertyvalue+'.%d.Fanart' % (increment,),thumb[1])
						self.homewindow.setProperty(propertyvalue+'.%d.Thumb' % (increment,),thumb[0])
						self.homewindow.setProperty(propertyvalue+'.%d.Title' % (increment,),field[8])
						if field[8] == "":
							self.homewindow.setProperty(propertyvalue+'.%d.Title' % (increment,),field[3])
						self.homewindow.setProperty(propertyvalue+'.%d.XBEPath' % (increment,),"RunXBE("+field[1]+")")
						
						if version > 3:
							# self.homewindow.setProperty(propertyvalue+'.%d.Rating' % (increment,),field[18])
							self.homewindow.setProperty(propertyvalue+'.%d.Synopsis' % (increment,),truncate_with_ellipsis(field[22], 365))
							# self.homewindow.setProperty(propertyvalue+'.%d.ExtraInfo' % (increment,),self.ExtraInfo(field) )
		
		if increment > 0:
			xbmc.executebuiltin("Skin.SetBool("+propertyvalue+")")

	def Artwork( self,var ):
		field = var[1]
		thumbcache = xbmc.getCacheThumbName(field)
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

	def ParseDB( self,var ):
		con = sqlite3.connect(myprograms6_db)
		cur = con.cursor()
		con.text_factory = str
		cur.execute(var)
		return cur.fetchall()

def truncate_with_ellipsis(text, max_length):
	text = ' '.join(text.split()).strip()
	# lines = text.splitlines()
	# cleaned_lines = [line.strip() for line in lines if line.strip()]
	# text = '\n'.join(cleaned_lines)
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
		print("Loaded Home Screen Items.py")
		start_time = time.time()
		try:
			if xbmcgui.getCurrentWindowId() == 10000:
				xbmc.executebuiltin("ActivateWindow(1100)")
			PopulateHome()
			xbmc.executebuiltin("Dialog.Close(1100)")
		finally:
			if 'con' in locals():
				con.close()
		print("Unloaded Home Screen Items.py - took {} seconds to complete".format(int(round(time.time() - start_time))))
