import os
import xbmc

# Check for custom views and if exist check if we need to rebuild the includes file and reload the skin (startup only)
def custom_views_update_programs(ThemeFile):
	try:
		programs_xml_path = xbmc.translatePath('Special://skin/xml/MyPrograms.xml')
		custom_views_path = xbmc.translatePath('Special://skin/xml/Includes_Custom_Views.xml')
		reloadskin = 0
		existing_content = ""
		existing_view_ids = set()
		if os.path.isfile(custom_views_path):
			with open(custom_views_path, 'r') as custom_xml:
				existing_content = custom_xml.read()
		with open(programs_xml_path, 'r') as file:
			lines = file.readlines()
		views_line_index = None
		for i, line in enumerate(lines):
			if '<views>' in line:
				views_line_index = i
				existing_view_ids = set(line.replace('<views>', '').replace('</views>', '').strip().split(','))
				break
		new_view_ids = set()
		new_content = '<includes>\n\t<include name="Custom Views">\n'
		default_folder = xbmc.translatePath('Special://skin/xml/custom views/_global')
		theme_folder = os.path.join(xbmc.translatePath('Special://skin/xml/custom views'), ThemeFile)
		for ID in range(80, 90):
			xbmc.executebuiltin('Skin.Reset(CustomViewtype_id_{})'.format(ID))
			xbmc.executebuiltin('Skin.Reset(CustomViewtype_id_{}_JPG)'.format(ID))
			default_xml_file = os.path.join(default_folder, "CustomViewtype_id_{}.xml".format(ID))
			default_jpg_file = os.path.join(default_folder, "CustomViewtype_id_{}.jpg".format(ID))
			theme_xml_file = os.path.join(theme_folder, "CustomViewtype_id_{}.xml".format(ID))
			theme_jpg_file = os.path.join(theme_folder, "CustomViewtype_id_{}.jpg".format(ID))
			if os.path.isfile(default_xml_file) and os.path.isfile(default_jpg_file) and not os.path.isfile(theme_xml_file) and not os.path.isfile(theme_jpg_file):
				xbmc.executebuiltin('Skin.SetBool(CustomViewtype_id_{})'.format(ID))
				xbmc.executebuiltin('Skin.SetString(CustomViewtype_id_{}_JPG, {}\\CustomViewtype_id_{}.jpg)'.format(ID, default_folder, ID))
				new_content += '\t\t<include file="custom views\\_global\\CustomViewtype_id_{}.xml" condition="Skin.HasSetting(CustomViewtype_id_{})">custom_id_{}</include>\n'.format(ID, ID, ID)
				new_view_ids.add(str(ID))
			elif os.path.isfile(theme_xml_file) and os.path.isfile(theme_jpg_file):
				xbmc.executebuiltin('Skin.SetBool(CustomViewtype_id_{})'.format(ID))
				xbmc.executebuiltin('Skin.SetString(CustomViewtype_id_{}_JPG, {}\\CustomViewtype_id_{}.jpg)'.format(ID, theme_folder, ID))
				new_content += '\t\t<include file="custom views\\{}\\CustomViewtype_id_{}.xml" condition="Skin.HasSetting(CustomViewtype_id_{})">custom_id_{}</include>\n'.format(ThemeFile, ID, ID, ID)
				new_view_ids.add(str(ID))
			else:
				if str(ID) in existing_view_ids:
					existing_view_ids.remove(str(ID))
		new_content += '\t</include>\n</includes>'
		
		if new_content != existing_content:
			with open(custom_views_path, 'w') as custom_xml:
				custom_xml.write(new_content)
			reloadskin = 1
			print "Custom View Builder:"
			print "    Building {}".format(os.path.basename(custom_views_path))
			print "        Added custom view IDs: {}.".format(','.join(sorted(new_view_ids, key=int)))
			print "    {} built.".format(os.path.basename(custom_views_path))
			if views_line_index is not None:
				updated_view_ids = existing_view_ids.union(new_view_ids)
				lines[views_line_index] = '\t<views>{}</views>\n'.format(','.join(sorted(updated_view_ids, key=int)))
				with open(programs_xml_path, 'w') as file:
					file.writelines(lines)
				print "    Updated MyPrograms.xml with new view ids: {}".format(','.join(sorted(new_view_ids, key=int)))
	except Exception as error:
		print 'Error in "Check for custom views": {}'.format(error)
	return reloadskin

# Check for custom views and add them to the myprograms.xml when rebuild xml files. This assumes they are already added to the includes file.
def xml_builder_check_custom_views(ThemeFile):
	custom_view_ids = set()
	try:
		custom_views_path = xbmc.translatePath('Special://skin/xml/Includes_Custom_Views.xml')
		with open(custom_views_path, 'w') as custom_xml:
			custom_xml.write('<includes>\n\t<include name="Custom Views">\n')
			default_folder = xbmc.translatePath('Special://skin/xml/custom views/_global')
			theme_folder = os.path.join(xbmc.translatePath('Special://skin/xml/custom views'), ThemeFile)
			print "    Building {}".format(os.path.basename(custom_views_path))
			for ID in range(80, 90):
				xbmc.executebuiltin('Skin.Reset(CustomViewtype_id_{})'.format(ID))
				xbmc.executebuiltin('Skin.Reset(CustomViewtype_id_{}_JPG)'.format(ID))
				default_xml_file = os.path.join(default_folder, "CustomViewtype_id_{}.xml".format(ID))
				default_jpg_file = os.path.join(default_folder, "CustomViewtype_id_{}.jpg".format(ID))
				theme_xml_file = os.path.join(theme_folder, "CustomViewtype_id_{}.xml".format(ID))
				theme_jpg_file = os.path.join(theme_folder, "CustomViewtype_id_{}.jpg".format(ID))
				
				if os.path.isfile(default_xml_file) and os.path.isfile(default_jpg_file) and not os.path.isfile(theme_xml_file) and not os.path.isfile(theme_jpg_file):
					xbmc.executebuiltin('Skin.SetBool(CustomViewtype_id_{})'.format(ID))
					xbmc.executebuiltin('Skin.SetString(CustomViewtype_id_{}_JPG, {}\\CustomViewtype_id_{}.jpg)'.format(ID, default_folder, ID))
					print "        Added custom view ID: {} (from global custom views)".format(ID)
					custom_xml.write('\t\t<include file="custom views\\_global\\CustomViewtype_id_{}.xml" condition="Skin.HasSetting(CustomViewtype_id_{})">custom_id_{}</include>\n'.format(ID, ID, ID))
					custom_view_ids.add(str(ID))
				elif os.path.isfile(theme_xml_file) and os.path.isfile(theme_jpg_file):
					xbmc.executebuiltin('Skin.SetBool(CustomViewtype_id_{})'.format(ID))
					xbmc.executebuiltin('Skin.SetString(CustomViewtype_id_{}_JPG, {}\\CustomViewtype_id_{}.jpg)'.format(ID, theme_folder, ID))
					print "        Added custom view ID: {} (from {} theme)".format(ID, ThemeFile)
					custom_xml.write('\t<include file="custom views\\{}\\CustomViewtype_id_{}.xml" condition="Skin.HasSetting(CustomViewtype_id_{})">custom_id_{}</include>\n'.format(ThemeFile, ID, ID, ID))
					custom_view_ids.add(str(ID))
			custom_xml.write('\t</include>\n</includes>')
			print "    {} built.".format(os.path.basename(custom_views_path))
	except Exception as error:
		print 'Error in "Check for custom views": {}'.format(error)
	return custom_view_ids