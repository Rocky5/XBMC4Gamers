:: Copyright of John Conn (Rocky5 Forums & JCRocky5 Twitter) 2016
:: Please don't re-release this as your own, if you make a better tool then I don't mind :-)

:Start
@Echo off & SetLocal EnableDelayedExpansion & mode con:cols=70 lines=8 & title XBMC4Kids Updater

if exist "XBMC" Set "foldername=XBMC"
if exist "Build" Set "foldername=Build"
if not exist "%foldername%" Exit

cls
Echo: & Echo: & Echo: & Echo   Please wait...

(
move "%foldername%\language\english" "%foldername%"
rd /q /s "%foldername%\language"
md "%foldername%\language" &  move "%foldername%\english" "%foldername%\language\"
rd /q /s "%foldername%\plugins"
rd /q /s "%foldername%\sounds"
rd /q /s "%foldername%\userdata"
rd /q /s "%foldername%\visualisations"
rd /q /s "%foldername%\web"
rd /q /s "%foldername%\system\keymaps"
rd /q /s "%foldername%\system\cdrip"
rd /q /s "%foldername%\system\scrapers"
rd /q /s "%foldername%\system\players\mplayer\codecs"
del /q /s "%foldername%\copying.txt"
del /q /s "%foldername%\keymapping.txt"
del /q /s "%foldername%\media\icon.png"
del /q /s "%foldername%\media\Splash_2007.png"
del /q /s "%foldername%\media\Splash_2008.png"
del /q /s "%foldername%\media\weather.rar"
rd /q /s "%foldername%\skin"
md "%foldername%\skin"
copy /y "Mod Files\system\backup\FileZilla Server.xml" "%foldername%\system\FileZilla Server.xml"
XCopy /s /e /i /h /r /y "Mod Files" "%foldername%"
copy /y "New XBMC xbe\default.xbe" "%foldername%\default.xbe"
rd /q /s "%foldername%\Apps\FTP"
rd /q /s "%foldername%\Updater"
del /q /s "%foldername%\skin\*.bat"
ren "%foldername%" "Update Files"
XCopy /s /e /i /h /r /y "Mod Files\Updater" "Updater"
XCopy /s /e /i /h /r /y "Update Files\language\english" "Updater\language\english"
XCopy /s /e /i /h /r /y "Update Files\skin\Manage Profiles Skin\Fonts" "Updater\skin\Updater\Fonts"
XCopy /s /e /i /h /r /y "Update Files\media\Fonts" "Updater\media\Fonts"
XCopy /s /e /i /h /r /y "Update Files\System\keymaps" "Updater\System\keymaps"
XCopy /s /e /i /h /r /y "Update Files\System\python" "Updater\System\python"
Copy "New XBMC xbe\default.xbe" "Updater"
Move "Update Files" "Updater"
) >NUL

cls
Echo: & Echo: & Echo:
Echo  Place the "Updater" folder inside your installation of XBMC4Kids
Echo  that is on your Xbox.
timeout /t 8 >NUL
cls
Echo: & Echo:
Echo  If you are running an old build that doesnt support auto updating
Echo  you will need to select the default.xbe inside the "Updater" folder
Echo  via the filemanager.
timeout /t 15 >NUL
