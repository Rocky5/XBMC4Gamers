@Echo off
Setlocal enabledelayedexpansion

Set "Skin1=Profile"
Set "Skin2=Add User"

Echo:
Echo !Skin1! Skin:
Echo:
for /f "Tokens=*" %%a in ('dir /b "!Skin1!\xml\*.xml"') do (
    Set "File1=!Skin1!\xml\%%a"
    Set "File2=Check\!Skin1!\xml\%%a"
    if exist "!File2!" (
		fc "!File1!" "!File2!" >nul
		if errorlevel 1 (
			Echo   Different:
			Echo     !File2!
		)
	)
)
Echo:
Echo:
Echo !Skin2! Skin:
Echo:
for /f "Tokens=*" %%a in ('dir /b "!Skin2!\xml\*.xml"') do (
    Set "File1=!Skin2!\xml\%%a"
    Set "File2=Check\!Skin2!\xml\%%a"
    if exist "!File2!" (
		fc "!File1!" "!File2!" >nul
		if errorlevel 1 (
			Echo   Different:
			Echo     !File2!
		)
	)
)
Echo:
Echo:
pause
