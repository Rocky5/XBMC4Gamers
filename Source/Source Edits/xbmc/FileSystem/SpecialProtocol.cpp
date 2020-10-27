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
#include "utils/log.h"
#include "SpecialProtocol.h"
#include "URL.h"
#include "Util.h"
#include "settings/GUISettings.h"
#include "settings/Settings.h"
#include "utils/URIUtils.h"
#include "xbox/IoSupport.h"

#ifdef _LINUX
#include <dirent.h>
#endif

using namespace std;

map<CStdString, CStdString> CSpecialProtocol::m_pathMap;

void CSpecialProtocol::SetProfilePath(const CStdString &dir)
{
  SetPath("profile", dir);
  CLog::Log(LOGNOTICE, "special://profile/ is mapped to: %s", GetPath("profile").c_str());
}

void CSpecialProtocol::SetXBMCPath(const CStdString &dir)
{
  SetPath("xbmc", dir);
}

void CSpecialProtocol::SetHomePath(const CStdString &dir)
{
  SetPath("home", dir);
}

void CSpecialProtocol::SetRootPath(const CStdString &dir)
{
  SetPath("root", dir);
}

void CSpecialProtocol::SetURLDownloaderPath(const CStdString &dir)
{
  SetPath("urldownloader", dir);
}

void CSpecialProtocol::SetScriptsPath(const CStdString &dir)
{
  SetPath("scripts", dir);
}

void CSpecialProtocol::SetUserHomePath(const CStdString &dir)
{
  SetPath("userhome", dir);
}

void CSpecialProtocol::SetMasterProfilePath(const CStdString &dir)
{
  SetPath("masterprofile", dir);
}

void CSpecialProtocol::SetTempPath(const CStdString &dir)
{
  SetPath("temp", dir);
}

bool CSpecialProtocol::XBMCIsHome()
{
  return TranslatePath("special://xbmc") == TranslatePath("special://home");
}

bool CSpecialProtocol::ComparePath(const CStdString &path1, const CStdString &path2)
{
  return TranslatePath(path1) == TranslatePath(path2);
}

CStdString CSpecialProtocol::TranslatePath(const CStdString &path)
{
  CURL url(path);
  if (!url.GetProtocol().Equals("special"))
  {
    return path;
  }
  
  return TranslatePath(url);
}

CStdString CSpecialProtocol::TranslatePath(const CURL &url)
{
  // check for special-protocol, if not, return
  if (!url.GetProtocol().Equals("special"))
  {
    return url.Get();
  }

  CStdString FullFileName = url.GetFileName();

  CStdString translatedPath;
  CStdString FileName;
  CStdString RootDir;

  // Split up into the special://root and the rest of the filename
  int pos = FullFileName.Find('/');
  if (pos != -1 && pos > 1)
  {
    RootDir = FullFileName.Left(pos);

    if (pos < FullFileName.GetLength())
      FileName = FullFileName.Mid(pos + 1);
  }
  else
    RootDir = FullFileName;

  if (RootDir.Equals("subtitles"))
    URIUtils::AddFileToFolder(g_guiSettings.GetString("subtitles.custompath"), FileName, translatedPath);
  else if (RootDir.Equals("userdata"))
    URIUtils::AddFileToFolder(g_settings.GetUserDataFolder(), FileName, translatedPath);
  else if (RootDir.Equals("database"))
    URIUtils::AddFileToFolder(g_settings.GetDatabaseFolder(), FileName, translatedPath);
  else if (RootDir.Equals("thumbnails"))
    URIUtils::AddFileToFolder(g_settings.GetThumbnailsFolder(), FileName, translatedPath);
  else if (RootDir.Equals("recordings") || RootDir.Equals("cdrips"))
    URIUtils::AddFileToFolder(g_guiSettings.GetString("audiocds.recordingpath", false), FileName, translatedPath);
  else if (RootDir.Equals("screenshots"))
    URIUtils::AddFileToFolder(g_guiSettings.GetString("debug.screenshotpath", false), FileName, translatedPath);
  else if (RootDir.Equals("musicplaylists"))
    URIUtils::AddFileToFolder(CUtil::MusicPlaylistsLocation(), FileName, translatedPath);
  else if (RootDir.Equals("videoplaylists"))
    URIUtils::AddFileToFolder(CUtil::VideoPlaylistsLocation(), FileName, translatedPath);
  else if (RootDir.Equals("skin"))
    URIUtils::AddFileToFolder(g_graphicsContext.GetMediaDir(), FileName, translatedPath);

  // from here on, we have our "real" special paths
  else if (RootDir.Equals("xbmc"))
    URIUtils::AddFileToFolder(GetPath("xbmc"), FileName, translatedPath);
  else if (RootDir.Equals("home"))
    URIUtils::AddFileToFolder(GetPath("home"), FileName, translatedPath);
  else if (RootDir.Equals("root"))
    URIUtils::AddFileToFolder(GetPath("root"), FileName, translatedPath);
  else if (RootDir.Equals("urldownloader"))
    URIUtils::AddFileToFolder(GetPath("urldownloader"), FileName, translatedPath);
  else if (RootDir.Equals("scripts"))
    URIUtils::AddFileToFolder(GetPath("scripts"), FileName, translatedPath);
  else if (RootDir.Equals("userhome"))
    URIUtils::AddFileToFolder(GetPath("userhome"), FileName, translatedPath);
  else if (RootDir.Equals("temp"))
    URIUtils::AddFileToFolder(GetPath("temp"), FileName, translatedPath);
  else if (RootDir.Equals("profile"))
    URIUtils::AddFileToFolder(GetPath("profile"), FileName, translatedPath);
  else if (RootDir.Equals("masterprofile"))
    URIUtils::AddFileToFolder(GetPath("masterprofile"), FileName, translatedPath);

  // check if we need to recurse in
  if (URIUtils::IsSpecial(translatedPath))
  { // we need to recurse in, as there may be multiple translations required
    return TranslatePath(translatedPath);
  }

  // Validate the final path, just in case
  return CUtil::ValidatePath(translatedPath);
}

CStdString CSpecialProtocol::TranslatePathConvertCase(const CStdString& path)
{
  CStdString translatedPath = TranslatePath(path);

#ifdef _LINUX
  if (translatedPath.Find("://") > 0)
    return translatedPath;

  // If the file exists with the requested name, simply return it
  struct stat stat_buf;
  if (stat(translatedPath.c_str(), &stat_buf) == 0)
    return translatedPath;

  CStdString result;
  vector<CStdString> tokens;
  CUtil::Tokenize(translatedPath, tokens, "/");
  CStdString file;
  DIR* dir;
  struct dirent* de;

  for (unsigned int i = 0; i < tokens.size(); i++)
  {
    file = result + "/" + tokens[i];
    if (stat(file.c_str(), &stat_buf) == 0)
    {
      result += "/" + tokens[i];
    }
    else
    {
      dir = opendir(result.c_str());
      if (dir)
      {
        while ((de = readdir(dir)) != NULL)
        {
          // check if there's a file with same name but different case
          if (strcasecmp(de->d_name, tokens[i]) == 0)
          {
            result += "/";
            result += de->d_name;
            break;
          }
        }

        // if we did not find any file that somewhat matches, just
        // fallback but we know it's not gonna be a good ending
        if (de == NULL)
          result += "/" + tokens[i];

        closedir(dir);
      }
      else
      { // this is just fallback, we won't succeed anyway...
        result += "/" + tokens[i];
      }
    }
  }

  return result;
#else
  return translatedPath;
#endif
}

CStdString CSpecialProtocol::ReplaceOldPath(const CStdString &oldPath, int pathVersion)
{
  if (pathVersion < 1)
  {
    if (oldPath.Left(2).CompareNoCase("P:") == 0)
      return URIUtils::AddFileToFolder("special://profile/", oldPath.Mid(2));
    else if (oldPath.Left(2).CompareNoCase("Q:") == 0)
      return URIUtils::AddFileToFolder("special://xbmc/", oldPath.Mid(2));
    else if (oldPath.Left(2).CompareNoCase("T:") == 0)
      return URIUtils::AddFileToFolder("special://masterprofile/", oldPath.Mid(2));
    else if (oldPath.Left(2).CompareNoCase("U:") == 0)
      return URIUtils::AddFileToFolder("special://home/", oldPath.Mid(2));
    else if (oldPath.Left(2).CompareNoCase("R:") == 0)
      return URIUtils::AddFileToFolder("special://root/", oldPath.Mid(2));
    else if (oldPath.Left(2).CompareNoCase("Z:") == 0)
      return URIUtils::AddFileToFolder("special://temp/", oldPath.Mid(2));
  }
  return oldPath;
}

void CSpecialProtocol::LogPaths()
{
  CLog::Log(LOGNOTICE, "special://xbmc/ is mapped to: %s", GetPath("xbmc").c_str());
  CLog::Log(LOGNOTICE, "special://masterprofile/ is mapped to: %s", GetPath("masterprofile").c_str());
  CLog::Log(LOGNOTICE, "special://home/ is mapped to: %s", GetPath("home").c_str());
  CLog::Log(LOGNOTICE, "special://root/ is mapped to: %s", GetPath("root").c_str());
  CLog::Log(LOGNOTICE, "special://urldownloader/ is mapped to: %s", GetPath("urldownloader").c_str());
  CLog::Log(LOGNOTICE, "special://scripts/ is mapped to: %s", GetPath("scripts").c_str());
  CLog::Log(LOGNOTICE, "special://temp/ is mapped to: %s", GetPath("temp").c_str());
  //CLog::Log(LOGNOTICE, "special://userhome/ is mapped to: %s", GetPath("userhome").c_str());
}

// private routines, to ensure we only set/get an appropriate path
void CSpecialProtocol::SetPath(const CStdString &key, const CStdString &path)
{
  m_pathMap[key] = path;
}

CStdString CSpecialProtocol::GetPath(const CStdString &key)
{
  map<CStdString, CStdString>::iterator it = m_pathMap.find(key);
  if (it != m_pathMap.end())
    return it->second;
  assert(false);
  return "";
}
