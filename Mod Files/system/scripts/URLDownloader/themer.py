### Used to theme the url downloader ui
import glob,os,shutil,xbmc,xbmcgui
skin_xml_path = 'xml'
if os.path.isfile('Special://skin/720p/includes.xml') and not os.path.isfile('Special://skin/xml/includes.xml'): skin_xml_path = '720p'
xbmc.executebuiltin('Dialog.Close(1904,false)')
Theme_Path = xbmc.translatePath('Special://skin/extras/urldownloader themes/XML files')
Ouput_Path = xbmc.translatePath('Special://skin/'+skin_xml_path+'/Includes_URLDownloader_Colours.xml')
Sorted_Theme_Path = [f for f in sorted(os.listdir(Theme_Path)) if f.endswith('.xml')]
Sorted_Theme_Path_Files = [os.path.splitext(x)[0] for x in Sorted_Theme_Path]
ThemeFolder = xbmcgui.Dialog().select("Select Theme",Sorted_Theme_Path_Files,10000)
if ThemeFolder == -1:
	pass
else:
	ThemeFile = os.path.join(Theme_Path,sorted(os.listdir(Theme_Path))[ThemeFolder])
	shutil.copy2(ThemeFile,Ouput_Path)
	xbmc.executebuiltin('ReloadSkin')
