'''
	Used to check for updates and notify the user.
'''
import os, time, urllib, urllib2, xbmc, xbmcgui
dialog = xbmcgui.Dialog()
try:
	home_url = 'http://www.xbmc-emustation.com/downloads/'
	download_path = 'Z:\\temp\\'
	if not os.path.exists( download_path ): os.makedirs( download_path )
	if not os.path.isfile(os.path.join(download_path,"version.bin")):
		if "Test Build" in xbmc.getLocalizedString(31000):
			urllib.urlretrieve(home_url + "/versions/TestBuildGamers.bin",os.path.join(download_path,"version.bin"))
			xbmc.executebuiltin('Notification(Checking for updates,Current version ' + xbmc.getLocalizedString(31000)[-7:] + ')')
			if os.path.isfile( os.path.join(download_path,"version.bin") ):
				with open( os.path.join(download_path,"version.bin"), 'r') as versioncheck:
					versioncheck = versioncheck.readline().rstrip()
				if int(xbmc.getLocalizedString(31000)[-7:].replace(".","")) < int(versioncheck.replace(".","")):
					xbmcgui.Dialog().ok("NOTICE","","New version has been found[CR]Test Build: "+versioncheck)
				else:
					xbmc.executebuiltin('Notification(Checking for updates,No new version found)')
		else:
			urllib.urlretrieve(home_url + "/versions/ReleaseGamers.bin",os.path.join(download_path,"version.bin"))
			xbmc.executebuiltin('Notification(Checking for updates,Current version ' + xbmc.getLocalizedString(31000)[-7:] + ')')
			if os.path.isfile( os.path.join(download_path,"version.bin") ):
				with open( os.path.join(download_path,"version.bin"), 'r') as versioncheck:
					versioncheck = versioncheck.readline().rstrip()
				if int(xbmc.getLocalizedString(31000)[-7:].replace(".","")) < int(versioncheck.replace(".","")):
					xbmcgui.Dialog().ok("NOTICE","","New version has been found[CR]Release Build: "+versioncheck)
				else:
					xbmc.executebuiltin('Notification(Checking for updates,No new version found)')
except: pass