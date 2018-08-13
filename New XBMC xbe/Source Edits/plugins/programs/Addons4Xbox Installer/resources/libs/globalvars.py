# If the dir exists with the requested name, simply return it

__all__ = [
    # public names
    "XBMC_IS_HOME",
    "SPECIAL_XBMC_DIR",
    "SPECIAL_HOME_DIR",
    "SPECIAL_TEMP_DIR",
    "SPECIAL_PROFILE_DIR",
    "SPECIAL_MASTERPROFILE_DIR",
    "SPECIAL_XBMC_HOME",
    "SPECIAL_SCRIPT_DATA",
    "DIR_ADDON_SKIN",
    "DIR_ADDON_SCRIPT",
    "DIR_ADDON",
    "DIR_ADDON_PLUGIN",
    "DIR_ADDON_MUSIC",
    "DIR_ADDON_PICTURES",
    "DIR_ADDON_PROGRAMS",
    "DIR_ADDON_VIDEO",
    "DIR_ADDON_WEATHER",
    "DIR_ADDON_MODULE",
    "DIR_ROOT",
    "DIR_CACHE",
    "DIR_CACHE_ADDONS",
    "DIR_ADDON_REPO",
    "PARAM_NAME",
    "PARAM_ACTION",
    "PARAM_TITLE",
    "PARAM_TYPE",
    "PARAM_LISTTYPE",
    "PARAM_LOCALPATH",
    "PARAM_INSTALL_FROM_ZIP",
    "PARAM_INSTALL_FROM_REPO",
    "PARAM_REPO_ID",
    "PARAM_REPO_NAME",
    "PARAM_ADDON_NAME",
    "PARAM_URL",
    "PARAM_DATADIR",
    "PARAM_REPO_FORMAT",
    "VALUE_LIST_CATEGORY",
    "VALUE_LIST_LOCAL_REPOS",
    "VALUE_LIST_ALL_ADDONS",
    "VALUE_LIST_ADDONS",
    "VALUE_DISPLAY_INFO",
    "REQUIRED_DEFAULT_LIB",
    "REPO_ID_HELIX",
    "REPO_ID_XBMC",
    "REPO_ID_XBMC4XBOX",
    "MISSING_MODULES_PATH"
    ]


# Modules General
import os
import sys

# Modules XBMC
from xbmc import translatePath#, getCondVisibility


try: pluginname = sys.modules[ "__main__" ].__plugin__
except: pluginname = os.path.basename( os.getcwd() )

SPECIAL_XBMC_DIR = translatePath( "special://xbmc/" )
if not os.path.isdir( SPECIAL_XBMC_DIR  ): SPECIAL_XBMC_DIR = translatePath( "Q:\\" )

SPECIAL_HOME_DIR = translatePath( "special://home/" )
if not os.path.isdir( SPECIAL_HOME_DIR  ): SPECIAL_HOME_DIR = translatePath( "U:\\" )

SPECIAL_TEMP_DIR = translatePath( "special://temp/" )
if not os.path.isdir( SPECIAL_TEMP_DIR  ): SPECIAL_TEMP_DIR = translatePath( "Z:\\" )

SPECIAL_PROFILE_DIR = translatePath( "special://profile/" )
if not os.path.isdir( SPECIAL_PROFILE_DIR  ): SPECIAL_PROFILE_DIR = translatePath( "P:\\" )

SPECIAL_MASTERPROFILE_DIR = translatePath( "special://masterprofile/" )
if not os.path.isdir( SPECIAL_MASTERPROFILE_DIR  ): SPECIAL_MASTERPROFILE_DIR = translatePath( "T:\\" )

SPECIAL_XBMC_HOME = ( SPECIAL_HOME_DIR, SPECIAL_XBMC_DIR )[ ( os.environ.get( "OS", "xbox" ).lower() == "xbox" ) ]

XBMC_IS_HOME = SPECIAL_HOME_DIR == SPECIAL_XBMC_DIR

SPECIAL_SCRIPT_DATA = os.path.join( SPECIAL_PROFILE_DIR, "plugin_data", "programs", pluginname )
if not os.path.isdir( SPECIAL_SCRIPT_DATA ): os.makedirs( SPECIAL_SCRIPT_DATA )


# Calculate directories needed by the installer
#DIR_XBMC_ROOT       = SPECIAL_XBMC_HOME
DIR_ADDON_SKIN     = os.path.join( SPECIAL_HOME_DIR )
DIR_ADDON_SCRIPT   = os.path.join( SPECIAL_HOME_DIR, "system", "scripts" )
DIR_ADDON          = os.path.join( SPECIAL_HOME_DIR, "system", "addons" )
DIR_ADDON_PLUGIN   = os.path.join( SPECIAL_HOME_DIR, "system", "plugins" )
DIR_ADDON_MUSIC    = os.path.join( DIR_ADDON_PLUGIN, "music" )
DIR_ADDON_PICTURES = os.path.join( DIR_ADDON_PLUGIN, "pictures" )
DIR_ADDON_PROGRAMS = os.path.join( DIR_ADDON_PLUGIN, "programs" )
DIR_ADDON_VIDEO    = os.path.join( DIR_ADDON_PLUGIN, "video" )
DIR_ADDON_WEATHER  = os.path.join( DIR_ADDON_PLUGIN, "weather" )
DIR_ADDON_MODULE   = os.path.join( SPECIAL_HOME_DIR, "system", "scripts", ".modules" )


DIR_ROOT            = os.getcwd().replace( ";", "" )
DIR_CACHE           = os.path.join( SPECIAL_SCRIPT_DATA, "cache" )
#DIR_CACHE_ADDONS    = os.path.join( DIR_CACHE, "addons" )
DIR_CACHE_ADDONS    = os.path.join( SPECIAL_SCRIPT_DATA, "dwl" )
DIR_ADDON_REPO      = os.path.join( SPECIAL_SCRIPT_DATA, "repositories")

VERSION_FILE        = os.path.join( SPECIAL_SCRIPT_DATA, "version.txt" )

MISSING_MODULES_PATH = os.path.join( DIR_CACHE, "missing_modules.txt" )

# define plugin param key names
PARAM_NAME                 = 'name'
PARAM_ACTION               = 'action'
PARAM_TITLE                = "title"
PARAM_TYPE                 = 'type'
PARAM_LISTTYPE             = 'listype'
PARAM_LOCALPATH            = 'localpath'
PARAM_INSTALL_FROM_ZIP     = 'installfromzip'
PARAM_INSTALL_FROM_REPO    = 'installfromrepo'
PARAM_REPO_ID              = 'repoid'
PARAM_REPO_NAME            = 'reponame'
PARAM_ADDON_NAME           = 'addonname'
PARAM_ADDON_ID             = 'addonid'
PARAM_URL                  = 'url'
PARAM_DATADIR              = 'datadir'
PARAM_REPO_FORMAT          = 'format'
VALUE_LIST_CATEGORY        = 'listcataddon'
VALUE_LIST_LOCAL_REPOS     = 'listlocalrepos'
VALUE_LIST_WIKI_REPOS      = 'listwikirepos'
VALUE_LIST_ALL_ADDONS      = 'alladdons'
VALUE_LIST_ADDONS          = 'listaddons'
VALUE_DISPLAY_INFO         = 'displayinfo'
VALUE_LIST_MANAGE_ADDONS   = 'manageaddons'
VALUE_LIST_MISSING_MODULES = 'missingmodules'

REQUIRED_DEFAULT_LIB = 'xbmc.python'
REPO_ID_XBMC4XBOX = 'repository.xbmc4xbox'
REPO_ID_XBMC = 'repository.xbmc.org'
REPO_ID_HELIX = 'repository.kodi.tv'
