"""
	-----------------------------------------------------------------------------------
	Inspiration/code from:	https://github.com/LoveMHz/XBEpy
	-----------------------------------------------------------------------------------
"""
import struct
from limpp import *


class xbeinfo:
	def __init__(self, data_file):
		with open(data_file, 'rb', buffering=3145728) as xbe: # <-- Buffer 3MB of data at a time
			xbe.seek(0)

			# Load XBE Header
			self.header = XBE_HEADER(xbe.read(376))  # <-- Read the relevant bytes for the XBE_HEADER

			# Load XBE Cert
			xbe.seek(self.header.dwCertificateAddr - self.header.dwBaseAddr)
			self.cert = XBE_CERT(xbe.read(388))  # <-- See the last XBE_CERT alternative signing key slice, don't need to use more space than necessary

			# Load XBE Section Headers and Section Names
			# self.sections = []
			for x in range(0, self.header.dwSections):
				# Load XBE Section Header
				xbe.seek(self.header.dwSectionHeadersAddr - self.header.dwBaseAddr + (56 * x))
				section = XBE_SECTION(xbe.read(56))  # <-- Read the sction information

				# Load XBE Section Name
				xbe.seek(section.dwSectionNameAddr - self.header.dwBaseAddr)
				section.name = struct.unpack('8s', xbe.read(8))[0].split("\x00")[0].rstrip()

				if section.name == '$$XTIMAG':
					# Hack to find the only section we care about, discarding the rest
					self.xbe_title_image = section

					# Load XBE section Data conditionally
					xbe.seek(section.dwRawAddr)
					section_data = xbe.read(section.dwSizeofRaw)
					section_data += '\x00' * (section.dwVirtualSize - len(section_data))  # This should pad the data to the correct length
					section.data = section_data

	def get_logo(self):
		return 0

	def image_png(self):
		if hasattr(self, 'xbe_title_image'):
			file_type = struct.unpack('4s', self.xbe_title_image.data[0:4])[0]

			with open( 'Z:\\TitleImage.xbx', "wb") as title_image:
				title_image.write(self.xbe_title_image.data)

			if file_type == 'XPR0':
				image = Get_image( file='Z:\\TitleImage.xbx' )
				image.Write_PNG( 'Z:\\default.png' )
	# print 'done'

class XBE_HEADER:
	def __init__(self, data):
		XOR_EP_DEBUG  = 0x94859D4B  # Entry Point (Debug)
		XOR_EP_RETAIL = 0xA8FC57AB  # Entry Point (Retail)
		XOR_KT_DEBUG  = 0xEFB1F152  # Kernel Thunk (Debug)
		XOR_KT_RETAIL = 0x5B6D40B6  # Kernel Thunk (Retail)

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


class XBE_CERT:
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


class XBE_SECTION:
	def __init__(self, data):
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