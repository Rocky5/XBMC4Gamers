# XBMC4Gamers
This is a skin for XBMC4Xbox v3.5.3+ that utilises custom python scripts that I created to do specific tasks.

The main objective of this project was to allow my kids to use the same Xbox but also have there own saves, so to stop fighting lol. Now the original Xbox doesn't allow this by default, so I had to think outside of the box and learn and create some Python script to do the job. It works quite well.

Now since the above, I have added scripts that fixes scrambled screen games on v.1.6 Xbox ( 480p video mode ) clean save directories of blank saves, clean program thumbnails or refresh them as well as others to do other tasks. It's a jack of all trades lol.

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Setup/Installation:

	1)	Download XBMC. *
	2)	Place the XBMC folder inside the XBMC4Gamers-master folder.
	3)	Double click "Build XBMC4Gamers.bat"
	4)	FTP the XBMC4Gamers folder anywhere on your Xbox. **
		
		*
			https://drive.google.com/folderview?pli=1&ddrp=1&id=0B9zNhNcNUdDTRVFBbHcwc2JCZFE#list
		**
			I would suggest leaving the "Enable individual save directories for each profile" disabled if you are using this as an application or only one profile.

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
Creating Profiles:

	1) Load the "Manage Profiles" profile.
	2) Select Add Profile...
	3) Enter your desired name.
	4) Now select an profile image.
	5) And Log out. (R) Stick pushed in.
	6) Disable Edit Mode if you wish.

Individual save script information:

	1) A backup is created of your orignal UDATA directory. ( named UDATA Backup )
	2) Any softmod or exploit saves are automatically transferred to a new profile.
	3) To transfer saves over to a new profile name, change the folder name & the *.profile file inside the directory. *

		*
			Example:
			Old profile = Connxtion
			New profile = Rocky5
			Find the "UDATA Connxtion" folder in "E:\" & I rename it to "UDATA Rocky5"
			Now also rename the "Connxtion.profile" file inside the now named "UDATA Rocky5" folder to "Rocky5.profile". Done!


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Edit Mode:

	Enter key combination at the login screen:
		Up, UP, DOWN, DOWN, LEFT, LEFT, RIGHT, RIGHT & A

	The above combination will also enable "Edit mode" if its disabled.
	Remember to disable after changing stuff.

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Controls: (can be viewed at the login screen)

	Edit Mode Users profile:
		1)	(A) button will select menus or play games.
		2)	(X) button will open the game preview/synopsis or music controls.
		3)	(Y) button will take a Screenshot.
		4)	(Black) button opens the options dialogue.
		5)	(White) button opens the context menu. (certain menus)
		6)	(Start) button will launch a disc based game.
		7)	(L) stick pressed in will reload the skin.
		8)	(R) stick pressed in logs out current user.
		9)	all default controls of XBMC

	User Mode Users profile:
		1)	(A) button will select menus or play games.
		2)	(X) button will open the game preview/synopsis or music controls.
		3)	(Black) button will load your favourites.
		4)	(White) button opens the context menu. (certain menus &amp; limited functionality in usermode)
		5)	(Start) button will launch a disc based game.
		6)	(R) stick pressed in logs out current user.
		7)	all default controls of XBMC

	Edit Mode Manage Profiles/DVD2Xbox profile:
		1)	(A) button will select menus.
		2)	(Y) button will take a Screenshot.
		3)	(Black) button cleans the Xbox cache.
		4)	(White) button opens the context menu. (certain menus)
		5)	(Start) button will launch a disc based game.
		6)	(L) stick pressed in will reload the skin.
		7)	(R) stick pressed in logs out current user.
		8)	all default controls of XBMC

	User Mode Manage Profiles/DVD2Xbox profile:
		1)	(A) button will select menus.
		2)	(Black) button cleans the Xbox cache.
		3)	(Start) button will launch a disc based game.
		4)	(R) stick pressed in logs out current user.
