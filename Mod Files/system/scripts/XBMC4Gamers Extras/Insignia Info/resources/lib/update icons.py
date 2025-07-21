# -*- coding: utf-8 -*-
from os.path import exists, getmtime, join
from os import getcwd, makedirs
from xbmc import executehttpapi, executebuiltin, log, LOGERROR
import xbmcgui
from BeautifulSoup import BeautifulSoup

# Enable the cancel button
xbmc.executebuiltin("Skin.SetString(DisableCancel,)")
executebuiltin('Dialog.Close(1100, false)')

URL = "https://insignia.live/games"
ROOT_FOLDER = getcwd().replace('\\resources\\lib', '')
DIR = join(ROOT_FOLDER, "resources\\images")

pDialog = xbmcgui.DialogProgress()
pDialog.update(0)

def progress(index, total_rows, label, game_name):
	progress_value = int((index + 1) / float(total_rows) * 100)
	pDialog.update(progress_value, "", "{}[CR]{}".format(label, game_name))

try:
	file_path = 'Z:\\temp\\full_games_webpage.txt'

	if not exists(file_path):
		pDialog.create("Update Insignia Images", "", "Downloading data")
		executehttpapi('FileDownloadFromInternet({}, {})'.format(URL, file_path))
		
		with open(file_path, 'r') as html:
			html_content = html.read()

		pDialog.update(0, "", "Processing data")
		table_start = html_content.find('<table')
		table_end = html_content.find('</table>') + len('</table>')
		html_content = html_content[table_start:table_end]

		with open(file_path, 'w') as html:
			html.write(html_content)
	else:
		pDialog.create("Update Insignia Images", "", "Reading cached data")
		with open(file_path, 'r') as html:
			html_content = html.read()
except Exception as error:
	log("Error fetching data: %s" % error, LOGERROR)
	pDialog.update(0, "", "Error...")
	xbmcgui.Dialog().ok("Error", "", "Couldn't download HTML data")
	html_content = ""

if html_content:
	table = BeautifulSoup(html_content).find("table")
	if table:
		rows = table.findAll("tr")
		if not exists(DIR):
			makedirs(DIR)

		total_rows = len(rows)

		for index, row in enumerate(rows):
			cells = row.findAll("td")
			if len(cells) > 1:
				
				title_id_tag = cells[1].find("small", {"class": "text-muted"})
				titleid = title_id_tag.string.strip() if title_id_tag and title_id_tag.string else "Unknown"

				img_tag = row.find("img")
				if img_tag and titleid != "Unknown":
					img_url = img_tag["src"]

					game_name = img_tag.get("alt", "Unknown").strip().encode('utf-8')

					file_path = join(DIR, "{}.png".format(titleid))

					if exists(file_path):
						label = 'Skipping:'
						progress(index, total_rows, label, game_name)
					else:
						label = 'Downloading:'
						progress(index, total_rows, label, game_name)
						try:
							executehttpapi('FileDownloadFromInternet({},{})'.format(img_url, file_path))
						except:
							continue

			if pDialog.iscanceled():
				break

xbmc.sleep(500)
executebuiltin('ActivateWindow(1100)')
pDialog.update(0)
pDialog.close()

executebuiltin('RunScript({}\\default.py)'.format(ROOT_FOLDER))