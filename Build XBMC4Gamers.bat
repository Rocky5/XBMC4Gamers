:: Copyright of Rocky5 Forums & JCRocky5 Twitter 2016
:: Please don't re-release this as your own, if you make a better tool then I don't mind :-)

@Echo off
SetLocal EnableDelayedExpansion
Mode con:cols=100 lines=10
Color 0B
title XBMC4Gamers Builder

:: Set date and time
Set d=%DATE:~0,2%/%DATE:~3,2%/%DATE:~6,4%
Set t=%TIME:~0,2%:%TIME:~3,2%
Set d=%d: =0%
Set t=%t: =0%

REM Set foldername based on existing directories
if exist "XBMC" (
    Set "foldername=XBMC"
) else if exist "Build" (
    Set "foldername=Build"
) else (
    Echo Error: place a fresh copy of XBMC next to this batch file and try again.
    timeout /t 5
    Exit /b
)

:Start
Set /p "version="<version.txt

title XBMC4Gamers Builder - %version%
cls
Echo: & Echo: & Echo: & Echo   Preparing files & Echo   Please wait...
(
    REM Clean up files
    Attrib /s -r -h -s "desktop.ini"
    Attrib /s -r -h -s "Thumbs.db"
    Del /Q /S "desktop.ini"
    Del /Q /S "Thumbs.db"
    rd /q /s "%foldername%\plugins"
    rd /q /s "%foldername%\sounds"
    rd /q /s "%foldername%\userdata"
    rd /q /s "%foldername%\visualisations"
    rd /q /s "%foldername%\web"
    rd /q /s "%foldername%\system\keymaps"
    rd /q /s "%foldername%\system\cdrip"
    rd /q /s "%foldername%\system\scrapers"
    rd /q /s "%foldername%\system\players\mplayer\codecs"
    rd /q /s "%foldername%\scripts"
    rd /q /s "%foldername%\skin"
    rd /q /s "%foldername%\screensavers"
    del /q "%foldername%\system\filezilla server.xml"
    del /q "%foldername%\copying.txt"
    del /q "%foldername%\keymapping.txt"
    del /q "%foldername%\media\icon.png"
    del /q "%foldername%\media\Splash_2007.png"
    del /q "%foldername%\media\Splash_2008.png"
    del /q "%foldername%\media\weather.rar"
    move "%foldername%\media" "%foldername%\system\"
    move "%foldername%\language" "%foldername%\system\"
    move "%foldername%\screenshots" "%foldername%\system\"
    move "%foldername%\UserData" "%foldername%\system\"
    XCopy /s /e /i /h /r /y "Mod Files" "%foldername%"

    REM Update language files
    for /f "tokens=*" %%a in ('dir /b "%foldername%\skins\Profile\language"') do (
        Call Other\Tools\repl.bat "XBMC4Gamers 0.0.000" "XBMC4Gamers Stable Build %version%" L < "%foldername%\skins\Profile\language\%%a\strings.po" >"%foldername%\skins\Profile\language\%%a\strings.tmp"
        Del "%foldername%\skins\Profile\language\%%a\strings.po"
        rename "%foldername%\skins\Profile\language\%%a\strings.tmp" "strings.po"
        
        Call Other\Tools\repl.bat "XBMC4Gamers datetime" "[CR]Stable Build %version%: %d% - %t%" L < "%foldername%\skins\Profile\language\%%a\strings.po" >"%foldername%\skins\Profile\language\%%a\strings.tmp"
        Del "%foldername%\skins\Profile\language\%%a\strings.po"
        rename "%foldername%\skins\Profile\language\%%a\strings.tmp" "strings.po"

        Call Other\Tools\repl.bat "build type" "Stable_Build" L < "%foldername%\skins\Profile\language\%%a\strings.po" >"%foldername%\skins\Profile\language\%%a\strings.tmp"
        Del "%foldername%\skins\Profile\language\%%a\strings.po"
        rename "%foldername%\skins\Profile\language\%%a\strings.tmp" "strings.po"
    )

    MD "%foldername%\system\SystemInfo"
    Call Other\Tools\repl.bat " " "" L < "changes.txt" >"%foldername%\system\SystemInfo\changes.txt"
    XCopy /s /e /i /h /r /y "%foldername%\skins\Profile\language\" "%foldername%\skins\Add User\language\"

    del /Q "%foldername%\Changes.txt"
    del /Q /S "%foldername%\*.bat"
    del /Q /S "%foldername%\empty.file"
    ren "%foldername%" "XBMC4Gamers"
)>nul 2>&1

cls
title XBMC4Gamers Builder - %version% Complete
Echo: & Echo: & Echo: & Echo   Done...
timeout /t 3 >NUL