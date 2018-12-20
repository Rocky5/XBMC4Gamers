import fileinput, os, shutil, xbmc, xbmcgui, zipfile
Root_Directory	= xbmc.translatePath("Special://root/")[:-8]
pDialog	= xbmcgui.DialogProgress()
dialog	= xbmcgui.Dialog()
zip_file = os.path.join( Root_Directory, 'updater\\Update Files\\update-files.zip' )
destination = Root_Directory
#Remove old files or files that are no longer needed.
if os.path.isdir( Root_Directory + 'system\\toggles' ): shutil.rmtree( Root_Directory + 'system\\toggles' )
if os.path.isfile( zip_file ):
	with zipfile.ZipFile( zip_file ) as zip:
		pDialog.create( "EXTRACTING ZIP","","Please wait..." )
		Total_TXT_Files = len( zip.namelist() ) or 1
		Devide = 100.0 / Total_TXT_Files
		Percent = 0
		for item in zip.namelist():
			Percent += Devide
			pDialog.update( int( Percent ),"[B][UPPERCASE]" + os.path.split(zip_file)[1] + "[/UPPERCASE][/B]",item )
			try:
				zip.extract( item, destination )
			except:
				print "Failed - " + item
autoexec_data = "import os, shutil\n\
if os.path.isdir( 'Q:\\Updater' ):\n\
	shutil.rmtree( 'Q:\\Updater' )\n\
	xbmc.executebuiltin('ActivateWindow(1400)')\n\
"
with open( os.path.join( Root_Directory,'system\\scripts\\autoexec.py') , 'w') as autoexec: autoexec.write( autoexec_data )
xbmc.executebuiltin('RunXBE('+ Root_Directory +'default.xbe)')
