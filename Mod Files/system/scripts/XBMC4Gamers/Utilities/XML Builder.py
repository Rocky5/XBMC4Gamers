# -*- coding: utf-8 -*- 
'''
	Script by Rocky5
	Used to build the MyPrograms.xml and Includes.xml on boot. This saves 2MB of memory instead of using includes.
	IDs are grabbed from the xml files, so when making custom views make sure you set the ID correctly.
	<visible>Control.IsVisible(ID) + !Control.IsVisible(50) + !Window.IsVisible(134)</visible>
'''
import os
import re
import sys
import time
import xbmc

sys.path.append(xbmc.translatePath('Special://scripts/XBMC4Gamers/Utilities/libs'))
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
	arg = sys.argv[1] if len(sys.argv) > 1 else 0
	skin = xbmc.translatePath("special://skin")
	
	if xbmc.getInfoLabel('system.profilename') != "Add User":
		print "XML Builder:"
		if xbmc.getCondVisibility('Window.IsVisible(2999)') or xbmc.getCondVisibility('Window.IsVisible(1)'):
			view_path = os.path.join(skin, 'xml/views/')
			control_views = set()
			control_views.update(build_xml(view_path))
			custom_view_ids = check_custom_views(xbmc.getInfoLabel('Skin.CurrentTheme'))
			control_views.update(custom_view_ids)
			output_path = os.path.join(skin, 'xml/MyPrograms.xml')
			build_final_xml(view_path, output_path, FILE_HEADER_TEMPLATE, FILE_FOOTER, control_views)

		includes_path = os.path.join(skin, 'xml/includes/')
		build_includes_xml(includes_path, os.path.join(skin, 'xml/Includes.xml'))

	if arg:
		print "Reloading skin"
		xbmc.executebuiltin('Reloadskin')

def build_xml(input_path):
	control_views = set()
	print "    Collecting view control IDs"
	for xml_file in sorted(os.listdir(input_path)):
		if xml_file.endswith('.xml'):
			file_path = os.path.join(input_path, xml_file)
			if os.path.isfile(file_path):
				with open(file_path, "r") as view_file:
					lines = view_file.readlines()
					for line in lines:
						if '<visible>Control.IsVisible(' in line:
							match = re.search(r'Control\.IsVisible\((.*?)\)', line)
							if match:
								control_views.add(match.group(1))
							break
					print "        Found in {}".format(xml_file)
	return control_views

def build_final_xml(input_path, output_path, header, footer, control_views):
	print "    Building {}".format(os.path.basename(output_path))
	file_contents = []
	for xml_file in sorted(os.listdir(input_path)):
		if xml_file.endswith('.xml'):
			file_path = os.path.join(input_path, xml_file)
			if os.path.isfile(file_path):
				with open(file_path, "r") as view_file:
					lines = view_file.readlines()
					file_contents.extend(lines)
					file_contents.append('\n')
					print "        Adding {}".format(xml_file)

	with open(output_path, "w") as write_file:
		header_content = header.format(views=','.join(sorted(control_views, key=int))) + "\n"
		write_file.write(header_content)
		write_file.write(''.join(file_contents))
		write_file.write('\n' + footer)

	print "    {} built.".format(os.path.basename(output_path))

def build_includes_xml(includes_path, output_path):
	print "    Building {}".format(os.path.basename(output_path))
	with open(output_path, "w") as write_file:
		write_file.write('<includes>\n')
		for xml_file in sorted(os.listdir(includes_path), reverse=True):
			if xml_file.endswith('.xml'):
				file_path = os.path.join(includes_path, xml_file)
				if os.path.isfile(file_path):
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