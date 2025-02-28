# -*- coding: utf-8 -*- 
import os
import sqlite3
import xbmcgui

MyPrograms_db = xbmc.translatePath('special://profile/database/MyPrograms6.db')
pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
pDialog.update(0)

class CancelledException(Exception):
	pass

def clean_database(rows, cursor):
	pDialog.create('Cleaning Database')
	total_rows = len(rows)
	deleted_count = 0
	dots = ['', '', '', '', '', '', '', '', '', '',
			'.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
			'..', '..', '..', '..', '..', '..', '..', '..', '..', '..',
			'...', '...', '...', '...', '...', '...', '...', '...', '...', '...']
	dot_index = 0
	
	for numb, row in enumerate(rows, start=1):
		Game_Title, FilePath, idFile = row[3], row[1], row[0]
		
		if not os.path.isfile(FilePath):
			cursor.execute('DELETE FROM files WHERE idFile = ?', (idFile,))
			deleted_count += 1
		
		progress = int((numb * 100) / total_rows)
		if numb % 20 == 0:
			pDialog.update(progress, '', 'Cleaning Database[CR]Please wait{}'.format(dots[dot_index]))
		
		dot_index = (dot_index + 1) % len(dots)
		if pDialog.iscanceled():
			raise CancelledException('You cancelled.')
	return deleted_count

def format_size(size_in_bytes):
	for unit in ['B', 'KB', 'MB', 'GB']:
		if size_in_bytes < 1024.0:
			return '%.2f %s' % (size_in_bytes, unit)
		size_in_bytes /= 1024.0

def main():
	if os.path.isfile(MyPrograms_db):
		try:
			start_size = os.path.getsize(MyPrograms_db)
			with sqlite3.connect(MyPrograms_db) as con:
				con.text_factory = str
				cur = con.cursor()
				cur.execute('BEGIN TRANSACTION')
				cur.execute('PRAGMA legacy_file_format=1')
				cur.execute('SELECT * FROM files')
				rows = cur.fetchall()
				deleted_count = clean_database(rows, cur)
				con.commit()
				cur.execute('VACUUM')
				cur.execute('PRAGMA integrity_check')
				integrity_check_result = cur.fetchone()
			
			end_size = os.path.getsize(MyPrograms_db)
			pDialog.close()
			if integrity_check_result and integrity_check_result[0] == 'ok':
				dialog.ok('Database integrity is {}'.format(integrity_check_result[0]), '', 
						  'Old database size: {}[CR]New database size: {}[CR]{} items removed from database.'.format(format_size(start_size), format_size(end_size), deleted_count))
			else:
				dialog.ok('Error', '', 'Database integrity check failed.')
		except CancelledException as cancel_error:
			pDialog.close()
			dialog.ok('Cancelled', '', str(cancel_error))
		except sqlite3.Error as error:
			pDialog.close()
			dialog.ok('Error', '', 'An error occurred while cleaning the database:[CR]{}'.format(error))
	else:
		dialog.ok('Error', '', 'MyPrograms6.db is missing.')

if __name__ == "__main__":
	main()