Synopsis Script for XBMC.

This script will allow you to show information/images on anything that uses a default.xbe and is scanned in by XBMC.


To integrate this into your skin:

	1) Place the 3 _Script* xml files into your 720p folder.
	2) Stick the Synopsis folder in you scripts folder.
	3) Replace your default.xbe with the new one.
	4) Yeah that's it.


The synopsis script looks for specific files in a specific folder structure.

	Example:
		Advent Rising
			_resources
				artwork
					banner.*
					fanart.*
					poster.*
				media
					preview.*
				screenshots
					collection of images
			default.xml
			
Now the default.xml must have specific tags.

	default.xml:
		<synopsis>
			<title>Advent Rising</title>
			<developer>Demiurge Studios</developer>
			<publisher>Majesco Entertainment</publisher>
			<features_general>Players: 1, Dolby 5.1 Surround</features_general>
			<features_online>Content Download, Friends</features_online>
			<esrb>T</esrb>
			<esrb_descriptors>Blood, Mild Language, Violence</esrb_descriptors>
			<genre>Action-adventure, third-person shooter Action-adventure</genre>
			<release_date>May 31, 2005</release_date>
			<rating>7.8</rating>
			<platform>Xbox</platform>
			<exclusive>No</exclusive>
			<titleid>4D4A0009</titleid>
			<overview>some info would go here</overview>
		</synopsis>
		
Here is a list of the variables you can use.

	Synopsis Information:

		Images:
			$INFO[Window(MyPrograms).Property(Alt_Synopsis_icon)]
			$INFO[Window(MyPrograms).Property(Synopsis_banner)]
			$INFO[Window(MyPrograms).Property(Synopsis_disc)]
			$INFO[Window(MyPrograms).Property(Synopsis_fanart)]
			$INFO[Window(MyPrograms).Property(Synopsis_fog)]
			$INFO[Window(MyPrograms).Property(Synopsis_icon)]
			$INFO[Window(MyPrograms).Property(Synopsis_poster)]
			$INFO[Window(MyPrograms).Property(Synopsis_screenshots)]

		Run XBE:
			RunXBE($INFO[Window(MyPrograms).Property(Synopsis_xbe)])

		Synopsis overview:
			$INFO[Window(MyPrograms).Property(Synopsis_title_alt)]
			$INFO[Window(MyPrograms).Property(Synopsis_titleid_alt)]
			$INFO[Window(MyPrograms).Property(Synopsis_overview_alt)]
			$INFO[Window(MyPrograms).Property(Synopsis_rating_alt)]

		Full Synopsis:
			$INFO[Window(MyPrograms).Property(Synopsis_title)]
			$INFO[Window(MyPrograms).Property(Synopsis_developer)]
			$INFO[Window(MyPrograms).Property(Synopsis_publisher)]
			$INFO[Window(MyPrograms).Property(Synopsis_esrb)]
			$INFO[Window(MyPrograms).Property(Synopsis_esrb_descriptors)]
			$INFO[Window(MyPrograms).Property(Synopsis_features_general)]
			$INFO[Window(MyPrograms).Property(Synopsis_features_online)]
			$INFO[Window(MyPrograms).Property(Synopsis_genre)]
			$INFO[Window(MyPrograms).Property(Synopsis_release_date)]
			$INFO[Window(MyPrograms).Property(Synopsis_rating)]
			$INFO[Window(MyPrograms).Property(Synopsis_platform)]
			$INFO[Window(MyPrograms).Property(Synopsis_exclusive)]
			$INFO[Window(MyPrograms).Property(Synopsis_titleid)]
			$INFO[Window(MyPrograms).Property(Synopsis_overview)]
			
		Video Preview:
			$INFO[Window(MyPrograms).Property(Synopsis_Video_Preview_Name)]
			PlayWith($INFO[Window(MyPrograms).Property(Player_Type)])
			PlayMedia($INFO[Window(MyPrograms).Property(Synopsis_Video_Preview_Path)],1,noresume)
			PlayMedia($INFO[Window(MyPrograms).Property(Preview_default)],1,noresume)
			PlayMedia($INFO[Window(MyPrograms).Property(Preview_alt)],1,noresume)

