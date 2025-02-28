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

:Start
Set "foldername=update-files"
Set "output_zip=XBMC4Gamers-test-build.zip"
Set /p "version="<version.txt

title XBMC4Gamers Test Builder ^(Test^) - %version%

Set /p "buildTSV="<RC.txt
if "%buildTSV%"=="true" (
	title XBMC4Gamers Test Builder ^(Release^) - %version%
	Echo timestamp=%d% %t%>"%USERPROFILE%\Desktop\New Downloader Builder\Downloader Builder\gamers_tb_timestamp"
	Echo version=%version%>"%USERPROFILE%\Desktop\New Downloader Builder\Downloader Builder\gamers_tb_version"
)

:: Prepare files
cls
Echo: & Echo: & Echo: & Echo   Preparing files & Echo    - Cleaning and copying file
(
	Attrib /s -r -h -s "desktop.ini"
	Attrib /s -r -h -s "Thumbs.db"
	Del /Q /S "desktop.ini"
	Del /Q /S "Thumbs.db"
	XCopy /s /e /i /h /r /y "Mod Files" "%foldername%"
	del /q "%foldername%\system\userdata\profiles.xml"
	del /q "%foldername%\system\userdata\guisettings.xml"
)>nul 2>&1

cls
Echo: & Echo: & Echo: & Echo   Processing additional files & Echo    - Adding info to language files
(
	REM Update language files
	for /f "tokens=*" %%a in ('dir /b "%foldername%\skins\Profile\language"') do (
		Call Other\Tools\repl.bat "XBMC4Gamers 0.0.000" "XBMC4Gamers Test Build %version%" L < "%foldername%\skins\Profile\language\%%a\strings.po" >"%foldername%\skins\Profile\language\%%a\strings.tmp"
		Del "%foldername%\skins\Profile\language\%%a\strings.po"
		rename "%foldername%\skins\Profile\language\%%a\strings.tmp" "strings.po"
		
		Call Other\Tools\repl.bat "XBMC4Gamers datetime" "[CR]Test Build %version%: %d% - %t%" L < "%foldername%\skins\Profile\language\%%a\strings.po" >"%foldername%\skins\Profile\language\%%a\strings.tmp"
		Del "%foldername%\skins\Profile\language\%%a\strings.po"
		rename "%foldername%\skins\Profile\language\%%a\strings.tmp" "strings.po"

		Call Other\Tools\repl.bat "build type" "Test_Build" L < "%foldername%\skins\Profile\language\%%a\strings.po" >"%foldername%\skins\Profile\language\%%a\strings.tmp"
		Del "%foldername%\skins\Profile\language\%%a\strings.po"
		rename "%foldername%\skins\Profile\language\%%a\strings.tmp" "strings.po"
	)
)>nul 2>&1

	If not exist "%foldername%\system\SystemInfo" MD "%foldername%\system\SystemInfo"
	Echo    - Processing changelog.txt
	Call Other\Tools\repl.bat "	" "" L < "changes.txt" >"%foldername%\system\SystemInfo\changes.txt"

(
	XCopy /s /e /i /h /r /y "%foldername%\skins\Profile\language\" "%foldername%\skins\Add User\language\"
	del /Q /S "%foldername%\*.bat"
	del /Q /S "%foldername%\empty.file"
	CD %foldername%\
	del /Q "Changes.txt"
)>nul 2>&1

cls
Echo: & Echo: & Echo: & Echo   Creating archives
	:: Create archive
	Echo    - Building %foldername%.zip
	"C:\Program Files\7-Zip\7z.exe" a "..\Other\update build\updater\Update Files\%foldername%.zip" "*" -mx=7 -r -y>nul 2>&1
	Echo    - Generating MD5Hash for %foldername%.zip
	"..\Other\Tools\md5.exe" -l "..\Other\update build\updater\Update Files\%foldername%.zip">"..\Other\update build\updater\Update Files\md5hash.bin"
	for /f "usebackq" %%b in ("..\Other\update build\updater\Update Files\md5hash.bin") do (
		echo %%b>"..\Other\update build\updater\Update Files\md5hash.bin"
	)
	Echo    - Building %output_zip%
	"C:\Program Files\7-Zip\7z.exe" a "..\%output_zip%" "..\Other\update build\*" -mx=7 -r -y>nul 2>&1
 
 (   
	cd ..\
	rd /q /s "Other\update build\updater\Update Files"
	rd /q /s "update-files"
)>nul 2>&1

cls
title XBMC4Gamers Test Builder ^(Test^) - %version% Complete
Echo: & Echo: & Echo: & Echo:
Echo  Current version: xbmc4gamers test build %version%
timeout /t 15 >NUL