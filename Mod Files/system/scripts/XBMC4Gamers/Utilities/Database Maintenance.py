# -*- coding: utf-8 -*- 
'''
	This script addresses common issues reported on Reddit, Facebook, and other platforms regarding fanart or posters not showing correctly on newer builds of Gamers.
	This script will update and clean your database, so no more questions!
'''
import os
import re
import sys
import time
import sqlite3
import xbmcgui
import zlib
import xml.etree.ElementTree as ET

DB_VERSIONS = [7]
MYPROGRAMS_DB = xbmc.translatePath('special://profile/database/MyPrograms6.db')
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
pDialog.update(0)

encoding = 'utf-8'

def column_exists(cursor, table_name, column_name):
	cursor.execute("PRAGMA table_info({})".format(table_name))
	columns = [row[1] for row in cursor.fetchall()]
	return column_name in columns

def compress_text(text):
	return zlib.compress(text.encode('utf-8'))

def decompress_text(compressed_text):
	return zlib.decompress(compressed_text).decode('utf-8')

def clean_database(version, rows, cursor):
	pDialog.create('Database Maintenance')
	total_rows = len(rows)
	dots = ['', '', '', '', '', '', '', '', '', '',
			'.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
			'..', '..', '..', '..', '..', '..', '..', '..', '..', '..',
			'...', '...', '...', '...', '...', '...', '...', '...', '...', '...']
	dot_index = 0
	for numb, row in enumerate(rows, start=1):
		Game_Title, FilePath, idFile = row[3], row[1], row[0]
		
		dialoginfo = "Optimising your database[CR]Please wait"
		if version < min(DB_VERSIONS):
			dialoginfo = "Updating and optimising your database[CR]Please wait"

		if not os.path.isfile(FilePath):
			cursor.execute('DELETE FROM files WHERE idFile = ?', (idFile,))

		# Check if _resources/default.xml exists and parse it, if it does
		FolderPath = unicode(os.path.dirname(FilePath), encoding)
		xml_path = os.path.join(FolderPath, u'_resources/default.xml')
		update_parse_and_insert_xml(version, cursor, xml_path, idFile, FolderPath)
		
		progress = int((numb * 100) / total_rows)
		if numb % 20 == 0:
			pDialog.update(progress, '', '{}{}'.format(dialoginfo, dots[dot_index]))
		dot_index = (dot_index + 1) % len(dots)

def replace_special_characters(text):
	text = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', text)
	text = re.sub(r"<?xml version='1.0' encoding='utf-8'?>", '<?xml version="1.0" encoding="utf-8"?>', text)
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
	# Update database so users don't need to refresh their games/apps etc...
	resources_path = os.path.join(FolderPath, u'_resources\\')

	# Update info if default.xml exits and database is older
	if version < min(DB_VERSIONS) and os.path.isfile(xml_path):
		try:
			with open(xml_path, 'rb') as xml_file:
				xml_content = xml_file.read().decode('utf-8', 'ignore').strip()
			xml_content = replace_special_characters(xml_content)
			
			root = ET.fromstring(xml_content.encode('utf-8'))
		except (IOError, ET.ParseError) as error:
			print "XML path: {}".format(resources_path)
			print "Error parsing XML: {}".format(error)
			return
		
		for synopsis in [root]:
			synopsis_text = synopsis.findtext('overview', "")
			
			# Remove white space from beginning of synopsis text
			start = 0
			while start < len(synopsis_text) and synopsis_text[start].isspace():
				start += 1
			synopsis_text = synopsis_text[start:]

			# Not used as I truncate as the menu is loading, this lets me have full and truncated synopsis info.
			# truncate_synopsis(synopsis_text)

			data = {
				'altname': synopsis.findtext('title', ""),
				'developer': synopsis.findtext('developer', ""),
				'publisher': synopsis.findtext('publisher', ""),
				'features_general': synopsis.findtext('features_general', "").replace(', ',' / '),
				'features_online': synopsis.findtext('features_online', "").replace(', ',' / '),
				'esrb': synopsis.findtext('esrb', "").replace('Not Rated','N/A'),
				'esrb_descriptors': synopsis.findtext('esrb_descriptors', "").replace(', ',' / ').replace('Not Rated','N/A'),
				'genre': synopsis.findtext('genre', "").replace(', ',' / '),
				'release_date': synopsis.findtext('release_date', ""),
				'year': synopsis.findtext('year', ""),
				'rating': synopsis.findtext('rating', ""),
				'platform': synopsis.findtext('platform', "").replace(', ',' / '),
				'exclusive': synopsis.findtext('exclusive', ""),
				'title_id': synopsis.findtext('titleid', ""),
				'synopsis': synopsis_text
			}
			
			# Fix the names/synopsis etc... or they show &amp; as it's only ET that has issues with &
			for key in data:
				if isinstance(data[key], str):
					data[key] = data[key].replace('&amp;', '&').lstrip()

			fix_data = ", ".join(["{} = ?".format(key) for key in data.keys()])
			cursor.execute("UPDATE files SET {} WHERE idFile = ?".format(fix_data), tuple(data.values()) + (idFile,))

	resources_exist = os.path.isdir(resources_path)
	preview_exists = os.path.isfile(os.path.join(resources_path, u'media/preview.mp4'))
	screenshot_exists = os.path.isfile(os.path.join(resources_path, u'screenshots/screenshot-1.jpg'))
	fanart_exists = os.path.isfile(os.path.join(resources_path, u'artwork/fanart.jpg'))
	if not fanart_exists: fanart_exists = os.path.isfile(os.path.join(FolderPath, u'fanart.jpg'))

	cursor.execute('UPDATE files SET resources = ?, preview = ?, screenshot = ?, fanart = ? WHERE idFile = ?',
					(resources_path if resources_exist else "", "1" if preview_exists else "", "1" if screenshot_exists else "", "1" if fanart_exists else "", idFile))

def unloaded():
	xbmcgui.Dialog().textviewer('Changelog', open('Special://root/system/SystemInfo/changes.txt').read())
	print "Unloaded Database Maintenance.py - took {} seconds to complete".format(int(round(time.time() - start_time)))

def main():
	try:
		start_size = os.path.getsize(MYPROGRAMS_DB)
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
				print "Updated to DB version: {}".format(version)
				for column in columns_to_add:
					if not column_exists(cur, 'files', column):
						cur.execute("ALTER TABLE files ADD COLUMN {} text NOT NULL DEFAULT ''".format(column))
			
			# Update version, UPDATE this if you update the database file again.
			cur.execute('UPDATE version SET idversion = {}'.format(max(DB_VERSIONS)))
			cur.execute('PRAGMA legacy_file_format=1')
			cur.execute('SELECT * FROM files')
			rows = cur.fetchall()
			
			clean_database(version, rows, cur)
			
			con.commit()
			cur.execute('VACUUM')
			cur.execute('PRAGMA integrity_check')
			integrity_check_result = cur.fetchone()

		pDialog.close()
		if integrity_check_result and integrity_check_result[0] == 'ok':
			unloaded()
			dialog.ok('Complete', '[CR]Welcome to latest version of XBMC4Gamers.[CR]I hope you enjoy the new features and that everything has been[CR]smooth sailing with the update.')
		else:
			unloaded()
			dialog.ok('Error', '', 'Database integrity check failed.')
	except sqlite3.Error as error:
		pDialog.close()
		unloaded()
		dialog.ok('Error', '', 'An error occurred while updating the database:[CR]{}'.format(error))

if __name__ == "__main__":
	if os.path.isfile(MYPROGRAMS_DB) and xbmcgui.getCurrentWindowId() == 12999:
		print "Loaded Database Maintenance.py"
		start_time = time.time()
		# Disable the cancel button
		xbmc.executebuiltin("Skin.SetString(DisableCancel,Disabled)")
		# Run main part of the script
		main()
		# Enable the cancel button
		xbmc.executebuiltin("Skin.SetString(DisableCancel,)")
	
	xbmc.executebuiltin("ActivateWindow(1114)")