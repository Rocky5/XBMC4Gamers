import os,shutil,sys,xbmc,xbmcgui

if xbmc.getCondVisibility('Skin.HasSetting(File_Manager_Compact_Mode)'):
	xbmc.executebuiltin('Skin.Reset(File_Manager_Compact_Mode)')
else:
	xbmc.executebuiltin('Skin.SetBool(File_Manager_Compact_Mode)')
xbmc.executebuiltin('ReloadSkin')