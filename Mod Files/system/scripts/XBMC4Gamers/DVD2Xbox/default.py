import xbmc
import xbmcgui
import os

# Close the script loading dialog
xbmc.executebuiltin('Dialog.Close(1100,true)')
# Check for default.xbe in D if not found give error.
if os.path.isfile("d:/default.xbe"):
    __title__ = "DVD2XBOX Runner"
    runself = xbmc.translatePath("special://root/default.xbe")  # should point to XBMC
    dvd2xbox_dir = xbmc.translatePath("Special://scripts/XBMC4Gamers/DVD2Xbox/")
    skin = "project_mayhem_iii"  # this is the name of the dvd2xbox skin dir to use

    # for now just have these as variables
    gamemodelist = ["normal", "iso"]
    destlist = ["E:\\Games\\", "F:\\Games\\", "G:\\Games\\", "Browse for Custom"]
    modeg = "normal"
    modev = "normal"
    modea = "mp3"
    destg = "E:\\Games\\"
    showkeyboard = "no"
    copyretrydialog = "yes"

    base_str = '''<remotecontrol>
        <skin>%s</skin>
        <runapp>%s</runapp>
        <delconf>yes</delconf>
        <gamecopy>
            <showkeyboard>%s</showkeyboard>
            <copyretrydialog>%s</copyretrydialog>
            <mode>%s</mode>
            <destination>%s</destination>
        </gamecopy>
        <videocopy>
            <showkeyboard>%s</showkeyboard>
            <copyretrydialog>%s</copyretrydialog>
            <mode>%s</mode>
            <destination>%s</destination>
        </videocopy>
        <audiocopy>
            <showkeyboard>%s</showkeyboard>
            <copyretrydialog>%s</copyretrydialog>
            <mode>%s</mode>
            <destination>%s</destination>
        </audiocopy>
    </remotecontrol>'''

    def createdir(destg):
        # Create directories
        if not os.path.exists(destg):
            os.mkdir(destg)
        else:
            print "Destination already exists"

    def writexml(curdat):
        # dvd2xbox_dir
        with open(dvd2xbox_dir + "remotecontrol.xml", 'w') as fb:
            fb.write(curdat)

    def yesno(q):
        retval = xbmcgui.Dialog().yesno(__title__, q)
        return "yes" if retval else "no"

    def doadvanced(destg):
        retval = xbmcgui.Dialog().select("Copy Mode", gamemodelist)
        modeg = gamemodelist[retval]
        showkeyboard = yesno("Allow Rename Dump Dir")
        copyretrydialog = yesno("Show Copy and Retry Dialog")
        curdat = base_str % (skin, runself, showkeyboard, copyretrydialog, modeg, destg, showkeyboard, copyretrydialog, modeg, destg, showkeyboard, copyretrydialog, modea, destg)
        writexml(curdat)
        from xbmc import executebuiltin
        exi_str = "XBMC.RunXBE(%sDefault.xbe)" % dvd2xbox_dir
        executebuiltin(exi_str)

    def doGames():
        retval = xbmcgui.Dialog().select("Choose Rip Dir", destlist)
        if retval != -1:
            destg = destlist[retval]
            if destg == "Browse for Custom":
                destg = xbmcgui.Dialog().browse(0, "Select Dir", "files") + '\\'
            advancedoptions = yesno("Set Advanced Options ?")
            if advancedoptions == "no":
                curdat = base_str % (skin, runself, showkeyboard, copyretrydialog, modeg, destg, showkeyboard, copyretrydialog, modeg, destg, showkeyboard, copyretrydialog, modea, destg)
                try:
                    createdir(destg)
                except:
                    pass
                writexml(curdat)
                from xbmc import executebuiltin
                exi_str = "XBMC.RunXBE(%sDefault.xbe)" % dvd2xbox_dir
                executebuiltin(exi_str)
            else:
                try:
                    createdir(destg)
                except:
                    pass
                doadvanced(destg)

    doGames()
else:
    dialog = xbmcgui.Dialog()
    dialog.ok("Error", "", "There is no [B]GAME[/B] disc in the dvd drive.", "Please insert a game disc & try again.")
