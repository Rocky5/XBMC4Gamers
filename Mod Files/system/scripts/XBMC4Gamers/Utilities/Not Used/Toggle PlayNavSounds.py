from sys import argv
from xbmc import enableNavSounds, executebuiltin, getLocalizedString

ARG = argv[1]
NAV_SOUND_MODE_OFF = 1223
NAV_SOUND_MODE_ON = 305
NAV_SOUND_MODE_ON_PLAYBACK = 21370

def set_nav_sound_mode(localized_string):
	executebuiltin('Skin.SetString(NavSoundMode,{})'.format(localized_string))
	enableNavSounds(1)

if ARG == "1":
	executebuiltin('Skin.SetString(NavSoundMode,{})'.format(getLocalizedString(NAV_SOUND_MODE_OFF)))
	enableNavSounds(0)
elif ARG == "2":
	set_nav_sound_mode(getLocalizedString(NAV_SOUND_MODE_ON))
	executebuiltin('SetSetting(lookandfeel.soundsduringplayback,False)')
elif ARG == "3":
	set_nav_sound_mode("{} + {}".format(getLocalizedString(NAV_SOUND_MODE_ON), getLocalizedString(NAV_SOUND_MODE_ON_PLAYBACK)))
	executebuiltin('SetSetting(lookandfeel.soundsduringplayback,True)')
else:
	set_nav_sound_mode(getLocalizedString(NAV_SOUND_MODE_ON))
	executebuiltin('SetSetting(lookandfeel.soundsduringplayback,False)')