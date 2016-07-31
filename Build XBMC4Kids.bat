:: Copyright of John Conn (Rocky5 Forums & JCRocky5 Twitter) 2016
:: Please don't re-release this as your own, if you make a better tool then I don't mind :-)

:Start
@Echo off & SetLocal EnableDelayedExpansion & mode con:cols=40 lines=8 & title XBMC4Kids Builder

if exist "XBMC" Set "foldername=XBMC"
if exist "Build" Set "foldername=Build"
if not exist "%foldername%" Exit

cls
Echo: & Echo: & Echo: & Echo   Please wait...

(
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
move "%foldername%\skin\Confluence Lite" "%foldername%\"
rd /q /s "%foldername%\skin"
md "%foldername%\skin"
move "%foldername%\Confluence Lite" "%foldername%\skin\"
ren "%foldername%" "XBMC4Kids"
copy /y "Mod Files\system\backup\FileZilla Server.xml" "XBMC4Kids\system\FileZilla Server.xml"
XCopy /s /e /i /h /r /y "Mod Files" "XBMC4Kids"
copy /y "New XBMC xbe\default.xbe" "XBMC4Kids\default.xbe"
rd /q /s "XBMC4Kids\Apps\FTP"
rd /q /s "XBMC4Kids\Updater"
del /q /s "XBMC4Kids\skin\*.bat"
) >NUL
cls
Echo:
Echo: & Echo: & Echo: & Echo   Done...
timeout /t 3 >NUL