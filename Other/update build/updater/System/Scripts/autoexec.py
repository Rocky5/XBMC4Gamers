import fileinput, os, shutil, time, xbmc, xbmcgui, zipfile
Root_Directory	= xbmc.translatePath("Special://root/")[:-8]
zip_file = os.path.join(Root_Directory, 'updater/Update Files/update-files.zip')
xbmc.executebuiltin('Skin.SetString(DashboardUpdatedSmall,0)')
xbmc.executebuiltin('Skin.Reset(DashboardUpdated)')
pDialog	= xbmcgui.DialogProgress()
dialog	= xbmcgui.Dialog()
if os.path.isfile(zip_file):
	pDialog.create('Stage 2 of 2')
	pDialog.update(0,"Download complete","Updating dashboard")
## Update folder names and remove old crap no longer needed
	# Update older backup to backups
	if os.path.isdir(Root_Directory+'system/backups') and os.path.isdir(Root_Directory+'system/backup'):
		shutil.rmtree(Root_Directory+'system/backup')
	elif os.path.isdir(Root_Directory+'system/backup'):
		os.rename(Root_Directory+'system/backup', Root_Directory+'system/backups')
	# Update older .modules to _modules
	if os.path.isdir(Root_Directory+'system/scripts/.modules'):
		os.rename(Root_Directory+'system/scripts/.modules', Root_Directory+'system/scripts/_modules')
	# Remove old folders or files that are no longer needed.
	if os.path.isdir(Root_Directory+'system/toggles'):
		shutil.rmtree(Root_Directory+'system/toggles')
	if os.path.isdir(Root_Directory+'skins/Manage Profiles Skin/720p'):
		shutil.rmtree(Root_Directory+'skins/Manage Profiles Skin/720p')
	if os.path.isdir(Root_Directory+'skins/Profile Skin/720p'):
		shutil.rmtree(Root_Directory+'skins/Profile Skin/720p')
	if os.path.isdir(Root_Directory+'skins/Profile Skin/media/backgrounds'):
		shutil.rmtree(Root_Directory+'skins/Profile Skin/media/backgrounds')
	if os.path.isdir(Root_Directory+'skins/Profile Skin/extras/splashes') and not os.path.isdir(Root_Directory+'skins/Profile Skin/extras/themes/splashes'):
		shutil.move(Root_Directory+'skins/Profile Skin/extras/splashes',Root_Directory+'skins/Profile Skin/extras/themes/splashes')
	else:
		if os.path.isdir(Root_Directory+'skins/Profile Skin/extras/splashes'):
			shutil.rmtree(Root_Directory+'skins/Profile Skin/extras/splashes')
	if os.path.isfile(Root_Directory+'system/scripts/XBMC4Gamers/Utilities/dialog res check.py'):
		os.remove(Root_Directory+'system/scripts/XBMC4Gamers/Utilities/dialog res check.py')
	if os.path.isdir(Root_Directory+'skins/Manage Profiles Skin/xml'):
		if os.path.isfile(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Snow.xml'):
			os.remove(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Snow.xml')
		if os.path.isfile(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Birthday.xml'):
			os.remove(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Birthday.xml')
		if os.path.isfile(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Easter.xml'):
			os.remove(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Easter.xml')
		if os.path.isfile(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Particles.xml'):
			os.remove(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Particles.xml')
	if os.path.isdir(Root_Directory+'skins/Profile Skin/xml'):
		if os.path.isfile(Root_Directory+'skins/Profile Skin/xml/Custom_View_Options.xml'):
			os.remove(Root_Directory+'skins/Profile Skin/xml/Custom_View_Options.xml')
		for viewfile in os.listdir(os.path.join(Root_Directory,'skins/Profile Skin/xml')):
			if viewfile.startswith('Viewtype_View'):
				os.remove(os.path.join(Root_Directory,'skins/Profile Skin/xml',viewfile))
	if os.path.isdir(Root_Directory+'skins/Profile Skin/media/disc artwork'):
		shutil.rmtree(Root_Directory+'skins/Profile Skin/media/disc artwork')
	if os.path.isdir(Root_Directory+'skins/Profile Skin/media/folder fanart'):
		if os.path.isdir(Root_Directory+'skins/Profile Skin/extras/folder fanart'):
			shutil.rmtree(Root_Directory+'skins/Profile Skin/extras/folder fanart')
		shutil.copytree(Root_Directory+'skins/Profile Skin/media/folder fanart',Root_Directory+'skins/Profile Skin/extras/folder fanart')
		shutil.rmtree(Root_Directory+'skins/Profile Skin/media/folder fanart')
	if os.path.isdir('E:/TDATA/Rocky5 needs these Logs'):
		for file in os.listdir('E:/TDATA/Rocky5 needs these Logs/'):
			if file.endswith('.log'):
				os.remove(os.path.join('E:/TDATA/Rocky5 needs these Logs/', file))
	if os.path.isdir('E:/TDATA/Rocky5 needs these Logs/XBMC4Gamers'):
		for file in os.listdir('E:/TDATA/Rocky5 needs these Logs/XBMC4Gamers'):
			if file.endswith('.log'):
				os.remove(os.path.join('E:/TDATA/Rocky5 needs these Logs/XBMC4Gamers', file))
	# Remove old save folder.
	if os.path.isdir('E:/UDATA/09999990'):
		shutil.rmtree('E:/UDATA/09999990')
## Extract the dashboard zip
	time.sleep(2)
	with zipfile.ZipFile(zip_file) as zip:
		Total_TXT_Files = len(zip.namelist()) or 1
		Devide = 100.0 / Total_TXT_Files
		Percent = 0
		for item in zip.namelist():
			xbmc.executebuiltin('Skin.SetString(DashboardUpdatedSmall,'+str(int(Percent))+')')
			Percent += Devide
			pDialog.update(int(Percent),"Download complete","Updating dashboard")
			try:
				zip.extract(item, Root_Directory)
			except:
				print "Failed - "+item
		pDialog.update(100,"Download complete","Updating dashboard complete")
		xbmc.executebuiltin('Skin.SetBool(DashboardUpdated)')
		time.sleep(3)
	if os.path.isdir(Root_Directory+'skins/DVD2Xbox Skin'):
		shutil.rmtree(Root_Directory+'skins/DVD2Xbox Skin')
		input = fileinput.input(Root_Directory+'system/userdata/profiles.xml', inplace=True)
		for line in input:
			 if '<name>DVD2Xbox</name>' in line:
				 for _ in range(19):
					 next(input, None)
			 else:
				 print line,
else:
	pDialog.create('Error')
	pDialog.update(0,"Download complete","Files are missing")
	time.sleep(5)
## Write the cleanup script and reload the dashboard xbe
autoexec_data = "import os, shutil, time, xbmcgui, zipfile\nif os.path.isdir('Q:/Updater'):\n	shutil.copy2('Q:/Updater/system/xbmc.log','Q:/system/xbmc-updater.log')\n	shutil.rmtree('Q:/Updater')\n	if os.path.isfile('Q:/system/keymaps/Enabled'): xbmc.executebuiltin('Skin.SetBool(editmode)')\n	time.sleep(2)\n	with open('Special://root/system/SystemInfo/changes.txt','r') as changes:\n		xbmcgui.Dialog().textviewer('Changes.txt', changes.read())\n	if os.path.isfile('Q:/skins/Profile Skin/extras/disc artwork.zip'):\n		with zipfile.ZipFile('Q:/skins/Profile Skin/extras/disc artwork.zip') as zip:\n			for item in zip.namelist():\n				try:\n					zip.extract(item,'Q:/skins/Profile Skin/extras/')\n				except:\n					print 'Failed - '+item\n		os.remove('Q:/skins/Profile Skin/extras/disc artwork.zip')"
with open(os.path.join(Root_Directory,'system/scripts/autoexec.py') , 'w') as autoexec: autoexec.write(autoexec_data)
time.sleep(3)
xbmc.executebuiltin('RunXBE('+ Root_Directory +'default.xbe)')