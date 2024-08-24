:: Copyright of John Conn (Rocky5 Forums & JCRocky5 Twitter) 2016
:: Please don't re-release this as your own, if you make a better tool then I don't mind :-)

@Echo off & SetLocal EnableDelayedExpansion & Mode con:cols=100 lines=10 & Color 0B
title XBMC4Gamers Builder

Set d=%DATE:~0,2%/%DATE:~3,2%/%DATE:~6,4%
Set t=%TIME:~0,2%:%TIME:~3,2%
Set d=%d: =0%
Set t=%t: =0%

:Start
Set "foldername=update-files"
Set "output_zip=XBMC4Gamers-update-files.zip"
Set /p "version="<version.txt

REM Set "fromDate=23/06/2022"
REM for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set dateformat=%%j
REM Set toDate=%dateformat:~6,2%^/%dateformat:~4,2%^/%dateformat:~0,4%
REM if exist "..\other\build for release.bin" (
	REM (
	REM echo fromDate^=CDate^("%fromDate%"^)
	REM echo toDate^=CDate^("%toDate%"^)
	REM echo WScript.Echo DateDiff^("d",fromDate,toDate,vbMonday^)
	REM )>tmp.vbs
	REM for /f %%a in ('cscript /nologo tmp.vbs') do (
	REM if %%a GEQ 100 Set "daytotal=%%a"
	REM if %%a LSS 100 Set "daytotal=0%%a"
	REM if %%a LSS 10 Set "daytotal=00%%a"
	REM )
	REM del tmp.vbs
REM ) else (
	REM Set daytotal=000
REM )

title XBMC4Gamers Update Builder ^(Test^) - %version%

Set /p "buildTSV="<RC.txt
if "%buildTSV%"=="true" (
	title XBMC4Gamers Update Builder ^(Release^) - %version%
	Echo timestamp=%d% %t%>"%USERPROFILE%\Desktop\New Downloader Builder\Downloader Builder\gamers_u_timestamp"
	Echo version=%version%>"%USERPROFILE%\Desktop\New Downloader Builder\Downloader Builder\gamers_u_version"
)

cls
Echo: & Echo: & Echo: & Echo   Preping files & Echo   Please wait...
(
Attrib /s -r -h -s "desktop.ini"
Attrib /s -r -h -s "Thumbs.db"
Del /Q /S "desktop.ini"
Del /Q /S "Thumbs.db"
XCopy /s /e /i /h /r /y "Mod Files" "%foldername%"
del /q "%foldername%\system\userdata\profiles.xml"
del /q "%foldername%\system\userdata\guisettings.xml"

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
Call Other\Tools\repl.bat "	" "" L < "changes.txt" >"%foldername%\system\SystemInfo\changes.txt"
XCopy /s /e /i /h /r /y "%foldername%\skins\Profile\language\" "%foldername%\skins\Manage Profiles\language\"

del /Q /S "%foldername%\*.bat"
del /Q /S "%foldername%\empty.file"
CD %foldername%\
del /Q "Changes.txt"
)>nul 2>&1

cls
Echo: & Echo: & Echo: & Echo   Creating archive & Echo   Please wait...
(
"C:\Program Files\7-Zip\7z.exe" a "..\Other\update build\updater\Update Files\%foldername%.zip" "*" -mx=7 -r -y
"..\Other\Tools\md5.exe" -l "..\Other\update build\updater\Update Files\%foldername%.zip">"..\Other\update build\updater\Update Files\md5hash.bin"
for /f "usebackq" %%b in ("..\Other\update build\updater\Update Files\md5hash.bin") do (
	echo %%b>"..\Other\update build\updater\Update Files\md5hash.bin"
)
"C:\Program Files\7-Zip\7z.exe" a "..\%output_zip%" "..\Other\update build\*" -mx=7 -r -y
cd ..\
rd /q /s "Other\update build\updater\Update Files"
rd /q /s "update-files"
)>nul 2>&1

cls
Echo: & Echo: & Echo: & Echo:
Echo  Current version: xbmc4gamers %version%
timeout /t 15 >NUL