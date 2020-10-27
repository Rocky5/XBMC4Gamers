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

#include "AddonDatabase.h"
#include "settings/Settings.h"
#include "FileSystem/Directory.h"

using namespace XFILE;

/*
 * Returns true if the specified addon is installed on the system.
 */
bool CAddonDatabase::HasAddon(const CStdString& addonID) {
  // Check if exists as full path.
  // e.g. "special://home/system/scripts/XBMC Subtitles"
  if (CDirectory::Exists(addonID)) {
    return true;
  }

  // Check if "script.NAME" exists.
  // Allows for "script.xbmc.subtitles" -> "special://home/system/scripts/xbmc subtitles"
  if (addonID.Left(7).Equals("script.")) {
    CStdString scriptName = addonID.Mid(7);
    scriptName.Replace(".", " ");
    CStdString scriptsFolder = g_settings.GetScriptsFolder() + "/" + scriptName;

    if (CDirectory::Exists(scriptsFolder.c_str())) {
      return true;
    }
  }

  // Default
  return false;
}