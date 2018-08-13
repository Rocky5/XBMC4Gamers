'''
	Edited to work with XBMC-Emustation and have vars passed to it for downloading files.
'''
import extract, fileinput, hashlib, hmac, logging, operator, os, requests, shutil, struct, time, traceback, urllib, urllib2, urlparse, xbmc, xbmcgui
dialog = xbmcgui.Dialog()
dprogress = xbmcgui.DialogProgress()
working_directory = os.getcwd() + '/'
def check_for_update(url):
	if not os.path.exists( update_path ): os.makedirs( update_path )
	path = os.path.join(update_path,url.split('/')[-1])
	download(url, path, dprogress)
def download_url(url):
	dprogress.create("DOWNLOADING","","Initializing")
	if not os.path.exists( download_path ): os.makedirs( download_path )
	path = os.path.join(download_path,url.split('/')[-1])
	dprogress.update(0,filename,"This can take some time, please be patient.")
	download(url, path, dprogress)
def download(url, dest, dprogress = None):
	dprogress.update(0)
	urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dprogress))
def _pbhook(numblocks, blocksize, filesize, url, dprogress):
	try:
		percent = min((numblocks*blocksize*100)/filesize, 100)
		dprogress.update(percent)
	except:
		percent = 100
		dprogress.update(percent)
	if dprogress.iscanceled():
		if allowcancellation == 1:	raise Exception("Canceled")
def extract_file(file):
	time.sleep(1)
	if not os.path.exists( xbmc.translatePath(destination) ): os.makedirs( xbmc.translatePath(destination) )
	dprogress.create("EXTRACTING","","Initializing")
	zippath = xbmc.translatePath(destination)
	dprogress.update(0,filename,"This can take some time, please be patient." )
	extract.all(file, zippath, dprogress)
	time.sleep(1)
def clear_X():
	try:
		dprogress.create("CACHE","","Initializing")
		for root, dirs, files in os.walk("X:/", topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
			dprogress.update(0,'', 'Prepping Cache')
			time.sleep(0.1)
	except:
		pass
# Used to check that you have internet access before letting you do anything.
try:
	urllib2.urlopen('http://www.xbmc-emustation.com', timeout=4)
	home_url = 'http://www.xbmc-emustation.com/downloads/'
	# args
	try:
		defaulturl = home_url + sys.argv[1:][0]
		md5hashurl = defaulturl[:-4] + ".md5"
		filename = defaulturl.split("/")[-1]
		exit = 1
	except:
		exit = 0
	try:
		destination = sys.argv[2:][0]
	except:
		destination = ""
	try:
		keyboardmode = sys.argv[3:][0]
	except:
		keyboardmode = ""
	if keyboardmode == "keyboard_mode":
		defaulturl = ''
		keyboard = xbmc.Keyboard('default', 'heading')
		keyboard.setDefault(defaulturl)
		keyboard.setHeading('Formating = URL,md5hash')
		xbmc.executebuiltin('Dialog.Close(1101,true)')
		keyboard.doModal()
		try:
			if (keyboard.isConfirmed()):
				defaulturl = keyboard.getText()
				if defaulturl.startswith('http://') or defaulturl.startswith('HTTP://'):
					pass
				elif defaulturl.startswith('https://') or defaulturl.startswith('HTTPS://'):
					pass
				elif defaulturl.startswith('ftp://') or defaulturl.startswith('FTP://'):
					pass
				else:
					defaulturl = 'http://'+defaulturl
				dprogress.create("REQUESTING URL","","Trying to resolve, please wait")
				dprogress.update(0)
				defaulturl = requests.head(defaulturl, allow_redirects=True).url
				dprogress.close()
				md5hash = defaulturl.split(",")[1]
				defaulturl = defaulturl.split(",")[0].replace('%20',' ')
				filename = defaulturl.split("/")[-1]
				exit = 1
			else:
				filename = ""
				exit = 0
		except Exception as err:
			print "Error 1:"; logging.error(traceback.format_exc())
			exit = 0
			dprogress.close()
			xbmcgui.Dialog().ok("ERROR","Could not resolve address","Please check you entered it correctly","Note: the server could also be offline")
	# vars
	if destination == "Emulator_Folder_Path":
		if xbmc.getCondVisibility( 'Skin.String(Custom_Emulator_Path)' ): destination = xbmc.getInfoLabel( 'Skin.String(Custom_Emulator_Path)' )
		else: destination = ""
	if destination == "Roms_Folder_Path":
		if xbmc.getCondVisibility( 'Skin.String(Custom_Roms_Path)' ): destination	= xbmc.getInfoLabel( 'Skin.String(Custom_Roms_Path)' )
		else: destination = ""
	if destination == "Media_Folder_Path":
		if xbmc.getCondVisibility( 'Skin.String(Custom_Media_Path)' ): destination = xbmc.getInfoLabel( 'Skin.String(Custom_Media_Path)' )
		else: destination = ""
	global allowcancellation
	allowcancellation = 0
	udhashlibmd5 = hashlib.md5()
	dlhashlibmd5 = hashlib.md5()
	hashlibsha1 = hashlib.sha1
	extensions = [ 'zip' ]
	download_path = 'X:/downloads/'
	update_path = 'Z:/temp/'
	dlcmode = 0
	xmlinvalid = 0
	urldinvalid = 0
	# Download the check file to see if there is an update. Doing it this way speeds up the loading after you download 1 files ad the files are kept until a reboot.
	if not os.path.isfile( 'Z:/temp/URLDownloader.bin' ):
		check_for_update( home_url + 'versions/URLDownloader.bin' )
		with open( working_directory + 'version.bin', 'r') as verfile:
			local_version = verfile.readline().rstrip()
		with open( 'Z:/temp/URLDownloader.bin', 'r') as verfile:
			urldversion = verfile.readline().rstrip()
		if int(local_version.replace(".","")) < int(urldversion.replace(".","")):
			os.remove( 'Z:/temp/URLDownloader.bin' )
			urldinvalid = 1
	if not os.path.isfile( 'Z:/temp/DownloadList.bin' ):
		check_for_update( home_url + 'versions/DownloadList.bin' )
		with open( 'Z:/temp/DownloadList.bin', 'r') as verfile:
			dlsversion = verfile.readline().rstrip()
		with open( xbmc.translatePath('Special://skin/720p/_Script_URLDownloader.xml'), "rb") as updatefile:
			udhashlibmd5.update( updatefile.read() )
		if udhashlibmd5.hexdigest() != dlsversion:
			os.remove( 'Z:/temp/DownloadList.bin' )
			xmlinvalid = 1
	# If hash doesn't match tell user to update, also if filename is the urldownloader.zip bypass.
	if xmlinvalid == 0 and urldinvalid == 0 or filename == "URLDownloader.zip" or xbmc.getInfoLabel('Control.GetLabel(1)') == "Download Assets":
		# This is here to fix compatibility issues with previous builds.
		file = os.path.join(download_path,filename)
		md5hashfile = file[:-4] + ".md5"
		# Truncate the filename to look cleaner and also get the titleid for DLC installation.
		if keyboardmode == "DLC":
			titleid = filename[-12:]; titleid = titleid[:-4]
			filename = filename[:-13]+'.zip'
			dlcmode = 1
		xbmc.executebuiltin('Dialog.Close(1101,true)')
		if os.path.isfile( file ):
			os.remove( file )
		if exit:
			if filename.endswith(tuple(extensions)):
				if dialog.yesno("URLDOWNLOADER","","Would you like to download[CR]" + filename):
					if destination == "":
						destination = dialog.browse( 3,"Select destination folder",'files','' )
						if keyboardmode == "MOD":
							if os.path.isfile( os.path.join( destination, 'default.xbe' ) ):
								pass
							else:
								dialog.ok("ERROR","Cant find a default.xbe","Did you select the proper folder?")
								destination = 0
					if destination:
						try:
							clear_X()
							allowcancellation = 1
							download_url( defaulturl )
							if keyboardmode != "keyboard_mode":
								download_url( md5hashurl )
								with open( md5hashfile, 'r') as md5file:
									md5hash = md5file.readline().rstrip()
								os.remove( md5hashfile )
							# Generate MD5 Hash from downloaded file.
							with open( file, "rb") as inputfile:
								percent = 0
								file_content = inputfile.read(1024*1024)
								dprogress.create("CHECKING CONSISTENCY","","Initializing")
								while file_content:
									dprogress.update(( percent * 100 ) / os.path.getsize( file ),"Calculating MD5 Hash","This can take some time, please be patient." )
									dlhashlibmd5.update( file_content )
									file_content = inputfile.read(1024*1024)
									percent = percent+1024*1024
							if md5hash == dlhashlibmd5.hexdigest():
								extract_file( file )
								os.remove( file )
								if dlcmode:
									dprogress.update(0)
									dprogress.create("DLC SIGNER","","Initializing" )
									# Had to use this while loop to get the HDD key as it will be Busy for a second or two.
									while True:
										key = xbmc.getInfoLabel('system.hddlockkey')
										time.sleep(1)
										if key != 'Busy':
											hddkey = key.decode('hex')
											filecount = 1
											countlist = 0
											break
									for folder, subfolder, file in os.walk('E:/TDATA/'+titleid):
										filecount += len(file)
									for folder, subfolder, file in os.walk('E:/TDATA/'+titleid):
										for xbxfile in file:
											xbxfile = xbxfile.lower()
											if xbxfile == "contentmeta.xbx":
												contextmetafile = os.path.join( folder, xbxfile )
												filesize = os.path.getsize(contextmetafile)
												readxbx = open(contextmetafile, 'r+b')
												filedata = readxbx.read(filesize)
												# Check the header fields.
												headersize = struct.unpack('I', filedata[24:28])[0]
												titleid = filedata[36:40]
												# Compute the HMAC key using the title id and HDD key.
												hmacKey = hmac.new(hddkey, titleid, hashlibsha1).digest()[0:20]
												# Compute the content signature.
												contentSignature = hmac.new(hmacKey, filedata[20:headersize], hashlibsha1).digest()[0:20]
												readxbx.seek(0,0)
												readxbx.write(contentSignature)
												countlist = countlist + 1
											dprogress.update(( countlist * 100 ) / filecount,"Signing ContextMeta.xbx","This can take some time, please be patient." )
											countlist = countlist + 1
								dprogress.close()
								if filename == "XBMC-Emustation-update-files.zip" or filename == "XBMC-Emustation-test-build.zip" and os.path.isfile( xbmc.translatePath('Special://xbmc/updater/default.xbe') ):
									xbmc.executebuiltin( 'RunXBE( ' + xbmc.translatePath( 'Special://xbmc/updater/default.xbe' ) + ')' )
								elif filename == "Cache Formatter.zip" and os.path.isfile( xbmc.translatePath('Special://xbmc/Cache Formatter/default.xbe') ):
									xbmc.executebuiltin( 'RunXBE( ' + xbmc.translatePath( 'Special://xbmc/Cache Formatter/default.xbe') + ')' )
								elif filename == "URLDownloader.zip" and os.path.isdir( xbmc.translatePath('Special://xbmc/system/scripts/tmp/urldownloader') ):
									xbmc.executebuiltin( 'RunScript( ' + xbmc.translatePath( 'Special://xbmc/system/scripts/autoexec.py') + ')' )
								else:
									dialog.ok("SUCCESS","",filename + " Installed")
							else:
								dprogress.close()
								dialog.ok("ERROR","MD5Hash Mismatch","Server Hash: " + md5hash,"Local Hash: " + dlhashlibmd5.hexdigest())
								os.remove( file )
						except Exception as err:
							print "Error 2:"; logging.error(traceback.format_exc())
							if dprogress.iscanceled():
								dprogress.close()
								dialog.ok("URLDOWNLOADER","You cancelled the download of",filename)
							else:
								dprogress.close()
								dialog.ok("ERROR","","Server or local network issue")
					else:
						pass
			else:
				dialog.ok("ERROR","Supported files",extensions)
		else:
			if keyboardmode == "": dialog.ok("ERROR","Missing required information.")
	else:
		xbmc.executebuiltin('Dialog.Close(1101,true)')
		xbmcgui.Dialog().ok("UPDATE AVAILABLE","Please update the","[B]URLDownloader[/B]")
except urllib2.URLError as err:
	print "Error 3:"; logging.error(traceback.format_exc())
	xbmc.executebuiltin('Dialog.Close(1101,true)')
	xbmcgui.Dialog().ok("ERROR","No network access","Please check your ethernet cable")