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
//-----------------------------------------------------------------------
//
//  File:      utils/StringUtils.h
//
//  Purpose:   ATL split string utility
//  Author:    Paul J. Weiss
//
//  Modified to support J O'Leary's CStdString class by kraqh3d
//
//------------------------------------------------------------------------

#ifndef __STRINGUTILS_H_
#define __STRINGUTILS_H_

#include "xbox/PlatformDefs.h"
#include "XBDateTime.h"
#include "utils/StdString.h"
#include <vector>

class StringUtils
{
public:
  static void JoinString(const CStdStringArray &strings, const CStdString& delimiter, CStdString& result);
  static CStdString JoinString(const CStdStringArray &strings, const CStdString& delimiter);
  static CStdString Join(const std::vector<std::string> &strings, const CStdString& delimiter);
  static int SplitString(const CStdString& input, const CStdString& delimiter, CStdStringArray &results, unsigned int iMaxStrings = 0);
  static CStdStringArray SplitString(const CStdString& input, const CStdString& delimiter, unsigned int iMaxStrings = 0);
  static std::vector<std::string> Split(const CStdString& input, const CStdString& delimiter, unsigned int iMaxStrings = 0);
  static int FindNumber(const CStdString& strInput, const CStdString &strFind);
  static int64_t AlphaNumericCompare(const char *left, const char *right);
  static long TimeStringToSeconds(const CStdString &timeString);
  static void RemoveCRLF(CStdString& strLine);

  /*! \brief convert a time in seconds to a string based on the given time format
   \param seconds time in seconds
   \param format the format we want the time in.
   \return the formatted time
   \sa TIME_FORMAT
   */
  static CStdString SecondsToTimeString(long seconds, TIME_FORMAT format = TIME_FORMAT_GUESS);

  static bool EqualsNoCase(const std::string &str1, const std::string &str2);
  static bool EqualsNoCase(const std::string &str1, const char *s2);
  static bool EqualsNoCase(const char *s1, const char *s2);
  
  static bool IsNaturalNumber(const CStdString& str);
  static bool IsInteger(const CStdString& str);
  static CStdString SizeToString(__int64 size);
  static const CStdString EmptyString;
  static size_t FindWords(const char *str, const char *wordLowerCase);
  static int FindEndBracket(const CStdString &str, char opener, char closer, int startPos = 0);
  static int DateStringToYYYYMMDD(const CStdString &dateString);
  static void WordToDigits(CStdString &word);
  static float GetFloat(const char* str); // ignores locale
};

#endif
