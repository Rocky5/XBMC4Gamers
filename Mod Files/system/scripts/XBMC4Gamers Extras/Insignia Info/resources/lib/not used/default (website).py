# -*- coding: utf-8 -*-
'''
	Script by Rocky5 to parse insignias website.
	It doesn't work 100% for session data as I need to enter games pages to extract that info
'''
import sqlite3
import xbmcgui
import xml.etree.ElementTree as ET
from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser
from os import remove
from os.path import exists, isfile, getmtime, join
import time
from xbmc import executehttpapi, executebuiltin, log, LOGERROR, translatePath
from zipfile import ZipFile

WEB_URL = "https://insignia.live/#games"
MYPROGRAMS6_DB = translatePath('special://profile/database/MyPrograms6.db')
WINDOW = xbmcgui.Window(10002)
SET_PROPERTY = WINDOW.setProperty
REFRESH_TIMEOUT = 60

def database_to_memory(var):
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
					log("Error inserting row: {}, Error: {}".format(row, error), LOGERROR)
					continue
					
	mem_conn.commit()
	disk_conn.close()
	return mem_conn

def fetch_data():
	file_path = 'Z:\\temp\\sessions_webpage.txt'
	try:
		if not exists(file_path) or time.time() - getmtime(file_path) > REFRESH_TIMEOUT:
			executehttpapi('FileDownloadFromInternet({}, {})'.format(WEB_URL, file_path))
		with open(file_path, 'r') as html:
			web_html = html.read()
		return web_html
	except Exception as error:
		log("Error fetching webpage: %s" % error, LOGERROR)
		return None

def ParseDB(conn, query, params=None):
	try:
		conn.text_factory = str
		cur = conn.cursor()
		cur.execute(query, params)
		return cur.fetchall()
	except sqlite3.Error as error:
		log("Error executing query: %s" % error, LOGERROR)
		return None

def parse_html(html_content):
	games_list = []
	try:
		soup = BeautifulSoup(html_content)
		games_section = soup.find("section", {"id": "games"})
		if not games_section:
			log("Games section not found in the HTML.", LOGERROR)
			return games_list

		table = games_section.find("table")
		if not table:
			log("Games table not found in the HTML section.", LOGERROR)
			return games_list

		rows = table.findAll("tr")
		for row in rows:
			game = {}
			try:
				# Game title
				game_name_tag = row.findAll("a")
				if game_name_tag and len(game_name_tag) > 1:
					game["title"] = HTMLParser().unescape(game_name_tag[1].text.strip())
				else:
					game["title"] = "Unknown"

				# Serial/TitleID
				serial_tag = row.findAll("td")
				if len(serial_tag) > 1:
					serial_text = serial_tag[1].contents[0].strip() if len(serial_tag[1].contents) > 0 else "Unknown"
					game["serial"] = serial_text
					title_id_tag = serial_tag[1].find("small", {"class": "text-muted"})
					game["titleid"] = title_id_tag.string.strip() if title_id_tag and title_id_tag.string else "Unknown"
				else:
					game["serial"] = "Unknown"
					game["titleid"] = "Unknown"

				# Players
				player_count_tag = serial_tag[2] if len(serial_tag) > 2 else None
				if player_count_tag and player_count_tag.text:
					game["current_players"] = player_count_tag.text.strip()
				else:
					game["current_players"] = "-"

				# Sessions
				session_count_tag = serial_tag[3] if len(serial_tag) > 3 else None
				if session_count_tag and session_count_tag.text:
					session_text = " ".join(session_count_tag.text.split())
					game["sessions"] = session_text
				else:
					game["sessions"] = "-"

				games_list.append(game)
			except Exception as game_error:
				log("Error processing row: %s" % game_error, LOGERROR)
				continue

	except Exception as error:
		log("Error parsing HTML content: %s" % error, LOGERROR)

	return games_list

def main(games_list, SCRIPT_ROOT_DIR):
	images_path = join(SCRIPT_ROOT_DIR, 'resources', 'images')

	conn = sqlite3.connect(MYPROGRAMS6_DB)
	conn.row_factory = sqlite3.Row

	for index, game in enumerate(games_list):
		try:
			game['titleid'] = link.text.split('/')[-1]
			query = 'SELECT strFileName FROM files WHERE titleId = ?'
			result = ParseDB(conn, query, (int(game['titleid'], 16),))
			game['XBEPath'] = result[0]['strFileName'] if result else None
		except (ValueError, sqlite3.Error) as error:
			log('Error processing game data: %s' % error, LOGERROR)
			game['XBEPath'] = None

		game['image_path'] = join(images_path, game['titleid'] + '.png')
		game['installed'] = isfile(game['XBEPath']) if game['XBEPath'] else False
		games_list.append(game)

	conn.close()
	
	for index, game in enumerate(games_list):
		SET_PROPERTY('%d.Title' % (index + 1), game['title'])
		SET_PROPERTY('%d.TitleID' % (index + 1), game['titleid'])
		SET_PROPERTY('%d.PlayerCount' % (index + 1), game['current_players'])
		SET_PROPERTY('%d.Sessions' % (index + 1), game['sessions'].replace(' sessions', '').replace(' session', ''))
		SET_PROPERTY('%d.Image' % (index + 1), game['image_path'])
		SET_PROPERTY('%d.Installed' % (index + 1), 'Yes' if game['installed'] else 'No')
		if game['installed']:
			SET_PROPERTY('%d.XBEPath' % (index + 1), 'RunXBE(' + game['XBEPath'] + ')')

def run(SCRIPT_ROOT_DIR):
	try:
		zip_src = join(SCRIPT_ROOT_DIR, 'resources', 'images.zip')
		zip_dst = join(SCRIPT_ROOT_DIR, 'resources')
		if exists(zip_src):
			with ZipFile(zip_src, 'r') as zf:
				zf.extractall(zip_dst)
			remove(zip_src)

		html_content = fetch_data()
		if rss_data:
			WINDOW.clearProperties()
			games_list = parse_html(html_content) if html_content else []
			main(games_list, SCRIPT_ROOT_DIR)

	except Exception as error:
		log("Error during script execution: %s" % error, LOGERROR)