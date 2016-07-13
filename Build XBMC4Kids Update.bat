@Echo off & SetLocal EnableDelayedExpansion & mode con:cols=56 lines=15 & Color 0B & Title XBMC4Kids Updater

Set "Version=1.0"

:: Directories
Set "Location=Mod Files"
Set "Output_Folder=XBMC4Kids Update"
Set "Enabled_All="
Set "Enabled_EditMode1="
Set "Enabled_EditMode2="

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: GUI Elements.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
Set "GUI_Element_1=Echo 컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴"
Set "GUI_Element_2=Echo 컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴 Created by Rocky5"
Set "GUI_Element_3=Echo 컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴 Version %Version%"
Set "GUI_Element_4=Echo 컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴컴 Error"

:Splash :D
CLS & Echo: & Echo: & Echo: & Echo:
%GUI_Element_1%
Echo  XBMC4Kids Updater
Echo:
%GUI_Element_2%
%GUI_Element_3%
timeout /t 2 >NUL

:menu
Set "pick="
CLS
Echo:
Echo:
Echo  Please select the appropriate options.
Echo:
%GUI_Element_1%
if "%Enabled_EditMode1%"==""  Echo  1) Edit Mode is Disabled [ ]
if "%Enabled_EditMode1%"=="1" Echo  1) Edit Mode is Disabled [-]
if "%Enabled_EditMode2%"==""  Echo  2) Edit Mode is Enabled  [ ]
if "%Enabled_EditMode2%"=="1" Echo  2) Edit Mode is Enabled  [-]
Echo:
Echo  B) to build the update
Echo:
%GUI_Element_1%
Set /p "pick="
:: 1 = true / 0 = false
::if "%Enabled_All%"=="" if "%pick%"=="5" Set "Enabled_All=1" & Goto menu

if "%Enabled_EditMode1%"=="" if "%pick%"=="1" Set "Enabled_EditMode1=1" & Set "Enabled_EditMode2="  & Goto menu
if "%Enabled_EditMode1%"=="1" if "%pick%"=="1" Set "Enabled_EditMode1=" & Set "Enabled_EditMode2="  & Goto menu

if "%Enabled_EditMode2%"=="" if "%pick%"=="2" Set "Enabled_EditMode2=1" & Set "Enabled_EditMode1=" & Goto menu
if "%Enabled_EditMode2%"=="1" if "%pick%"=="2" Set "Enabled_EditMode2=" & Set "Enabled_EditMode1=" & Goto menu

if "%pick%"=="b" if "%Enabled_EditMode1%"=="1" if "%Enabled_EditMode2%"=="" goto start
if "%pick%"=="B" if "%Enabled_EditMode1%"=="1" if "%Enabled_EditMode2%"=="" goto start
if "%pick%"=="b" if "%Enabled_EditMode1%"=="" if "%Enabled_EditMode2%"=="1" goto start
if "%pick%"=="B" if "%Enabled_EditMode1%"=="" if "%Enabled_EditMode2%"=="1" goto start

goto menu

:reset_vars
Set "Enabled_All="
Set "Enabled_EditMode1="
Set "Enabled_EditMode2="
Goto menu

:start
:: Code
cls
Echo:
Echo:
Echo:
Echo:
%GUI_Element_1%
Echo  About to make update folder
Echo:
%GUI_Element_1%
timeout /t 5 >NUL & cls

if "%Enabled_EditMode1%"=="1" (
MD "%Output_Folder%" 2>NUL
Echo:
Echo  Checking Cache, please wait...
if "%Enabled_EditMode1%"=="1" Xcopy /S /E /I /Y /D /J "%Location%" "%Output_Folder%"
if "%Enabled_EditMode1%"=="1" Copy /Y "%Location%\system\keymaps\Usermode.file" "%Output_Folder%\system\keymaps\gamepad.xml"
if "%Enabled_EditMode1%"=="1" Del /Q /S "%Output_Folder%\system\keymaps\Enabled"
if "%Enabled_EditMode1%"=="1" RD /Q /S "%Output_Folder%\UserData"
if "%Enabled_EditMode1%"=="1" Del /Q /S "%Output_Folder%\skin\*.bat"
Echo:
)

if "%Enabled_EditMode2%"=="1" (
MD "%Output_Folder%" 2>NUL
Echo:
Echo  Checking Cache, please wait...
if "%Enabled_EditMode2%"=="1" Xcopy /S /E /I /Y /D /J "%Location%" "%Output_Folder%"
if "%Enabled_EditMode2%"=="1" RD /Q /S "%Output_Folder%\UserData"
if "%Enabled_EditMode2%"=="1" Del /Q /S "%Output_Folder%\skin\*.bat"
Echo:
)

Goto reset_vars