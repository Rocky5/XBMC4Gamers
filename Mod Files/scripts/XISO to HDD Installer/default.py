########################################################################################################################################
'''
	Script by Rocky5
	Used to prep a XISO so it can be playd from the Xbox HDD. It also extracts images and the xbe header so trainers work.
	
	Original script by headphone - http://www.emuxtras.net/forum/viewtopic.php?f=187&t=3228&start=40#p70178
'''
########################################################################################################################################

import binascii, io, os, shutil, string, struct, sys, time, xbmcgui, glob
from shutil import copyfile
from struct import unpack
from limpp import Get_image


pDialog = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
pDialog.update( 0 )
				
########################################################################################################################################
# Start markings for the log file.
########################################################################################################################################
print "================================================================================"
print "| Scripts\XISO to HDD Installer\default.py loaded."
print "| ------------------------------------------------------------------------------"


#-----------------------------------------------------------------------------------
#Inspiration/code from:	xbox360iso.py Copyright (c) 2014 Rob Lambell (MIT License)
#						xbiso.pl (c) 30/06/2004 codex(at)bogus.net
#						xboxsig.py Copyright (c) <2015> <Pete Stanley>
#-----------------------------------------------------------------------------------

def check_iso( iso_file ):
	iso_info = {}
	## check for validity
	iso_file.seek( 0x10000 )
	if iso_file.read( 0x14 ).decode( "ascii", "ignore" ) == 'MICROSOFT*XBOX*MEDIA':
		iso_info['sector_size'] = 0x800
		## read the directory table
		iso_file.seek( 0x10014 )
		iso_info['root_dir_sector'] = unpack('I', iso_file.read(4))[0] #dtable
		iso_info['root_dir_size'] = unpack('I', iso_file.read(4))[0]
		return iso_info
		iso_file.seek( 0x107ec ) # skip unused info
	elif iso_file.read( 0x14 ).decode( "ascii", "ignore" ) != 'MICROSOFT*XBOX*MEDIA':  # read tailend of header
		print( "FATAL: header tail mismatch -- possible corruption?" )
		print("FATAL: this doesn't appear to be an xbox iso image")
		return False

def extract_defaultxbe( iso_file, iso_info ):
	#seek to root sector
	iso_file.seek( ( iso_info[ 'root_dir_sector' ] * iso_info[ 'sector_size' ] ) )
	
	# read the root sector into a bytes object
	root_sector_buffer = io.BytesIO()
	root_sector_buffer.write( iso_file.read( iso_info[ 'root_dir_size' ] ) )
	root_sector_buffer.seek(0)
	
	# case insensitive search of root sector for default.xbe
	for i in range( 0, iso_info[ 'root_dir_size' ] - 12 ):
		root_sector_buffer.seek( i )
		root_sector_buffer.read( 1 )  # file_attribute
		
		if struct.unpack( '<' + 'B'*1, root_sector_buffer.read( 1 ) )[ 0 ] == 11:
			if root_sector_buffer.read( 11 ).decode( "ascii", "ignore" ).lower() == "default.xbe":
			
				# found default.xbe
				root_sector_buffer.seek( i - 8 )
				file_sector = unpack( 'I', root_sector_buffer.read( 4 ) )[ 0 ]
				file_size	= unpack( 'I', root_sector_buffer.read( 4 ) )[ 0 ]
				file_size	= file_size / 2
				
				# seek to default.xbe
				iso_file.seek( file_sector * iso_info[ 'sector_size' ] )
				
				# write default.xbe to a file
				# Could probably just keep this in memory in the future when I fix this mess...
				f = open( os.path.join( ISO_Directory,"default.xbe" ),"wb" )
				f.write( iso_file.read( file_size ) )
				f.close()
				# Had to split the xbe in half so the Xbox doesn't run out of memory.
				iso_file.seek( file_sector * iso_info[ 'sector_size' ] + file_size )
				f = open( os.path.join( ISO_Directory,"default.xbe" ),"wb" )
				f.seek( file_size )
				f.write( iso_file.read( file_size ) )
				f.close()
				
				# dump the xbe quarterly, but I don't use this, may come in handy if there is a huge xbe file.
				'''
				file_size	= file_size / 4
				
				# seek to default.xbe
				iso_file.seek( file_sector * iso_info[ 'sector_size' ] )
				
				# write default.xbe to a file
				# Could probably just keep this in memory in the future when I fix this mess...
				# Had to split the xbe in quarters so the Xbox doesn't run out of memory.
				f = open( os.path.join( ISO_Directory,"default.xbe" ),"wb" )
				f.write( iso_file.read( file_size ) )
				f.close()
				iso_file.seek( file_sector * iso_info[ 'sector_size' ] + file_size )
				f = open( os.path.join( ISO_Directory,"default.xbe" ),"wb" )
				f.seek( file_size )
				f.write( iso_file.read( file_size ) )
				f.close()
				iso_file.seek( file_sector * iso_info[ 'sector_size' ] + file_size + file_size )
				f = open( os.path.join( ISO_Directory,"default.xbe" ),"wb" )
				f.seek( file_size + file_size )
				f.write( iso_file.read( file_size ) )
				f.close()
				iso_file.seek( file_sector * iso_info[ 'sector_size' ] + file_size + file_size + file_size )
				f = open( os.path.join( ISO_Directory,"default.xbe" ),"wb" )
				f.seek( file_size + file_size + file_size )
				f.write( iso_file.read( file_size ) )
				f.close()
				'''

def prepare_attachxbe( iso_filename ):
	iso_name	= os.path.splitext( os.path.basename( iso_filename ) )[0]
	iso_folder_name	= (iso_name[:36]) if len(iso_name) > 36 else iso_name # truncate the name to 42 characters, reason is the .iso.
	iso_folder		= os.path.join( ISO_Directory, iso_folder_name + ' (ISO)' )
	
	
	print iso_folder

	copyfile( os.path.join( intial_dir,"attach.xbe" ), os.path.join( iso_folder,"attach.xbe" ) )

	## DEFAULT XBE TITLE
	default_xbe_file = open( os.path.join( ISO_Directory,'default.xbe' ),'rb' )

	#move to base address
	default_xbe_file.seek( 260, 0 )
	base = default_xbe_file.read( 4 )

	#move to cert address
	default_xbe_file.seek( 280, 0 )
	cert = default_xbe_file.read( 4 )

	#get the location of the cert
	certAddress = unpack( "i", cert ) # init32 values
	baseAddress = unpack( "i", base ) # init32 values
	loc = certAddress[0] - baseAddress[0]

	#move to the titleid
	default_xbe_file.seek( loc + 8, 0 )
	xbe_certificate = default_xbe_file.read( 168 )
	default_xbe_file.close()
	
	##
	# I'm not too worried about reuising all these vars...
	# ATTACH XBE FILE
	attach_xbe_file = open( os.path.join( iso_folder,'attach.xbe' ), 'r+b' )

	#move to base address
	attach_xbe_file.seek( 260, 0 )
	base = attach_xbe_file.read( 4 )

	#move to cert address
	attach_xbe_file.seek(  280, 0)
	cert = attach_xbe_file.read( 4 )

	#get the location of the cert
	certAddress = unpack( "i", cert ) # init32 values
	baseAddress = unpack( "i", base ) # init32 values
	loc = certAddress[0] - baseAddress[0]

	#move to the titleid
	attach_xbe_file.seek( loc + 8, 0 )
	attach_xbe_file.write( xbe_certificate )
	attach_xbe_file.close()
	##
	try: # this is to move on if there is an error with extracting the image.
		XBE( os.path.join( ISO_Directory,"default.xbe" ) ).image_png()
		os.remove( os.path.join( ISO_Directory,"TitleImage.xbx" ) )
		shutil.move( os.path.join( ISO_Directory,"default.png" ),os.path.join( iso_folder,"default.tbn" ) )
		shutil.copy2( os.path.join( iso_folder,"default.tbn" ),os.path.join( iso_folder,"icon.png" ) )
	except:
		print "| Error: Cannot extract the Titleimage.xbx, haven't a clue why"
	if os.path.isfile( os.path.join( ISO_Directory,"default.xbe" ) ): os.remove( os.path.join( ISO_Directory,"default.xbe" ) )
	shutil.move( os.path.join( iso_folder,"attach.xbe" ),os.path.join( iso_folder,"default.xbe" ) )

def search_tree():
	CountList = 1
	for Item in sorted( os.listdir( ISO_Directory ) ):
		if os.path.isfile( os.path.join( ISO_Directory, Item ) ):
			if Item.lower().endswith( ( '.iso' ) ) :
				current_iso = os.path.join( ISO_Directory, Item )

				# progress bar
				if CountList == 1:
					pDialog.create( "XISO to HDD Installer" )
					pDialog.update( 0 )
					time.sleep(0.7)
				pDialog.update( ( CountList * 100 ) / len( os.listdir( ISO_Directory ) ),"Scanning XISO Files",Item,ISO_Directory )

				iso_file = open( current_iso, 'rb' ) # open iso
				iso_info = check_iso( iso_file ) # check iso is an xbox game and record some details
				if iso_info is False: # doesn't work, if no xbe files is found inside the xiso. (yeah I was testing and forgot the xbe lol)
					iso_file.close()
				extract_defaultxbe( iso_file, iso_info ) # find and extract default.xbe from the iso
				iso_file.close() # close iso
				iso_name		= os.path.splitext( os.path.basename( current_iso ) )[0] # make a new folder for the current game
				iso_folder_name	= (iso_name[:36]) if len(iso_name) > 36 else iso_name # truncate the name to 42 characters, reason is the .iso.
				iso_folder		= os.path.join( ISO_Directory, iso_folder_name + ' (ISO)' )
				os.mkdir(iso_folder)
				
				try:
					# Patch the title + id into attach.xbe...
					prepare_attachxbe( current_iso )
					# Move the game ISO to its own folder!
					shutil.move( current_iso, iso_folder )
					CountList = CountList + 1
				except:
					pDialog.close()
					shutil.rmtree( iso_folder )
					print "ERROR 2 : Not a valid XISO?"
					print "ERROR 2 : Could not extract the Default.xbe"
					dialog.ok( "ERROR: 2 ","Not a valid XISO?","Could not extract the [B]Default.xbe[/B]",current_iso )

'''
	-----------------------------------------------------------------------------------
	Inspiration/code from:	https://github.com/LoveMHz/XBEpy
	-----------------------------------------------------------------------------------
'''			
class XBE:
	m_file = None

	def __init__(self, file):
		self.m_file = open(file, 'rb').read()

		# Load XBE Header
		self.header = XBE_HEADER(self.m_file)
		self.cert	= XBE_CERT(self.m_file[self.header.dwCertificateAddr - self.header.dwBaseAddr:len(self.m_file)])

		# Load XBE Section Headers
		self.sections = []
		for x in range(0, self.header.dwSections):
			self.sections.append(XBE_SECTION(self.m_file[self.header.dwSectionHeadersAddr - self.header.dwBaseAddr + (x * 56):len(self.m_file)], self.m_file))

		# Load XBE Section Names
		for section in self.sections:
			section.name = struct.unpack('8s', self.m_file[section.dwSectionNameAddr - self.header.dwBaseAddr:
														   section.dwSectionNameAddr - self.header.dwBaseAddr + 8])[0].split("\x00")[0].rstrip()


	def get_logo(self):
		return 0

	def image_png(self):
		for section in self.sections:
			if section.name == '$$XTIMAG':
				data = section.data
				type = struct.unpack('4s', data[0:4])[0]

				newFile = open( ISO_Directory + 'TitleImage.xbx', "wb")
				# write to file
				newFile.write(data)
				newFile.close()

				if type == 'XPR0':
					image = Get_image( file=ISO_Directory + 'TitleImage.xbx' )
					image.Write_PNG( ISO_Directory + 'default.png' )
		print 'done';

class XBE_HEADER():
	def __init__(self, data):
		XOR_EP_DEBUG  = 0x94859D4B # Entry Point (Debug)
		XOR_EP_RETAIL = 0xA8FC57AB # Entry Point (Retail)
		XOR_KT_DEBUG  = 0xEFB1F152 # Kernel Thunk (Debug)
		XOR_KT_RETAIL = 0x5B6D40B6 # Kernel Thunk (Retail)

		self.dwMagic					   = struct.unpack('4s', data[0:4])[0]		# Magic number [should be "XBEH"]
		self.pbDigitalSignature			   = struct.unpack('256B', data[4:260])	   # Digital signature
		self.dwBaseAddr					   = struct.unpack('I', data[260:264])[0]  # Base address
		self.dwSizeofHeaders			   = struct.unpack('I', data[264:268])[0]  # Size of headers
		self.dwSizeofImage				   = struct.unpack('I', data[268:272])[0]  # Size of image
		self.dwSizeofImageHeader		   = struct.unpack('I', data[272:276])[0]  # Size of image header
		self.dwTimeDate					   = struct.unpack('I', data[276:280])[0]  # Timedate stamp
		self.dwCertificateAddr			   = struct.unpack('I', data[280:284])[0]  # Certificate address
		self.dwSections					   = struct.unpack('I', data[284:288])[0]  # Number of sections
		self.dwSectionHeadersAddr		   = struct.unpack('I', data[288:292])[0]  # Section headers address

		# Struct init_flags
		self.dwInitFlags				   = struct.unpack('I', data[292:296])[0]  # Mount utility drive flag
		self.init_flags_mount_utility_drive	 = None # Mount utility drive flag
		self.init_flags_format_utility_drive = None # Format utility drive flag
		self.init_flags_limit_64mb			 = None # Limit development kit run time memory to 64mb flag
		self.init_flags_dont_setup_harddisk	 = None # Don't setup hard disk flag
		self.init_flags_unused				 = None # Unused (or unknown)
		self.init_flags_unused_b1			 = None # Unused (or unknown)
		self.init_flags_unused_b2			 = None # Unused (or unknown)
		self.init_flags_unused_b3			 = None # Unused (or unknown)

		self.dwEntryAddr				   = struct.unpack('I', data[296:300])[0]  # Entry point address
		self.dwTLSAddr					   = struct.unpack('I', data[300:304])[0]  # TLS directory address
		self.dwPeStackCommit			   = struct.unpack('I', data[304:308])[0]  # Size of stack commit
		self.dwPeHeapReserve			   = struct.unpack('I', data[308:312])[0]  # Size of heap reserve
		self.dwPeHeapCommit				   = struct.unpack('I', data[312:316])[0]  # Size of heap commit
		self.dwPeBaseAddr				   = struct.unpack('I', data[316:320])[0]  # Original base address
		self.dwPeSizeofImage			   = struct.unpack('I', data[320:324])[0]  # Size of original image
		self.dwPeChecksum				   = struct.unpack('I', data[324:328])[0]  # Original checksum
		self.dwPeTimeDate				   = struct.unpack('I', data[328:332])[0]  # Original timedate stamp
		self.dwDebugPathnameAddr		   = struct.unpack('I', data[332:336])[0]  # Debug pathname address
		self.dwDebugFilenameAddr		   = struct.unpack('I', data[336:340])[0]  # Debug filename address
		self.dwDebugUnicodeFilenameAddr	   = struct.unpack('I', data[340:344])[0]  # Debug unicode filename address
		self.dwKernelImageThunkAddr		   = struct.unpack('I', data[344:348])[0]  # Kernel image thunk address
		self.dwNonKernelImportDirAddr	   = struct.unpack('I', data[348:352])[0]  # Non kernel import directory address
		self.dwLibraryVersions			   = struct.unpack('I', data[352:356])[0]  # Number of library versions
		self.dwLibraryVersionsAddr		   = struct.unpack('I', data[356:360])[0]  # Library versions address
		self.dwKernelLibraryVersionAddr	   = struct.unpack('I', data[360:364])[0]  # Kernel library version address
		self.dwXAPILibraryVersionAddr	   = struct.unpack('I', data[364:368])[0]  # XAPI library version address
		self.dwLogoBitmapAddr			   = struct.unpack('I', data[368:372])[0]  # Logo bitmap address
		self.dwSizeofLogoBitmap			   = struct.unpack('I', data[372:376])[0]  # Logo bitmap size

		self.dwEntryAddr_f				   = self.dwEntryAddr ^ XOR_EP_RETAIL	   # Entry point address


class XBE_CERT():
	def __init__(self, data):
		self.dwSize						   = struct.unpack('I', data[0:4])[0]	   # 0x0000 - size of certificate
		self.dwTimeDate					   = struct.unpack('I', data[4:8])[0]	   # 0x0004 - timedate stamp
		self.dwTitleId					   = struct.unpack('I', data[8:12])[0]	   # 0x0008 - title id
		self.wszTitleName				   = struct.unpack('40s', data[12:52])[0]  # 0x000C - title name (unicode)
		self.dwAlternateTitleId			   = struct.unpack('16B', data[52:68])	   # 0x005C - alternate title ids
		self.dwAllowedMedia				   = struct.unpack('I', data[68:72])[0]	   # 0x009C - allowed media types
		self.dwGameRegion				   = struct.unpack('I', data[72:76])[0]	   # 0x00A0 - game region
		self.dwGameRatings				   = struct.unpack('I', data[80:84])[0]	   # 0x00A4 - game ratings
		self.dwDiskNumber				   = struct.unpack('I', data[84:88])[0]	   # 0x00A8 - disk number
		self.dwVersion					   = struct.unpack('I', data[92:96])[0]	   # 0x00AC - version
		self.bzLanKey					   = struct.unpack('16B', data[100:116])   # 0x00B0 - lan key
		self.bzSignatureKey				   = struct.unpack('16B', data[116:132])   # 0x00C0 - signature key
		self.bzTitleAlternateSignatureKey  = [									   # 0x00D0 - alternate signature keys
			struct.unpack('16B', data[132:148]),
			struct.unpack('16B', data[148:164]),
			struct.unpack('16B', data[164:180]),
			struct.unpack('16B', data[180:196]),
			struct.unpack('16B', data[196:212]),
			struct.unpack('16B', data[212:228]),
			struct.unpack('16B', data[228:244]),
			struct.unpack('16B', data[244:260]),
			struct.unpack('16B', data[260:276]),
			struct.unpack('16B', data[276:292]),
			struct.unpack('16B', data[292:308]),
			struct.unpack('16B', data[308:324]),
			struct.unpack('16B', data[324:340]),
			struct.unpack('16B', data[340:356]),
			struct.unpack('16B', data[356:372]),
			struct.unpack('16B', data[372:388])
		]

		# Title name cleanup
		self.wszTitleName = self.wszTitleName.decode('utf-16')


class XBE_SECTION(XBE):
	def __init__(self, data, data_file):
		self.name = None
		self.data = None

		# Header
		self.dwFlags					= struct.unpack('I', data[0:4])[0]	  # Virtual address
		self.flag_bWritable				= struct.unpack('I', data[0:4])[0]	  # writable flag
		self.flag_bPreload				= struct.unpack('I', data[0:4])[0]	  # preload flag
		self.flag_bExecutable			= struct.unpack('I', data[0:4])[0]	  # executable flag
		self.flag_bInsertedFile			= struct.unpack('I', data[0:4])[0]	  # inserted file flag
		self.flag_bHeadPageRO			= struct.unpack('I', data[0:4])[0]	  # head page read only flag
		self.flag_bTailPageRO			= struct.unpack('I', data[0:4])[0]	  # tail page read only flag
		self.flag_Unused_a1				= struct.unpack('I', data[0:4])[0]	  # unused (or unknown)
		self.flag_Unused_a2				= struct.unpack('I', data[0:4])[0]	  # unused (or unknown)
		self.flag_Unused_b1				= struct.unpack('I', data[0:4])[0]	  # unused (or unknown)
		self.flag_Unused_b2				= struct.unpack('I', data[0:4])[0]	  # unused (or unknown)
		self.flag_Unused_b3				= struct.unpack('I', data[0:4])[0]	  # unused (or unknown)

		self.dwVirtualAddr				= struct.unpack('I', data[4:8])[0]	  # Virtual address
		self.dwVirtualSize				= struct.unpack('I', data[8:12])[0]	  # Virtual size
		self.dwRawAddr					= struct.unpack('I', data[12:16])[0]  # File offset to raw data
		self.dwSizeofRaw				= struct.unpack('I', data[16:20])[0]  # Size of raw data
		self.dwSectionNameAddr			= struct.unpack('I', data[20:24])[0]  # Section name addr
		self.dwSectionRefCount			= struct.unpack('I', data[24:28])[0]  # Section reference count
		self.dwHeadSharedRefCountAddr	= struct.unpack('I', data[28:32])[0]  # Head shared page reference count address
		self.dwTailSharedRefCountAddr	= struct.unpack('I', data[32:36])[0]  # Tail shared page reference count address
		self.bzSectionDigest			= struct.unpack('20B', data[36:56])	  # Section digest

		# Section Data
		self.data  = data_file[self.dwRawAddr:self.dwRawAddr + self.dwSizeofRaw]
		self.data += '\x00' * (self.dwVirtualSize - len(self.data))


class XBE_LIB(XBE):
	def __init__(self):
		print('wtf')


class XBE_TLS(XBE):
	def __init__(self):
		print('wtf')

################################################################################################################################
################################################################################################################################
		
intial_dir	= os.getcwd()
ISO_Found = "False"
Root_Directory = dialog.browse( 0,"Select a folder","files" )

for Items in sorted( glob.glob( Root_Directory + "*.iso" ) ):
	if os.path.isfile( Items ):
		ISO_Directory = Root_Directory		
		ISO_Found = "True"
	
try:
	if ISO_Found == "True":
		try:		
			search_tree()
			pDialog.close()
			dialog.ok( "XISO to HDD Installer","","Everything is setup, just launch the game like any other game." )
		except:
			pDialog.close()
			print "ERROR: Some shit went wrong!"
			dialog.ok( "ERROR:","",'Some shit went wrong!\nlast entry = ' + Items )
except:
	pass

print "================================================================================"