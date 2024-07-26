# -*- coding: utf-8 -*-
### URLDownloading by Rocky5.
import extract, hashlib, math, os, requests, socket, struct, time, traceback

requests.packages.urllib3.disable_warnings(
	requests.packages.urllib3.exceptions.InsecureRequestWarning
)
from hmac import new
from urllib import quote
from xbmc import (
	executebuiltin,
	getLocalizedString,
	getInfoLabel,
	getCondVisibility,
	translatePath,
)
from xbmcgui import Dialog, DialogProgress

dialog = Dialog()
dprogress = DialogProgress()
working_directory = os.getcwd() + "/"

# Updated to new location
URLDownloader_Bin = "1jX2Y5wUHeT0-3hSAAfce3bI0xG7aOUoI~versions/URLDownloader.bin"
DownloadList_Bin = "1jKhRDRa-Enk9eev0jovhpFr6rnQbedf8~versions/DownloadList.bin"
URLDownloader_Zip = "1j568Tyojriizqflk3LGW4JUbEn4NuplD~updates/URLDownloader.zip"


def download_url(url):
	global StartTime
	StartTime = time.clock()
	if not os.path.exists(download_path):
		os.makedirs(download_path)
	download(
		url=str(url),
		dest_path=str(download_path + filename),
		zipsize=int(zipsize),
		filename=filename,
		showprogress=1,
	)


def download(url, dest_path, zipsize, filename, showprogress):
	global current_size
	global invalidlink
	global responsecode
	dprogress.update(0)
	httperrors4 = [
		"400 Bad Request",
		"401 Unauthorized",
		"402 Payment Required (Experimental)",
		"403 Forbidden",
		"404 Not Found",
		"405 Method Not Allowed",
		"406 Not Acceptable",
		"407 Proxy Authentication Required",
		"408 Request Timeout",
		"409 Conflict",
		"410 Gone",
		"411 Length Required",
		"412 Precondition Failed",
		"413 Request Entity Too Large",
		"414 Request-URI Too Long",
		"415 Unsupported Media Type",
		"416 Requested Range Not Satisfiable",
		"417 Expectation Failed",
		"418 I?m a teapot (RFC 2324)",
		"420 Enhance Your Calm (Twitter)",
		"422 Unprocessable Entity (WebDAV)",
		"423 Locked (WebDAV)",
		"424 Failed Dependency (WebDAV)",
		"425 Too Early (WebDAV)",
		"426 Upgrade Required",
		"428 Precondition Required",
		"429 Too Many Requests",
		"431 Request Header Fields Too Large",
		"444 No Response (Nginx)",
		"449 Retry With (Microsoft)",
		"450 Blocked by Windows Parental Controls (Microsoft)",
		"451 Unavailable For Legal Reasons",
		"499 Client Closed Request (Nginx)",
	]
	httperrors5 = [
		"500 Internal Server Error",
		"501 Not Implemented",
		"502 Bad Gateway",
		"503 Service Unavailable",
		"504 Gateway Timeout",
		"505 HTTP Version Not Supported (Experimental)",
		"506 Variant Also Negotiates (Experimental)",
		"507 Insufficient Storage (WebDAV)",
		"508 Loop Detected (WebDAV)",
		"510 Not Extended",
		"511 Network Authentication Required",
	]
	current_size = 0
	GDURL = "https://docs.google.com/uc?export=download"
	X4GURL = "https://www.xbmc4gamers.co.uk/X4G-XEmu/urldownloader/{}".format(quote(url.split("~")[1]))
	GDCode = url.split("~")[0]

	if filename == "Update":
		executebuiltin(
			"Skin.SetString(DisableProgress,Disabled)"
		)
		executebuiltin(
			"Skin.SetString(DisableCancel,Disabled)"
		)

	print("URLDownloader: Using GoogleDrive")

	if filename == "Update":
		dprogress.create(
			"CHECKING FOR UPDATE",
			"",
			"Please wait..."
		)
	else:
		dprogress.create(
			"Using GoogleDrive",
			filename.replace(".zip", ""),
			"Resolving link"
		)

	# Google Drive attempt
	# token = get_confirm_token(requests.Session().get(GDURL, params={'id': GDCode}, stream=True))
	token = "t"
	response = requests.Session().post(
		GDURL,
		headers={"User-Agent": "Mozilla/5.0"},
		params={"id": GDCode, "confirm": token},
		stream=True,
		verify=False,
	)

	# Google Drive status, if fails use XBMC4Gamers.co.uk
	if str(response.status_code).startswith("2"):
		save_response_content(
			response, dest_path, showprogress, current_size, zipsize, filename
		)
	else:
		if str(response.status_code).startswith("4"):
			for error in httperrors4:
				if error.startswith(str(response.status_code)):
					print("URLDownloader: GoogleDrive Failed: " + error)

		if str(response.status_code).startswith("5"):
			for error in httperrors5:
				if error.startswith(str(response.status_code)):
					print("URLDownloader: GoogleDrive Failed: " + error)

		print("URLDownloader: Falling back to www.xbmc4gamers.co.uk")

		if filename == "Update":
			dprogress.create(
				"CHECKING FOR UPDATE",
				"",
				"Please wait..."
			)
		else:
			dprogress.create(
				"Using XBMC4Gamers.co.uk",
				filename.replace(".zip", "")
			)

		# XBMC4Gamers.co.uk attempt time out if request is blocked
		timeout = 5
		max_retries = 5
		for _ in range(max_retries):
			if dprogress.iscanceled():
				break
			response = requests.Session().get(
				X4GURL,
				headers={"User-Agent": "Mozilla/5.0"},
				stream=True,
				verify=False,
			)

			if str(response.status_code).startswith("2"):
				save_response_content(
					response, dest_path, showprogress, current_size, zipsize, filename
				)

			if str(response.status_code).startswith("429"):
				timeoutcount = timeout
				for _ in range(timeout):
					dprogress.update(
						0,
						filename.replace(".zip", ""),
						"Retrying in: " + str(timeoutcount)
					)
					time.sleep(1)
					timeoutcount -= 1
					if dprogress.iscanceled():
						break
			else:
				break
			timeout += 5

	if str(response.status_code).startswith("4"):
		for error in httperrors4:
			if error.startswith(str(response.status_code)):
				responsecode = error
		invalidlink = 1
		raise Exception("Download Error: Both sites issue, couldn't download file")

	if str(response.status_code).startswith("5"):
		for error in httperrors5:
			if error.startswith(str(response.status_code)):
				responsecode = error
		invalidlink = 2
		raise Exception("Download Error: Both sites issue, couldn't download file")


def get_confirm_token(response):
	return response.text.startswith("<!DOCTYPE html>")


def save_response_content(response, dest_path, showprogress, current_size, zipsize, filename):
	percent = 1
	current_size = int(current_size)
	StartTime = time.clock()
	CHUNK_SIZE = 256 * 1024

	with open(dest_path, "wb") as f:
		for chunk in response.iter_content(CHUNK_SIZE):
			if chunk:  # filter out keep-alive new chunks
				f.write(chunk)

				if showprogress:
					percent = current_size * 101 / zipsize
					current_size += CHUNK_SIZE
					# calculate time renaming
					ElapsedTime = time.clock() - StartTime
					ChunksPerTime = current_size / ElapsedTime
					EstimatedTotalTime = zipsize / ChunksPerTime
					TimeLeftInSeconds = (EstimatedTotalTime - ElapsedTime) * 10 / 10 + 1  # adding + 1 makes it finish on 0 instead of being 0 with 1 second left
					TimeLeftInMinutes = TimeLeftInSeconds / 60
					TimeLeftInHours = TimeLeftInMinutes / 60

					if TimeLeftInHours >= 1:
						TimeLeft = "Estimated time left {} hour, {} minutes ".format(int(TimeLeftInHours),int(TimeLeftInMinutes) % 60)
					elif TimeLeftInMinutes >= 1:
						TimeLeft = "Estimated time left {} minutes, {} seconds".format(int(TimeLeftInMinutes) % 60,int(TimeLeftInSeconds) % 60)
					elif TimeLeftInSeconds < 60:
						TimeLeft = "Estimated time left {} seconds".format(int(TimeLeftInSeconds) % 60)

					# dprogress.update(percent,filename.replace('.zip',''),TimeLeft,"Downloaded: "+convert_size(current_size)+" at "+convert_size(CHUNK_SIZE)+"s")
					# dprogress.update(percent,filename.replace('.zip',''),TimeLeft,"Downloaded: "+convert_size(current_size))
					dprogress.update(
						percent,
						filename.replace(".zip", ""),
						TimeLeft
					)

					if dprogress.iscanceled():
						global allowcancellation
						allowcancellation = 1
						raise Exception("User cancelled download")


def extract_file(file, source_name, rename_stuff):
	if os.path.isfile(file):
		if not os.path.exists(translatePath(install_path)):
			os.makedirs(translatePath(install_path))

		dprogress.create(
			"INSTALLING",
			file.replace(".zip", "")
		)
		zippath = translatePath(install_path)
		dprogress.update(
			0,
			filename.replace(".zip", ""),
			"This may take some time, please be patient."
		)
		extract.all(file, zippath, source_name, rename_stuff, dprogress)


def download_update_check(url):
	download(
		url=str(url),
		dest_path=str(update_path + updatename),
		zipsize=int(0),
		filename="Update",
		showprogress=0,
	)


def clear_X():
	try:
		dprogress.create(
			"INITIALIZING"
		)
		dprogress.update(
			0,
			"Preparing Cache Partition",
			"This may take some time, please be patient."
		)
		for root, dirs, files in os.walk("X:/", topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))

	except Exception as error:
		traceback.print_exc()
		exceptiondata = traceback.format_exc().splitlines()
		exceptionarray = exceptiondata[1:-1]
		dialog.ok(
			"ERROR",
			"Clearing cache partitions failed.",
			exceptionarray
		)


def convert_size(size_bytes):

	if size_bytes == 0:
		return "0B"

	size_name = ("B", "KB", "MB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 1)
	return "%s %s" % (s, size_name[i].zfill(1))


def update_check():
	global updatename
	global urldinvalid
	global xmlinvalid
	xmlinvalid = 0
	urldinvalid = 0

	if not os.path.isfile("Z:/temp/URLDownloader.bin"):
		updatename = "URLDownloader.bin"
		download_update_check(str(URLDownloader_Bin))

		with open(os.path.join(working_directory, "version.bin"), "r") as verfile:
			local_version = verfile.readline().rstrip()

		with open("Z:/temp/URLDownloader.bin", "r") as verfile:
			urldversion = verfile.readline().rstrip()

		if int(local_version.replace(".", "")) < int(urldversion.replace(".", "")):
			os.remove("Z:/temp/URLDownloader.bin")
			urldinvalid = 1

	if not os.path.isfile("Z:/temp/DownloadList.bin"):
		updatename = "DownloadList.bin"
		download_update_check(str(DownloadList_Bin))

		with open("Z:/temp/DownloadList.bin", "r") as verfile:
			dlsversion = verfile.readline().rstrip()

		with open(
			translatePath("Special://skin/xml/_Script_URLDownloader.xml"), "rb"
		) as updatefile:
			udhashlibmd5.update(updatefile.read())

		if udhashlibmd5.hexdigest() != dlsversion:
			os.remove("Z:/temp/DownloadList.bin")
			xmlinvalid = 1

	dprogress.close()


def dash_update_check():
	# Updated check
	updatename = "updatecheck.bin"
	if "emustation" in getLocalizedString(31000).lower():
		if "test build" in getLocalizedString(31000).lower():
			with open("Z:/temp/" + updatename, "w") as UC:
				UC.write(
					getInfoLabel("Skin.String(TestBuild_Emustation_Server_Version)")
				)
		else:
			with open("Z:/temp/" + updatename, "w") as UC:
				UC.write(getInfoLabel("Skin.String(Stable_Emustation_Server_Version)"))
	else:
		if "test build" in getLocalizedString(31000).lower():
			with open("Z:/temp/" + updatename, "w") as UC:
				UC.write(getInfoLabel("Skin.String(TestBuild_Gamers_Server_Version)"))
		else:
			with open("Z:/temp/" + updatename, "w") as UC:
				UC.write(getInfoLabel("Skin.String(Stable_Gamers_Server_Version)"))
	dprogress.close()


def internet_check():
	try:
		_ = requests.head("http://google.com/", timeout=3)
	except requests.ConnectionError:
		raise Exception("No Interweb access. Please check your network settings")

def calculate_sha256(file_path):
	hash = hashlib.sha256()
	read_buffer = 1024 * 1024 * 5
	current_data = 0

	with open(file_path, "rb", buffering=read_buffer) as f:
		while True:
			data = f.read(read_buffer)
			hash.update(data)
			current_data += len(data)
			if not data:
				break
	
	return hash.hexdigest()

def dlc_hashing(titleid):
	hddkeybin = os.path.join(working_directory, "hdd-key.bin")
	hddkeytxt = "Special://xbmc/system/hdd-key.txt"
	filecount = 0
	readhddkey = 1
	countlist = 0
	dprogress.update(0)
	executebuiltin(
		"Skin.SetString(DisableProgress,Disabled)"
	)

	# Check for a txt/bin file with the hdd key or use the eeprom.
	if os.path.isfile(hddkeybin):
		readhddkey = 0
		hddkey = None

		with open(hddkeybin) as hex:
			hddkey = hex.readline()

		if len(hddkey) == 32:
			dprogress.create(
				"DLC INSTALLER",
				"Loading.",
				""
			)
			hddkey = bytearray.fromhex(hddkey)
		else:
			dprogress.create(
				"HDDKEY PROCESSING",
				"Loading",
				""
			)
			readhddkey = 1

	while readhddkey:
		key = getInfoLabel("system.hddlockkey")

		if len(key.strip()) < 32:
			for _ in range(3):
				dprogress.update(
					0,
					"Saving HDD Key",
					"."
				)
				time.sleep(0.5)
				dprogress.update(
					0,
					"Saving HDD Key",
					".."
				)
				time.sleep(0.5)
				dprogress.update(
					0,
					"Saving HDD Key",
					"..."
				)
				time.sleep(0.5)
		else:
			with open(hddkeybin, "w") as txteeprom:
				txteeprom.write(key.strip())
			hddkey = key.strip().decode("hex")
			break

	dprogress.update(
		0,
		"Signing ContextMeta.xbx",
		"This may take some time, please be patient."
	)
	executebuiltin(
		"Skin.SetString(DisableProgress,)"
	)

	for folder, subfolder, file in os.walk("E:/TDATA/" + titleid):
		filecount += len(file)

	for folder, subfolder, file in os.walk("E:/TDATA/" + titleid):

		for xbxfile in file:
			xbxfile = xbxfile.lower()

			if xbxfile == "contentmeta.xbx":
				contextmetafile = os.path.join(folder, xbxfile)
				filesize = os.path.getsize(contextmetafile)
				readxbx = open(contextmetafile, "r+b")
				# All DLC installed to HDD must have this byte set to 0x01. Must be done before signing to calculate the correct signature.
				# Credit to sinikal6969 for letting me know about this.
				readxbx.seek(32, 0)
				readxbx.write(bytearray.fromhex("01").decode())
				readxbx.seek(0, 0)
				filedata = readxbx.read(filesize)
				# Check the header fields.
				headersize = struct.unpack("I", filedata[24:28])[0]
				titleid = filedata[36:40]
				# Compute the HMAC key using the title id and HDD key.
				hmacKey = new(hddkey, titleid, hashlibsha1).digest()[0:20]
				# Compute the content signature.
				contentSignature = new(
					hmacKey, filedata[20:headersize], hashlibsha1
				).digest()[0:20]
				readxbx.seek(0, 0)
				readxbx.write(contentSignature)
				countlist = countlist + 1
				time.sleep(1)

			dprogress.update(
				(countlist * 100) / filecount,
				"Signing ContextMeta.xbx",
				"This may take some time, please be patient.",
			)
			countlist = countlist + 1


def call_exception(Exception):
	exception_type = type(error).__name__
	exception_message = str(error)
	stack_trace = traceback.format_exc().splitlines()

	exceptionarray = []
	exceptionarray.append(
		"An error of type {} occurred. Arguments:\n{}\n".format(exception_type, exception_message)
	)
	exceptionarray.append("Stack trace:")
	for line in stack_trace:
		exceptionarray.append("\t" + line)

	dialog.textviewer(
		"ERROR",
		"\n".join(exceptionarray)
	)

# Some variables Set outside the loop
re_focus_download_button = "9000"

try:
	# Check for Insignia DNS + 0.0.0.0
	if getInfoLabel('Network.DNS1Address') == "46.101.64.175" and getInfoLabel('Network.DNS2Address') == "0.0.0.0":
		raise Exception("Insignia DNS detected. You have not set a secondary DNS.")
	try:
		# Check for network/internet activity
		internet_check()
		executebuiltin(
			'Dialog.Close(1904,false)'
		)
		global httperrors
		httperrors = None
		global allowcancellation
		allowcancellation = 0
		global responsecode
		global invalidlink
		invalidlink = 0
		extensions = [ 'zip' ]
		download_path = 'X:/downloads/'
		update_path = 'Z:/temp/'
		udhashlibmd5 = hashlib.md5()
		hashlibsha1 = hashlib.sha1
		rename_stuff = ""
		source_name = ""
		dlcmode = 0
		skip = 0
		xawinstal = 0
		xmlinvalid = 0
		urldinvalid = 0
		
		# args passed from xml
		defaulturl = sys.argv[1] if len(sys.argv) > 1 else "1kENriKoSIVU_31LTerhsWIknndbfAjh7~updates/URLDownloader.zip"
		filename = sys.argv[2] if len(sys.argv) > 2 else "URLDownloader.zip"
		zipsize = sys.argv[3] if len(sys.argv) > 3 else "3055001"
		zipsizecheck = sys.argv[4] if len(sys.argv) > 4 else "3585632"
		install_path = sys.argv[5] if len(sys.argv) > 5 else "Q:/system/scripts/"
		mod_dlc_mode = sys.argv[6] if len(sys.argv) > 6 else ""
		
		valid_arguments = all([defaulturl, filename, zipsize, zipsizecheck])
		
		# vars
		if install_path == "Emulator_Folder_Path":

			if getCondVisibility('Skin.String(Custom_Emulator_Path)'):
				install_path = getInfoLabel('Skin.String(Custom_Emulator_Path)')
			else:
				install_path = ""
		
		if install_path == "Roms_Folder_Path":
			
			if getCondVisibility('Skin.String(Custom_Roms_Path)'):
				install_path	= getInfoLabel('Skin.String(Custom_Roms_Path)')
			else:
				install_path = ""
		
		if install_path == "Media_Folder_Path":
			
			if getCondVisibility('Skin.String(Custom_Media_Path)'):
				install_path = getInfoLabel('Skin.String(Custom_Media_Path)')
			else:
				install_path = ""
		
		if valid_arguments:

			# Create folders required so there is no errors
			if not os.path.exists( download_path ):
				os.makedirs(download_path)
			if not os.path.exists( update_path ):
				os.makedirs(update_path)

			# # Check file to see if there is an update for the dashboards.
			# if filename == "URLDownloader.zip":
				# dash_update_check()
			# else:
				# # Download the check file to see if there is an update. Doing it this way speeds up the loading after you download 1 files and the files are kept until a reboot.
				# try:
					# update_check()
					# executebuiltin(
						# 'Skin.SetString(DisableCancel,)'
					# )
					# executebuiltin(
						# 'Skin.SetString(DisableProgress,)'
					# )
				# except Exception as error:
					# executebuiltin(
						# 'Dialog.Close(1902,false)'
					# )
					# call_exception(error)
			
			# If hash doesn't match tell user to update, also if filename is the urldownloader.zip bypass.
			if xmlinvalid == 0 and urldinvalid == 0 or filename == "URLDownloader.zip" or getInfoLabel('Control.GetLabel(1)') == "Download Assets":
				# This is here to fix compatibility issues with previous builds.
				file = os.path.join(download_path,filename)
				
				# Truncate the filename to look cleaner and also get the titleid for DLC installation.
				if mod_dlc_mode == "DLC":
					titleid = filename[-12:]; titleid = titleid[:-4]
					filename = filename[:-13]+'.zip'
					file = os.path.join(download_path,filename)
					dlcmode = 1

				if install_path == "XAWI":
					xawinstal = 1
				
				if os.path.isfile(file):
					os.remove(file)
				
				if filename == "URLDownloader.zip" or dialog.yesno('DOWNLOAD','','{}[CR]Install size {}'.format(filename,convert_size(float(zipsize))),'',xbmc.getLocalizedString(106),xbmc.getLocalizedString(107)):

					try:
						if install_path == "C:\\":
							if os.path.isfile('C:\\xboxdash.xbe'):
								# this is the sha256 hash of the softmod xboxdash.xbe
								if calculate_sha256('C:\\xboxdash.xbe') == "3ae2f3eae3917e0130d1e1a5c8e1c5df207ea31703646a174d98f7be9a769495":
									source_name = getInfoLabel('Skin.String(downloader_label)')
									rename_stuff = "msdash"
									if not dialog.yesno(
										'WARNING: POTENTIAL SOFTMOD FOUND',
										"Would you like me to patch the files to ensure compatibility with the[CR]softmod? A shortcut to the new xb0xdash.xbe will be placed in the[CR]Applications folder."
										"",
										"",
										"",
										xbmc.getLocalizedString(106),
										xbmc.getLocalizedString(107)
									):
										raise Exception("WARNING: POTENTIAL SOFTMOD FOUND")
						
						if install_path == "":
							if getInfoLabel('Skin.String(dashboard_name)').lower() == 'xbmc4gamers' and 'emulators' in getInfoLabel('Skin.String(downloader_thumb)').lower():
								source_name = getInfoLabel('Skin.String(downloader_label)')
								rename_stuff = "emulator"
							
							install_path = dialog.browse(3,'Select destination folder','files','')
							
							if mod_dlc_mode == "MOD" and not install_path == "" and not os.path.isfile(os.path.join(install_path,'default.xbe')):
								dialog.ok(
									'ERROR',
									'Can not find a default.xbe',
									'Did you select the proper folder?'
								)
								install_path = 0

						if xawinstal: # If Xbox Artwork Installer Files process it
							if os.path.isfile('E:\\UDATA\\09999993\\location.bin'):
								with open('E:\\UDATA\\09999993\\location.bin','r') as input:
									install_path = input.readline().strip()
									if not os.path.isfile(os.path.join(install_path,"default.xbe")):
										install_path = "0"
										xawinstal = 2
							else:
								xawinstal = 2
						
						if install_path:
							
							try:
								free_space_check = install_path # Check for free space
								
								if free_space_check.startswith('Special:') or free_space_check.startswith('Q:'):
									free_space_check = translatePath('Special://root/')[:2]
								
								partition_free_space = getInfoLabel('System.Freespace({})'.format(free_space_check[:1])).replace(free_space_check[:2]+' ','').split(' ')[0]
								
								if int(partition_free_space)*1024*1024 > int(zipsizecheck)+(1024*1024*2):
									
									try:
										# clear_X()
										download_url(defaulturl)
										executebuiltin(
											'Skin.SetString(DisableCancel,Disabled)'
										) # Disable the cancel button
										
										try:
											extract_file(file,source_name,rename_stuff)
											os.remove(file)
											
											if dlcmode: # If DLC process the files
												dlc_hashing(titleid)
											
											executebuiltin(
												'Skin.SetString(DisableCancel,)'
											) # Enable the cancel button								
											
											check_filename = filename.lower()
											
											if check_filename == "xbox artwork installer.zip" or check_filename == "xbox artwork installer online.zip":
												if not os.path.isdir('E:\\UDATA\\09999993'):
													os.makedirs('E:\\UDATA\\09999993')
												with open('E:\\UDATA\\09999993\\location.bin','w') as input:
													if 'online' in check_filename.lower():
														input.write("{}Xbox Artwork Installer Online".format(install_path))
													else: input.write("{}Xbox Artwork Installer".format(install_path))
											
											if check_filename == "xbmc-emustation-update-files.zip" or check_filename == "xbmc-emustation-test-build.zip" and os.path.isfile(translatePath('Special://xbmc/updater/default.xbe')):
												dprogress.close()
												
												if dialog.yesno(
													'QUESTION',
													'',
													'Update the built-in emulators?[CR]This is optional and not required.',
													'',
													xbmc.getLocalizedString(106),
													xbmc.getLocalizedString(107)
												):
													with open(os.path.join(working_directory,'skip_emus.bin'), 'w') as tmp: tmp.write('')
												
												executebuiltin(
													'RunXBE({})'.format(translatePath('Special://xbmc/updater/default.xbe'))
												)
											
											elif check_filename == "xbmc4gamers-update-files.zip" or check_filename == "xbmc4gamers-test-build.zip" and os.path.isfile(translatePath('Special://xbmc/updater/default.xbe')):
												executebuiltin(
													'RunXBE({})'.format(translatePath('Special://xbmc/updater/default.xbe'))
												)
											
											elif check_filename == "cache formatter.zip" and os.path.isfile(translatePath('Special://xbmc/Cache Formatter/default.xbe')):
												executebuiltin(
													'RunXBE({})'.format(translatePath('Special://xbmc/Cache Formatter/default.xbe'))
												)
											
											elif check_filename == "urldownloader.zip" and os.path.isdir(translatePath('Special://xbmc/system/scripts/tmp/urldownloader')):
												executebuiltin(
													'RunScript({})'.format(translatePath('Special://xbmc/system/scripts/autoexec.py'))
												)

											else:
												dprogress.close()
												executebuiltin(
													'Dialog.Close(1902,false)'
												)
												dialog.ok(
													'SUCCESS',
													'',
													filename.replace('.zip','') + ' Installed'
												)
										
										except Exception as error:
											dprogress.close()
											call_exception(error)
									
									except Exception as error:
										executebuiltin(
											'Dialog.Close(1902,false)'
										)
										traceback.print_exc()
										
										if allowcancellation == 1:
											dprogress.close()
											dialog.ok(
												'DOWNLOADER',
												'',
												'You cancelled the download of',
												filename.replace('.zip','')
											)
										
										elif invalidlink == 1:
											dprogress.close()
											dialog.ok(
												'4xx: Client Error',
												str(responsecode),
												'File: '+filename,
												'Try again later.'
											)
										
										elif invalidlink == 2:
											dprogress.close()
											dialog.ok(
												'5xx: Server Error',
												str(responsecode),'File: '+filename,
												'This is a Server issue let me know ASAP.'
											)
										
										else:
											call_exception(error)
								else:
									dialog.ok(
										'ERROR',
										'',
										'Insufficient space on '+free_space_check
									)
							
							except Exception as error:
								call_exception(error)
								
								if xawinstal == 2:
									dprogress.close()
									executebuiltin(
										'Dialog.Close(1902,false)'
									)
									dialog.ok(
										'UH-OH',
										'',
										'Please download and/or run[CR]The Xbox Artwork installer at least once.',
										''
									)
						
						else:
							pass
				
					except Exception as error:
						dialog.ok(
							'WARNING: POTENTIAL SOFTMOD FOUND',
							"If this was/is a false positive, please fix or clean your C partition.[CR]It contains files that are used for softmods.[CR][CR]Please proceed with caution."
						)
					
				else:
					pass
			
			else:
				if xmlinvalid == 1 or urldinvalid == 1:
					dialog.ok(
						'UPDATE AVAILABLE',
						'Press (A) to update the',
						'[B]URLDownloader[/B]'
					)
					executebuiltin(
						'ActivateWindow(1904)'
					)
					executebuiltin(
						'RunScript(Special://urldownloader/default.py,{},URLDownloader.zip,2247055,2822733,Q:/system/scripts/)'.format(str(URLDownloader_Zip))
					)
		
		else:
			dialog.ok(
				'ERROR',
				'Corrupt _Script_URLDownloader.xml',
				'Update URLDownloader'
			)
			executebuiltin(
				'Dialog.Close(1902,false)'
			)
		
		try: # Used to zero the progress bar after everything is done
			dprogress.update(0)
		except:
			pass
		
		executebuiltin('SetFocus({})'.format(re_focus_download_button)) # Set focus to download button

	except Exception as ex:
		executebuiltin(
			'Dialog.Close(1904,false)'
		)
		dialog.ok(
			'ERROR: NETWORK CHECK FAILED',
			'No Internet access',
			'Please check your network settings'
		)
		executebuiltin(
			'SetFocus({})'.format(re_focus_download_button)
		)

except Exception as ex:
	executebuiltin(
		'Dialog.Close(1904,false)'
	)
	dialog.ok(
		'ERROR: INSIGNIA DNS DETECTED',
		'You have not set a secondary DNS.',
		'The downloader will not function without it set.'
	)
	executebuiltin(
		'SetFocus({})'.format(re_focus_download_button)
	)