Synopsis Script for XBMC.

This script will allow you to show information/images on anything that uses a default.xbe and is scanned in by XBMC.


To integrate this script into your skin I have a separate build that has all its labels and colours separate from the skin so it works out of the box.
( https://github.com/Rocky5/XBMC4Kids/tree/master/Synopsis%20Example )

You must call the scrip within the MyPrograms window, ie, when a game or other title is highlighted.

	Example:
		Windowed Mode:
			<control type="button" id="9000">
				<onfocus>RunScript( Special://xbmc/scripts/XBMC4Kids Extras/Synopsis/default.py )</onfocus>
			</control>
		Dialog Mode:
			<control type="button" id="9000">
				<onfocus>RunScript( Special://xbmc/scripts/XBMC4Kids Extras/Synopsis/default.py,dialog )</onfocus>
			</control>

The synopsis script looks for specific files in a specific folder structure.

	Example:
		Advent Rising
			_resources
				artwork
					banner.jpg
					fanart.jpg
					poster.jpg
				media
					preview.xmv/wmv/mp4/mpg
				screenshots
					collection of images
			default.xml
			
Now the default.xml must have specific tags or the script will fail.

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

Now to use the scrip there are a couple things you need to do first, there is a custom window included with the toggle already set, though you will need to fix it up as the images wont all work.

	The script uses 4 skin settings:

		SynopsisMode		= If this is enables the bellow options become accessible, without this setting enabled it will default to the game preview window.
		Synopsis			= This enables the default view.
		Synopsis_alt_view	= This enables the old/alternative view.
		Synopsis_Autoplay	= This enables auto play of the preview video if found, for the alt view only.
		
Here is a list of the variables you can use.

	Synopsis Information:

		Images:
			$INFO[Window(MyPrograms).Property(Synopsis_banner)]
			$INFO[Window(MyPrograms).Property(Synopsis_fanart)]
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






