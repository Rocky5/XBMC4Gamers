Binary patcher for XBMC4Gamers
This I made for fun as I was bored and wanted something people could use to patch games easily.

--------------------------------------------------------------------------------------------------
	Patch file header information
--------------------------------------------------------------------------------------------------

	# Author:
		This is optional, but credit the patch authors.

	# Credits:
		This is optional, it's additional information.

	# Info:
		This is used to describe what the patch does.
		(You can create new lines by using [CR])

	# Region:
		This is mandatory. MULTI, PAL, NTSC and NTSC-J

	# Title:
		This is the games name, it's used for the selection list.

	# TitleID:
		This is mandatory as it's used to detect if the game folder you selected is the correct game.
		As patches can be region specific.
	
	# Type:
		This is what the patch does, it can be whatever you want it to be but I use the following.
			480p Patch
			720p Patch
			Certificate Patch
			Certificate & FATX Patch
			Multi Patch
			Other Patch
			Widescreen Patch

	#:
		# without the above is used to as a comment line. These are skipped and for manual viewing purposes only.

--------------------------------------------------------------------------------------------------
	Example patch
-------------------------------------------------------------------------------------------
	
	Patch files content:
		# Author: Lord Crass
		# Credits: Lord Crass
		# Info: Fixes long file name check, removes FatX checks, disables save corruption and sector offset protection.
		# Region: All
		# Title: Race Driver 3
		# TitleID: 434d0050
		# Type: Multi Patch

		CP|default.xbe|default_orig.xbe
		RM|dashupdate.xbe|update.xbe

		# Rename the long files (assumes they are already truncated at 42 characters)
		MV|015662574029570062573498458618274029349857|01566257402957006257
		MV|071362571270516956224586848573710713625712|07136257127051695622
		MV|514379286257514395994055516907134055562284|51437928625751439599
		MV|737101561827458646126257684072935622458684|73710156182745864612
		MV|737101561827458668148485015672935622904223|73710156182745866814

		# Remove first FATX check
		HR|default.xbe|1|85C07508C7442420000048008D44241C|85C0750890909090909090908D44241C

		# Fix internal generation of long file names
		HR|default.xbe|1|C744242014000000EB038D49|C744242005000000EB038D49

		# Hardcode internal sector offset key to 7d07c
		HR|default.xbe|1|8bf056e800f00300|b87cd00700909090

		# Return default bogus offset for query and avoid second FATX/GDFX check
		HR|default.xbe|1|568d450850ff3530c7340083ceff|be563412008bc65ec9c204009090

		# Remove silent save corrupter
		HR|default.xbe|1|C705EC6A3A0000000000|90909090909090909090

--------------------------------------------------------------------------------------------------
	CP = Copy
-------------------------------------------------------------------------------------------
	
	Used to copy files to new locations or for backup purposes.
	
		Example:
			CP|default.xbe|default_orig.xbe
		
		You can use this to copy a file to a new filename and then patch that xbe instead.
		Example:
			CP|default.xbe|defaultws.xbe
			HR|defaultws.xbe|2|DDDD|2222

		Note:
			If the files already exists it wont copy, so remove existing file first then copy.

--------------------------------------------------------------------------------------------------
	HR = Hex replace.
-------------------------------------------------------------------------------------------

	Used to patch a file using a search method.
	
		The |2| value is how many instances of the "DDDD" string it will replace with "2222".
		Example:
			HR|default.xbe|2|DDDD|2222

		You can string multiple search together or keep them separate.
		Example:
			HR|default.xbe|2|DDDD|2222|1|456732|909090
		or
			HR|default.xbe|2|DDDD|2222
			HR|default.xbe|1|456732|909090

--------------------------------------------------------------------------------------------------
	MV = Move
-------------------------------------------------------------------------------------------

	This just moves a file to a new location and or filename.

		Example:
			MV|default.xbe|default_orig.xbe

--------------------------------------------------------------------------------------------------
	OF = Offset patching, can be chained or as a new entry.
-------------------------------------------------------------------------------------------

	This uses static offsets to place strings of bytes.

		This will write "2222" at offset 100 (dec)
		Example:
			OF|default.xbe|100|2222

		You can string multiple offsets together or keep them separate.
		Example:
			OF|default.xbe|100|2222|200|DDDD
		or
			OF|default.xbe|100|2222
			OF|default.xbe|200|DDDD

--------------------------------------------------------------------------------------------------
	RM = Remove
-------------------------------------------------------------------------------------------

	This will remove files.
	
		Example:
			RM|dashupdate.xbe
		
		You can string multiple files together or keep them separate.
		Example:
			RM|dashupdate.xbe|update.xbe
		or
			RM|dashupdate.xbe
			RM|update.xbe

--------------------------------------------------------------------------------------------------
	RN = Rename
-------------------------------------------------------------------------------------------

	This will rename files.
	
		Example:
			RN|default.xbe|default_orig.xbe

--------------------------------------------------------------------------------------------------
	SM = Supported Media
-------------------------------------------------------------------------------------------

	This will patch an xbe files to allow all media types.
	
		Example:
			SN|default.xbe|C00001FF

--------------------------------------------------------------------------------------------------
	SR = Supported Regions
-------------------------------------------------------------------------------------------

	This will patch an xbe files to allow multi region support + debug.
	
		Example:
			SR|default.xbe|80000007
