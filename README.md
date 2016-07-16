# XBMC4Kids
This is a skin with custom python scripts (allow each profile to have there own saves) for people that want a fancy UI for just there games.

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Setup/Installation:

	1)	Download XBMC. *
	2)	Place the XBMC folder inside the XBMC4Kids-master. **
	3)	Double click "Build XBMC4Kids.bat"
	4)	FTP the XBMC4Kids folder anywhere on your Xbox. ***
		
		*
			https://drive.google.com/folderview?pli=1&ddrp=1&id=0B9zNhNcNUdDTRVFBbHcwc2JCZFE#list
		**
			If you got this from the git (Github) place the XBMC folder inside the trunk folder.
		***
			I would suggest leaving the "Enable individual save directories for each profile" disabled if you are using this as an application or only one profile.

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	
Creating Profiles:

	1) Load the "Manage Profiles" profile.
	2) Select "Manage Profiles".
	3) Select Add Profile...
	4) Enter your desired name.
	5) Now select OK
	6) Again select OK
	7) Now select start fresh, for both options.
	8) And Log out. (R) Stick pushed in.
	10) Disable Edit Mode if you wish.

What not to do:

	1) Change profile names after creation, will will break my script. (it will create a new save folder)
	2) To transfer saves over to a new profile, change the folder name & the *.profile file inside the directory. *

		*
			Example:
			Profile name Connxtion, but I want to change it to Rocky5 & keep my saves.
			I find the "UDATA Connxtion" folder in "E:\" & I rename it to "UDATA Rocky5"
			I now also rename the "Connxtion.profile" file inside to "Rocky5.profile". Done!


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Edit Mode:

	Enter key combination at the login screen:
		Up, UP, DOWN, DOWN, LEFT, LEFT, RIGHT, RIGHT & A

	The above combination will also enable the Edit mode if its disabled.
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
		4)	(White) button opens the context menu. (certain menus & limited functionality in usermode)
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
