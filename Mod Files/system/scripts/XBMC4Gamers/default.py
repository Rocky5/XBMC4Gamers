# -*- coding: utf-8 -*-
from filecmp import cmp as compare_file
from os.path import isfile
from os import remove
from shutil import copyfile
import xml.etree.ElementTree as ET
import re
import time
from xbmcgui import Dialog, getCurrentWindowId, Window
from xbmc import executebuiltin, getCondVisibility, getInfoLabel, getLocalizedString, getSkinDir, setSkin, translatePath
from fileinput import input as fileinput

sys.path.append('Q:/system/scripts/XBMC4Gamers/Utilities/libs')
from custom_views import custom_views_update_programs as check_custom_views

CURRENT_THEME = getInfoLabel('Skin.CurrentTheme')
FONT_PATH = translatePath('Special://skin/xml/Font.xml')
AUTOEXEC_FILE = translatePath('special://scripts/autoexec.py')
SOURCES_XML_PATH = "P:/Sources.xml"
XML_FILE_PATH = "Special://skin/xml/Custom_Dialog_Quick_Change.xml"
MASTER_PROFILE_NAME = "Add User"
MASTER_PROFILE_SKIN = "Add User"
SETPROPERTY = Window(getCurrentWindowId()).setProperty
GETPROPERTY = Window(getCurrentWindowId()).getProperty

def clean_autoexec_script():
	try:
		remove(AUTOEXEC_FILE)
		return True
	except:
		return False

def check_kioskmode():
	if isfile(translatePath("special://xbmc/system/keymaps/Enabled")):
		executebuiltin('Skin.SetBool(kioskmode)')
		executebuiltin('Skin.Reset(AdultProfile)')
	else:
		executebuiltin('Skin.Reset(kioskmode)')

def check_skin(username):
	if getSkinDir() == MASTER_PROFILE_SKIN:
		setSkin("Profile")
		print 'Error with profile {}: Settings might have been corrupted, or setting up new profile.'.format(username)
		return False
	else:
		return True

def generate_content(names):
	source_items = [{"label": "[UPPERCASE]{}[/UPPERCASE]".format(name), "onclick": ["Dialog.Close(1115)", "ActivateWindow(1,{})".format(name)], "icon": "-"} for name in names]
	custom_items = [
		{"label": "[UPPERCASE]$INFO[Skin.String(CustomQuickChange1)][/UPPERCASE]", "onclick": ["Dialog.Close(1115)", "ActivateWindow(1,$INFO[Skin.String(CustomQuickChange1)])"], "icon": "-", "visible": "Skin.HasSetting(CustomQuickChange1Enabled) + String.IsEmpty($INFO[Skin.String(CustomQuickChange1)])"},
		{"label": "[UPPERCASE]$INFO[Skin.String(CustomQuickChange2)][/UPPERCASE]", "onclick": ["Dialog.Close(1115)", "ActivateWindow(1,$INFO[Skin.String(CustomQuickChange2)])"], "icon": "-", "visible": "Skin.HasSetting(CustomQuickChange2Enabled) + String.IsEmpty($INFO[Skin.String(CustomQuickChange2)])"},
		{"label": "[UPPERCASE]$INFO[Skin.String(CustomQuickChange3)][/UPPERCASE]", "onclick": ["Dialog.Close(1115)", "ActivateWindow(1,$INFO[Skin.String(CustomQuickChange3)])"], "icon": "-", "visible": "Skin.HasSetting(CustomQuickChange3Enabled) + String.IsEmpty($INFO[Skin.String(CustomQuickChange3)])"},
		{"label": "[UPPERCASE]$INFO[Skin.String(CustomQuickChange4)][/UPPERCASE]", "onclick": ["Dialog.Close(1115)", "ActivateWindow(1,$INFO[Skin.String(CustomQuickChange4)])"], "icon": "-", "visible": "Skin.HasSetting(CustomQuickChange4Enabled) + String.IsEmpty($INFO[Skin.String(CustomQuickChange4)])"},
		{"label": "[UPPERCASE]$INFO[Skin.String(CustomQuickChange5)][/UPPERCASE]", "onclick": ["Dialog.Close(1115)", "ActivateWindow(1,$INFO[Skin.String(CustomQuickChange5)])"], "icon": "-", "visible": "Skin.HasSetting(CustomQuickChange5Enabled) + String.IsEmpty($INFO[Skin.String(CustomQuickChange5)])"},
		{"label": "[UPPERCASE]$INFO[Skin.String(CustomQuickChange6)][/UPPERCASE]", "onclick": ["Dialog.Close(1115)", "ActivateWindow(1,$INFO[Skin.String(CustomQuickChange6)])"], "icon": "-", "visible": "Skin.HasSetting(CustomQuickChange6Enabled) + String.IsEmpty($INFO[Skin.String(CustomQuickChange6)])"},
	]
	all_items = source_items + custom_items
	content_element = ET.Element("content")
	for i, item in enumerate(all_items):
		item_element = ET.SubElement(content_element, "item", id=str(i))
		label_element = ET.SubElement(item_element, "label")
		label_element.text = item["label"]
		for action in item["onclick"]:
			onclick_element = ET.SubElement(item_element, "onclick")
			onclick_element.text = action
		icon_element = ET.SubElement(item_element, "icon")
		icon_element.text = item["icon"]
		if "visible" in item:
			visible_element = ET.SubElement(item_element, "visible")
			visible_element.text = item["visible"]
	return content_element

def update_quick_change_xml(xml_path, sources_xml):
	try:
		tree = ET.parse(sources_xml)
		names = sorted([source.find("name").text for source in tree.getroot().findall(".//programs/source") if source.find("name") is not None], key=str.lower)
		tree = ET.parse(xml_path)
		root = tree.getroot()
		content_element = root.find(".//content")
		if content_element is not None:
			content_element.clear()
			content_element.extend(generate_content(names))
		tree.write(xml_path, encoding="utf-8", xml_declaration=False)
	except Exception as error:
		print("Error updating XML file: {}".format(error))

def check_skin_settings():
	memory_check = getCondVisibility('StringCompare(System.memory(total),64MB)')

	# Set global skin settings
	executebuiltin("Skin.SetBool(xbmc4gamers)")
	executebuiltin("Skin.SetString(dashboard_name,XBMC4Gamers)")
	executebuiltin("Skin.SetBool(urldownloader_new)")
	executebuiltin("Skin.SetString(urldownloader,Special://urldownloader/)")
	executebuiltin("Skin.Reset(ArtworkInstallerHeader)")
	executebuiltin("Skin.SetString(DisableCancel,)")

	# Wallpaper size settings based on ram amount
	if memory_check:
		if getCondVisibility('StringCompare(Skin.String(WallpaperWidth),)') or getCondVisibility('StringCompare(Skin.String(WallpaperHeight),)'):
			executebuiltin("Skin.SetString(WallpaperWidth,720)")
			executebuiltin("Skin.SetString(WallpaperHeight,405)")
	else:
		if getCondVisibility('StringCompare(Skin.String(WallpaperWidth),)') or getCondVisibility('StringCompare(Skin.String(WallpaperHeight),)'):
			executebuiltin("Skin.SetString(WallpaperWidth,953)")
			executebuiltin("Skin.SetString(WallpaperHeight,536)")

	# Other skin settings
	if getCondVisibility('StringCompare(Skin.String(WallpaperQuality),)'):
		executebuiltin("ReloadAdvancedSettings")
		executebuiltin("Skin.SetString(WallpaperQuality,100)")

	if getCondVisibility('StringCompare(Skin.String(FolderFanartPath),)'):
		executebuiltin("Skin.SetString(FolderFanartPath,Special://skin/extras/folder fanart/default)")

	if getCondVisibility('StringCompare(Skin.String(HomeWindow),)'):
		executebuiltin("Skin.SetString(HomeWindow,Root)")

	if getCondVisibility('StringCompare(Skin.String(HomeWindow_name),)'):
		executebuiltin("Skin.SetString(HomeWindow_name,{}".format(getLocalizedString(20108)))

	if getCondVisibility('StringCompare(Skin.String(HomeWindowSource),)'):
		executebuiltin("Skin.SetString(HomeWindowSource,Programs)")

	if getCondVisibility('StringCompare(Skin.String(Background_Image),)') or not isfile(getInfoLabel('Skin.String(Background_Image)')):
		executebuiltin('Skin.Reset(custom_wallpaper_set)')
		executebuiltin('SetWallpaper(Background_Image, {}, {}, {}, Q:\\skins\\Profile\\backgrounds\\{}\\0.jpg)'.format(
			getInfoLabel('Skin.String(WallpaperWidth)'),
			getInfoLabel('Skin.String(WallpaperHeight)'),
			getInfoLabel('Skin.String(WallpaperQuality)'),
			CURRENT_THEME
		))

def check_theme_fonts():
	backup_xml = translatePath('Special://root/skins/{}/xml/Font.xml'.format(MASTER_PROFILE_SKIN))
	theme_xml = translatePath('Special://skin/extras/themes/xmls/{}_fonts.xml'.format(CURRENT_THEME))
	theme_fonts_installed = translatePath('Special://skin/xml/Fonts_Custom_Installed.xml')
	font_needs_update = False
	dont_skip_font_update = True

	if getCondVisibility('System.HasLoginScreen'):
		if isfile(theme_xml):
			if not compare_file(theme_xml, FONT_PATH, shallow=False):
				copyfile(theme_xml, FONT_PATH)
				with open(theme_fonts_installed, "w") as installed:
					installed.write("")
				font_needs_update = True
		else:
			if isfile(theme_fonts_installed):
				copyfile(backup_xml, FONT_PATH)
				remove(theme_fonts_installed)
				font_needs_update = True
			
			for i, line in enumerate(fileinput(FONT_PATH, inplace=True)):
				line = line.lower()
				if i < 8 and '<filename>' in line and '{}.ttf'.format(CURRENT_THEME).lower() in line:
					dont_skip_font_update = False

				if dont_skip_font_update and '<filename>' in line and '<filename>monofont-' not in line and '<filename>home.ttf' not in line:
					line = '            <filename>{}.ttf</filename>\n'.format(CURRENT_THEME)
					font_needs_update = True
				print line,

	return font_needs_update

def manage_profiles_setup():
	current_profile_setup = translatePath('special://profile/setup.bin')
	if isfile(current_profile_setup):
		remove(current_profile_setup)
		executebuiltin("ReplaceWindow(11)")
		Dialog().ok(
			"Welcome to XBMC4Gamers", 
			"[CR]Please calibrate the screen to fit your TV.[CR]Move the top left and bottom right chevrons to the corners of your TV[CR](no red visible) and adjust the disc to be as circular as possible."
		)
		wait_for_condition(lambda: getCurrentWindowId() != 10011, 120)

def wait_for_condition(condition_func, timeout=5):
	start_time = time.time()
	while not condition_func() and (time.time() - start_time) < timeout:
		time.sleep(0.1)
	if not condition_func():
		print "Timeout reached before the condition was met."

def main(username):
	# Perform kiosk mode check
	check_kioskmode()
	
	# Remove autoexec.py as it's only ever used once for updates and downloader updates
	if isfile(AUTOEXEC_FILE):
		wait_for_condition(clean_autoexec_script)

	# Manage setup for master profile
	if username == MASTER_PROFILE_NAME:
		manage_profiles_setup()
		executebuiltin('Skin.Reset(UpdateDB)')
		return False

	# Update the Custom_Dialog_Quick_Change.xml with your added sources.
	update_quick_change_xml(XML_FILE_PATH, SOURCES_XML_PATH)

	# Perform settings check
	check_skin_settings()

	# Check and handle custom views for non-master profiles and fonts
	font_needs_update = check_theme_fonts()
	custom_views_needs_update = check_custom_views(getInfoLabel('Skin.CurrentTheme'))

	if font_needs_update or custom_views_needs_update:
		print "Reload skin required."
		return True

	return False

def unload():
	print "Unloaded XBMC4Gamers\\default.py - took {} seconds to complete".format(
		int(round(time.time() - start_time))
	)

if __name__ == "__main__":
	print "Loaded XBMC4Gamers\\default.py"
	start_time = time.time()

	username = getInfoLabel('system.profilename')
	run_main = True
	reload_skin = False

	# Check skin condition for non-master profiles
	if username != MASTER_PROFILE_NAME:
		run_main = check_skin(username)

	if run_main:
		reload_skin = main(username)
		unload()
		if getCondVisibility('Skin.HasSetting(UpdateDB)') and not getCondVisibility('Skin.HasSetting(AdultProfile)'):
			# Loops until the programs file is built, then processes the database
			SETPROPERTY("MyScript.ExternalRunning", "True")
			executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/XML Builder.py,2)')
			wait_for_condition(lambda: GETPROPERTY("MyScript.ExternalRunning") != "True", 10)
			executebuiltin('RunScript(Special://scripts/XBMC4Gamers/Utilities/Database Maintenance.py)')
		else:
			executebuiltin("ActivateWindow(1114)")

			if reload_skin:
				executebuiltin("ReloadSkin")
				print "Reloaded skin to apply changes."
	else:
		unload()
		executebuiltin("ReloadSkin")
		print 'Reset skin and reloaded.'