# By Donno [darkdonno@gmail.com] modified by Jezz-X
# Modded by Rocky5
# 1 - Added support for getting XBMCs location.
# 2 - Added support for creating the destination directories if they don't exist.
# 3 - Added check for default.xbe in the dvd drive for the Auto Install Game option
import xbmc
import xbmcgui
import os
# Check for default.xbe in D if not found give error.
if os.path.isfile("d:/default.xbe"):
	__title__ = "DVD2XBOX Runner"
	runself = xbmc.translatePath("special://root/default.xbe") # should point to XBMC
	dvd2xbox_dir = xbmc.translatePath("special://xbmc/Apps/DVD2Xbox/")
	skin = "project_mayhem_iii"  # this is the name of the dvd2xbox skin dir to use
	# for now just have these as varibles
	gamemodelist = ["normal","iso"]
	destlist = ["E:\\Games\\","F:\\Games\\","G:\\Games\\","Browse for Custom"]
	modeg = "normal"
	modev = "normal"
	modea = "mp3"
	destg = "E:\\Games\\"
	showkeyboard = "no"
	copyretrydialog = "yes"
	base_str = '<remotecontrol>\n\
		<skin>%s</skin>\n\
		<runapp>%s</runapp>\n\
		<delconf>yes</delconf>\n\
		<gamecopy>\n\
			<showkeyboard>%s</showkeyboard>\n\
			<copyretrydialog>%s</copyretrydialog>\n\
			<mode>%s</mode>\n\
			<destination>%s</destination>\n\
		</gamecopy>\n\
		<videocopy>\n\
			<showkeyboard>%s</showkeyboard> \n\
			<copyretrydialog>%s</copyretrydialog> \n\
			<mode>%s</mode>\n\
			<destination>%s</destination>\n\
		</videocopy>\n\
		<audiocopy>\n\
			<showkeyboard>%s</showkeyboard> \n\
			<copyretrydialog>%s</copyretrydialog> \n\
			<mode>%s</mode>\n\
			<destination>%s</destination>\n\
		</audiocopy>\n\
	</remotecontrol>'
	def createdir(destg):
		#Create directories
		if not os.path.exists(destg):
			os.mkdir(destg)
		else:
			print "Destination already exist"
	def writexml(curdat):
		#dvd2xbox_dir
		fb = open(dvd2xbox_dir+"remotecontrol.xml",'w')
		fb.write(curdat)
		fb.close()
	def yesno(q):
		retval = xbmcgui.Dialog().yesno(__title__,q)
		if retval == -1: return "no"
		if retval == 0: return "no"
		if retval == 1: return "yes"
	def doadvanced(destg):
		retval = xbmcgui.Dialog().select("Copy Mode",gamemodelist)
		modeg = gamemodelist[retval]
		showkeyboard = yesno("Allow Rename Dump Dir")
		copyretrydialog = yesno("Show Copy and Retry Dialog")
		curdat= base_str % (skin,runself,showkeyboard,copyretrydialog,modeg,destg,showkeyboard,copyretrydialog,modeg,destg,showkeyboard,copyretrydialog,modea,destg)
		writexml(curdat)
		from xbmc import executebuiltin
		exi_str =  "XBMC.RunXBE(%sDefault.xbe)" % dvd2xbox_dir
		executebuiltin(exi_str)  
	def doGames():
			retval = xbmcgui.Dialog().select("Choose Rip Dir",destlist)
			if retval != -1:    
				destg = destlist[retval]
				if destg == "Browse for Custom":
					destg = xbmcgui.Dialog().browse(0,"Select Dir","files")
					destg = destg + '\\'
				advancedoptions = yesno("Set Advanced Options ?")
				if advancedoptions == "no":
					curdat= base_str % (skin,runself,showkeyboard,copyretrydialog,modeg,destg,showkeyboard,copyretrydialog,modeg,destg,showkeyboard,copyretrydialog,modea,destg)
					try:
						createdir(destg)
					except: pass
					writexml(curdat)
					from xbmc import executebuiltin
					exi_str =  "XBMC.RunXBE(%sDefault.xbe)" % dvd2xbox_dir
					executebuiltin(exi_str)  
				else:
					try:
						createdir(destg)
					except: pass
					doadvanced(destg) 
	doGames()
else:
	dialog = xbmcgui.Dialog()
	dialog.ok("Error","","There is no [B]GAME[/B] disc in the dvd drive.","Please insert a game disc & try again.")