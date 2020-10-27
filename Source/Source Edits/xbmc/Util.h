#pragma once
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
#include <vector>
#include "MediaSource.h"
#include "interfaces/Builtins.h"
#ifdef HAS_XBOX_HARDWARE
#include "xbox/custom_launch_params.h"
#else
typedef void CUSTOM_LAUNCH_DATA;
#endif

// A list of filesystem types for LegalPath/FileName
#define LEGAL_NONE            0
#define LEGAL_WIN32_COMPAT    1
#define LEGAL_FATX            2

namespace XFILE
{
  class IFileCallback;
}

class CFileItem;
class CFileItemList;
class CURL;
class CTrainer;

// for 'cherry' patching
typedef enum
{
  COUNTRY_NULL = 0,
  COUNTRY_USA,
  COUNTRY_JAP,
  COUNTRY_EUR
} F_COUNTRY;

typedef enum
{
  VIDEO_NULL = 0,
  VIDEO_NTSCM,
  VIDEO_NTSCJ,
  VIDEO_PAL50,
  VIDEO_PAL60
} F_VIDEO;

struct sortstringbyname
{
  bool operator()(const CStdString& strItem1, const CStdString& strItem2)
  {
    CStdString strLine1 = strItem1;
    CStdString strLine2 = strItem2;
    strLine1 = strLine1.ToLower();
    strLine2 = strLine2.ToLower();
    return strcmp(strLine1.c_str(), strLine2.c_str()) < 0;
  }
};

struct XBOXDETECTION
{
  std::vector<CStdString> client_ip;
  std::vector<CStdString> client_info;
  std::vector<unsigned int> client_lookup_count;
  std::vector<bool> client_informed;
};

class CUtil
{
public:
  CUtil(void);
  virtual ~CUtil(void);
  static bool GetVolumeFromFileName(const CStdString& strFileName, CStdString& strFileTitle, CStdString& strVolumeNumber);
  static void CleanString(const CStdString& strFileName, CStdString& strTitle, CStdString& strTitleAndYear, CStdString& strYear, bool bRemoveExtension = false, bool bCleanChars = true);
  static CStdString GetTitleFromPath(const CStdString& strFileNameAndPath, bool bIsFolder = false);
  static void GetQualifiedFilename(const CStdString &strBasePath, CStdString &strFilename);
  static bool InstallTrainer(CTrainer& trainer);
  static bool RemoveTrainer();
  static bool PatchCountryVideo(F_COUNTRY Country, F_VIDEO Video);
  static void RunShortcut(const char* szPath);
  static void RunXBE(const char* szPath, char* szParameters = NULL, F_VIDEO ForceVideo=VIDEO_NULL, F_COUNTRY ForceCountry=COUNTRY_NULL, CUSTOM_LAUNCH_DATA* pData=NULL);
  static void LaunchXbe(const char* szPath, const char* szXbe, const char* szParameters, F_VIDEO ForceVideo=VIDEO_NULL, F_COUNTRY ForceCountry=COUNTRY_NULL, CUSTOM_LAUNCH_DATA* pData=NULL); 
  static void GetHomePath(CStdString& strPath);
  static bool ExcludeFileOrFolder(const CStdString& strFileOrFolder, const CStdStringArray& regexps);
  static void GetFileAndProtocol(const CStdString& strURL, CStdString& strDir);
  static int GetDVDIfoTitle(const CStdString& strPathFile);
  static bool CacheXBEIcon(const CStdString& strFilePath, const CStdString& strIcon);
  static bool GetXBEDescription(const CStdString& strFileName, CStdString& strDescription);
  static bool SetXBEDescription(const CStdString& strFileName, const CStdString& strDescription);
  static DWORD GetXbeID( const CStdString& strFilePath);
  static bool GetDirectoryName(const CStdString& strFileName, CStdString& strDescription);
  static void CreateShortcuts(CFileItemList &items);
  static void CreateShortcut(CFileItem* pItem);
  static void GetFatXQualifiedPath(CStdString& strFileNameAndPath);
  static bool ShortenFileName(CStdString& strFileNameAndPath);
  static bool IsWritable(const CStdString& strFile);
  static bool IsPicture(const CStdString& strFile);
  static void GetDVDDriveIcon( const CStdString& strPath, CStdString& strIcon );
  static void RemoveTempFiles();
  static void DeleteGUISettings();

  static void RemoveIllegalChars( CStdString& strText);
  static void CacheSubtitles(const CStdString& strMovie, CStdString& strExtensionCached, XFILE::IFileCallback *pCallback = NULL);
  static bool CacheRarSubtitles(const CStdString& strRarPath, const CStdString& strCompare);
  static void ClearSubtitles();
  static void PrepareSubtitleFonts();
  static __int64 ToInt64(DWORD dwHigh, DWORD dwLow);
  static bool ThumbExists(const CStdString& strFileName, bool bAddCache = false);
  static bool ThumbCached(const CStdString& strFileName);
  static void ThumbCacheAdd(const CStdString& strFileName, bool bFileExists);
  static void ThumbCacheClear();
  static void PlayDVD();
  static CStdString GetNextFilename(const CStdString &fn_template, int max);
  static void TakeScreenshot();
  static void TakeScreenshot(const CStdString& strFileName, bool flash);
  static void SetBrightnessContrastGamma(float Brightness, float Contrast, float Gamma, bool bImmediate);
  static void SetBrightnessContrastGammaPercent(float brightness, float contrast, float gamma, bool immediate);
  static void Tokenize(const CStdString& path, std::vector<CStdString>& tokens, const std::string& delimiters);
  static void FlashScreen(bool bImmediate, bool bOn);
  static void RestoreBrightnessContrastGamma();
  static void InitGamma();
  static void StatToStatI64(struct _stati64 *result, struct stat *stat);
  static void Stat64ToStatI64(struct _stati64 *result, struct __stat64 *stat);
  static void StatI64ToStat64(struct __stat64 *result, struct _stati64 *stat);
  static void Stat64ToStat(struct _stat *result, struct __stat64 *stat);
  static bool CreateDirectoryEx(const CStdString& strPath);

#ifdef _WIN32
  static CStdString MakeLegalFileName(const CStdString &strFile, int LegalType=LEGAL_WIN32_COMPAT);
  static CStdString MakeLegalPath(const CStdString &strPath, int LegalType=LEGAL_WIN32_COMPAT);
#else
  static CStdString MakeLegalFileName(const CStdString &strFile, int LegalType=LEGAL_NONE);
  static CStdString MakeLegalPath(const CStdString &strPath, int LegalType=LEGAL_NONE);
#endif
  static CStdString ValidatePath(const CStdString &path, bool bFixDoubleSlashes = false); ///< return a validated path, with correct directory separators.
  
  static bool IsUsingTTFSubtitles();
  static void SplitParams(const CStdString &paramString, std::vector<CStdString> &parameters);
  static void SplitExecFunction(const CStdString &execString, CStdString &function, std::vector<CStdString> &parameters);
  static int GetMatchingSource(const CStdString& strPath, VECSOURCES& VECSOURCES, bool& bIsSourceName);
  static CStdString TranslateSpecialSource(const CStdString &strSpecial);
  static void DeleteDirectoryCache(const CStdString &prefix = "");
  static void DeleteMusicDatabaseDirectoryCache();
  static void DeleteVideoDatabaseDirectoryCache();
  static CStdString MusicPlaylistsLocation();
  static CStdString VideoPlaylistsLocation();

  static bool SetSysDateTimeYear(int iYear, int iMonth, int iDay, int iHour, int iMinute);
  static int GMTZoneCalc(int iRescBiases, int iHour, int iMinute, int &iMinuteNew);
  static bool GetFTPServerUserName(int iFTPUserID, CStdString &strFtpUser1, int &iUserMax );
  static bool SetFTPServerUserPassword(CStdString strFtpUserName, CStdString strFtpUserPassword);
  static bool SetXBOXNickName(CStdString strXboxNickNameIn, CStdString &strXboxNickNameOut);
  static bool GetXBOXNickName(CStdString &strXboxNickNameOut);
  static bool AutoDetectionPing(CStdString strFTPUserName, CStdString strFTPPass, CStdString strNickName, int iFTPPort);
  static bool AutoDetection();
  static void AutoDetectionGetSource(VECSOURCES &share);
  static void GetSkinThemes(std::vector<CStdString>& vecTheme);
  static void GetRecursiveListing(const CStdString& strPath, CFileItemList& items, const CStdString& strMask, bool bUseFileDirectories=false);
  static void GetRecursiveDirsListing(const CStdString& strPath, CFileItemList& items);
  static void WipeDir(const CStdString& strPath);
  static void ForceForwardSlashes(CStdString& strPath);
  static bool PWMControl(const CStdString &strRGBa, const CStdString &strRGBb, const CStdString &strWhiteA, const CStdString &strWhiteB, const CStdString &strTransition, int iTrTime);
  static bool RunFFPatchedXBE(CStdString szPath1, CStdString& szNewPath, CStdString& szBuiltin);
  static void RemoveKernelPatch();
  static void initilise();
  static bool LookForKernelPatch();

  static double AlbumRelevance(const CStdString& strAlbumTemp1, const CStdString& strAlbum1, const CStdString& strArtistTemp1, const CStdString& strArtist1);
  static bool MakeShortenPath(CStdString StrInput, CStdString& StrOutput, int iTextMaxLength);
  static float CurrentCpuUsage();
  /*! \brief Checks wether the supplied path supports Write file operations (e.g. Rename, Delete, ...)

   \param strPath the path to be checked

   \return true if Write file operations are supported, false otherwise
   */
  static bool SupportsWriteFileOperations(const CStdString& strPath);
  /*! \brief Checks wether the supplied path supports Read file operations (e.g. Copy, ...)

   \param strPath the path to be checked

   \return true if Read file operations are supported, false otherwise
   */
  static bool SupportsReadFileOperations(const CStdString& strPath);

  static CStdString GetCachedMusicThumb(const CStdString &path);
  static CStdString GetCachedAlbumThumb(const CStdString &album, const CStdString &artist);
  static CStdString GetDefaultFolderThumb(const CStdString &folderThumb);

  static void BootToDash();
  
  static void InitRandomSeed();

  // Get decimal integer representation of roman digit, ivxlcdm are valid
  // return 0 for other chars;
  static int LookupRomanDigit(char roman_digit);
  // Translate a string of roman numerals to decimal a decimal integer
  // return -1 on error, valid range is 1-3999
  static int TranslateRomanNumeral(const char* roman_numeral);
};


