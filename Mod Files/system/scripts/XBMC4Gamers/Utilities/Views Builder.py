'''	
	Script by Rocky5
	Used to build the MyPrograms.xml on boot. This saves 2MB of memory instead of using includes.
'''
import glob,os,sys,time,xbmc
print "Loaded Views Builder.py"
start_time = time.time()
MyProgramsFile = '<window id="1">\n\
		<defaultcontrol always="true">50</defaultcontrol>\n\
		<allowoverlay>no</allowoverlay>\n\
		<onload condition="Skin.HasSetting(run_random_script)">RunScript(Special://root/system/scripts/XBMC4Gamers/Utilities/Random Select.py)</onload>\n\
		<views>50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,79,80,81,82,83,84,85,86,87,88,89</views>\n\
		<controls>\n\
				<include condition="!Skin.HasSetting(kioskmode)">Kiosk.Mode.Secret.Code</include>\n\
				<include>Synopsis.Loader</include>\n\
				<include>Global.Backgrounds</include>\n\
				<include>Fanart</include>\n\
				<control type="group">\n\
						<visible>!Window.IsActive(1101)</visible>\n\
						<animation effect="fade" start="100" end="0" time="100" delay="400">hidden</animation>\n\
						<animation effect="fade" start="0" end="100" delay="0" time="100">visible</animation>\n\
						%s\n\
						<!-- Custom views -->\n\
						<include file="custom views\CustomViewtype_id_80.xml" condition="Skin.HasSetting(CustomViewtype_id_80)">custom_id_80</include>\n\
						<include file="custom views\CustomViewtype_id_81.xml" condition="Skin.HasSetting(CustomViewtype_id_81)">custom_id_81</include>\n\
						<include file="custom views\CustomViewtype_id_82.xml" condition="Skin.HasSetting(CustomViewtype_id_82)">custom_id_82</include>\n\
						<include file="custom views\CustomViewtype_id_83.xml" condition="Skin.HasSetting(CustomViewtype_id_83)">custom_id_83</include>\n\
						<include file="custom views\CustomViewtype_id_84.xml" condition="Skin.HasSetting(CustomViewtype_id_84)">custom_id_84</include>\n\
						<include file="custom views\CustomViewtype_id_85.xml" condition="Skin.HasSetting(CustomViewtype_id_85)">custom_id_85</include>\n\
						<include file="custom views\CustomViewtype_id_86.xml" condition="Skin.HasSetting(CustomViewtype_id_86)">custom_id_86</include>\n\
						<include file="custom views\CustomViewtype_id_87.xml" condition="Skin.HasSetting(CustomViewtype_id_87)">custom_id_87</include>\n\
						<include file="custom views\CustomViewtype_id_88.xml" condition="Skin.HasSetting(CustomViewtype_id_88)">custom_id_88</include>\n\
						<include file="custom views\CustomViewtype_id_89.xml" condition="Skin.HasSetting(CustomViewtype_id_89)">custom_id_89</include>\n\
				</control>\n\
				<control type="group">\n\
						<include>Dialog.Effect.Fast</include>\n\
						<include>Window.Header</include>\n\
						<include>Window.Footer</include>\n\
				</control>\n\
				<include condition="Skin.HasSetting(kioskmode)">View_Options</include>\n\
		</controls>\n\
</window>'

try: arg = int(sys.argv[1:][0])
except: arg = 0
if xbmc.getCondVisibility('Window.IsVisible(2999)') or xbmc.getCondVisibility('Window.IsVisible(1)'):
	print "Building Views Views Builder.py"
	ViewsStored = ""
	viewPath = xbmc.translatePath('Q:/skins/profile skin/xml/views/')
	ProgramsPath = xbmc.translatePath('Q:/skins/profile skin/xml/')
	Filter_XMLS = sorted([os.path.basename(x) for x in glob.glob(viewPath+'Viewtype_*.xml')], key=None, reverse=0)

	for xmls in Filter_XMLS:
		with open(os.path.join(viewPath,xmls), "r") as ViewsRead:
			ViewsStored = ViewsStored+ViewsRead.read()

	with open(os.path.join(ProgramsPath,'MyPrograms.xml'), "w") as WriteProgramsFile:
		WriteProgramsFile.write(MyProgramsFile % (ViewsStored))

if arg: xbmc.executebuiltin('Reloadskin')

print "Unloaded Views Builder.py - took %s seconds to complete" % int(round((time.time() - start_time)))