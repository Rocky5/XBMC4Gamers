## xbmcaddon emulator module for xbmc4xbox

__all__ = [ "Addon" ]
__author__ = "nuka1195"

import sys
# set this here, hopefully sys.argv will be more accurate the faster we have it
sysargv = sys.argv
import os
import xbmc
from xml.dom.minidom import parseString


class Addon:
    """
        Addon(id) -- Creates a new Addon class.

        id          : string - id of the addon.

        example:
         - self.Addon = xbmcaddon.Addon(id="script.xbmc.lyrics")
    """
    # dictionary to hold addon info
    _info = {}
    
    def __init__( self, id = None):
        """
            Initializer for passing the addon's id and setting addon info.
        """
        # get root dir
        cwd = self._get_root_dir( sysargv[0] )

        xbmc.log( "xbmcaddon: cwd = " + cwd, xbmc.LOGDEBUG )

        # if we have no plugin id we have to hope we can get it from the addon.xml (and that we are in the addon folder)
        if id == None:
            self._set_addon_info( xbmc.translatePath( cwd ), id )
            location = cwd
        else:
            xbmc.log( "xbmcaddon: id  = " + id,  xbmc.LOGDEBUG )
            parts = id.split( '.' )
            # search locations for the addon
            locations = []
            if cwd:
                locations.append(cwd)                            # current directory
                locations.append("%s/%s" % (cwd, id))            # subdirectory in current directory
            locations.append("Q:\scripts\.modules\%s" % ( id ))  # script modules

            # plugin.music|video|etc.something addons
            if len( parts ) == 3 and parts[ 0 ] == "plugin":
                pluginType = parts[ 1 ].replace("audio", "music")
                pluginName = parts[ 2 ]
                locations.append("plugin://%s/%s" % ( pluginType, pluginName ))

            xbmc.log( "xbmcaddon: locations = " + str(locations), xbmc.LOGDEBUG )

            for location in locations:
                if self._set_addon_info( xbmc.translatePath( location ), id ) != None:
                    break

            # have we got the right dir now?
            if self._info.get( 'id', '' ) != id:
                # walk plugin directories to try to find correct one
                base_path = os.path.dirname( xbmc.translatePath( cwd ) ) + os.sep
                for directory in os.listdir(base_path):
                    location = "plugin://%s/%s" % ( parts[ 1 ], directory )
                    # parse addon.xml and reset all addon info
                    if self._set_addon_info( xbmc.translatePath( location ), id ) != None:
                        break

        # get settings and language methods
        self._get_methods( location )
        xbmc.log( "xbmcaddon: using " + location, xbmc.LOGDEBUG )

    def _get_root_dir( self, path ):
        # get current working directory, we need to reset sys.argv[ 0 ] to a plugin for weather plugins as they aren't run as plugins, but they are categorized as plugins
        cwd = os.path.dirname( xbmc.validatePath( path.replace( "Q:\\plugins\\weather\\", "plugin://weather/" ) ) )
        # check if we're at root folder of addon
        if ( not os.path.isfile( os.path.join( xbmc.translatePath( cwd ), "addon.xml" ) ) ):
            # we're not at root, assume resources/lib/
            cwd = os.path.dirname( os.path.dirname( cwd ) )
        # return result
        return cwd

    def _get_methods( self, cwd ):
        # language module
        self._language_ = xbmc.Language( cwd ).getLocalizedString
        # settings module, try catch necessary as not all scripts have settings
        try:
            self._settings_ = xbmc.Settings( cwd )
        except:
            self._settings_ = None

    def _set_addon_info( self, cwd, id ):
        xbmc.log( "xbmcaddon: trying " + cwd, xbmc.LOGDEBUG )
        # get source
        try:
            xml_file = os.path.join( cwd, "addon.xml" )
            xml = open( xml_file, "r" ).read()
            # parse source
            dom = parseString( xml )
            # get main element
            item = dom.getElementsByTagName( "addon" )[ 0 ]
            # clear out old info
            self._info = {}
            # set info
            self._info[ "id" ] = item.getAttribute( "id" )
            if id != None and self._info[ "id" ] != id:
                return None
            self._info[ "name" ] = item.getAttribute( "name" )
            self._info[ "version" ] = item.getAttribute( "version" )
            self._info[ "author" ] = item.getAttribute( "provider-name" )
            for extension in dom.getElementsByTagName( "extension" ):
                # get library and type
                if ( extension.hasAttribute( "library" ) ):
                    self._info[ "library" ] = extension.getAttribute( "library" )
                    self._info[ "type" ] = extension.getAttribute( "point" )
                # get any meta data
                if ( extension.getAttribute( "point" ) == "xbmc.addon.metadata" ):
                    locale = xbmc.getRegion( "locale" )
                    for metatype in [ "disclaimer", "summary", "description" ]:
                        metadict = { "en": "" }
                        for metadata in extension.getElementsByTagName( metatype ):
                            if ( metadata.getAttribute( "lang" ) != "" ):
                                try:
                                    metadict[ metadata.getAttribute( "lang" ) ] = metadata.firstChild.data
                                except:
                                    metadict[ metadata.getAttribute( "lang" ) ] = ""
                            else:
                                try:
                                    metadict[ "en" ] = metadata.firstChild.data
                                except:
                                    metadict[ "en" ] = ""
                        if ( metadict.has_key( locale ) ):
                            self._info[ metatype ] = metadict[ locale ]
                        else:
                            self._info[ metatype ] = metadict[ "en" ]
            # reset this to default.py as that's what xbox uses
            self._info[ "library" ] = "default.py"
            self._info[ "path" ] = cwd
            self._info[ "libpath" ] = os.path.join( cwd, self._info[ "library" ] )
            self._info[ "icon" ] = os.path.join( cwd, "default.tbn" )
            self._info[ "fanart" ] = os.path.join( cwd, "fanart.jpg" )
            self._info[ "changelog" ] = os.path.join( cwd, "changelog.txt" )
            if ( cwd.startswith( "Q:\\plugins" ) ):
                self._info[ "profile" ] = "special://profile/plugin_data/%s/%s" % ( os.path.basename( os.path.dirname( cwd ) ), os.path.basename( cwd ), )
            else:
                self._info[ "profile" ] = "special://profile/script_data/%s" % ( os.path.basename( cwd ), )
            # cleanup
            dom.unlink()
        except:
            xbmc.log( "xbmcaddon: could not open " + xml_file, xbmc.LOGDEBUG )
            return None

        return id

    def getAddonInfo( self, id ):
        """
            getAddonInfo(id) -- Returns the value of an addon property as a string.

            id        : string - id of the property you want returned.

            *values for id: author, changelog, description, disclaimer, fanart. icon, id, libpath,
                            library, name, path, profile, stars, summary, type, version

            example:
              - profile_path = self.Addon.getAddonInfo(id="profile")
        """
        return self._info[ id.lower() ]

    def getLocalizedString( self, id ):
        """
            getLocalizedString(id) -- Returns the localized string as a unicode object.

            id             : integer - id# of the string you want to localize.

            example:
              - locstr = self.Addon.getLocalizedString(id=30000)
        """
        return self._language_( id )

    def getSetting( self, id ):
        """
            getSetting(id) -- Returns the value of a setting as a unicode object.

            id        : string - id of the setting you want returned.

            example:
              - username = self.Addon.getSetting(id="username")
        """
        if self._settings_:
            return self._settings_.getSetting( id )
        else:
            return None

    def setSetting( self, id, value ):
        """
            setSetting(id, value) -- Sets a setting for this addon.

            id        : string - id of the setting you want to set.
            value     : string or unicode - value of the setting.

            example:
              - self.Addon.setSetting(id="username", value="nuka1195")
        """
        self._settings_.setSetting( id, value )

    def openSettings( self ):
        """
            openSettings() -- Opens this addons settings dialog.

            example:
              - self.Addon.openSettings()
        """
        self._settings_.openSettings()
