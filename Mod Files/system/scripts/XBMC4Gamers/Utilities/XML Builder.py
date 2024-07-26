'''
	Script by Rocky5
	Used to build the MyPrograms.xml and Includes.xml on boot. This saves 2MB of memory instead of using includes.
'''
import glob
import os
import sys
import time
import xbmc

FILE_HEADER = '''<window id="1">
	<defaultcontrol always="true">50</defaultcontrol>
	<allowoverlay>no</allowoverlay>
	<onload condition="Skin.HasSetting(run_random_script)">RunScript(Special://scripts/XBMC4Gamers/Utilities/Random Select.py)</onload>
	<views>50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,79,80,81,82,83,84,85,86,87,88,89</views>
	<controls>
		<include condition="!Skin.HasSetting(kioskmode)">Kiosk.Mode.Secret.Code</include>
		<include>Synopsis.Loader</include>
		<include>Global.Backgrounds</include>
		<include>Fanart</include>
		<control type="group">
			<visible>!Window.IsActive(1101)</visible>
			<animation effect="fade" start="100" end="0" time="100" delay="400">hidden</animation>
			<animation effect="fade" start="0" end="100" delay="0" time="100">visible</animation>'''

FILE_FOOTER = '''            <!-- Custom views -->
			<include file="custom views\CustomViewtype_id_80.xml" condition="Skin.HasSetting(CustomViewtype_id_80)">custom_id_80</include>
			<include file="custom views\CustomViewtype_id_81.xml" condition="Skin.HasSetting(CustomViewtype_id_81)">custom_id_81</include>
			<include file="custom views\CustomViewtype_id_82.xml" condition="Skin.HasSetting(CustomViewtype_id_82)">custom_id_82</include>
			<include file="custom views\CustomViewtype_id_83.xml" condition="Skin.HasSetting(CustomViewtype_id_83)">custom_id_83</include>
			<include file="custom views\CustomViewtype_id_84.xml" condition="Skin.HasSetting(CustomViewtype_id_84)">custom_id_84</include>
			<include file="custom views\CustomViewtype_id_85.xml" condition="Skin.HasSetting(CustomViewtype_id_85)">custom_id_85</include>
			<include file="custom views\CustomViewtype_id_86.xml" condition="Skin.HasSetting(CustomViewtype_id_86)">custom_id_86</include>
			<include file="custom views\CustomViewtype_id_87.xml" condition="Skin.HasSetting(CustomViewtype_id_87)">custom_id_87</include>
			<include file="custom views\CustomViewtype_id_88.xml" condition="Skin.HasSetting(CustomViewtype_id_88)">custom_id_88</include>
			<include file="custom views\CustomViewtype_id_89.xml" condition="Skin.HasSetting(CustomViewtype_id_89)">custom_id_89</include>
		</control>
		<control type="group">
			<include>Window.Header</include>
			<include>Window.Footer</include>
		</control>
		<include condition="Skin.HasSetting(kioskmode)">View_Options</include>
	</controls>
</window>'''

def main():
	arg = sys.argv[1] if len(sys.argv) > 1 else 0
	skin = xbmc.translatePath("special://skin")
	
	if xbmc.getInfoLabel('system.profilename') != "Manage Profiles":
		print "XML Builder:"
		if xbmc.getCondVisibility('Window.IsVisible(2999)') or xbmc.getCondVisibility('Window.IsVisible(1)'):
			view_path = os.path.join(skin,'xml/views/')
			build_myprograms_xml(view_path, os.path.join(skin,'xml/MyPrograms.xml'))

		includes_path = os.path.join(skin,'xml/includes/')
		build_includes_xml(includes_path, os.path.join(skin,'xml/Includes.xml'))

	if arg:
		print "Reloading skin"
		xbmc.executebuiltin('Reloadskin')

def build_myprograms_xml(view_path, output_path):
	print "	Building MyPrograms.xml"
	with open(output_path, "w") as write_file:
		write_file.write(FILE_HEADER)
		for xml_file in sorted(os.listdir(view_path)):
			if os.path.isfile(os.path.join(view_path, xml_file)):
				print "		Adding {}".format(xml_file)
				with open(os.path.join(view_path, xml_file), "r") as view_file:
					write_file.write(view_file.read() + "\n")
		write_file.write(FILE_FOOTER)
		print "	MyPrograms.xml built."

def build_includes_xml(includes_path, output_path):
	print "	Building Includes.xml"
	with open(output_path, "w") as write_file:
		write_file.write('<includes>\n')
		for xml_file in sorted(os.listdir(includes_path), reverse=True):
			if os.path.isfile(os.path.join(includes_path, xml_file)):
				print "		Adding {}".format(xml_file)
				with open(os.path.join(includes_path, xml_file), "r") as include_file:
					write_file.write(include_file.read() + "\n")
		write_file.write('\n</includes>')
		print "	Includes.xml built."

if __name__ == "__main__":
	print "Loaded XML Builder.py"
	start_time = time.time()
	main()
	print "Unloaded XML Builder.py - took %s seconds to complete" % int(round((time.time() - start_time)))
