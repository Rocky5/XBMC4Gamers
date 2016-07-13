# Script by Rocky5
# This will replace the Filezilla Server.xml if it becomes corrupt, to stop hanging when entering "Programs,Games".
# I also increased the user count to 99 and made the timeout a lot longer.

import os
import xbmc
import shutil

# Set file variables.
backup = xbmc.translatePath( "special://xbmc/system/backup/FileZilla Server.xml" )
original = xbmc.translatePath( "special://xbmc/system/FileZilla Server.xml" )

# Get file sizes.
backupsize = os.path.getsize(backup)
originalsize = os.path.getsize(original)

# Set output directory.
destination = xbmc.translatePath( "special://xbmc/system/" )

if backupsize == originalsize:
	print "==================================="
	print "= Filezilla Server.xml is working ="
	print "==================================="
else:
	shutil.copy2(backup, destination)
	print "====================================================================================="
	print "= Filezilla Server.xml was corrupt.", "I fixed that by replacing it with the backup ="
	print "====================================================================================="
