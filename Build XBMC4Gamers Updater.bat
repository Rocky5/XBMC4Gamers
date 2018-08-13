:: Copyright of John Conn (Rocky5 Forums & JCRocky5 Twitter) 2016
:: Please don't re-release this as your own, if you make a better tool then I don't mind :-)
:Start
@Echo off & SetLocal EnableDelayedExpansion & Mode con:cols=100 lines=10 & Color 0B
title XBMC4Gamers Builder

Attrib /s -r -h -s "Thumbs.db" >NUL
Del /Q /S "Thumbs.db" 2>NUL

Set "foldername=update-files"
Set "fromDate=06/03/2018"
Set "toDate=%date%"
Set "version=1.0"
(
echo fromDate^=CDate^("%fromDate%"^)
echo toDate^=CDate^("%toDate%"^)
echo WScript.Echo DateDiff^("d",fromDate,toDate,vbMonday^)
)>tmp.vbs
for /f %%a in ('cscript /nologo tmp.vbs') do (
if %%a GEQ 100 Set "daytotal=%%a"
if %%a LSS 100 Set "daytotal=0%%a"
if %%a LSS 10 Set "daytotal=00%%a"
)
del tmp.vbs

cls
Echo: & Echo: & Echo: & Echo   Please wait...

(
XCopy /s /e /i /h /r /y "Mod Files" "%foldername%"
del /q /s "%foldername%\*.bat"
copy "New XBMC xbe\default.xbe" "%foldername%\"
copy "New XBMC xbe\default.xbe" "other\update build\updater\"
)
CD %foldername%\
"C:\Program Files\7-Zip\7z.exe" a "..\Other\update build\updater\Update Files\%foldername%.zip" "*" -mx=7 -r -y
"C:\Program Files\7-Zip\7z.exe" a "..\XBMC4Gamers-update-files.zip" "..\Other\update build\*" -mx=7 -r -y
del /Q "..\Other\update build\updater\Update Files\%foldername%.zip"
cls
Echo: & Echo:
Echo  Just overwrite your existing install of XBMC4Gamers
Echo  None of your scanned content or settings will be lost.
timeout /t 15 >NUL