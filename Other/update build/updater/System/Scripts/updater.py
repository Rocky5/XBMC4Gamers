import fileinput, os, shutil, xbmc, xbmcgui, zipfile
# Gets current XBMC-Emustation directory.
CharCount = 100 # How many characters you want after 'The executable running is: '
with open( xbmc.translatePath( "special://xbmc/" ) + "xbmc.log", "r" ) as XBMCLOG:
	for line in XBMCLOG:
		left,found,right = line.partition("The executable running is: ")
		if found:
			Working_Directory	= ( right[:CharCount] )
			Root_Directory      = os.path.dirname( Working_Directory ) + '\\'
			Root_Directory		= Root_Directory[:-8]
pDialog	= xbmcgui.DialogProgress()
dialog	= xbmcgui.Dialog()
zip_file = os.path.join( Root_Directory, 'updater\\Update Files\\update-files.zip' )
destination = Root_Directory
#Remove old files or files that are no longer needed.
if os.path.isfile( Root_Directory + 'default skin\\media\\Texture.xpr' ): os.remove( Root_Directory + 'default skin\\media\\Texture.xpr' )
if os.path.isfile( Root_Directory + '.emustation\\scripts\\versioner.py' ): os.remove( Root_Directory + '.emustation\\scripts\\versioner.py' )
if os.path.isfile( Root_Directory + '.emustation\\scripts\\scanner.py' ): os.remove( Root_Directory + '.emustation\\scripts\\scanner.py' )
if os.path.isfile( Root_Directory + 'system\\version.bin' ): os.remove( Root_Directory + 'system\\version.bin' )
if os.path.isdir( Root_Directory + 'system\\UserData\\Thumbnails\\Programs' ): shutil.rmtree( Root_Directory + 'system\\UserData\\Thumbnails\\Programs' )
if os.path.isdir( Root_Directory + '.emustation\\layouts\\home\\previews' ):	shutil.rmtree( Root_Directory + '.emustation\\layouts\\home\\previews' )
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
				pass
	for line in fileinput.input( os.path.join( Root_Directory, 'system\\userdata\\guisettings.xml' ), inplace=1):
		if line.strip().startswith('<font>'):
			line = '<font>SKINDEFAULT</font>\n'
		if line.strip().startswith('<skincolors>'):
			line = '<skincolors>.xml</skincolors>\n'
		if line.strip().startswith('<skintheme>'):
			line = '<skintheme>skindefault</skintheme>\n'
		if line.strip().startswith('<soundskin>'):
			line = '<soundskin></soundskin>\n'
		print line,

autoexec_data = "import os, shutil\n\
if os.path.isdir( 'Q:\\Updater' ):\n\
	shutil.rmtree( 'Q:\\Updater' )\n\
	xbmc.executebuiltin('ActivateWindow(1400)')\n\
"
with open( os.path.join( Root_Directory,'system\\scripts\\autoexec.py') , 'w') as autoexec: autoexec.write( autoexec_data )
xbmc.executebuiltin('RunXBE('+ Root_Directory +'default.xbe)')
