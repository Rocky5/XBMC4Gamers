# -*- coding: utf-8 -*- 
'''
	Script by Rocky5
	Used to build the MyPrograms.xml and Includes.xml on boot. This saves 2MB of memory instead of using includes.
	IDs are grabbed from the xml files, so when making custom views make sure you set the ID correctly.
	<visible>Control.IsVisible(ID) + !Control.IsVisible(50) + !Window.IsVisible(134)</visible>
'''
from os.path import basename, join, isfile
from os import listdir
from re import search
from sys import argv
import time
from xbmcgui import getCurrentWindowId, Window
from xbmc import executebuiltin, getCondVisibility, getInfoLabel, translatePath

sys.path.append(translatePath('Special://scripts/XBMC4Gamers/Utilities/libs'))
from custom_views import xml_builder_check_custom_views as check_custom_views

FILE_HEADER_TEMPLATE = '''<window id="1">
	<defaultcontrol always="true">50</defaultcontrol>
	<allowoverlay>no</allowoverlay>
	<onload condition="Skin.HasSetting(run_random_script)">RunScript(Special://scripts/XBMC4Gamers/Utilities/Random Select.py)</onload>
	<views>{views}</views>
	<controls>
		<include condition="!Skin.HasSetting(kioskmode)">Kiosk.Mode.Secret.Code</include>
		<include>Synopsis.Loader</include>
		<include>Global.Backgrounds</include>
		<control type="group">
			<visible>!Window.IsActive(1101)</visible>
			<animation effect="fade" start="100" end="0" time="100" delay="400">hidden</animation>
			<animation effect="fade" start="0" end="100" delay="0" time="100">visible</animation>'''

FILE_FOOTER = '''            <!-- Custom views -->
			<include>Custom Views</include>
		</control>
		<include>Window.Footer</include>
		<include condition="Skin.HasSetting(kioskmode)">View_Options</include>
	</controls>
</window>'''

def main():
	arg = int(argv[1]) if len(argv) > 1 else 0
	skin = translatePath("special://skin")

	if getInfoLabel('system.profilename') != "Add User":
		print "XML Builder:"
		if arg == 2 or getCondVisibility('Window.IsVisible(2999)') or getCondVisibility('Window.IsVisible(1)'):
			view_path = join(skin, 'xml/views/')
			control_views = set()
			control_views.update(build_xml(view_path))
			custom_view_ids = check_custom_views(getInfoLabel('Skin.CurrentTheme'))
			control_views.update(custom_view_ids)
			filtered_views = filter_xml_files(view_path, control_views, custom_view_ids)
			output_path = join(skin, 'xml/MyPrograms.xml')
			build_final_xml(view_path, output_path, FILE_HEADER_TEMPLATE, FILE_FOOTER, filtered_views)

		if arg != 2:
			includes_path = join(skin, 'xml/includes/')
			build_includes_xml(includes_path, join(skin, 'xml/Includes.xml'))

	if arg == 1:
		print "Reloading skin"
		executebuiltin('Reloadskin')

def filter_xml_files(input_path, enabled_ids, custom_view_ids):
	filtered_views = set(custom_view_ids)
	# print "    Filtering XML files"
	for xml_file in sorted(listdir(input_path)):
		if xml_file.endswith('.xml'):
			for view_id in enabled_ids:
				if view_id in xml_file:
					filtered_views.add(view_id)
					# print "        Keeping View ID: {}".format(view_id)
					break

	return filtered_views

def build_xml(input_path):
	control_views = set()
	# print "    Collecting view control IDs"
	for xml_file in sorted(listdir(input_path)):
		if xml_file.endswith('.xml'):
			file_path = join(input_path, xml_file)
			if isfile(file_path):
				with open(file_path, "r") as view_file:
					lines = view_file.readlines()
					for line in lines:
						if '<visible>Control.IsVisible(' in line:
							match = search(r'Control\.IsVisible\((.*?)\)', line)
							if match:
								view_id = match.group(1)
								if getCondVisibility('Skin.HasSetting(View{}_Disabled)'.format(view_id)) == 0:
									control_views.add(view_id)
							break
					# print "        Found in {}".format(xml_file)
	
	return control_views

def build_final_xml(input_path, output_path, header, footer, control_views):
	print "    Building {}".format(basename(output_path))
	file_contents = []
	for xml_file in sorted(listdir(input_path)):
		if xml_file.endswith('.xml'):
			if any(view_id in xml_file for view_id in control_views):
				file_path = join(input_path, xml_file)
				if isfile(file_path):
					with open(file_path, "r") as view_file:
						lines = view_file.readlines()
						file_contents.extend(lines)
						file_contents.append('\n')
						print "        Adding {}".format(xml_file)

	with open(output_path, "w") as write_file:
		sorted_views = sorted(control_views, key=lambda x: int(''.join(filter(str.isdigit, x))))
		header_content = header.format(views=','.join(sorted_views)) + "\n"
		write_file.write(header_content)
		write_file.write(''.join(file_contents))
		write_file.write('\n' + footer)

	print "    {} built.".format(basename(output_path))

def build_includes_xml(includes_path, output_path):
	print "    Building {}".format(basename(output_path))
	with open(output_path, "w") as write_file:
		write_file.write('<includes>\n')
		for xml_file in sorted(listdir(includes_path), reverse=True):
			if xml_file.endswith('.xml'):
				file_path = join(includes_path, xml_file)
				if isfile(file_path):
					print "        Adding {}".format(xml_file)
					with open(file_path, "r") as include_file:
						write_file.write(include_file.read() + "\n")
		write_file.write('\n</includes>')
	print "    Includes.xml built."

if __name__ == "__main__":
	print "Loaded XML Builder.py"
	start_time = time.time()
	main()
	print "Unloaded XML Builder.py - took {} seconds to complete".format(int(round(time.time() - start_time)))
	
	# For when there is an update
	if getCondVisibility('Skin.HasSetting(UpdateDB)') and not getCondVisibility('Skin.HasSetting(AdultProfile)'):
		Window(getCurrentWindowId()).setProperty("MyScript.ExternalRunning", "False")