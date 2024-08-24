@Echo off

Set "ProfileSkin=%CD%\Profile"
Set "MasterSkin=%CD%\Manage Profiles"

Echo colors\Defaults.xml
Copy /Y "%ProfileSkin%\colors\Defaults.xml"							"%MasterSkin%\colors\" >Nul
Echo xml\Defaults.xml
Copy /Y "%ProfileSkin%\xml\Defaults.xml"							"%MasterSkin%\xml\" >Nul
Echo xml\DialogBusy.xml
Copy /Y "%ProfileSkin%\xml\DialogBusy.xml"							"%MasterSkin%\xml\" >Nul
Echo xml\DialogGamepad.xml
Copy /Y "%ProfileSkin%\xml\DialogGamepad.xml"						"%MasterSkin%\xml\" >Nul
Echo xml\DialogKaiToast.xml
Copy /Y "%ProfileSkin%\xml\DialogKaiToast.xml"						"%MasterSkin%\xml\" >Nul
Echo xml\DialogKeyboard.xml
Copy /Y "%ProfileSkin%\xml\DialogKeyboard.xml"						"%MasterSkin%\xml\" >Nul
Echo DialogMuteBug.xml
Copy /Y "%ProfileSkin%\xml\DialogMuteBug.xml"						"%MasterSkin%\xml\" >Nul
Echo DialogNetworkSetup.xml
Copy /Y "%ProfileSkin%\xml\DialogNetworkSetup.xml"					"%MasterSkin%\xml\" >Nul
Echo DialogNumeric.xml
Copy /Y "%ProfileSkin%\xml\DialogNumeric.xml"						"%MasterSkin%\xml\" >Nul
Echo xml\DialogOK.xml
Copy /Y "%ProfileSkin%\xml\DialogOK.xml"							"%MasterSkin%\xml\" >Nul
Echo xml\DialogProgress.xml
Copy /Y "%ProfileSkin%\xml\DialogProgress.xml"						"%MasterSkin%\xml\" >Nul
Echo xml\DialogOverlay.xml
Copy /Y "%ProfileSkin%\xml\DialogOverlay.xml"						"%MasterSkin%\xml\" >Nul
Echo xml\DialogScriptInfo.xml
Copy /Y "%ProfileSkin%\xml\DialogScriptInfo.xml"					"%MasterSkin%\xml\" >Nul
Echo xml\DialogSeekBar.xml
Copy /Y "%ProfileSkin%\xml\DialogSeekBar.xml"						"%MasterSkin%\xml\" >Nul
Echo xml\DialogSelect.xml
Copy /Y "%ProfileSkin%\xml\DialogSelect.xml"						"%MasterSkin%\xml\" >Nul
Echo xml\DialogTextViewer.xml
Copy /Y "%ProfileSkin%\xml\DialogTextViewer.xml"					"%MasterSkin%\xml\" >Nul
Echo xml\DialogYesNo.xml
Copy /Y "%ProfileSkin%\xml\DialogYesNo.xml"							"%MasterSkin%\xml\" >Nul
Echo xml\FileBrowser.xml
Copy /Y "%ProfileSkin%\xml\FileBrowser.xml"							"%MasterSkin%\xml\" >Nul
Echo xml\FileManager.xml
Copy /Y "%ProfileSkin%\xml\FileManager.xml"							"%MasterSkin%\xml\" >Nul
Echo xml\Font.xml
Copy /Y "%ProfileSkin%\xml\Font.xml"								"%MasterSkin%\xml\" >Nul
Echo xml\Pointer.xml
Copy /Y "%ProfileSkin%\xml\Pointer.xml"								"%MasterSkin%\xml\" >Nul
Echo xml\SettingsCategory.xml
Copy /Y "%ProfileSkin%\xml\SettingsCategory.xml"					"%MasterSkin%\xml\" >Nul
Echo xml\SettingsScreenCalibration.xml
Copy /Y "%ProfileSkin%\xml\SettingsScreenCalibration.xml"			"%MasterSkin%\xml\" >Nul
Echo xml\SettingsSystemInfo.xml
Copy /Y "%ProfileSkin%\xml\SettingsSystemInfo.xml"					"%MasterSkin%\xml\" >Nul
Echo language\
XCopy /s /e /i /h /r /y "%ProfileSkin%\language\"					"%MasterSkin%\language" >Nul

timeout /t 2