'''
	Script by Rocky5
	Used to patch games.
'''
from os.path import basename, isdir, join
from os import getcwd, mkdir
from glob import glob
from xbmc import translatePath
import xbmcaddon
import resources.lib.__init__ as addon_init

Addon = xbmcaddon.Addon('File Patcher')
__scriptname__ = Addon.getAddonInfo('name')
__version__ = Addon.getAddonInfo('version')
__path__ = Addon.getAddonInfo('path')
print "[SCRIPT][{}] version {} initialized!".format(__scriptname__, __version__)

if (__name__ == "__main__"):
	import resources.lib.__init__ as __init__
	
	header = '''<window id="129">
	<defaultcontrol always="true">3000</defaultcontrol>
	<onload>Dialog.Close(1100,false)</onload>
	<controls>
		<include>Behind.Dialog</include>
		<control type="group">
			<include>Dialog.Effect.Zoom.Fast</include>
			<control type="image">
				<left>270</left>
				<top>80</top>
				<width>740</width>
				<height>560</height>
				<aspectratio>stretch</aspectratio>
				<texture colordiffuse="colour.dialog.diffuse.main">windows\\dialogs\\select_browser\\main.png</texture>
				<animation effect="zoom" start="270,80,740,560" end="120,80,1040,560" time="0" condition="true">Conditional</animation>
			</control>
			<control type="image">
				<left>286</left>
				<top>99</top>
				<width>709</width>
				<height>61</height>
				<aspectratio>stretch</aspectratio>
				<texture colordiffuse="colour.dialog.diffuse.header">windows\\dialogs\\select_browser\\header.png</texture>
				<animation effect="zoom" start="286,99,709,61" end="142,99,996,61" time="0" condition="true">Conditional</animation>
			</control>
			<control type="label">
				<description>Heading label</description>
				<left>313</left>
				<top>107</top>
				<width>731</width>
				<height>37</height>
				<include>Dialog.Select.Font</include>
				<scroll>true</scroll>
				<align>left</align>
				<aligny>center</aligny>
				<textcolor>colour.dialog.label.header</textcolor>
				<shadowcolor>-</shadowcolor>
				<label>File Patcher</label>
				<animation effect="slide" start="0,0" end="-144,0" time="0" condition="true">Conditional</animation>
			</control>
			<control type="grouplist">
				<description>Control Info</description>
				<left>360</left>
				<top>565</top>
				<width>561</width>
				<height>80</height>
				<itemgap>10</itemgap>
				<orientation>Horizontal</orientation>
				<align>center</align>
				<!-- A Button -->
				<control type="image">
					<left>0</left>
					<top>0</top>
					<width>32</width>
					<height>32</height>
					<aspectratio>stretch</aspectratio>
					<texture colordiffuse="colour.dialog.diffuse.a_button">pad_buttons\\dialogs\\a_button.png</texture>
				</control>
				<control type="label">
					<left>0</left>
					<top>0</top>
					<width min="40" max="147">auto</width>
					<height>32</height>
					<font>size_19</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>$LOCALIZE[424]</label>
				</control>
				<!-- B Button -->
				<control type="image">
					<left>0</left>
					<top>0</top>
					<width>32</width>
					<height>32</height>
					<aspectratio>stretch</aspectratio>
					<texture colordiffuse="colour.dialog.diffuse.b_button">pad_buttons\\dialogs\\b_button.png</texture>
				</control>
				<control type="label">
					<left>0</left>
					<top>0</top>
					<width min="40" max="147">auto</width>
					<height>32</height>
					<font>size_19</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>$LOCALIZE[31108]</label>
				</control>
			</control>
			<control type="group">
				<left>681</left>
				<top>229</top>
				<control type="textbox">
					<left>0</left>
					<top>-55</top>
					<width>435</width>
					<height>125</height>
					<font>size_35</font>
					<align>left</align>
					<aligny>bottom</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>[B]$INFO[Container(3000).ListItem.Label][/B]</label>
					<autoscroll delay="8000" time="2000" repeat="10000" condition="true">Conditional</autoscroll>
				</control>
				<control type="label">
					<left>0</left>
					<top>75</top>
					<width>150</width>
					<height>15</height>
					<font>size_17</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>[B]Region:[/B]</label>
				</control>
				<control type="label">
					<left>85</left>
					<top>75</top>
					<width>355</width>
					<height>15</height>
					<font>size_17</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>$INFO[Container(3000).ListItem.Label2]</label>
				</control>
				<control type="label">
					<left>0</left>
					<top>100</top>
					<width>150</width>
					<height>15</height>
					<font>size_17</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>[B]TitleID:[/B]</label>
				</control>
				<control type="label">
					<left>85</left>
					<top>100</top>
					<width>355</width>
					<height>15</height>
					<font>size_17</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>$INFO[Container(3000).ListItem.Property(TitleID)]</label>
					<scroll>true</scroll>
				</control>
				<control type="label">
					<left>0</left>
					<top>125</top>
					<width>150</width>
					<height>15</height>
					<font>size_17</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>[B]Type:[/B]</label>
				</control>
				<control type="label">
					<left>85</left>
					<top>125</top>
					<width>355</width>
					<height>15</height>
					<font>size_17</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>$INFO[Container(3000).ListItem.Property(Type)]</label>
					<scroll>true</scroll>
				</control>
				<control type="label">
					<left>0</left>
					<top>150</top>
					<width>150</width>
					<height>15</height>
					<font>size_17</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>[B]Credits:[/B]</label>
				</control>
				<control type="label">
					<left>85</left>
					<top>150</top>
					<width>355</width>
					<height>15</height>
					<font>size_17</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>$INFO[Container(3000).ListItem.Property(Credits)]</label>
					<scroll>true</scroll>
				</control>
				<control type="label">
					<left>0</left>
					<top>175</top>
					<width>150</width>
					<height>15</height>
					<font>size_17</font>
					<align>left</align>
					<aligny>center</aligny>
					<textcolor>colour.dialog.label.context</textcolor>
					<label>[B]Information:[/B]</label>
				</control>
				<control type="textbox">
					<left>0</left>
					<top>190</top>
					<width>435</width>
					<height>125</height>
					<font>size_17</font>
					<align>justify</align>
					<textcolor>colour.dialog.label.context</textcolor>
					<scrolltime>200</scrolltime>
					<label>$INFO[Container(3000).ListItem.Property(Info)]</label>
					<autoscroll delay="10000" time="1000" repeat="10000" condition="ControlGroup(9001).HasFocus(10)">Conditional</autoscroll>
				</control>
			</control>
			<control type="list" id="3000">
				<description>button area</description>
				<left>305</left>
				<top>170</top>
				<width>510</width>
				<height>378</height>
				<onup>3</onup>
				<ondown>3</ondown>
				<onleft>60</onleft>
				<onright>9000</onright>
				<pagecontrol>60</pagecontrol>
				<scrolltime>200</scrolltime>
				<animation effect="slide" start="0,0" end="-144,0" time="0" condition="true">Conditional</animation>
				<itemlayout height="42" width="510">
					<control type="image">
						<left>0</left>
						<top>0</top>
						<width>510</width>
						<height>40</height>
						<aspectratio>stretch</aspectratio>
						<texture border="3" colordiffuse="colour.dialog.diffuse.button.nofocus">windows\\dialogs\\select_browser\\button_no_focus.png</texture>
					</control>
					<control type="label">
						<left>10</left>
						<top>0</top>
						<height>40</height>
						<width>430</width>
						<font>size_16</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>colour.dialog.button.nofocus</textcolor>
						<label>$INFO[ListItem.Label]</label>
						<scroll>false</scroll>
					</control>
					<control type="label">
						<right>10</right>
						<top>0</top>
						<height>40</height>
						<width>60</width>
						<font>size_16</font>
						<align>right</align>
						<aligny>center</aligny>
						<textcolor>colour.dialog.button.nofocus</textcolor>
						<label>$INFO[ListItem.Label2]</label>
						<scroll>false</scroll>
					</control>
				</itemlayout>
				<focusedlayout height="42" width="510">
					<control type="image">
						<left>0</left>
						<top>0</top>
						<width>510</width>
						<height>40</height>
						<aspectratio>stretch</aspectratio>
						<texture border="3" colordiffuse="colour.dialog.diffuse.button.focus">windows\\dialogs\\select_browser\\button_focus.png</texture>
					</control>
					<control type="label">
						<left>10</left>
						<top>0</top>
						<height>40</height>
						<width>430</width>
						<font>size_16</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>colour.dialog.button.focus</textcolor>
						<label>$INFO[ListItem.Label]</label>
						<scroll>false</scroll>
					</control>
					<control type="label">
						<right>10</right>
						<top>0</top>
						<height>40</height>
						<width>60</width>
						<font>size_16</font>
						<align>right</align>
						<aligny>center</aligny>
						<textcolor>colour.dialog.button.focus</textcolor>
						<label>$INFO[ListItem.Label2]</label>
						<scroll>false</scroll>
					</control>
				</focusedlayout>
				<content>'''
	
	footer = '''				</content>
			</control>
		</control>
		<control type="scrollbar" id="60">
			<left>301</left>
			<top>170</top>
			<width>4</width>
			<height>376</height>
			<onright>3000</onright>
			<texturesliderbackground border="2,2,2,2">scrollbar_bar_back2.png</texturesliderbackground>
			<texturesliderbar border="2,16,2,16">scrollbar_bar.png</texturesliderbar>
			<texturesliderbarfocus border="2,16,2,16">scrollbar_bar.png</texturesliderbarfocus>
			<textureslidernib>-</textureslidernib>
			<textureslidernibfocus>-</textureslidernibfocus>
			<showonepage>false</showonepage>
			<orientation>vertical</orientation>
			<animation reversible="false" effect="fade" start="40" end="100" time="100">Focus</animation>
			<animation reversible="false" effect="fade" start="100" end="40" time="100" condition="!Control.HasFocus(60)">Conditional</animation>
			<animation effect="slide" start="0,0" end="-144,0" time="0" condition="true">Conditional</animation>
		</control>
		<control type="label">
			<description>number of files in list text label</description>
			<right>295</right>
			<bottom>105</bottom>
			<width>550</width>
			<height>15</height>
			<font>size_15</font>
			<align>right</align>
			<aligny>center</aligny>
			<scroll>false</scroll>
			<textcolor>colour.dialog.label.context</textcolor>
			<label>$INFO[Container(3000).CurrentItem]/$INFO[Container(3000).NumItems]</label>
			<animation reversible="false" effect="fade" start="0" end="75" time="300">Visible</animation>
			<animation reversible="false" effect="fade" start="75" end="0" time="0">Hidden</animation>
			<animation effect="slide" start="0,0" end="144,0" time="0" condition="true">Conditional</animation>
		</control>
		<control type="button" id="3001">
			<onleft>3000</onleft>
			<onright>3000</onright>
			<visible allowhiddenfocus="true">false</visible>
		</control>
	</controls>
</window>'''

	template = '''
						<item id="%s">
							<label>%s</label>
							<label2>%s</label2>
							<property name="Author">%s</property>
							<property name="Credits">%s</property>
							<property name="Info">%s</property>
							<property name="TitleID">%s </property>
							<property name="Type">%s</property>
							<onclick>%s</onclick>
							<onclick>SetFocus(3001)</onclick>
						</item>
'''

	# Build XML list
	cwd = getcwd()
	CountList = 0
	Patches = join(cwd, 'resources/lib/patches/')
	UserPatches = join(cwd, 'user patches/')
	if not isdir(UserPatches):
		mkdir(UserPatches)
	with open(join(cwd, 'resources/skins/default/xml/main.xml'), "w") as WriteFile:
		WriteFile.write(header)

		patch_files = [x for x in glob(translatePath(Patches + '*.pf'))]
		user_patch_files = [x for x in glob(translatePath(UserPatches + '*.pf'))]
		combined_files = patch_files + user_patch_files
		sorted_files = sorted(combined_files,key=lambda f: (0 if 'generic patches' in f.lower() else 1,basename(f).lower()))

		for pfs in sorted_files:
			CountList += 1
			author = "Unknown"
			credits = "Unknown"
			info = "Unknown"
			region = "Unknown"
			title = "Unknown"
			titleid = "Unknown"
			type = "Unknown"

			with open(pfs, 'r') as patch_file:
				read_file = patch_file.readlines()
				for line in read_file:
					if '#' in line:
						if 'Author:' in line:
							author = line.rstrip().split('Author: ')[1]
						elif 'Credits:' in line:
							credits = line.rstrip().split('Credits: ')[1]
						elif 'Title:' in line:
							title = line.rstrip().split('Title: ')[1]
						elif 'Info:' in line:
							info = line.rstrip().split('Info: ')[1]
						elif 'Region:' in line:
							region = line.rstrip().split('Region: ')[1]
						elif 'TitleID:' in line:
							titleid = line.rstrip().split('TitleID: ')[1]
						elif 'Type:' in line:
							type = line.rstrip().split('Type: ')[1]

			WriteFile.write(
				template % (
					CountList,
					title.upper(),
					region,
					author,
					credits,
					info,
					titleid,
					type,
					'RunScript(%s)' % (
						join(cwd, 'resources\\lib\\default.py,%s') % (pfs)
					)
				)
			)
		WriteFile.write(footer)
	
	ui = __init__.GUI('%s.xml' %  "main",__path__, 'default')
	ui.doModal()
	del ui