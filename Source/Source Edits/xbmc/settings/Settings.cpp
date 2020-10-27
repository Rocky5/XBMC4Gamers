/*
 *      Copyright (C) 2005-2013 Team XBMC
 *      http://xbmc.org
 *
 *  This Program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2, or (at your option)
 *  any later version.
 *
 *  This Program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with XBMC; see the file COPYING.  If not, see
 *  <http://www.gnu.org/licenses/>.
 *
 */

#include "system.h"
#include "settings/Settings.h"
#include "settings/AdvancedSettings.h"
#include "Application.h"
#include "input/KeyboardLayoutConfiguration.h"
#include "Util.h"
#include "URL.h"
#include "windows/GUIWindowFileManager.h"
#include "dialogs/GUIDialogButtonMenu.h"
#include "settings/GUIDialogContentSettings.h"
#include "GUIFontManager.h"
#include "utils/LangCodeExpander.h"
#include "input/ButtonTranslator.h"
#include "XMLUtils.h"
#include "PasswordManager.h"
#include "GUIAudioManager.h"
#include "AudioContext.h"
#include "GUIInfoManager.h"
#include "xbox/Network.h"
#include "FileSystem/MultiPathDirectory.h"
#include "FileSystem/SpecialProtocol.h"
#include "GUIBaseContainer.h" // for VIEW_TYPE enum
#include "utils/FanController.h"
#include "storage/MediaManager.h"
#include "XBVideoConfig.h"
#include "network/DNSNameCache.h"
#include "GUIWindowManager.h"
#include "dialogs/GUIDialogYesNo.h"
#include "FileSystem/Directory.h"
#include "FileItem.h"
#include "LangInfo.h"
#ifdef HAS_XBOX_HARDWARE
#include "utils/MemoryUnitManager.h"
#endif
#include "cores/playercorefactory/PlayerCoreFactory.h"
#include "utils/URIUtils.h"
#include "LocalizeStrings.h"
#include "utils/CharsetConverter.h"
#include "utils/log.h"

using namespace std;
using namespace XFILE;
using namespace MEDIA_DETECT;

class CSettings g_settings;

extern CStdString g_LoadErrorStr;

CSettings::CSettings(void)
{
}

void CSettings::Initialize()
{
  for (int i = HDTV_1080i; i <= PAL60_16x9; i++)
  {
    g_graphicsContext.ResetScreenParameters((RESOLUTION)i);
    g_graphicsContext.ResetOverscan((RESOLUTION)i, m_ResInfo[i].Overscan);
  }

  m_iMyVideoStack = STACK_NONE;

  strcpy(g_settings.szOnlineArenaPassword, "");
  strcpy(g_settings.szOnlineArenaDescription, "It's Good To Play Together!");

  m_bMyMusicSongInfoInVis = true;    // UNUSED - depreciated.
  m_bMyMusicSongThumbInVis = false;  // used for music info in vis screen

  m_bMyMusicPlaylistRepeat = false;
  m_bMyMusicPlaylistShuffle = false;

  m_bMyVideoPlaylistRepeat = false;
  m_bMyVideoPlaylistShuffle = false;
  m_bMyVideoNavFlatten = false;
  m_bStartVideoWindowed = false;

  m_nVolumeLevel = 0;
  m_dynamicRangeCompressionLevel = 0;
  m_iPreMuteVolumeLevel = 0;
  m_bMute = false;
  m_fZoomAmount = 1.0f;
  m_fPixelRatio = 1.0f;

  m_pictureExtensions = ".png|.jpg|.jpeg|.bmp|.gif|.ico|.tif|.tiff|.tga|.pcx|.cbz|.zip|.cbr|.rar|.m3u|.dng|.nef|.cr2|.crw|.orf|.arw|.erf|.3fr|.dcr|.x3f|.mef|.raf|.mrw|.pef|.sr2";
  m_musicExtensions = ".nsv|.m4a|.flac|.aac|.strm|.pls|.rm|.rma|.mpa|.wav|.wma|.ogg|.mp3|.mp2|.m3u|.mod|.amf|.669|.dmf|.dsm|.far|.gdm|.imf|.it|.m15|.med|.okt|.s3m|.stm|.sfx|.ult|.uni|.xm|.sid|.ac3|.dts|.cue|.aif|.aiff|.wpl|.ape|.mac|.mpc|.mp+|.mpp|.shn|.zip|.rar|.wv|.nsf|.spc|.gym|.adplug|.adx|.dsp|.adp|.ymf|.ast|.afc|.hps|.xsp|.xwav|.waa|.wvs|.wam|.gcm|.idsp|.mpdsp|.mss|.spt|.rsd|.mid|.kar|.sap|.cmc|.cmr|.dmc|.mpt|.mpd|.rmt|.tmc|.tm8|.tm2|.oga|.url|.pxml";
  m_videoExtensions = ".m4v|.3g2|.3gp|.nsv|.tp|.ts|.ty|.strm|.pls|.rm|.rmvb|.m3u|.m3u8|.ifo|.mov|.qt|.divx|.xvid|.bivx|.vob|.nrg|.img|.iso|.pva|.wmv|.asf|.asx|.ogm|.m2v|.avi|.bin|.dat|.mpg|.mpeg|.mp4|.mkv|.avc|.vp3|.svq3|.nuv|.viv|.dv|.fli|.flv|.rar|.001|.wpl|.zip|.vdr|.dvr-ms|.xsp|.mts|.m2t|.m2ts|.evo|.ogv|.sdp|.avs|.rec|.url|.pxml|.vc1|.h264|.rcv|.rss|.mpls|.webm|.xmv|.bik|.sfd";
  // internal music extensions
  m_musicExtensions += "|.sidstream|.oggstream|.nsfstream|.asapstream|.cdda";

  // This shouldn't be set here but in CApp::Create!!!!!
//  m_logFolder = "Q:\\";              // log file location
  m_logFolder = "";

  // defaults for scanning
  m_bMyMusicIsScanning = false;

  iAdditionalSubtitleDirectoryChecked = 0;
  m_iMyMusicStartWindow = WINDOW_MUSIC_FILES;
  m_iVideoStartWindow = WINDOW_VIDEO_FILES;
  m_iMyVideoWatchMode = VIDEO_SHOW_ALL;
  m_iSystemTimeTotalUp = 0;
  m_HttpApiBroadcastLevel = 0;
  m_HttpApiBroadcastPort = 8278;

  m_usingLoginScreen = false;
  m_lastUsedProfile = 0;
  m_currentProfile = 0;
}

CSettings::~CSettings(void)
{
}


void CSettings::Save() const
{
  if (g_application.m_bStop)
  {
    //don't save settings when we're busy stopping the application
    //a lot of screens try to save settings on deinit and deinit is called
    //for every screen when the application is stopping.
    return ;
  }
  if (!SaveSettings(GetSettingsFile()))
  {
    CLog::Log(LOGERROR, "Unable to save settings to %s", GetSettingsFile().c_str());
  }
}

bool CSettings::Reset()
{
  CLog::Log(LOGINFO, "Resetting settings");
  CFile::Delete(GetSettingsFile());
  Save();
  return LoadSettings(GetSettingsFile());
}

bool CSettings::Load(bool& bXboxMediacenter, bool& bSettings)
{
  // load settings file...
  bXboxMediacenter = bSettings = false;

#ifdef _XBOX
  char szDevicePath[1024];
  CStdString strMnt = _P(GetProfileUserDataFolder());
  if (strMnt.Left(2).Equals("Q:"))
  {
    CUtil::GetHomePath(strMnt);
    strMnt += _P(GetProfileUserDataFolder()).substr(2);
  }
  CIoSupport::GetPartition(strMnt.c_str()[0], szDevicePath);
  strcat(szDevicePath,strMnt.c_str()+2);
  CIoSupport::RemapDriveLetter('P', szDevicePath);
#endif
  CSpecialProtocol::SetProfilePath(GetProfileUserDataFolder());
  CLog::Log(LOGNOTICE, "loading %s", GetSettingsFile().c_str());
  if (!LoadSettings(GetSettingsFile()))
  {
    CLog::Log(LOGERROR, "Unable to load %s, creating new %s with default values", GetSettingsFile().c_str(), GetSettingsFile().c_str());
    Save();
    if (!(bSettings = Reset()))
      return false;
  }

  // clear sources, then load xml file...
  m_fileSources.clear();
  m_musicSources.clear();
  m_pictureSources.clear();
  m_programSources.clear();
  m_videoSources.clear();
  CStdString strXMLFile = GetSourcesFile();
  CLog::Log(LOGNOTICE, "%s", strXMLFile.c_str());
  TiXmlDocument xmlDoc;
  TiXmlElement *pRootElement = NULL;
  if ( xmlDoc.LoadFile( strXMLFile ) )
  {
    pRootElement = xmlDoc.RootElement();
    CStdString strValue;
    if (pRootElement)
      strValue = pRootElement->Value();
    if ( strValue != "sources")
      CLog::Log(LOGERROR, "%s sources.xml file does not contain <sources>", __FUNCTION__);
  }
  else if (CFile::Exists(strXMLFile))
    CLog::Log(LOGERROR, "%s Error loading %s: Line %d, %s", __FUNCTION__, strXMLFile.c_str(), xmlDoc.ErrorRow(), xmlDoc.ErrorDesc());

  // look for external sources file
  TiXmlNode *pInclude = pRootElement ? pRootElement->FirstChild("remote") : NULL;
  if (pInclude)
  {
    CStdString strRemoteFile = pInclude->FirstChild()->Value();
    if (!strRemoteFile.IsEmpty())
    {
      CLog::Log(LOGDEBUG, "Found <remote> tag");
      CLog::Log(LOGDEBUG, "Attempting to retrieve remote file: %s", strRemoteFile.c_str());
      // sometimes we have to wait for the network
      if (!g_application.getNetwork().IsAvailable(true) && CFile::Exists(strRemoteFile))
      {
        if ( xmlDoc.LoadFile(strRemoteFile) )
        {
          pRootElement = xmlDoc.RootElement();
          CStdString strValue;
          if (pRootElement)
            strValue = pRootElement->Value();
          if ( strValue != "sources")
            CLog::Log(LOGERROR, "%s remote_sources.xml file does not contain <sources>", __FUNCTION__);
        }
        else
          CLog::Log(LOGERROR, "%s unable to load file: %s, Line %d, %s", __FUNCTION__, strRemoteFile.c_str(), xmlDoc.ErrorRow(), xmlDoc.ErrorDesc());
      }
      else
        CLog::Log(LOGNOTICE, "Could not retrieve remote file, defaulting to local sources");
    }
  }

  if (pRootElement)
  { // parse sources...
    GetSources(pRootElement, "programs", m_programSources, m_defaultProgramSource);
    GetSources(pRootElement, "pictures", m_pictureSources, m_defaultPictureSource);
    GetSources(pRootElement, "files", m_fileSources, m_defaultFileSource);
    GetSources(pRootElement, "music", m_musicSources, m_defaultMusicSource);
    GetSources(pRootElement, "video", m_videoSources, m_defaultVideoSource);
  }

  bXboxMediacenter = true;

  LoadRSSFeeds();
  LoadUserFolderLayout();

  return true;
}

void CSettings::ConvertHomeVar(CStdString& strText)
{
  // Replaces first occurence of $HOME with the home directory.
  // "$HOME\foo" becomes for instance "e:\apps\xbmc\foo"

  char szText[1024];
  char szTemp[1024];
  char *pReplace, *pReplace2;

  CStdString strHomePath = "Q:";
  strcpy(szText, strText.c_str());

  pReplace = strstr(szText, "$HOME");

  if (pReplace != NULL)
  {
    pReplace2 = pReplace + sizeof("$HOME") - 1;
    strcpy(szTemp, pReplace2);
    strcpy(pReplace, strHomePath.c_str() );
    strcat(szText, szTemp);
  }
  strText = szText;
  // unroll any relative paths used
  vector<CStdString> token;
  CUtil::Tokenize(strText,token,"\\");
  if (token.size() > 1)
  {
    strText = "";
    for (unsigned int i=0;i<token.size();++i)
      if (token[i] == "..")
      {
        CStdString strParent;
        URIUtils::GetParentPath(strText,strParent);
        strText = strParent;
      }
      else
        strText += token[i]+"\\";
  }
}

VECSOURCES *CSettings::GetSourcesFromType(const CStdString &type)
{
  if (type == "programs" || type == "myprograms")
    return &m_programSources;
  else if (type == "files")
    return &m_fileSources;
  else if (type == "music")
    return &m_musicSources;
  else if (type == "video")
    return &m_videoSources;
  else if (type == "pictures")
    return &m_pictureSources;

  return NULL;
}

CStdString CSettings::GetDefaultSourceFromType(const CStdString &type)
{
  CStdString defaultShare;
  if (type == "programs" || type == "myprograms")
    defaultShare = m_defaultProgramSource;
  else if (type == "files")
    defaultShare = m_defaultFileSource;
  else if (type == "music")
    defaultShare = m_defaultMusicSource;
  else if (type == "video")
    defaultShare = m_defaultVideoSource;
  else if (type == "pictures")
    defaultShare = m_defaultPictureSource;
  return defaultShare;
}

void CSettings::GetSources(const TiXmlElement* pRootElement, const CStdString& strTagName, VECSOURCES& items, CStdString& strDefault)
{
  //CLog::Log(LOGDEBUG, "  Parsing <%s> tag", strTagName.c_str());
  strDefault = "";

  items.clear();
  const TiXmlNode *pChild = pRootElement->FirstChild(strTagName.c_str());
  if (pChild)
  {
    pChild = pChild->FirstChild();
    while (pChild > 0)
    {
      CStdString strValue = pChild->Value();
      if (strValue == "source" || strValue == "bookmark") // "bookmark" left in for backwards compatibility
      {
        CMediaSource share;
        if (GetSource(strTagName, pChild, share))
        {
          items.push_back(share);
        }
        else
        {
          CLog::Log(LOGERROR, "    Missing or invalid <name> and/or <path> in source");
        }
      }

      if (strValue == "default")
      {
        const TiXmlNode *pValueNode = pChild->FirstChild();
        if (pValueNode)
        {
          const char* pszText = pChild->FirstChild()->Value();
          if (strlen(pszText) > 0)
            strDefault = pszText;
          CLog::Log(LOGDEBUG, "    Setting <default> source to : %s", strDefault.c_str());
        }
      }
      pChild = pChild->NextSibling();
    }
  }
  else
  {
    CLog::Log(LOGDEBUG, "  <%s> tag is missing or sources.xml is malformed", strTagName.c_str());
  }
}

bool CSettings::GetSource(const CStdString &category, const TiXmlNode *source, CMediaSource &share)
{
  //CLog::Log(LOGDEBUG,"    ---- SOURCE START ----");
  const TiXmlNode *pNodeName = source->FirstChild("name");
  CStdString strName;
  if (pNodeName && pNodeName->FirstChild())
  {
    strName = pNodeName->FirstChild()->Value();
    //CLog::Log(LOGDEBUG,"    Found name: %s", strName.c_str());
  }
  // get multiple paths
  vector<CStdString> vecPaths;
  const TiXmlElement *pPathName = source->FirstChildElement("path");
  while (pPathName)
  {
    if (pPathName->FirstChild())
    {
      int pathVersion = 0;
      pPathName->Attribute("pathversion", &pathVersion);
      CStdString strPath = pPathName->FirstChild()->Value();
      strPath = CSpecialProtocol::ReplaceOldPath(strPath, pathVersion);
      // make sure there are no virtualpaths or stack paths defined in xboxmediacenter.xml
      //CLog::Log(LOGDEBUG,"    Found path: %s", strPath.c_str());
      if (!URIUtils::IsStack(strPath))
      {
        // translate special tags
        if (!strPath.IsEmpty() && strPath.at(0) == '$')
        {
          CStdString strPathOld(strPath);
          strPath = CUtil::TranslateSpecialSource(strPath);
          if (!strPath.IsEmpty())
          {
            //CLog::Log(LOGDEBUG,"    -> Translated to path: %s", strPath.c_str());
          }
          else
          {
            //CLog::Log(LOGERROR,"    -> Skipping invalid token: %s", strPathOld.c_str());
            pPathName = pPathName->NextSiblingElement("path");
            continue;
          }
        }
        URIUtils::AddSlashAtEnd(strPath);
        vecPaths.push_back(strPath);
      }
      else
        CLog::Log(LOGERROR,"    Invalid path type (%s) in source", strPath.c_str());
    }
    pPathName = pPathName->NextSiblingElement("path");
  }

  const TiXmlNode *pLockMode = source->FirstChild("lockmode");
  const TiXmlNode *pLockCode = source->FirstChild("lockcode");
  const TiXmlNode *pBadPwdCount = source->FirstChild("badpwdcount");
  const TiXmlNode *pThumbnailNode = source->FirstChild("thumbnail");

  if (!strName.IsEmpty() && vecPaths.size() > 0)
  {
    vector<CStdString> verifiedPaths;
    // disallowed for files, or theres only a single path in the vector
    if ((category.Equals("files")) || (vecPaths.size() == 1))
      verifiedPaths.push_back(vecPaths[0]);

    // multiple paths?
    else
    {
      // validate the paths
      for (int j = 0; j < (int)vecPaths.size(); ++j)
      {
        CURL url(vecPaths[j]);
        CStdString protocol = url.GetProtocol();
        bool bIsInvalid = false;

        // for my programs
        if (category.Equals("programs") || category.Equals("myprograms"))
        {
          // only allow HD and plugins
          if (url.IsLocal() || protocol.Equals("plugin"))
            verifiedPaths.push_back(vecPaths[j]);
          else
            bIsInvalid = true;
        }

        // for others allow everything (if the user does something silly, we can't stop them)
        else
          verifiedPaths.push_back(vecPaths[j]);

        // error message
        if (bIsInvalid)
          CLog::Log(LOGERROR,"    Invalid path type (%s) for multipath source", vecPaths[j].c_str());
      }

      // no valid paths? skip to next source
      if (verifiedPaths.size() == 0)
      {
        CLog::Log(LOGERROR,"    Missing or invalid <name> and/or <path> in source");
        return false;
      }
    }

    share.FromNameAndPaths(category, strName, verifiedPaths);

    share.m_iBadPwdCount = 0;
    if (pLockMode)
    {
      share.m_iLockMode = LockType(atoi(pLockMode->FirstChild()->Value()));
      share.m_iHasLock = 2;
    }

    if (pLockCode)
    {
      if (pLockCode->FirstChild())
        share.m_strLockCode = pLockCode->FirstChild()->Value();
    }

    if (pBadPwdCount)
    {
      if (pBadPwdCount->FirstChild())
        share.m_iBadPwdCount = atoi( pBadPwdCount->FirstChild()->Value() );
    }

    if (pThumbnailNode)
    {
      if (pThumbnailNode->FirstChild())
        share.m_strThumbnailImage = pThumbnailNode->FirstChild()->Value();
    }

    return true;
  }
  return false;
}

bool CSettings::GetPath(const TiXmlElement* pRootElement, const char *tagName, CStdString &strValue)
{
  CStdString strDefault = strValue;
  if (XMLUtils::GetPath(pRootElement, tagName, strValue))
  { // tag exists
    // check for "-" for backward compatibility
    if (!strValue.Equals("-"))
      return true;
  }
  // tag doesn't exist - set default
  strValue = strDefault;
  return false;
}

bool CSettings::GetString(const TiXmlElement* pRootElement, const char *tagName, CStdString &strValue, const CStdString& strDefaultValue)
{
  if (XMLUtils::GetString(pRootElement, tagName, strValue))
  { // tag exists
    // check for "-" for backward compatibility
    if (!strValue.Equals("-"))
      return true;
  }
  // tag doesn't exist - set default
  strValue = strDefaultValue;
  return false;
}

bool CSettings::GetString(const TiXmlElement* pRootElement, const char *tagName, char *szValue, const CStdString& strDefaultValue)
{
  CStdString strValue;
  bool ret = GetString(pRootElement, tagName, strValue, strDefaultValue);
  if (szValue)
    strcpy(szValue, strValue.c_str());
  return ret;
}

bool CSettings::GetInteger(const TiXmlElement* pRootElement, const char *tagName, int& iValue, const int iDefault, const int iMin, const int iMax)
{
  if (XMLUtils::GetInt(pRootElement, tagName, iValue, iMin, iMax))
    return true;
  // default
  iValue = iDefault;
  return false;
}

bool CSettings::GetFloat(const TiXmlElement* pRootElement, const char *tagName, float& fValue, const float fDefault, const float fMin, const float fMax)
{
  if (XMLUtils::GetFloat(pRootElement, tagName, fValue, fMin, fMax))
    return true;
  // default
  fValue = fDefault;
  return false;
}

void CSettings::GetViewState(const TiXmlElement *pRootElement, const CStdString &strTagName, CViewState &viewState, SORT_METHOD defaultSort, int defaultView)
{
  const TiXmlElement* pNode = pRootElement->FirstChildElement(strTagName);
  if (!pNode)
  {
    viewState.m_sortMethod = defaultSort;
    viewState.m_viewMode = defaultView;
    return;
  }
  GetInteger(pNode, "viewmode", viewState.m_viewMode, defaultView, DEFAULT_VIEW_LIST, DEFAULT_VIEW_MAX);

  int sortMethod;
  GetInteger(pNode, "sortmethod", sortMethod, defaultSort, SORT_METHOD_NONE, SORT_METHOD_MAX);
  viewState.m_sortMethod = (SORT_METHOD)sortMethod;

  int sortOrder;
  GetInteger(pNode, "sortorder", sortOrder, SORT_ORDER_ASC, SORT_ORDER_NONE, SORT_ORDER_DESC);
  viewState.m_sortOrder = (SORT_ORDER)sortOrder;
}

void CSettings::SetViewState(TiXmlNode *pRootNode, const CStdString &strTagName, const CViewState &viewState) const
{
  TiXmlElement newElement(strTagName);
  TiXmlNode *pNewNode = pRootNode->InsertEndChild(newElement);
  if (pNewNode)
  {
    XMLUtils::SetInt(pNewNode, "viewmode", viewState.m_viewMode);
    XMLUtils::SetInt(pNewNode, "sortmethod", (int)viewState.m_sortMethod);
    XMLUtils::SetInt(pNewNode, "sortorder", (int)viewState.m_sortOrder);
  }
}

bool CSettings::LoadCalibration(const TiXmlElement* pElement, const CStdString& strSettingsFile)
{
  // reset the calibration to the defaults
  //g_graphicsContext.SetD3DParameters(NULL, m_ResInfo);
  //for (int i=0; i<10; i++)
  //  g_graphicsContext.ResetScreenParameters((RESOLUTION)i);

  const TiXmlElement *pRootElement;
  CStdString strTagName = pElement->Value();
  if (!strcmp(strTagName.c_str(), "calibration"))
  {
    pRootElement = pElement;
  }
  else
  {
    pRootElement = pElement->FirstChildElement("calibration");
  }
  if (!pRootElement)
  {
    g_LoadErrorStr.Format("%s Doesn't contain <calibration>", strSettingsFile.c_str());
    return false;
  }
  const TiXmlElement *pResolution = pRootElement->FirstChildElement("resolution");
  while (pResolution)
  {
    // get the data for this resolution
    int iRes;
    GetInteger(pResolution, "id", iRes, (int)PAL_4x3, HDTV_1080i, PAL60_16x9); //PAL4x3 as default data
    GetString(pResolution, "description", m_ResInfo[iRes].strMode, m_ResInfo[iRes].strMode);
    // get the appropriate "safe graphics area" = 10% for 4x3, 3.5% for 16x9
    float fSafe;
    if (iRes == PAL_4x3 || iRes == NTSC_4x3 || iRes == PAL60_4x3 || iRes == HDTV_480p_4x3)
      fSafe = 0.1f;
    else
      fSafe = 0.035f;
    GetInteger(pResolution, "subtitles", m_ResInfo[iRes].iSubtitles, (int)((1 - fSafe)*m_ResInfo[iRes].iHeight), m_ResInfo[iRes].iHeight / 2, m_ResInfo[iRes].iHeight*5 / 4);
    GetFloat(pResolution, "pixelratio", m_ResInfo[iRes].fPixelRatio, 128.0f / 117.0f, 0.5f, 2.0f);

    // get the overscan info
    const TiXmlElement *pOverscan = pResolution->FirstChildElement("overscan");
    if (pOverscan)
    {
      GetInteger(pOverscan, "left", m_ResInfo[iRes].Overscan.left, 0, -m_ResInfo[iRes].iWidth / 4, m_ResInfo[iRes].iWidth / 4);
      GetInteger(pOverscan, "top", m_ResInfo[iRes].Overscan.top, 0, -m_ResInfo[iRes].iHeight / 4, m_ResInfo[iRes].iHeight / 4);
      GetInteger(pOverscan, "right", m_ResInfo[iRes].Overscan.right, m_ResInfo[iRes].iWidth, m_ResInfo[iRes].iWidth / 2, m_ResInfo[iRes].iWidth*3 / 2);
      GetInteger(pOverscan, "bottom", m_ResInfo[iRes].Overscan.bottom, m_ResInfo[iRes].iHeight, m_ResInfo[iRes].iHeight / 2, m_ResInfo[iRes].iHeight*3 / 2);
    }
    
    CPasswordManager::GetInstance().Clear();

/*    CLog::Log(LOGDEBUG, "  calibration for %s %ix%i", m_ResInfo[iRes].strMode, m_ResInfo[iRes].iWidth, m_ResInfo[iRes].iHeight);
    CLog::Log(LOGDEBUG, "    subtitle yposition:%i pixelratio:%03.3f offsets:(%i,%i)->(%i,%i)",
              m_ResInfo[iRes].iSubtitles, m_ResInfo[iRes].fPixelRatio,
              m_ResInfo[iRes].Overscan.left, m_ResInfo[iRes].Overscan.top,
              m_ResInfo[iRes].Overscan.right, m_ResInfo[iRes].Overscan.bottom);*/

    // iterate around
    pResolution = pResolution->NextSiblingElement("resolution");
  }
  return true;
}

bool CSettings::SaveCalibration(TiXmlNode* pRootNode) const
{
  TiXmlElement xmlRootElement("calibration");
  TiXmlNode *pRoot = pRootNode->InsertEndChild(xmlRootElement);
  for (int i = 0; i < 10; i++)
  {
    // Write the resolution tag
    TiXmlElement resElement("resolution");
    TiXmlNode *pNode = pRoot->InsertEndChild(resElement);
    // Now write each of the pieces of information we need...
    XMLUtils::SetString(pNode, "description", m_ResInfo[i].strMode);
    XMLUtils::SetInt(pNode, "id", i);
    XMLUtils::SetInt(pNode, "subtitles", m_ResInfo[i].iSubtitles);
    XMLUtils::SetFloat(pNode, "pixelratio", m_ResInfo[i].fPixelRatio);
    // create the overscan child
    TiXmlElement overscanElement("overscan");
    TiXmlNode *pOverscanNode = pNode->InsertEndChild(overscanElement);
    XMLUtils::SetInt(pOverscanNode, "left", m_ResInfo[i].Overscan.left);
    XMLUtils::SetInt(pOverscanNode, "top", m_ResInfo[i].Overscan.top);
    XMLUtils::SetInt(pOverscanNode, "right", m_ResInfo[i].Overscan.right);
    XMLUtils::SetInt(pOverscanNode, "bottom", m_ResInfo[i].Overscan.bottom);
  }
  return true;
}

bool CSettings::LoadSettings(const CStdString& strSettingsFile)
{
  // load the xml file
  TiXmlDocument xmlDoc;

  if (!xmlDoc.LoadFile(strSettingsFile))
  {
    g_LoadErrorStr.Format("%s, Line %d\n%s", strSettingsFile.c_str(), xmlDoc.ErrorRow(), xmlDoc.ErrorDesc());
    return false;
  }

  TiXmlElement *pRootElement = xmlDoc.RootElement();
  if (strcmpi(pRootElement->Value(), "settings") != 0)
  {
    g_LoadErrorStr.Format("%s\nDoesn't contain <settings>", strSettingsFile.c_str());
    return false;
  }

  // mymusic settings
  TiXmlElement *pElement = pRootElement->FirstChildElement("mymusic");
  if (pElement)
  {
    TiXmlElement *pChild = pElement->FirstChildElement("playlist");
    if (pChild)
    {
      XMLUtils::GetBoolean(pChild, "repeat", m_bMyMusicPlaylistRepeat);
      XMLUtils::GetBoolean(pChild, "shuffle", m_bMyMusicPlaylistShuffle);
    }
    // if the user happened to reboot in the middle of the scan we save this state
    pChild = pElement->FirstChildElement("scanning");
    if (pChild)
    {
      XMLUtils::GetBoolean(pChild, "isscanning", m_bMyMusicIsScanning);
    }
    GetInteger(pElement, "startwindow", m_iMyMusicStartWindow, WINDOW_MUSIC_FILES, WINDOW_MUSIC_FILES, WINDOW_MUSIC_NAV); //501; view songs
    XMLUtils::GetBoolean(pElement, "songinfoinvis", m_bMyMusicSongInfoInVis);
    XMLUtils::GetBoolean(pElement, "songthumbinvis", m_bMyMusicSongThumbInVis);
    GetPath(pElement, "defaultlibview", m_defaultMusicLibSource);
  }
  // myvideos settings
  pElement = pRootElement->FirstChildElement("myvideos");
  if (pElement)
  {
    GetInteger(pElement, "startwindow", m_iVideoStartWindow, WINDOW_VIDEO_FILES, WINDOW_VIDEO_FILES, WINDOW_VIDEO_NAV);
    GetInteger(pElement, "stackvideomode", m_iMyVideoStack, STACK_NONE, STACK_NONE, STACK_SIMPLE);

    GetPath(pElement, "defaultlibview", m_defaultVideoLibSource);
    GetInteger(pElement, "watchmode", m_iMyVideoWatchMode, VIDEO_SHOW_ALL, VIDEO_SHOW_ALL, VIDEO_SHOW_WATCHED);
    XMLUtils::GetBoolean(pElement, "flatten", m_bMyVideoNavFlatten);

    TiXmlElement *pChild = pElement->FirstChildElement("playlist");
    if (pChild)
    { // playlist
      XMLUtils::GetBoolean(pChild, "repeat", m_bMyVideoPlaylistRepeat);
      XMLUtils::GetBoolean(pChild, "shuffle", m_bMyVideoPlaylistShuffle);
    }
  }

  pElement = pRootElement->FirstChildElement("viewstates");
  if (pElement)
  {
    GetViewState(pElement, "musicnavartists", m_viewStateMusicNavArtists);
    GetViewState(pElement, "musicnavalbums", m_viewStateMusicNavAlbums);
    GetViewState(pElement, "musicnavsongs", m_viewStateMusicNavSongs);
    GetViewState(pElement, "musicshoutcast", m_viewStateMusicShoutcast);
    GetViewState(pElement, "musiclastfm", m_viewStateMusicLastFM);
    GetViewState(pElement, "videonavactors", m_viewStateVideoNavActors);
    GetViewState(pElement, "videonavyears", m_viewStateVideoNavYears);
    GetViewState(pElement, "videonavgenres", m_viewStateVideoNavGenres);
    GetViewState(pElement, "videonavtitles", m_viewStateVideoNavTitles);
    GetViewState(pElement, "videonavepisodes", m_viewStateVideoNavEpisodes, SORT_METHOD_EPISODE);
    GetViewState(pElement, "videonavtvshows", m_viewStateVideoNavTvShows);
    GetViewState(pElement, "videonavseasons", m_viewStateVideoNavSeasons);
    GetViewState(pElement, "videonavmusicvideos", m_viewStateVideoNavMusicVideos);

    GetViewState(pElement, "programs", m_viewStatePrograms, SORT_METHOD_LABEL, DEFAULT_VIEW_AUTO);
    GetViewState(pElement, "pictures", m_viewStatePictures, SORT_METHOD_LABEL, DEFAULT_VIEW_AUTO);
    GetViewState(pElement, "videofiles", m_viewStateVideoFiles, SORT_METHOD_LABEL, DEFAULT_VIEW_AUTO);
    GetViewState(pElement, "musicfiles", m_viewStateMusicFiles, SORT_METHOD_LABEL, DEFAULT_VIEW_AUTO);
  }

  // general settings
  pElement = pRootElement->FirstChildElement("general");
  if (pElement)
  {
    GetInteger(pElement, "systemtotaluptime", m_iSystemTimeTotalUp, 0, 0, INT_MAX);
    GetInteger(pElement, "httpapibroadcastlevel", m_HttpApiBroadcastLevel, 0, 0,5);
    GetInteger(pElement, "httpapibroadcastport", m_HttpApiBroadcastPort, 8278, 1, 65535);
  }

  pElement = pRootElement->FirstChildElement("defaultvideosettings");
  if (pElement)
  {
    int interlaceMethod;
    GetInteger(pElement, "interlacemethod", interlaceMethod, VS_INTERLACEMETHOD_NONE, VS_INTERLACEMETHOD_NONE, VS_INTERLACEMETHOD_DEINTERLACE);
    m_defaultVideoSettings.m_InterlaceMethod = (EINTERLACEMETHOD)interlaceMethod;

    GetFloat(pElement, "filmgrain", m_defaultVideoSettings.m_FilmGrain, 0, 0, 10);
    GetInteger(pElement, "viewmode", m_defaultVideoSettings.m_ViewMode, VIEW_MODE_NORMAL, VIEW_MODE_NORMAL, VIEW_MODE_CUSTOM);
    GetFloat(pElement, "zoomamount", m_defaultVideoSettings.m_CustomZoomAmount, 1.0f, 0.5f, 2.0f);
    GetFloat(pElement, "pixelratio", m_defaultVideoSettings.m_CustomPixelRatio, 1.0f, 0.5f, 2.0f);
    GetFloat(pElement, "volumeamplification", m_defaultVideoSettings.m_VolumeAmplification, VOLUME_DRC_MINIMUM * 0.01f, VOLUME_DRC_MINIMUM * 0.01f, VOLUME_DRC_MAXIMUM * 0.01f);
    GetFloat(pElement, "noisereduction", m_defaultVideoSettings.m_NoiseReduction, 0.0f, 0.0f, 1.0f);
    XMLUtils::GetBoolean(pElement, "postprocess", m_defaultVideoSettings.m_PostProcess);
    GetFloat(pElement, "sharpness", m_defaultVideoSettings.m_Sharpness, 0.0f, -1.0f, 1.0f);
    XMLUtils::GetBoolean(pElement, "outputtoallspeakers", m_defaultVideoSettings.m_OutputToAllSpeakers);
    XMLUtils::GetBoolean(pElement, "showsubtitles", m_defaultVideoSettings.m_SubtitleOn);
    GetFloat(pElement, "brightness", m_defaultVideoSettings.m_Brightness, 50, 0, 100);
    GetFloat(pElement, "contrast", m_defaultVideoSettings.m_Contrast, 50, 0, 100);
    GetFloat(pElement, "gamma", m_defaultVideoSettings.m_Gamma, 20, 0, 100);
    GetFloat(pElement, "audiodelay", m_defaultVideoSettings.m_AudioDelay, 0.0f, -10.0f, 10.0f);
    GetFloat(pElement, "subtitledelay", m_defaultVideoSettings.m_SubtitleDelay, 0.0f, -10.0f, 10.0f);

    m_defaultVideoSettings.m_SubtitleCached = false;
  }
  // audio settings
  pElement = pRootElement->FirstChildElement("audio");
  if (pElement)
  {
    GetInteger(pElement, "volumelevel", m_nVolumeLevel, VOLUME_MAXIMUM, VOLUME_MINIMUM, VOLUME_MAXIMUM);
    GetInteger(pElement, "dynamicrangecompression", m_dynamicRangeCompressionLevel, VOLUME_DRC_MINIMUM, VOLUME_DRC_MINIMUM, VOLUME_DRC_MAXIMUM);
    for (int i = 0; i < 4; i++)
    {
      CStdString setting;
      setting.Format("karaoke%i", i);
#ifndef HAS_XBOX_AUDIO
#define XVOICE_MASK_PARAM_DISABLED (-1.0f)
#endif
      GetFloat(pElement, setting + "energy", m_karaokeVoiceMask[i].energy, XVOICE_MASK_PARAM_DISABLED, XVOICE_MASK_PARAM_DISABLED, 1.0f);
      GetFloat(pElement, setting + "pitch", m_karaokeVoiceMask[i].pitch, XVOICE_MASK_PARAM_DISABLED, XVOICE_MASK_PARAM_DISABLED, 1.0f);
      GetFloat(pElement, setting + "whisper", m_karaokeVoiceMask[i].whisper, XVOICE_MASK_PARAM_DISABLED, XVOICE_MASK_PARAM_DISABLED, 1.0f);
      GetFloat(pElement, setting + "robotic", m_karaokeVoiceMask[i].robotic, XVOICE_MASK_PARAM_DISABLED, XVOICE_MASK_PARAM_DISABLED, 1.0f);
    }
  }

  LoadCalibration(pRootElement, strSettingsFile);
  g_guiSettings.LoadXML(pRootElement);
  LoadSkinSettings(pRootElement);

  // Configure the PlayerCoreFactory
  LoadPlayerCoreFactorySettings("special://xbmc/system/playercorefactory.xml", true);
  LoadPlayerCoreFactorySettings(GetUserDataItem("playercorefactory.xml"), false);

  // Advanced settings
  g_advancedSettings.Load();

  // Default players?
  CLog::Log(LOGNOTICE, "Default Video Player: %s", GetDefaultVideoPlayerName().c_str());
  CLog::Log(LOGNOTICE, "Default Audio Player: %s", GetDefaultAudioPlayerName().c_str());

  // setup logging...
  if (g_guiSettings.GetBool("debug.showloginfo"))
  {
    g_advancedSettings.m_logLevel = std::max(g_advancedSettings.m_logLevelHint, LOG_LEVEL_DEBUG_FREEMEM);
    CLog::SetLogLevel(g_advancedSettings.m_logLevel);
    CLog::Log(LOGNOTICE, "Enabled debug logging due to GUI setting (%d)", g_advancedSettings.m_logLevel);
  }
  
  // Override settings with avpack settings
  if ( GetCurrentProfile().useAvpackSettings())
  {
    CLog::Log(LOGNOTICE, "Per AV pack settings are on");
    LoadAvpackXML();
  }
  else
    CLog::Log(LOGNOTICE, "Per AV pack settings are off");

  return true;
}

bool CSettings::LoadPlayerCoreFactorySettings(const CStdString& fileStr, bool clear)
{
  CLog::Log(LOGNOTICE, "Loading player core factory settings from %s.", fileStr.c_str());
  if (!CFile::Exists(fileStr))
  { // tell the user it doesn't exist
    CLog::Log(LOGNOTICE, "%s does not exist. Skipping.", fileStr.c_str());
    return false;
  }

  TiXmlDocument playerCoreFactoryXML;
  if (!playerCoreFactoryXML.LoadFile(fileStr))
  {
    CLog::Log(LOGERROR, "Error loading %s, Line %d (%s)", fileStr.c_str(), playerCoreFactoryXML.ErrorRow(), playerCoreFactoryXML.ErrorDesc());
    return false;
  }

  return CPlayerCoreFactory::LoadConfiguration(playerCoreFactoryXML.RootElement(), clear);
}

bool CSettings::LoadAvpackXML()
{
  CStdString avpackSettingsXML;
  avpackSettingsXML  = GetAvpackSettingsFile();
  TiXmlDocument avpackXML;
  if (!CFile::Exists(avpackSettingsXML))
  {
    CLog::Log(LOGERROR, "Error loading AV pack settings : %s not found !", avpackSettingsXML.c_str());
    return false;
  }

  CLog::Log(LOGNOTICE, "%s found : loading %s",
    g_videoConfig.GetAVPack().c_str(), avpackSettingsXML.c_str());

  if (!avpackXML.LoadFile(avpackSettingsXML.c_str()))
  {
    CLog::Log(LOGERROR, "Error loading %s, Line %d\n%s",
      avpackSettingsXML.c_str(), avpackXML.ErrorRow(), avpackXML.ErrorDesc());
    return false;
  }

  TiXmlElement *pMainElement = avpackXML.RootElement();
  if (!pMainElement || strcmpi(pMainElement->Value(),"settings") != 0)
  {
    CLog::Log(LOGERROR, "Error loading %s, no <settings> node", avpackSettingsXML.c_str());
    return false;
  }

  TiXmlElement *pRoot = pMainElement->FirstChildElement(g_videoConfig.GetAVPack());
  if (!pRoot)
  {
    CLog::Log(LOGERROR, "Error loading %s, no <%s> node",
      avpackSettingsXML.c_str(), g_videoConfig.GetAVPack().c_str());
    return false;
  }

  // Load guisettings
  g_guiSettings.LoadXML(pRoot);

  // Load calibration
  return LoadCalibration(pRoot, avpackSettingsXML);
}

// Save the avpack settings in the current 'avpacksettings.xml' file
bool CSettings::SaveAvpackXML() const
{
  CStdString avpackSettingsXML;
  avpackSettingsXML  = GetAvpackSettingsFile();

  CLog::Log(LOGNOTICE, "Saving %s settings in %s",
    g_videoConfig.GetAVPack().c_str(), avpackSettingsXML.c_str());

  // The file does not exist : Save defaults
  if (!CFile::Exists(avpackSettingsXML))
    return SaveNewAvpackXML();

  // The file already exists :
  // We need to preserve other avpack settings

  // First load the previous settings
  TiXmlDocument xmlDoc;
  if (!xmlDoc.LoadFile(avpackSettingsXML))
  {
    CLog::Log(LOGERROR, "SaveAvpackSettings : Error loading %s, Line %d\n%s\nCreating new file.",
      avpackSettingsXML.c_str(), xmlDoc.ErrorRow(), xmlDoc.ErrorDesc());
    return SaveNewAvpackXML();
  }

  // Get the main element
  TiXmlElement *pMainElement = xmlDoc.RootElement();
  if (!pMainElement || strcmpi(pMainElement->Value(),"settings") != 0)
  {
    CLog::Log(LOGERROR, "SaveAvpackSettings : Error loading %s, no <settings> node.\nCreating new file.",
      avpackSettingsXML.c_str());
    return SaveNewAvpackXML();
  }

  // Delete the plugged avpack root if it exists, then recreate it
  // TODO : to support custom avpack settings, the two XMLs should
  // be synchronized, not just overwrite the old one
  TiXmlNode *pRoot = pMainElement->FirstChild(g_videoConfig.GetAVPack());
  if (pRoot)
    pMainElement->RemoveChild(pRoot);

  TiXmlElement pluggedNode(g_videoConfig.GetAVPack());
  pRoot = pMainElement->InsertEndChild(pluggedNode);
  if (!pRoot) return false;

  if (!SaveAvpackSettings(pRoot))
    return false;

  return xmlDoc.SaveFile(avpackSettingsXML);
}

// Create an 'avpacksettings.xml' file with in the current profile directory
bool CSettings::SaveNewAvpackXML() const
{
  TiXmlDocument xmlDoc;
  TiXmlElement xmlMainElement("settings");
  TiXmlNode *pMain = xmlDoc.InsertEndChild(xmlMainElement);
  if (!pMain) return false;

  TiXmlElement pluggedNode(g_videoConfig.GetAVPack());
  TiXmlNode *pRoot = pMain->InsertEndChild(pluggedNode);
  if (!pRoot) return false;

  if (!SaveAvpackSettings(pRoot))
    return false;

  return xmlDoc.SaveFile(GetAvpackSettingsFile());
}

// Save avpack settings in the provided xml node
bool CSettings::SaveAvpackSettings(TiXmlNode *io_pRoot) const
{
  TiXmlElement programsNode("myprograms");
  TiXmlNode *pNode = io_pRoot->InsertEndChild(programsNode);
  if (!pNode) return false;
  XMLUtils::SetBoolean(pNode, "gameautoregion", g_guiSettings.GetBool("myprograms.gameautoregion"));
  XMLUtils::SetInt(pNode, "ntscmode", g_guiSettings.GetInt("myprograms.ntscmode"));

  // default video settings
  TiXmlElement videoSettingsNode("defaultvideosettings");
  pNode = io_pRoot->InsertEndChild(videoSettingsNode);
  if (!pNode) return false;
  XMLUtils::SetInt(pNode, "interlacemethod", g_settings.m_defaultVideoSettings.m_InterlaceMethod);
  XMLUtils::SetFloat(pNode, "filmgrain", g_settings.m_currentVideoSettings.m_FilmGrain);
  XMLUtils::SetInt(pNode, "viewmode", g_settings.m_currentVideoSettings.m_ViewMode);
  XMLUtils::SetFloat(pNode, "zoomamount", g_settings.m_currentVideoSettings.m_CustomZoomAmount);
  XMLUtils::SetFloat(pNode, "pixelratio", g_settings.m_currentVideoSettings.m_CustomPixelRatio);
  XMLUtils::SetFloat(pNode, "volumeamplification", g_settings.m_currentVideoSettings.m_VolumeAmplification);
  XMLUtils::SetBoolean(pNode, "outputtoallspeakers", g_settings.m_currentVideoSettings.m_OutputToAllSpeakers);
  XMLUtils::SetBoolean(pNode, "showsubtitles", g_settings.m_currentVideoSettings.m_SubtitleOn);
  XMLUtils::SetFloat(pNode, "brightness", g_settings.m_currentVideoSettings.m_Brightness);
  XMLUtils::SetFloat(pNode, "contrast", g_settings.m_currentVideoSettings.m_Contrast);
  XMLUtils::SetFloat(pNode, "gamma", g_settings.m_currentVideoSettings.m_Gamma);

  TiXmlElement audiooutputNode("audiooutput");
  pNode = io_pRoot->InsertEndChild(audiooutputNode);
  if (!pNode) return false;
  XMLUtils::SetInt(pNode, "mode", g_guiSettings.GetInt("audiooutput.mode"));
  XMLUtils::SetBoolean(pNode, "ac3passthrough", g_guiSettings.GetBool("audiooutput.ac3passthrough"));
  XMLUtils::SetBoolean(pNode, "dtspassthrough", g_guiSettings.GetBool("audiooutput.dtspassthrough"));

  TiXmlElement videooutputNode("videooutput");
  pNode = io_pRoot->InsertEndChild(videooutputNode);
  if (!pNode) return false;
  XMLUtils::SetInt(pNode, "aspect", g_guiSettings.GetInt("videooutput.aspect"));
  XMLUtils::SetBoolean(pNode, "hd480p", g_guiSettings.GetBool("videooutput.hd480p"));
  XMLUtils::SetBoolean(pNode, "hd720p", g_guiSettings.GetBool("videooutput.hd720p"));
  XMLUtils::SetBoolean(pNode, "hd1080i", g_guiSettings.GetBool("videooutput.hd1080i"));

  TiXmlElement videoscreenNode("videoscreen");
  pNode = io_pRoot->InsertEndChild(videoscreenNode);
  if (!pNode) return false;
  XMLUtils::SetInt(pNode, "flickerfilter", g_guiSettings.GetInt("videoscreen.flickerfilter"));
  XMLUtils::SetInt(pNode, "resolution", g_guiSettings.GetInt("videoscreen.resolution"));
  XMLUtils::SetBoolean(pNode, "soften", g_guiSettings.GetBool("videoscreen.soften"));

  TiXmlElement videoplayerNode("videoplayer");
  pNode = io_pRoot->InsertEndChild(videoplayerNode);
  if (!pNode) return false;
  XMLUtils::SetInt(pNode, "displayresolution", g_guiSettings.GetInt("videoplayer.displayresolution"));
  XMLUtils::SetInt(pNode, "flicker", g_guiSettings.GetInt("videoplayer.flicker"));
  XMLUtils::SetBoolean(pNode, "soften", g_guiSettings.GetBool("videoplayer.soften"));

  return SaveCalibration(io_pRoot);
}
bool CSettings::SaveSettings(const CStdString& strSettingsFile, CGUISettings *localSettings /* = NULL */) const
{
  TiXmlDocument xmlDoc;
  TiXmlElement xmlRootElement("settings");
  TiXmlNode *pRoot = xmlDoc.InsertEndChild(xmlRootElement);
  if (!pRoot) return false;
  // write our tags one by one - just a big list for now (can be flashed up later)

  // mymusic settings
  TiXmlElement musicNode("mymusic");
  TiXmlNode *pNode = pRoot->InsertEndChild(musicNode);
  if (!pNode) return false;
  {
    TiXmlElement childNode("playlist");
    TiXmlNode *pChild = pNode->InsertEndChild(childNode);
    if (!pChild) return false;
    XMLUtils::SetBoolean(pChild, "repeat", m_bMyMusicPlaylistRepeat);
    XMLUtils::SetBoolean(pChild, "shuffle", m_bMyMusicPlaylistShuffle);
  }
  {
    TiXmlElement childNode("scanning");
    TiXmlNode *pChild = pNode->InsertEndChild(childNode);
    if (!pChild) return false;
    XMLUtils::SetBoolean(pChild, "isscanning", m_bMyMusicIsScanning);
  }

  XMLUtils::SetInt(pNode, "startwindow", m_iMyMusicStartWindow);
  XMLUtils::SetBoolean(pNode, "songinfoinvis", m_bMyMusicSongInfoInVis);
  XMLUtils::SetBoolean(pNode, "songthumbinvis", m_bMyMusicSongThumbInVis);
  XMLUtils::SetPath(pNode, "defaultlibview", m_defaultMusicLibSource);

  // myvideos settings
  TiXmlElement videosNode("myvideos");
  pNode = pRoot->InsertEndChild(videosNode);
  if (!pNode) return false;

  XMLUtils::SetInt(pNode, "startwindow", m_iVideoStartWindow);

  XMLUtils::SetInt(pNode, "stackvideomode", m_iMyVideoStack);

  XMLUtils::SetPath(pNode, "defaultlibview", m_defaultVideoLibSource);

  XMLUtils::SetInt(pNode, "watchmode", m_iMyVideoWatchMode);
  XMLUtils::SetBoolean(pNode, "flatten", m_bMyVideoNavFlatten);

  { // playlist window
    TiXmlElement childNode("playlist");
    TiXmlNode *pChild = pNode->InsertEndChild(childNode);
    if (!pChild) return false;
    XMLUtils::SetBoolean(pChild, "repeat", m_bMyVideoPlaylistRepeat);
    XMLUtils::SetBoolean(pChild, "shuffle", m_bMyVideoPlaylistShuffle);
  }

  // view states
  TiXmlElement viewStateNode("viewstates");
  pNode = pRoot->InsertEndChild(viewStateNode);
  if (pNode)
  {
    SetViewState(pNode, "musicnavartists", m_viewStateMusicNavArtists);
    SetViewState(pNode, "musicnavalbums", m_viewStateMusicNavAlbums);
    SetViewState(pNode, "musicnavsongs", m_viewStateMusicNavSongs);
    SetViewState(pNode, "musicshoutcast", m_viewStateMusicShoutcast);
    SetViewState(pNode, "musiclastfm", m_viewStateMusicLastFM);
    SetViewState(pNode, "videonavactors", m_viewStateVideoNavActors);
    SetViewState(pNode, "videonavyears", m_viewStateVideoNavYears);
    SetViewState(pNode, "videonavgenres", m_viewStateVideoNavGenres);
    SetViewState(pNode, "videonavtitles", m_viewStateVideoNavTitles);
    SetViewState(pNode, "videonavepisodes", m_viewStateVideoNavEpisodes);
    SetViewState(pNode, "videonavseasons", m_viewStateVideoNavSeasons);
    SetViewState(pNode, "videonavtvshows", m_viewStateVideoNavTvShows);
    SetViewState(pNode, "videonavmusicvideos", m_viewStateVideoNavMusicVideos);

    SetViewState(pNode, "programs", m_viewStatePrograms);
    SetViewState(pNode, "pictures", m_viewStatePictures);
    SetViewState(pNode, "videofiles", m_viewStateVideoFiles);
    SetViewState(pNode, "musicfiles", m_viewStateMusicFiles);
  }

  // general settings
  TiXmlElement generalNode("general");
  pNode = pRoot->InsertEndChild(generalNode);
  if (!pNode) return false;
  XMLUtils::SetInt(pNode, "systemtotaluptime", m_iSystemTimeTotalUp);
  XMLUtils::SetInt(pNode, "httpapibroadcastport", m_HttpApiBroadcastPort);
  XMLUtils::SetInt(pNode, "httpapibroadcastlevel", m_HttpApiBroadcastLevel);

  // default video settings
  TiXmlElement videoSettingsNode("defaultvideosettings");
  pNode = pRoot->InsertEndChild(videoSettingsNode);
  if (!pNode) return false;
  XMLUtils::SetInt(pNode, "interlacemethod", m_defaultVideoSettings.m_InterlaceMethod);
  XMLUtils::SetFloat(pNode, "filmgrain", m_defaultVideoSettings.m_FilmGrain);
  XMLUtils::SetFloat(pNode, "noisereduction", m_defaultVideoSettings.m_NoiseReduction);
  XMLUtils::SetBoolean(pNode, "postprocess", m_defaultVideoSettings.m_PostProcess);
  XMLUtils::SetFloat(pNode, "sharpness", m_defaultVideoSettings.m_Sharpness);
  XMLUtils::SetInt(pNode, "viewmode", m_defaultVideoSettings.m_ViewMode);
  XMLUtils::SetFloat(pNode, "zoomamount", m_defaultVideoSettings.m_CustomZoomAmount);
  XMLUtils::SetFloat(pNode, "pixelratio", m_defaultVideoSettings.m_CustomPixelRatio);
  XMLUtils::SetFloat(pNode, "volumeamplification", m_defaultVideoSettings.m_VolumeAmplification);
  XMLUtils::SetBoolean(pNode, "outputtoallspeakers", m_defaultVideoSettings.m_OutputToAllSpeakers);
  XMLUtils::SetBoolean(pNode, "showsubtitles", m_defaultVideoSettings.m_SubtitleOn);
  XMLUtils::SetFloat(pNode, "brightness", m_defaultVideoSettings.m_Brightness);
  XMLUtils::SetFloat(pNode, "contrast", m_defaultVideoSettings.m_Contrast);
  XMLUtils::SetFloat(pNode, "gamma", m_defaultVideoSettings.m_Gamma);
  XMLUtils::SetFloat(pNode, "audiodelay", m_defaultVideoSettings.m_AudioDelay);
  XMLUtils::SetFloat(pNode, "subtitledelay", m_defaultVideoSettings.m_SubtitleDelay);


  // audio settings
  TiXmlElement volumeNode("audio");
  pNode = pRoot->InsertEndChild(volumeNode);
  if (!pNode) return false;
  XMLUtils::SetInt(pNode, "volumelevel", m_nVolumeLevel);
  XMLUtils::SetInt(pNode, "dynamicrangecompression", m_dynamicRangeCompressionLevel);
  for (int i = 0; i < 4; i++)
  {
    CStdString setting;
    setting.Format("karaoke%i", i);
    XMLUtils::SetFloat(pNode, setting + "energy", m_karaokeVoiceMask[i].energy);
    XMLUtils::SetFloat(pNode, setting + "pitch", m_karaokeVoiceMask[i].pitch);
    XMLUtils::SetFloat(pNode, setting + "whisper", m_karaokeVoiceMask[i].whisper);
    XMLUtils::SetFloat(pNode, setting + "robotic", m_karaokeVoiceMask[i].robotic);
  }

  SaveCalibration(pRoot);

  if (localSettings) // local settings to save
    localSettings->SaveXML(pRoot);
  else // save the global settings
    g_guiSettings.SaveXML(pRoot);

  SaveSkinSettings(pRoot);

  if ( GetCurrentProfile().useAvpackSettings())
    SaveAvpackXML();

  // For mastercode
  SaveProfiles(PROFILES_FILE);

  // save the file
  return xmlDoc.SaveFile(strSettingsFile);
}

bool CSettings::LoadProfile(unsigned int index)
{
  unsigned int oldProfile = m_currentProfile;
  m_currentProfile = index;
  bool bSourcesXML=true;
  CStdString strOldSkin = g_guiSettings.GetString("lookandfeel.skin");
  CStdString strOldFont = g_guiSettings.GetString("lookandfeel.font");
  CStdString strOldTheme = g_guiSettings.GetString("lookandfeel.skintheme");
  CStdString strOldColors = g_guiSettings.GetString("lookandfeel.skincolors");
  //int iOldRes = g_guiSettings.GetInt("videoscreen.resolution");
  if (Load(bSourcesXML,bSourcesXML))
  {
    CreateProfileFolders();

    // initialize our charset converter
    g_charsetConverter.reset();

    // Load the langinfo to have user charset <-> utf-8 conversion
    CStdString strLanguage = g_guiSettings.GetString("locale.language");
    strLanguage[0] = toupper(strLanguage[0]);

    CStdString strLangInfoPath;
    strLangInfoPath.Format("special://xbmc/system/language/%s/langinfo.xml", strLanguage.c_str());
    CLog::Log(LOGINFO, "load language info file:%s", strLangInfoPath.c_str());
    g_langInfo.Load(strLangInfoPath);

#ifdef _XBOX
    CStdString strKeyboardLayoutConfigurationPath;
    strKeyboardLayoutConfigurationPath.Format("special://xbmc/system/language/%s/keyboardmap.xml", strLanguage.c_str());
    CLog::Log(LOGINFO, "load keyboard layout configuration info file: %s", strKeyboardLayoutConfigurationPath.c_str());
    g_keyboardLayoutConfiguration.Load(strKeyboardLayoutConfigurationPath);
#endif

    CButtonTranslator::GetInstance().Load();
    g_localizeStrings.Load("special://xbmc/system/language/", strLanguage);

    g_infoManager.ResetCache();
    g_infoManager.ResetLibraryBools();

    // always reload the skin - we need it for the new language strings
    g_application.LoadSkin(g_guiSettings.GetString("lookandfeel.skin"));

    if (m_currentProfile != 0)
    {
      TiXmlDocument doc;
      if (doc.LoadFile(URIUtils::AddFileToFolder(GetUserDataFolder(),"guisettings.xml")))
        g_guiSettings.LoadMasterLock(doc.RootElement());
    }
    
#ifdef HAS_XBOX_HARDWARE
    if (g_guiSettings.GetBool("system.autotemperature"))
    {
      CLog::Log(LOGNOTICE, "start fancontroller");
      CFanController::Instance()->Start(g_guiSettings.GetInt("system.targettemperature"), g_guiSettings.GetInt("system.minfanspeed"));
    }
    else if (g_guiSettings.GetBool("system.fanspeedcontrol"))
    {
      CLog::Log(LOGNOTICE, "setting fanspeed");
      CFanController::Instance()->SetFanSpeed(g_guiSettings.GetInt("system.fanspeed"));
    }
    g_application.StartLEDControl(false);
#endif

    // to set labels - shares are reloaded
    CDetectDVDMedia::UpdateState();
    // init windows
    CGUIMessage msg(GUI_MSG_NOTIFY_ALL,0,0,GUI_MSG_WINDOW_RESET);
    g_windowManager.SendMessage(msg);

    CUtil::DeleteMusicDatabaseDirectoryCache();
    CUtil::DeleteVideoDatabaseDirectoryCache();

    return true;
  }

  m_currentProfile = oldProfile;

  return false;
}

bool CSettings::DeleteProfile(unsigned int index)
{
  const CProfile *profile = GetProfile(index);
  if (!profile)
    return false;

  CGUIDialogYesNo* dlgYesNo = (CGUIDialogYesNo*)g_windowManager.GetWindow(WINDOW_DIALOG_YES_NO);
  if (dlgYesNo)
  {
    CStdString message;
    CStdString str = g_localizeStrings.Get(13201);
    message.Format(str.c_str(), profile->getName());
    dlgYesNo->SetHeading(13200);
    dlgYesNo->SetLine(0, message);
    dlgYesNo->SetLine(1, "");
    dlgYesNo->SetLine(2, "");
    dlgYesNo->DoModal();

    if (dlgYesNo->IsConfirmed())
    {
      //delete profile
      CStdString strDirectory = profile->getDirectory();
      m_vecProfiles.erase(m_vecProfiles.begin()+index);
      if (index == m_currentProfile)
      {
        LoadProfile(0);
        Save();
      }

      CFileItem item(URIUtils::AddFileToFolder(GetUserDataFolder(), strDirectory));
      item.SetPath(URIUtils::AddFileToFolder(GetUserDataFolder(), strDirectory + "\\"));
      item.m_bIsFolder = true;
      item.Select(true);
      CGUIWindowFileManager::DeleteItem(&item);
    }
    else
      return false;
  }

  SaveProfiles(PROFILES_FILE);
  return true;
}

void CSettings::DeleteAllProfiles()
{
  m_vecProfiles.erase(g_settings.m_vecProfiles.begin()+1,g_settings.m_vecProfiles.end());
}

void CSettings::LoadProfiles(const CStdString& profilesFile)
{
  // clear out our profiles
  m_vecProfiles.clear();

  TiXmlDocument profilesDoc;
  if (CFile::Exists(profilesFile))
  {
    if (profilesDoc.LoadFile(profilesFile))
    {
      TiXmlElement *rootElement = profilesDoc.RootElement();
      if (rootElement && strcmpi(rootElement->Value(),"profiles") == 0)
      {
        XMLUtils::GetUInt(rootElement, "lastloaded", m_lastUsedProfile);
        XMLUtils::GetBoolean(rootElement, "useloginscreen", m_usingLoginScreen);

        TiXmlElement* pProfile = rootElement->FirstChildElement("profile");
        
        CStdString defaultDir("special://home/system/userdata");
        if (!CDirectory::Exists(defaultDir))
          defaultDir = "special://xbmc/userdata";
        while (pProfile)
        {
          CProfile profile(defaultDir);
          profile.Load(pProfile);
          m_vecProfiles.push_back(profile);
          pProfile = pProfile->NextSiblingElement("profile");
        }
      }
      else
        CLog::Log(LOGERROR, "Error loading %s, no <profiles> node", profilesFile.c_str());
    }
    else
      CLog::Log(LOGERROR, "Error loading %s, Line %d\n%s", profilesFile.c_str(), profilesDoc.ErrorRow(), profilesDoc.ErrorDesc());
  }
 
  if (m_vecProfiles.empty())
  { // add the master user
    CProfile profile("special://masterprofile/", "Master user");
    m_vecProfiles.push_back(profile);
  }

  // check the validity of the previous profile index
  if (m_lastUsedProfile >= m_vecProfiles.size())
    m_lastUsedProfile = 0;

  m_currentProfile = m_lastUsedProfile;

  // the login screen runs as the master profile, so if we're using this, we need to ensure
  // we switch to the master profile
  if (m_usingLoginScreen)
    m_currentProfile = 0;
}

bool CSettings::SaveProfiles(const CStdString& profilesFile) const
{
  TiXmlDocument xmlDoc;
  TiXmlElement xmlRootElement("profiles");
  TiXmlNode *pRoot = xmlDoc.InsertEndChild(xmlRootElement);
  if (!pRoot) return false;
  XMLUtils::SetInt(pRoot,"lastloaded", m_currentProfile);
  XMLUtils::SetBoolean(pRoot,"useloginscreen",m_usingLoginScreen);
  for (unsigned int i = 0; i < m_vecProfiles.size(); ++i)
    m_vecProfiles[i].Save(pRoot);
  // save the file
  return xmlDoc.SaveFile(profilesFile);
}

bool CSettings::LoadUPnPXml(const CStdString& strSettingsFile)
{
  TiXmlDocument UPnPDoc;

  if (!CFile::Exists(strSettingsFile))
  { // set defaults, or assume no rss feeds??
    return false;
  }
  if (!UPnPDoc.LoadFile(strSettingsFile))
  {
    CLog::Log(LOGERROR, "Error loading %s, Line %d\n%s", strSettingsFile.c_str(), UPnPDoc.ErrorRow(), UPnPDoc.ErrorDesc());
    return false;
  }

  TiXmlElement *pRootElement = UPnPDoc.RootElement();
  if (!pRootElement || strcmpi(pRootElement->Value(),"upnpserver") != 0)
  {
    CLog::Log(LOGERROR, "Error loading %s, no <upnpserver> node", strSettingsFile.c_str());
    return false;
  }
  // load settings

  // default values for ports
  m_UPnPPortServer = 0;
  m_UPnPPortRenderer = 0;
  m_UPnPMaxReturnedItems = 0;

  XMLUtils::GetString(pRootElement, "UUID", m_UPnPUUIDServer);
  XMLUtils::GetInt(pRootElement, "Port", m_UPnPPortServer);
  XMLUtils::GetInt(pRootElement, "MaxReturnedItems", m_UPnPMaxReturnedItems);
  XMLUtils::GetString(pRootElement, "UUIDRenderer", m_UPnPUUIDRenderer);
  XMLUtils::GetInt(pRootElement, "PortRenderer", m_UPnPPortRenderer);

  return true;
}

bool CSettings::SaveUPnPXml(const CStdString& strSettingsFile) const
{
  TiXmlDocument xmlDoc;
  TiXmlElement xmlRootElement("upnpserver");
  TiXmlNode *pRoot = xmlDoc.InsertEndChild(xmlRootElement);
  if (!pRoot) return false;

  // create a new Element for UUID
  XMLUtils::SetString(pRoot, "UUID", m_UPnPUUIDServer);
  XMLUtils::SetInt(pRoot, "Port", m_UPnPPortServer);
  XMLUtils::SetInt(pRoot, "MaxReturnedItems", m_UPnPMaxReturnedItems);
  XMLUtils::SetString(pRoot, "UUIDRenderer", m_UPnPUUIDRenderer);
  XMLUtils::SetInt(pRoot, "PortRenderer", m_UPnPPortRenderer);

  // save the file
  return xmlDoc.SaveFile(strSettingsFile);
}

bool CSettings::UpdateShare(const CStdString &type, const CStdString oldName, const CMediaSource &share)
{
  VECSOURCES *pShares = GetSourcesFromType(type);

  if (!pShares) return false;

  // update our current share list
  CMediaSource* pShare=NULL;
  for (IVECSOURCES it = pShares->begin(); it != pShares->end(); it++)
  {
    if ((*it).strName == oldName)
    {
      (*it).strName = share.strName;
      (*it).strPath = share.strPath;
      (*it).vecPaths = share.vecPaths;
      pShare = &(*it);
      break;
    }
  }

  if (!pShare)
    return false;

  // Update our XML file as well
  return SaveSources();
}

// NOTE: This function does NOT save the sources.xml file - you need to call SaveSources() separately.
bool CSettings::UpdateSource(const CStdString &strType, const CStdString strOldName, const CStdString &strUpdateElement, const CStdString &strUpdateText)
{
  VECSOURCES *pShares = GetSourcesFromType(strType);

  if (!pShares) return false;

  for (IVECSOURCES it = pShares->begin(); it != pShares->end(); it++)
  {
    if ((*it).strName == strOldName)
    {
      if ("name" == strUpdateElement)
        (*it).strName = strUpdateText;
      else if ("lockmode" == strUpdateElement)
        (*it).m_iLockMode = LockType(atoi(strUpdateText));
      else if ("lockcode" == strUpdateElement)
        (*it).m_strLockCode = strUpdateText;
      else if ("badpwdcount" == strUpdateElement)
        (*it).m_iBadPwdCount = atoi(strUpdateText);
      else if ("thumbnail" == strUpdateElement)
        (*it).m_strThumbnailImage = strUpdateText;
      else if ("path" == strUpdateElement)
      {
        (*it).vecPaths.clear();
        (*it).strPath = strUpdateText;
        (*it).vecPaths.push_back(strUpdateText);
      }
      else
        return false;
      return true;
    }
  }
  return false;
}

bool CSettings::DeleteSource(const CStdString &strType, const CStdString strName, const CStdString strPath, bool virtualSource)
{
  VECSOURCES *pShares = GetSourcesFromType(strType);
  if (!pShares) return false;

  bool found(false);

  for (IVECSOURCES it = pShares->begin(); it != pShares->end(); it++)
  {
    if ((*it).strName == strName && (*it).strPath == strPath)
    {
      CLog::Log(LOGDEBUG,"found share, removing!");
      pShares->erase(it);
      found = true;
      break;
    }
  }

  if (virtualSource)
    return found;

  return SaveSources();
}

bool CSettings::AddShare(const CStdString &type, const CMediaSource &share)
{
  VECSOURCES *pShares = GetSourcesFromType(type);
  if (!pShares) return false;

  // translate dir and add to our current shares
  CStdString strPath1 = share.strPath;
  strPath1.ToUpper();
  if(strPath1.IsEmpty())
  {
    CLog::Log(LOGERROR, "unable to add empty path");
    return false;
  }

  CMediaSource shareToAdd = share;
  if (strPath1.at(0) == '$')
  {
    shareToAdd.strPath = CUtil::TranslateSpecialSource(strPath1);
    if (!share.strPath.IsEmpty())
      CLog::Log(LOGDEBUG, "%s Translated (%s) to Path (%s)",__FUNCTION__ ,strPath1.c_str(),shareToAdd.strPath.c_str());
    else
    {
      CLog::Log(LOGDEBUG, "%s Skipping invalid special directory token: %s",__FUNCTION__,strPath1.c_str());
      return false;
    }
  }
  pShares->push_back(shareToAdd);

  if (!share.m_ignore)
  {
    return SaveSources();
  }
  return true;
}

bool CSettings::SaveSources()
{
  // TODO: Should we be specifying utf8 here??
  TiXmlDocument doc;
  TiXmlElement xmlRootElement("sources");
  TiXmlNode *pRoot = doc.InsertEndChild(xmlRootElement);
  if (!pRoot) return false;

  // ok, now run through and save each sources section
  SetSources(pRoot, "programs", m_programSources, m_defaultProgramSource);
  SetSources(pRoot, "video", m_videoSources, m_defaultVideoSource);
  SetSources(pRoot, "music", m_musicSources, m_defaultMusicSource);
  SetSources(pRoot, "pictures", m_pictureSources, m_defaultPictureSource);
  SetSources(pRoot, "files", m_fileSources, m_defaultFileSource);

  return doc.SaveFile(GetSourcesFile());
}

bool CSettings::SetSources(TiXmlNode *root, const char *section, const VECSOURCES &shares, const char *defaultPath)
{
  TiXmlElement sectionElement(section);
  TiXmlNode *sectionNode = root->InsertEndChild(sectionElement);
  if (sectionNode)
  {
    XMLUtils::SetPath(sectionNode, "default", defaultPath);
    for (unsigned int i = 0; i < shares.size(); i++)
    {
      const CMediaSource &share = shares[i];
      if (share.m_ignore)
        continue;
      TiXmlElement source("source");

      XMLUtils::SetString(&source, "name", share.strName);

      for (unsigned int i = 0; i < share.vecPaths.size(); i++)
        XMLUtils::SetPath(&source, "path", share.vecPaths[i]);

      if (share.m_iHasLock)
      {
        XMLUtils::SetInt(&source, "lockmode", share.m_iLockMode);
        XMLUtils::SetString(&source, "lockcode", share.m_strLockCode);
        XMLUtils::SetInt(&source, "badpwdcount", share.m_iBadPwdCount);
      }
      if (!share.m_strThumbnailImage.IsEmpty())
        XMLUtils::SetPath(&source, "thumbnail", share.m_strThumbnailImage);

      sectionNode->InsertEndChild(source);
    }
  }
  return true;
}

void CSettings::LoadSkinSettings(const TiXmlElement* pRootElement)
{
  int number = 0;
  const TiXmlElement *pElement = pRootElement->FirstChildElement("skinsettings");
  if (pElement)
  {
    m_skinStrings.clear();
    m_skinBools.clear();
    const TiXmlElement *pChild = pElement->FirstChildElement("setting");
    while (pChild)
    {
      CStdString settingName = pChild->Attribute("name");
      if (pChild->Attribute("type") && strcmpi(pChild->Attribute("type"),"string") == 0)
      { // string setting
        CSkinString string;
        string.name = settingName;
        string.value = pChild->FirstChild() ? pChild->FirstChild()->Value() : "";
        m_skinStrings.insert(pair<int, CSkinString>(number++, string));
      }
      else
      { // bool setting
        CSkinBool setting;
        setting.name = settingName;
        setting.value = pChild->FirstChild() ? strcmpi(pChild->FirstChild()->Value(), "true") == 0 : false;
        m_skinBools.insert(pair<int, CSkinBool>(number++, setting));
      }
      pChild = pChild->NextSiblingElement("setting");
    }
  }
}

void CSettings::SaveSkinSettings(TiXmlNode *pRootElement) const
{
  // add the <skinsettings> tag
  TiXmlElement xmlSettingsElement("skinsettings");
  TiXmlNode *pSettingsNode = pRootElement->InsertEndChild(xmlSettingsElement);
  if (!pSettingsNode) return;
  for (map<int, CSkinBool>::const_iterator it = m_skinBools.begin(); it != m_skinBools.end(); ++it)
  {
    // Add a <setting type="bool" name="name">true/false</setting>
    TiXmlElement xmlSetting("setting");
    xmlSetting.SetAttribute("type", "bool");
    xmlSetting.SetAttribute("name", (*it).second.name.c_str());
    TiXmlText xmlBool((*it).second.value ? "true" : "false");
    xmlSetting.InsertEndChild(xmlBool);
    pSettingsNode->InsertEndChild(xmlSetting);
  }
  for (map<int, CSkinString>::const_iterator it = m_skinStrings.begin(); it != m_skinStrings.end(); ++it)
  {
    // Add a <setting type="string" name="name">string</setting>
    TiXmlElement xmlSetting("setting");
    xmlSetting.SetAttribute("type", "string");
    xmlSetting.SetAttribute("name", (*it).second.name.c_str());
    TiXmlText xmlLabel((*it).second.value);
    xmlSetting.InsertEndChild(xmlLabel);
    pSettingsNode->InsertEndChild(xmlSetting);
  }
}

void CSettings::Clear()
{
  m_programSources.clear();
  m_pictureSources.clear();
  m_fileSources.clear();
  m_musicSources.clear();
  m_videoSources.clear();
//  m_vecIcons.clear();
  m_vecProfiles.clear();
  m_mapRssUrls.clear();
  m_skinBools.clear();
  m_skinStrings.clear();
}

int CSettings::TranslateSkinString(const CStdString &setting)
{
  CStdString settingName;
  settingName.Format("%s.%s", g_guiSettings.GetString("lookandfeel.skin").c_str(), setting);
  // run through and see if we have this setting
  for (map<int, CSkinString>::const_iterator it = m_skinStrings.begin(); it != m_skinStrings.end(); it++)
  {
    if (settingName.Equals((*it).second.name))
      return (*it).first;
  }
  // didn't find it - insert it
  CSkinString skinString;
  skinString.name = settingName;
  m_skinStrings.insert(pair<int, CSkinString>(m_skinStrings.size() + m_skinBools.size(), skinString));
  return m_skinStrings.size() + m_skinBools.size() - 1;
}

const CStdString &CSettings::GetSkinString(int setting) const
{
  map<int, CSkinString>::const_iterator it = m_skinStrings.find(setting);
  if (it != m_skinStrings.end())
  {
    return (*it).second.value;
  }
  return StringUtils::EmptyString;
}

void CSettings::SetSkinString(int setting, const CStdString &label)
{
  map<int, CSkinString>::iterator it = m_skinStrings.find(setting);
  if (it != m_skinStrings.end())
  {
    (*it).second.value = label;
    return;
  }
  assert(false);
  CLog::Log(LOGFATAL, "%s : Unknown setting requested", __FUNCTION__);
}

void CSettings::ResetSkinSetting(const CStdString &setting)
{
  CStdString settingName;
  settingName.Format("%s.%s", g_guiSettings.GetString("lookandfeel.skin").c_str(), setting);
  // run through and see if we have this setting as a string
  for (map<int, CSkinString>::iterator it = m_skinStrings.begin(); it != m_skinStrings.end(); it++)
  {
    if (settingName.Equals((*it).second.name))
    {
      (*it).second.value = "";
      return;
    }
  }
  // and now check for the skin bool
  for (map<int, CSkinBool>::iterator it = m_skinBools.begin(); it != m_skinBools.end(); it++)
  {
    if (settingName.Equals((*it).second.name))
    {
      (*it).second.value = false;
      return;
    }
  }
}

int CSettings::TranslateSkinBool(const CStdString &setting)
{
  CStdString settingName;
  settingName.Format("%s.%s", g_guiSettings.GetString("lookandfeel.skin").c_str(), setting);
  // run through and see if we have this setting
  for (map<int, CSkinBool>::const_iterator it = m_skinBools.begin(); it != m_skinBools.end(); it++)
  {
    if (settingName.Equals((*it).second.name))
      return (*it).first;
  }
  // didn't find it - insert it
  CSkinBool skinBool;
  skinBool.name = settingName;
  skinBool.value = false;
  m_skinBools.insert(pair<int, CSkinBool>(m_skinBools.size() + m_skinStrings.size(), skinBool));
  return m_skinBools.size() + m_skinStrings.size() - 1;
}

bool CSettings::GetSkinBool(int setting) const
{
  map<int, CSkinBool>::const_iterator it = m_skinBools.find(setting);
  if (it != m_skinBools.end())
  {
    return (*it).second.value;
  }
  // default is to return false
  return false;
}

void CSettings::SetSkinBool(int setting, bool set)
{
  map<int, CSkinBool>::iterator it = m_skinBools.find(setting);
  if (it != m_skinBools.end())
  {
    (*it).second.value = set;
    return;
  }
  assert(false);
  CLog::Log(LOGFATAL,"%s : Unknown setting requested", __FUNCTION__);
}

void CSettings::ResetSkinSettings()
{
  CStdString currentSkin = g_guiSettings.GetString("lookandfeel.skin") + ".";
  // clear all the settings and strings from this skin.
  map<int, CSkinBool>::iterator it = m_skinBools.begin();
  while (it != m_skinBools.end())
  {
    CStdString skinName = (*it).second.name;
    if (skinName.Left(currentSkin.size()) == currentSkin)
      (*it).second.value = false;

    it++;
  }
  map<int, CSkinString>::iterator it2 = m_skinStrings.begin();
  while (it2 != m_skinStrings.end())
  {
    CStdString skinName = (*it2).second.name;
    if (skinName.Left(currentSkin.size()) == currentSkin)
      (*it2).second.value = "";

    it2++;
  }
  g_infoManager.ResetCache();
}

void CSettings::LoadUserFolderLayout()
{
  // check them all
  CStdString strDir = g_guiSettings.GetString("system.playlistspath");
  if (strDir == "set default")
  {
    strDir = "special://profile/playlists/";
    g_guiSettings.SetString("system.playlistspath",strDir.c_str());
  }
  CDirectory::Create(strDir);
  CDirectory::Create(URIUtils::AddFileToFolder(strDir,"music"));
  CDirectory::Create(URIUtils::AddFileToFolder(strDir,"video"));
  CDirectory::Create(URIUtils::AddFileToFolder(strDir,"mixed"));
}

CStdString CSettings::GetProfileUserDataFolder() const
{
  CStdString folder;
  if (m_currentProfile == 0)
    return GetUserDataFolder();

  URIUtils::AddFileToFolder(GetUserDataFolder(),GetCurrentProfile().getDirectory(),folder);

  return folder;
}

CStdString CSettings::GetUserDataItem(const CStdString& strFile) const
{
  CStdString folder;
  folder = "special://profile/"+strFile;
  //check if item exists in the profile
  //(either for folder or for a file (depending on slashAtEnd of strFile)
  //otherwise return path to masterprofile
  if ( (URIUtils::HasSlashAtEnd(folder) && !CDirectory::Exists(folder)) || !CFile::Exists(folder))
    folder = "special://masterprofile/"+strFile;
  return folder;
}

CStdString CSettings::GetUserDataFolder() const
{
  return GetMasterProfile().getDirectory();
}

CStdString CSettings::GetDatabaseFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Database", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Database", folder);

  return folder;
}

CStdString CSettings::GetCDDBFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Database/CDDB", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Database/CDDB", folder);

  return folder;
}

CStdString CSettings::GetThumbnailsFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails", folder);

  return folder;
}

CStdString CSettings::GetMusicThumbFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/Music", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Music", folder);

  return folder;
}

CStdString CSettings::GetLastFMThumbFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/Music/LastFM", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Music/LastFM", folder);

  return folder;
}

CStdString CSettings::GetMusicArtistThumbFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/Music/Artists", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Music/Artists", folder);

  return folder;
}

CStdString CSettings::GetVideoThumbFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/Video", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Video", folder);

  return folder;
}

CStdString CSettings::GetVideoFanartFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/Video/Fanart", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Video/Fanart", folder);

  return folder;
}

CStdString CSettings::GetMusicFanartFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/Music/Fanart", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Music/Fanart", folder);

  return folder;
}

CStdString CSettings::GetBookmarksThumbFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/Video/Bookmarks", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Video/Bookmarks", folder);

  return folder;
}

CStdString CSettings::GetPicturesThumbFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/Pictures", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Pictures", folder);

  return folder;
}

CStdString CSettings::GetProgramsThumbFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/Programs", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Programs", folder);

  return folder;
}

CStdString CSettings::GetGameSaveThumbFolder() const
{
  CStdString folder;
  if (GetCurrentProfile().hasDatabases())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(), "Thumbnails/GameSaves", folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/GameSaves", folder);

  return folder;
}

CStdString CSettings::GetProfilesThumbFolder() const
{
  CStdString folder;
  URIUtils::AddFileToFolder(GetUserDataFolder(), "Thumbnails/Profiles", folder);

  return folder;
}

CStdString CSettings::GetFFmpegDllFolder() const
{
  CStdString folder = "Q:\\system\\players\\dvdplayer\\";
  if (g_guiSettings.GetBool("videoplayer.allcodecs"))
    folder += "full\\";
  return folder;
}

CStdString CSettings::GetPlayerName(const int& player) const
{
  CStdString strPlayer;
  
  if (player == PLAYER_PAPLAYER)
    strPlayer = "paplayer";
  else
  if (player == PLAYER_MPLAYER)
    strPlayer = "mplayer";
  else
  if (player == PLAYER_DVDPLAYER)
    strPlayer = "dvdplayer";

  return strPlayer;
}

CStdString CSettings::GetDefaultVideoPlayerName() const
{
  return GetPlayerName(g_guiSettings.GetInt("videoplayer.defaultplayer"));
}

CStdString CSettings::GetDefaultAudioPlayerName() const
{
  return GetPlayerName(g_guiSettings.GetInt("musicplayer.defaultplayer"));
}

CStdString CSettings::GetSourcesFile() const
{
  CStdString folder;
  if (GetCurrentProfile().hasSources())
    URIUtils::AddFileToFolder(GetProfileUserDataFolder(),"sources.xml",folder);
  else
    URIUtils::AddFileToFolder(GetUserDataFolder(),"sources.xml",folder);

  return folder;
}

CStdString CSettings::GetSkinFolder() const
{
  CStdString folder;

  // Get the Current Skin Path
  return GetSkinFolder(g_guiSettings.GetString("lookandfeel.skin"));
}

CStdString CSettings::GetScriptsFolder() const
{
  CStdString folder = "special://home/system/scripts";

  if ( CDirectory::Exists(folder) )
    return folder;

  folder = "special://xbmc/system/scripts";
  return folder;
}

CStdString CSettings::GetSkinFolder(const CStdString &skinName) const
{
  CStdString folder;

  // Get the Current Skin Path
  URIUtils::AddFileToFolder("special://home/skins/", skinName, folder);
  if ( ! CDirectory::Exists(folder) )
    URIUtils::AddFileToFolder("special://xbmc/skins/", skinName, folder);

  return folder;
}

void CSettings::LoadRSSFeeds()
{
  CStdString rssXML;
  rssXML = GetUserDataItem("RssFeeds.xml");
  TiXmlDocument rssDoc;
  if (!CFile::Exists(rssXML))
  { // set defaults, or assume no rss feeds??
    return;
  }
  if (!rssDoc.LoadFile(rssXML))
  {
    CLog::Log(LOGERROR, "Error loading %s, Line %d\n%s", rssXML.c_str(), rssDoc.ErrorRow(), rssDoc.ErrorDesc());
    return;
  }

  TiXmlElement *pRootElement = rssDoc.RootElement();
  if (!pRootElement || strcmpi(pRootElement->Value(),"rssfeeds") != 0)
  {
    CLog::Log(LOGERROR, "Error loading %s, no <rssfeeds> node", rssXML.c_str());
    return;
  }

  m_mapRssUrls.clear();
  TiXmlElement* pSet = pRootElement->FirstChildElement("set");
  while (pSet)
  {
    int iId;
    if (pSet->QueryIntAttribute("id", &iId) == TIXML_SUCCESS)
    {
      RssSet set;
      set.rtl = pSet->Attribute("rtl") && stricmp(pSet->Attribute("rtl"),"true")==0;
      TiXmlElement* pFeed = pSet->FirstChildElement("feed");
      while (pFeed)
      {
        int iInterval;
        if ( pFeed->QueryIntAttribute("updateinterval",&iInterval) != TIXML_SUCCESS)
        {
          iInterval=30; // default to 30 min
          CLog::Log(LOGDEBUG,"no interval set, default to 30!");
        }
        if (pFeed->FirstChild())
        {
          // TODO: UTF-8: Do these URLs need to be converted to UTF-8?
          //              What about the xml encoding?
          CStdString strUrl = pFeed->FirstChild()->Value();
          set.url.push_back(strUrl);
          set.interval.push_back(iInterval);
        }
        pFeed = pFeed->NextSiblingElement("feed");
      }
      m_mapRssUrls.insert(make_pair(iId,set));
    }
    else
      CLog::Log(LOGERROR,"found rss url set with no id in RssFeeds.xml, ignored");

    pSet = pSet->NextSiblingElement("set");
  }
}

CStdString CSettings::GetSettingsFile() const
{
  CStdString settings;
  if (m_currentProfile == 0)
    settings = "special://masterprofile/guisettings.xml";
  else
    settings = "special://profile/guisettings.xml";
  return settings;
}

CStdString CSettings::GetAvpackSettingsFile() const
{
  CStdString  strAvpackSettingsFile;
  if (m_currentProfile == 0)
    strAvpackSettingsFile = "T:\\avpacksettings.xml";
  else
    strAvpackSettingsFile = "P:\\avpacksettings.xml";
  return strAvpackSettingsFile;
}

void CSettings::CreateProfileFolders()
{
  CDirectory::Create(GetDatabaseFolder());
  CDirectory::Create(GetCDDBFolder());

  // Thumbnails/
  CDirectory::Create(GetThumbnailsFolder());
  CDirectory::Create(GetMusicThumbFolder());
  CDirectory::Create(GetMusicArtistThumbFolder());
  CDirectory::Create(GetLastFMThumbFolder());
  CDirectory::Create(GetVideoThumbFolder());
  CDirectory::Create(GetVideoFanartFolder());
  CDirectory::Create(GetMusicFanartFolder());
  CDirectory::Create(GetBookmarksThumbFolder());
  CDirectory::Create(GetProgramsThumbFolder());
  CDirectory::Create(GetPicturesThumbFolder());
  CDirectory::Create(GetGameSaveThumbFolder());
  CLog::Log(LOGINFO, "thumbnails folder: %s", GetThumbnailsFolder().c_str());
  for (unsigned int hex=0; hex < 16; hex++)
  {
    CStdString strHex;
    strHex.Format("%x",hex);
    CDirectory::Create(URIUtils::AddFileToFolder(GetPicturesThumbFolder(), strHex));
    CDirectory::Create(URIUtils::AddFileToFolder(GetMusicThumbFolder(), strHex));
    CDirectory::Create(URIUtils::AddFileToFolder(GetVideoThumbFolder(), strHex));
    CDirectory::Create(URIUtils::AddFileToFolder(GetProgramsThumbFolder(), strHex));
  }
  CDirectory::Create("special://profile/visualisations");
}

static CProfile emptyProfile;

const CProfile &CSettings::GetMasterProfile() const
{
  if (GetNumProfiles())
    return m_vecProfiles[0];
  CLog::Log(LOGERROR, "%s - master profile requested while none exists", __FUNCTION__);
  return emptyProfile;
}

const CProfile &CSettings::GetCurrentProfile() const
{
  if (m_currentProfile < m_vecProfiles.size())
    return m_vecProfiles[m_currentProfile];
  CLog::Log(LOGERROR, "%s - last profile index (%u) is outside the valid range (%u)", __FUNCTION__, m_currentProfile, m_vecProfiles.size());
  return emptyProfile;
}

void CSettings::UpdateCurrentProfileDate()
{
  if (m_currentProfile < m_vecProfiles.size())
    m_vecProfiles[m_currentProfile].setDate();
}

const CProfile *CSettings::GetProfile(unsigned int index) const
{
  if (index < GetNumProfiles())
    return &m_vecProfiles[index];
  return NULL;
}

CProfile *CSettings::GetProfile(unsigned int index)
{
  if (index < GetNumProfiles())
    return &m_vecProfiles[index];
  return NULL;
}

unsigned int CSettings::GetNumProfiles() const
{
  return m_vecProfiles.size();
}

int CSettings::GetProfileIndex(const CStdString &name) const
{
  for (unsigned int i = 0; i < m_vecProfiles.size(); i++)
    if (m_vecProfiles[i].getName().Equals(name))
      return i;
  return -1;
}

void CSettings::AddProfile(const CProfile &profile)
{
  m_vecProfiles.push_back(profile);
}

void CSettings::LoadMasterForLogin()
{
  // save the previous user
  m_lastUsedProfile = m_currentProfile;
  if (m_currentProfile != 0)
    LoadProfile(0);
}
