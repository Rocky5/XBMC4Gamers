import os, requests, time, warnings, xbmc, xbmcgui
class GoogleDriveDownloader:
	CHUNK_SIZE = 32768
	DOWNLOAD_URL = "https://docs.google.com/uc?export=download"
	@staticmethod
	def download_file_from_google_drive(file_id, dest_path, overwrite=False):
		destination_directory = os.path.dirname(dest_path)
		if not os.path.exists(destination_directory):
			makedirs(destination_directory)
		if not os.path.exists(dest_path) or overwrite:
			session = requests.Session()
			response = session.get(GoogleDriveDownloader.DOWNLOAD_URL, params={'id': file_id}, stream=True)
			token = GoogleDriveDownloader._get_confirm_token(response)
			if token:
				params = {'id': file_id, 'confirm': token}
				response = session.get(GoogleDriveDownloader.DOWNLOAD_URL, params=params, stream=True)
			GoogleDriveDownloader._save_response_content(response, dest_path)
	@staticmethod
	def _get_confirm_token(response):
		for key, value in response.cookies.items():
			if key.startswith('download_warning'):
				return value
		return None
	@staticmethod
	def _save_response_content(response, destination):
		with open(destination, 'wb') as f:
			for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
				if chunk:  # filter out keep-alive new chunks
					f.write(chunk)
### ---------------------------------------------------------------------------------
if xbmc.getInfoLabel('Skin.HasSetting(xbmc-emustation)'):
	releasebuild = "1r2lqgNXDIzWclXPh6Fmql2YqixJg1sWT"
	testbuild = "1fCozD6I8VZ_I7ZGAE6sWrQCmJ5L5jrOB"
elif xbmc.getInfoLabel('Skin.HasSetting(xbmc4gamers)'):
	releasebuild = "13n7qaptf57qtlPu-mmQRLSd6PxPpRliU"
	testbuild = "1f-fU6zWrCY1nqWcPTENKboxpLeXJy1k_"
download_path = 'Z:\\temp'
if not os.path.exists(download_path): os.makedirs(download_path)
xbmc.executebuiltin('Notification(Checking for updates,Please wait)')
try:
	if "test build" in xbmc.getLocalizedString(31000).lower():
		GoogleDriveDownloader.download_file_from_google_drive(file_id=testbuild, dest_path=os.path.join(download_path,"version.bin"), overwrite=True)
		with open(os.path.join(download_path,"version.bin"), 'r') as versioncheck:
			versioncheck = versioncheck.readline().rstrip()
		if int(xbmc.getLocalizedString(31000)[-7:].replace(".","")) < int(versioncheck.replace(".","")):
			xbmc.executebuiltin('Notification(New version is available,Test Build: '+versioncheck+')')
		else:
			xbmc.executebuiltin('Notification(Checking for updates,No new version found)')
	else:
		GoogleDriveDownloader.download_file_from_google_drive(file_id=releasebuild, dest_path=os.path.join(download_path,"version.bin"), overwrite=True)
		with open(os.path.join(download_path,"version.bin"), 'r') as versioncheck:
			versioncheck = versioncheck.readline().rstrip()
		if int(xbmc.getLocalizedString(31000)[-7:].replace(".","")) < int(versioncheck.replace(".","")):
			xbmc.executebuiltin('Notification(New version is available,Release Build: '+versioncheck+')')
		else:
			xbmc.executebuiltin('Notification(Checking for updates,No new version found)')
except:
	# internet aint working if you get here.
	xbmc.executebuiltin("Notification(Can't Reach Server,Please check your network)")