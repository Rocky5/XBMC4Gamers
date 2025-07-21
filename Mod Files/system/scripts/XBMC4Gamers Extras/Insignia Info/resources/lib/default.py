# -*- coding: utf-8 -*-
'''
	Script by Rocky5 to parse OGXbox.org insignias rss feed.
'''
import datetime
import re
import sqlite3
import time
import xbmcgui
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
from os import remove
from os.path import exists, getmtime ,isfile, join
from sys import argv
from xbmc import executehttpapi, executebuiltin, log, LOGERROR, translatePath
from zipfile import ZipFile

RSS_URL = 'https://ogxbox.org/rss/insignia?matchmakingonly&noevents'
EVENTS_URL = 'https://ogxbox.org/rss/insignia?events'
MYPROGRAMS6_DB = translatePath('special://profile/database/MyPrograms6.db')
WINDOW = xbmcgui.Window(10002)
SET_PROPERTY = WINDOW.setProperty
SCRIPT_ROOT_DIR = __path__
REFRESH_TIMEOUT = 60

def clean_description(input):
	description = re.sub(r'(?<=\n)<br />\n', '', input)
	description = re.sub(r'<br />$', '', description, flags=re.MULTILINE)
	return description

def extract_date(title):
	match = re.search(r"(\w{3}, \w{3} \d{1,2})", title)
	if match:
		try:
			return datetime.datetime.strptime(match.group(0), "%a, %b %d").date().replace(year=datetime.date.today().year)
		except ValueError:
			pass
	return None

def fetch_data(URL, Type):
	file_path = 'Z:\\temp\\{}.txt'.format(Type)
	rss_feed = '<item><title>Error</title></item>'
	try:
		if not exists(file_path) or (time.time() - getmtime(file_path) > REFRESH_TIMEOUT and Type != "events"):
			executehttpapi('FileDownloadFromInternet({}, {})'.format(URL, file_path))
		with open(file_path, 'r') as html:
			rss_feed = html.read()
		return rss_feed
	except Exception as error:
		log("Error fetching RSS feed: %s" % error, LOGERROR)
		return '<item><title>Error</title></item>'

def ParseDB(conn, query, params=None):
	try:
		conn.text_factory = str
		cur = conn.cursor()
		cur.execute(query, params)
		return cur.fetchall()
	except sqlite3.Error as error:
		log("Error executing query: %s" % error, LOGERROR)
		return None

def process_title_info(title_text):
	game_info = {}
	title_text = HTMLParser().unescape(title_text)
	players_pos = max(title_text.find('player'), title_text.find('players'))
	if players_pos != -1:
		colon_pos = title_text.rfind(':', 0, players_pos)
		if colon_pos != -1:
			game_info['title'] = title_text[:colon_pos].strip()
			details = title_text[colon_pos + 1:].strip()
			players_sessions = details.split('(')
			game_info['current_players'] = players_sessions[0].strip().split()[0] if players_sessions else '0'
			game_info['sessions'] = players_sessions[1].strip(')') if len(players_sessions) > 1 else '0'
		else:
			game_info['title'] = title_text.strip()
			game_info['current_players'] = '0'
			game_info['sessions'] = '0'
	else:
		game_info['title'] = title_text.strip()
		game_info['current_players'] = '0'
		game_info['sessions'] = '0'
	return game_info

def parse_sessions_data(rss_data):
	games_list = []
	images_path = join(SCRIPT_ROOT_DIR, 'resources', 'images')

	conn = sqlite3.connect(MYPROGRAMS6_DB)
	conn.row_factory = sqlite3.Row

	try:
		root = ET.fromstring(rss_data.encode('utf-8'))
	except ET.ParseError as error:
		log('Error parsing XML: %s' % error, LOGERROR)
		conn.close()
		return

	for item in root.findall('.//item'):
		link = item.find('link')
		if link is not None:
			game = process_title_info(item.find('title').text)
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

	games_list.sort(key=lambda x: int(x["current_players"]), reverse=True)
	
	for index, game in enumerate(games_list):
		SET_PROPERTY('%d.Title' % (index + 1), game['title'])
		SET_PROPERTY('%d.TitleID' % (index + 1), game['titleid'])
		SET_PROPERTY('%d.PlayerCount' % (index + 1), game['current_players'])
		SET_PROPERTY('%d.Sessions' % (index + 1), game['sessions'].replace(' sessions', '').replace(' session', ''))
		SET_PROPERTY('%d.Image' % (index + 1), game['image_path'])
		SET_PROPERTY('%d.Installed' % (index + 1), 'Yes' if game['installed'] else 'No')
		if game['installed']:
			SET_PROPERTY('%d.XBEPath' % (index + 1), 'RunXBE(' + game['XBEPath'] + ')')

def convert_timestamp(text):
	pattern = r"<t:\s*(\d+)\s*:t>"
	def replace_match(match):
		timestamp = int(match.group(1))
		readable_time = datetime.datetime.utcfromtimestamp(timestamp).strftime('%H:%M %p')
		return readable_time
	return re.sub(pattern, replace_match, text)

def parse_events_data(rss_data):
	today = datetime.date.today()
	tomorrow = today + datetime.timedelta(days=1)
	events_today = []
	events_tomorrow = []
	events_other = []

	try:
		root = ET.fromstring(rss_data.encode('utf-8'))
	except ET.ParseError as error:
		log("Error parsing XML: %s" % error, LOGERROR)
		return []

	for item in root.findall('.//item'):
		title = item.find('title')
		description = item.find('description')

		if title is not None and description is not None:
			event = {
				"title": title.text.replace("event Event - ", ""),
				"description": convert_timestamp(clean_description(description.text)),
				"date": extract_date(title.text)
			}

			if "Today" in title.text:
				events_today.append(event)
			elif "Tomorrow" in title.text:
				events_tomorrow.append(event)
			else:
				events_other.append(event)

	events_today.sort(key=lambda x: x["title"].split(":")[1].strip() if ":" in x["title"] else x["title"])
	events_tomorrow.sort(key=lambda x: x["title"].split(":")[1].strip() if ":" in x["title"] else x["title"])
	events_other.sort(key=lambda x: x["date"] or datetime.date.max)
	events_list = events_today + events_tomorrow + events_other

	for index, event in enumerate(events_list):
		SET_PROPERTY('%d.Title' % (index + 1), event['title'].replace('Game Event - ', ''))
		SET_PROPERTY('%d.Description' % (index + 1), event['description'])

def main(url_type):
	try:
		zip_src = join(SCRIPT_ROOT_DIR, 'resources', 'images.zip')
		zip_dst = join(SCRIPT_ROOT_DIR, 'resources')
		if exists(zip_src):
			with ZipFile(zip_src, 'r') as zf:
				zf.extractall(zip_dst)
			remove(zip_src)

		WINDOW.clearProperties()
		
		if url_type == 'sessions':
			rss_data = fetch_data(RSS_URL, url_type)
			if rss_data:
				parse_sessions_data(rss_data)
				executebuiltin('SetFocus(9201)')
		else:
			rss_data = fetch_data(EVENTS_URL, url_type)
			if rss_data:
				parse_events_data(rss_data)
				executebuiltin('SetFocus(9202)')

	except Exception as error:
		log("Error during script execution: %s" % error, LOGERROR)

if __name__ == '__main__':
	arg = argv[1] if len(argv) > 1 else 'sessions'
	main(arg)
	