# -*- coding: utf-8 -*- 
'''
	This script addresses common issues reported on Reddit, Facebook, and other platforms regarding fanart or posters not showing correctly on newer builds of Gamers.
	This script will update and clean your database, so no more questions!
'''
from os import remove
from os.path import dirname, isdir, isfile, getsize, join
from re import sub
import time
from HTMLParser import HTMLParser
from xbmc import getCacheThumbName, getInfoLabel, translatePath
from xbmcgui import Dialog, DialogProgress, getCurrentWindowId
import sqlite3
# import zlib
import xml.etree.ElementTree as ET

DB_VERSIONS = [8]
MYPROGRAMS_DB = translatePath('special://profile/database/MyPrograms6.db')
X4GSETTINGS_WINDOW = getCurrentWindowId() == 11111
pDialog = DialogProgress()
dialog = Dialog()
pDialog.update(0)

encoding = 'utf-8'

def column_exists(cursor, table_name, column_name):
	cursor.execute("PRAGMA table_info({})".format(table_name))
	columns = [row[1] for row in cursor.fetchall()]
	return column_name in columns

# def compress_text(text):
	# return zlib.compress(text.encode(encoding))

# def decompress_text(compressed_text):
	# return zlib.decompress(compressed_text).decode(encoding)

def clean_database(version, rows, cursor):
	pDialog.create('Database Maintenance')
	deleted_count = 0
	total_rows = len(rows)

	for numb, row in enumerate(rows, start=1):
		Game_Title, FilePath, idFile = row[3], row[1], row[0]
		
		dialoginfo = "Optimising your database[CR]Please wait..."
		if version < min(DB_VERSIONS) or X4GSETTINGS_WINDOW:
			dialoginfo = "Updating and optimising your database[CR]Please wait..."

		if not isfile(FilePath):
			cursor.execute('DELETE FROM files WHERE idFile = ?', (idFile,))
			thumbcache = getCacheThumbName(FilePath)
			thumbcache = translatePath('Special://profile/Thumbnails/Programs/{}/{}'.format(thumbcache[0], thumbcache))
			if isfile(thumbcache):
				remove(thumbcache)
			deleted_count += 1

		# Check if _resources/default.xml exists and parse it, if it does
		FolderPath = unicode(dirname(FilePath), encoding)
		xml_path = join(FolderPath, '_resources\\default.xml')
		update_parse_and_insert_xml(version, cursor, xml_path, idFile, FolderPath)
		
		progress = int((numb * 100) / total_rows)
		if numb % 25 == 0:
			pDialog.update(progress, '', '{}'.format(dialoginfo))
	
	return deleted_count

def replace_special_characters(text):
	text = HTMLParser().unescape(text)
	text = sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', text)
	text = sub(r"<?xml version='1.0' encoding='utf-8'?>", '<?xml version="1.0" encoding="utf-8"?>', text)
	return text
	
def truncate_synopsis(synopsis_text):
	if len(synopsis_text) > 500:
		pos_comma = synopsis_text.find(',', 500)
		pos_space = synopsis_text.find(' ', 500)

		if pos_comma != -1:
			synopsis_text = synopsis_text[:pos_comma] + "..."
		elif pos_space != -1:
			synopsis_text = synopsis_text[:pos_space] + "..."
		else:
			synopsis_text = synopsis_text[:500] + "..."
	
	return synopsis_text

def update_parse_and_insert_xml(version, cursor, xml_path, idFile, FolderPath):
	language = getInfoLabel('System.Language').replace(' (', '_').replace(')', '').lower()
	resources_path = join(FolderPath, '_resources\\')

	if version < min(DB_VERSIONS) and isfile(xml_path) or X4GSETTINGS_WINDOW:
		try:
			with open(xml_path, 'rb') as xml_file:
				xml_content = xml_file.read().decode(encoding, 'ignore').strip()
			xml_content = replace_special_characters(xml_content)

			root = ET.fromstring(xml_content.encode(encoding))
			child_element = next((elem for elem in root if elem.tag.lower() == language), None)
		except (IOError, ET.ParseError) as error:
			print(u"XML path: {}".format(resources_path).encode(encoding))
			print(u"Error parsing XML: {}".format(error).encode(encoding))
			return

		data = {
			'altname': root.findtext('title', ""),
			'developer': root.findtext('developer', ""),
			'publisher': root.findtext('publisher', ""),
			'features_general': root.findtext('features_general', "").replace(', ', ' / '),
			'features_online': root.findtext('features_online', "").replace(', ', ' / '),
			'esrb': root.findtext('esrb', "").replace('Not Rated', 'N/A'),
			'esrb_descriptors': root.findtext('esrb_descriptors', "").replace(', ', ' / ').replace('Not Rated', 'N/A'),
			'genre': root.findtext('genre', "").replace(', ', ' / '),
			'release_date': root.findtext('release_date', ""),
			'year': root.findtext('year', ""),
			'rating': root.findtext('rating', ""),
			'platform': root.findtext('platform', "").replace(', ', ' / '),
			'exclusive': root.findtext('exclusive', ""),
			'title_id': root.findtext('titleid', ""),
			'synopsis': root.findtext('overview', "").lstrip()
		}

		if child_element is not None:
			alt_title = child_element.findtext('title')
			if alt_title and alt_title.strip():
				data['altname'] = alt_title.strip()

			alt_overview = child_element.findtext('overview')
			if alt_overview and alt_overview.strip():
				data['synopsis'] = alt_overview.strip()

			for key in data:
				if key not in ['altname', 'synopsis']:
					alt_value = child_element.findtext(key)
					if alt_value and alt_value.strip():
						data[key] = alt_value.strip()

		for key in data:
			if isinstance(data[key], str):
				data[key] = data[key].replace('&amp;', '&').lstrip()

		fix_data = ", ".join(["{} = ?".format(key) for key in data.keys()])
		cursor.execute("UPDATE files SET {} WHERE idFile = ?".format(fix_data), tuple(data.values()) + (idFile,))

	resources_exist = isdir(resources_path)
	preview_exists = isfile(join(resources_path, 'media\\preview.mp4'))
	screenshot_exists = isfile(join(resources_path, 'screenshots\\screenshot-1.jpg'))
	fanart_exists = isfile(join(resources_path, 'artwork\\fanart.jpg'))
	if not fanart_exists: fanart_exists = isfile(join(FolderPath, 'fanart.jpg'))

	cursor.execute('UPDATE files SET resources = ?, preview = ?, screenshot = ?, fanart = ? WHERE idFile = ?',
				   (resources_path if resources_exist else "", "1" if preview_exists else "", "1" if screenshot_exists else "", "1" if fanart_exists else "", idFile))

def format_size(size_in_bytes):
	for unit in ['B', 'KB', 'MB', 'GB']:
		if size_in_bytes < 1024.0:
			return '%.2f %s' % (size_in_bytes, unit)
		size_in_bytes /= 1024.0

def unloaded():
	print "Unloaded Database Maintenance.py - took {} seconds to complete".format(int(round(time.time() - start_time)))

def main():
	try:
		start_size = getsize(MYPROGRAMS_DB)
		with sqlite3.connect(MYPROGRAMS_DB) as con:
			con.text_factory = str
			cur = con.cursor()
			
			con.execute('BEGIN TRANSACTION')
			cur.execute('SELECT idversion FROM version')
			version = cur.fetchone()[0]
			columns_to_add = []
			
			# Add new columns to the database before I update anything
			columns_to_add = [
				"altname", "developer", "publisher", "features_general", "features_online", 
				"esrb", "esrb_descriptors", "genre", "release_date", "year", 
				"rating", "platform", "exclusive", "title_id", "synopsis", 
				"resources", "preview", "screenshot", "fanart", "alt_xbe", "last_played"
			]
			
			if columns_to_add:
				for column in columns_to_add:
					if not column_exists(cur, 'files', column):
						cur.execute("ALTER TABLE files ADD COLUMN {} TEXT NOT NULL DEFAULT ''".format(column))
			
			# Update version, UPDATE this if you update the database file again.
			if version < min(DB_VERSIONS):
				print "Updated to DB version: {}".format(version)
				cur.execute('UPDATE version SET idversion = {}'.format(max(DB_VERSIONS)))
			
			cur.execute('PRAGMA legacy_file_format=1')
			cur.execute('SELECT * FROM files')
			rows = cur.fetchall()
			
			deleted_count = clean_database(version, rows, cur)
			
			con.commit()
			cur.execute('VACUUM')
			cur.execute('PRAGMA integrity_check')
			integrity_check_result = cur.fetchone()

		pDialog.close()
		if integrity_check_result and integrity_check_result[0] == 'ok':
			unloaded()
			if X4GSETTINGS_WINDOW:
				end_size = getsize(MYPROGRAMS_DB)
				dialog.ok('Database Update Complete', '', 'Old size: {}[CR]New size: {}[CR]{} items removed.'.format(format_size(start_size), format_size(end_size), deleted_count))
			else:
				Dialog().textviewer('Changelog', open('Special://root/system/SystemInfo/changes.txt').read())
				dialog.ok('Complete', '[CR]Welcome to latest version of XBMC4Gamers.[CR]I hope you enjoy the new features and that everything has been[CR]smooth sailing with the update.')
		else:
			unloaded()
			dialog.ok('Error', '', 'Database integrity check failed.')
	except sqlite3.Error as error:
		pDialog.close()
		unloaded()
		dialog.ok('Error', '', 'An error occurred while updating the database:[CR]{}'.format(error))

if __name__ == "__main__":
	# Close the script loading dialog
	xbmc.executebuiltin('Dialog.Close(1100,false)')
	if isfile(MYPROGRAMS_DB) and getCurrentWindowId() == 12999 or isfile(MYPROGRAMS_DB) and X4GSETTINGS_WINDOW:
		print "Loaded Database Maintenance.py"
		start_time = time.time()
		# Disable the cancel button
		xbmc.executebuiltin("Skin.SetString(DisableCancel,Disabled)")
		# Run main part of the script
		main()
		# Enable the cancel button
		xbmc.executebuiltin("Skin.SetString(DisableCancel,)")

	if getCurrentWindowId() != 11111:
		xbmc.executebuiltin("ActivateWindow(1114)")