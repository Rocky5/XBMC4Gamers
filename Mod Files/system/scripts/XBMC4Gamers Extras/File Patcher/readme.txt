Binary patcher for XBMC4Gamers
This I made for fun as I was bored and wanted something people could use to patch games easily.

How it works is you have 6 options available to use.

--------------------------------------------------------------------------------------------------
	CP = Copy
--------------------------------------------------------------------------------------------------
	
	Used to copy files to new locations or for backup purposes.
	
		Example:
			CP|default.xbe|default_orig.xbe
		
		You can use this to copy a file to a new filename and then patch that xbe instead.
		Example:
			CP|default.xbe|defaultws.xbe
			HR|defaultws.xbe|2|DDDD|2222

--------------------------------------------------------------------------------------------------
	HR = Hex replace.
--------------------------------------------------------------------------------------------------

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
--------------------------------------------------------------------------------------------------

	This just moves a file to a new location and or filename.

		Example:
			MV|default.xbe|default_orig.xbe

--------------------------------------------------------------------------------------------------
	OF = Offset patching, can be chained or as a new entry.
--------------------------------------------------------------------------------------------------

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
--------------------------------------------------------------------------------------------------

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
--------------------------------------------------------------------------------------------------

	This will rename files.
	
		Example:
			RN|default.xbe|default_orig.xbe

--------------------------------------------------------------------------------------------------
	Naming of files. (used for sorting the list)
--------------------------------------------------------------------------------------------------
	
	Patch types:
		ct	=	Certificate
		hd	=	720p
		mp	=	Multi Patch
		ot	=	Other
		ws	=	Widescreen Patch
	
	Regions:
		a	=	Region Free
		p	=	PAL
		u	=	USA
		j	=	JPN

	Below is a multi patch and region free patch
	Example:
		mp-a-toca race driver 3.pf

