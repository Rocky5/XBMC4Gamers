'''
	Script by Rocky5
	Used to patch games.
'''
import os, sys, glob
import xbmcgui, xbmcaddon
Addon = xbmcaddon.Addon('File Patcher')
#####	Script constants
__scriptname__ = Addon.getAddonInfo('name')
__id__ = Addon.getAddonInfo('id')
__author__ = Addon.getAddonInfo('author')
__version__ = Addon.getAddonInfo('version')
__path__ = Addon.getAddonInfo('path')
getLocalizedString = Addon.getLocalizedString
getSetting = Addon.getSetting
print '[SCRIPT][%s] version %s initialized!' % (__scriptname__, __version__)
if (__name__ == "__main__"):
	import resources.lib.__init__ as __init__
	
	header = '''<window id="129">
	<defaultcontrol always="true">3000</defaultcontrol>
	<coordinates>
		<system>1</system>
		<left>320</left>
		<top>10</top>
	</coordinates>
	<controls>
		<control type="image">
			<left>-320</left>
			<top>-10</top>
			<include>1280x720</include>
			<texture>black-back.png</texture>
			<include>Dialog.Effect</include>
		</control>
		<control type="group">
			<include>Dialog.Effect.Zoom.Fast</include>
			<control type="group">
				<left>270</left>
				<top>28</top>
				<control type="image">
					<left>30</left>
					<top>34</top>
					<width>580</width>
					<height>580</height>
					<texture border="20,20,20,20">thumbnofo.png</texture>
				</control>
				<control type="group">
					<top>160</top>
					<left>50</left>
					<control type="textbox">
						<left>0</left>
						<top>-30</top>
						<width>540</width>
						<height>100</height>
						<font>size_40</font>
						<font>size_40</font>
						<align>left</align>
						<aligny>bottom</aligny>
						<textcolor>2000_label</textcolor>
						<label>[B]$INFO[Container(3000).ListItem.Label][/B]</label>
						<autoscroll delay="8000" time="2000" repeat="10000" condition="true">Conditional</autoscroll>
					</control>
					<control type="label">
						<left>0</left>
						<top>70</top>
						<width>115</width>
						<height>20</height>
						<font>size_17</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>2000_label</textcolor>
						<label>Region</label>
					</control>
					<control type="label">
						<left>85</left>
						<top>70</top>
						<width>690</width>
						<height>20</height>
						<font>size_17</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>2000_label</textcolor>
						<label>$INFO[Container(3000).ListItem.Label2]</label>
					</control>
					<control type="label">
						<left>0</left>
						<top>100</top>
						<width>115</width>
						<height>20</height>
						<font>size_17</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>2000_label</textcolor>
						<label>TitleID</label>
					</control>
					<control type="label">
						<left>85</left>
						<top>100</top>
						<width>690</width>
						<height>20</height>
						<font>size_17</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>2000_label</textcolor>
						<label>$INFO[Container(3000).ListItem.Property(TitleID)]</label>
					</control>
					<control type="label">
						<left>0</left>
						<top>130</top>
						<width>115</width>
						<height>20</height>
						<font>size_17</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>2000_label</textcolor>
						<label>Type</label>
					</control>
					<control type="label">
						<left>85</left>
						<top>130</top>
						<width>690</width>
						<height>20</height>
						<font>size_17</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>2000_label</textcolor>
						<label>$INFO[Container(3000).ListItem.Property(Type)]</label>
					</control>
					<control type="label">
						<left>0</left>
						<top>160</top>
						<width>115</width>
						<height>20</height>
						<font>size_17</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>2000_label</textcolor>
						<label>Credits</label>
					</control>
					<control type="label">
						<left>85</left>
						<top>160</top>
						<width>690</width>
						<height>20</height>
						<font>size_17</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>2000_label</textcolor>
						<label>$INFO[Container(3000).ListItem.Property(Credits)]</label>
					</control>
					<control type="label">
						<left>0</left>
						<top>200</top>
						<width>115</width>
						<height>20</height>
						<font>size_17</font>
						<align>left</align>
						<aligny>center</aligny>
						<textcolor>2000_label</textcolor>
						<label>Information</label>
					</control>
					<control type="textbox">
						<left>0</left>
						<top>230</top>
						<width>540</width>
						<height>100</height>
						<font>size_17</font>
						<align>justify</align>
						<textcolor>2000_label</textcolor>
						<scrolltime>200</scrolltime>
						<autoscroll delay="10000" time="1000" repeat="10000" condition="ControlGroup(9001).HasFocus(10)">Conditional</autoscroll>
						<label>$INFO[Container(3000).ListItem.Property(Info)]</label>
					</control>
				</control>
			</control>
			<control type="group">
				<top>28</top>
				<animation effect="slide" start="0,0" end="-275,0" time="300" condition="true">Conditional</animation>
				<control type="image">
					<description>background image</description>
					<left>30</left>
					<top>34</top>
					<width>550</width>
					<height>580</height>
					<texture border="20,20,20,20">thumbnofo.png</texture>
				</control>
				<control type="label">
					<description>heading label</description>
					<left>40</left>
					<top>35</top>
					<width>510</width>
					<height>40</height>
					<align>center</align>
					<aligny>center</aligny>
					<font>size_21_bold</font>
					<label>FILE PATCHER</label>
					<textcolor>2000_label</textcolor>
				</control>
				<control type="list" id="3000">
					<left>45</left>
					<top>90</top>
					<width>500</width>
					<height>480</height>
					<onup>3000</onup>
					<ondown>3000</ondown>
					<onleft>5</onleft>
					<onright>61</onright>
					<pagecontrol>61</pagecontrol>
					<scrolltime>200</scrolltime>
					<itemlayout height="40">
						<control type="image">
							<left>0</left>
							<top>0</top>
							<width>500</width>
							<height>35</height>
							<texture border="5">button-nofocus.png</texture>
						</control>
						<control type="label">
							<left>430</left>
							<top>-1</top>
							<width>70</width>
							<height>35</height>
							<font>size_16</font>
							<align>center</align>
							<aligny>center</aligny>
							<colordiffuse>20FFFFFF</colordiffuse>
							<textcolor>2000_label</textcolor>
							<info>ListItem.Label2</info>
						</control>
						<control type="label">
							<left>10</left>
							<top>-1</top>
							<width>420</width>
							<height>35</height>
							<font>size_20</font>
							<align>left</align>
							<aligny>center</aligny>
							<colordiffuse>20FFFFFF</colordiffuse>
							<textcolor>2000_label</textcolor>
							<info>ListItem.Label</info>
						</control>
					</itemlayout>
					<focusedlayout height="40">
						<control type="image">
							<left>0</left>
							<top>0</top>
							<width>500</width>
							<height>35</height>
							<texture border="5">button-focus2.png</texture>
						</control>
						<control type="label">
							<left>430</left>
							<top>-1</top>
							<width>70</width>
							<height>35</height>
							<font>size_16</font>
							<align>center</align>
							<aligny>center</aligny>
							<textcolor>2000_label</textcolor>
							<info>ListItem.Label2</info>
						</control>
						<control type="label">
							<left>10</left>
							<top>-1</top>
							<width>420</width>
							<height>35</height>
							<font>size_20</font>
							<align>left</align>
							<aligny>center</aligny>
							<textcolor>2000_label</textcolor>
							<info>ListItem.Label</info>
						</control>
					</focusedlayout>
					<content>'''
	
	footer = '''					</content>
				</control>
			</control>
			<control type="group">
				<top>28</top>
				<animation effect="slide" start="0,0" end="-275,0" time="300" condition="true">Conditional</animation>
				<control type="scrollbar" id="61">
					<left>550</left>
					<top>90</top>
					<width>20</width>
					<height>475</height>
					<texturesliderbackground border="2,2,2,2">scrollbar_bar_back2.png</texturesliderbackground>
					<texturesliderbar border="2,16,2,16">scrollbar_bar.png</texturesliderbar>
					<texturesliderbarfocus border="2,16,2,16">scrollbar_bar_focus.png</texturesliderbarfocus>
					<textureslidernib>scrollbar_nib.png</textureslidernib>
					<textureslidernibfocus>scrollbar_nib.png</textureslidernibfocus>
					<onleft>3000</onleft>
					<onright>3000</onright>
					<ondown>61</ondown>
					<onup>61</onup>
					<showonepage>false</showonepage>
					<orientation>vertical</orientation>
				</control>
				<control type="label">
					<description>number of files/pages in list text label</description>
					<left>30</left>
					<top>570</top>
					<width>550</width>
					<height>35</height>
					<font>size_20</font>
					<align>center</align>
					<aligny>center</aligny>
					<scroll>true</scroll>
					<textcolor>2000_label</textcolor>
					<label>($INFO[Container(3000).NumItems]) $LOCALIZE[31211] - $LOCALIZE[31210] ($INFO[Container(3000).CurrentPage]/$INFO[Container(3000).NumPages])</label>
				</control>
				<control type="button" id="3001">
					<left>-500</left>
					<onleft>3000</onleft>
					<onright>3000</onright>
				</control>
			</control>
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

	# build xml list
	cwd = os.getcwd()
	CountList = 0
	mainXml = os.path.join(cwd,'resources/lib/patches/')
	with open(os.path.join(cwd,'resources/skins/default/xml/main.xml'), "w") as WriteFile:
		WriteFile.write(header)
		# for xmls in sorted([x.lower().replace('generic patches','Generic patches') for x in os.listdir(mainXml)], key=None, reverse=0):
		for xmls in sorted([x.lower().replace('generic patches','Generic patches') for x in glob.glob(xbmc.translatePath(mainXml+'*.pf'))], key=None, reverse=0):
			CountList = CountList+1
			author = "Unknown"
			Credits = "Unknown"
			info = "Unknown"
			region = "Unknown"
			title = "Unknown"
			titleid = "Unknown"
			type = "Unknown"
			with open(xmls, 'r') as patch_file:
				read_file=patch_file.readlines()
				for line in read_file:
					if '#' in line:
						if 'Author:' in line:
							author=line.rstrip().split('Author: ')[1]
						elif 'Credits:' in line:
							credits=line.rstrip().split('Credits: ')[1]
						elif 'Title:' in line:
							title=line.rstrip().split('Title: ')[1]
						elif 'Info:' in line:
							info=line.rstrip().split('Info: ')[1]
						elif 'Region:' in line:
							region=line.rstrip().split('Region: ')[1]
						elif 'TitleID:' in line:
							titleid=line.rstrip().split('TitleID: ')[1]
						elif 'Type:' in line:
							type=line.rstrip().split('Type: ')[1]
						else:
							pass

			with open(xmls, "r") as Views:
				WriteFile.write(
					template % (
						CountList,
						title,
						region,
						author,
						credits,
						info,
						titleid,
						type,
						'RunScript(%s)' % (
							os.path.join(cwd,'resources\\lib\\default.py,%s') % (os.path.basename(xmls))
						)
					)
				)
		WriteFile.write(footer)
	
	
	ui = __init__.GUI('%s.xml' %  "main",__path__, 'default')
	ui.doModal()
	print '[SCRIPT][%s] version %s exited!' % (__scriptname__, __version__)
	del ui
sys.modules.clear()











































