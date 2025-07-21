'''
	Script by Rocky5:
	Used to edit settings in the E:\Cerbios\Cerbios.ini
'''
import xml.etree.ElementTree as ET
from os.path import isfile
from sys import argv
from time import sleep
from xbmc import executebuiltin, getCondVisibility, getInfoLabel, getLocalizedString
from xbmcgui import Dialog

# Set path for the skin
executebuiltin('SetProperty(script_path,{}\\resources\\lib\\config_edit.py,3000)'.format(__path__))

ini_file = "E:\\Cerbios\\cerbios.ini"

# Default mapping for the cerbios.ini or if skin settings are set they are used
skin_mappings = {
	"AdvCPUSupport": ("cerbios_advcpusupport", False),
	"ApplyTitlePatches": ("cerbios_titlepatches", False),
	"AVCheck": ("cerbios_avcheck", True),
	"BlockDashUpdate": ("cerbios_blockupdate", False),
	"BootAnimPath": ("cerbios_bootanimpath", "E:\\Cerbios\\BootAnims\\Xbox\\BootAnim.xbe"),
	"CPUMPLLCoeff": ("cerbios_cpumpllcoeff", "000000"),
	"DashPath": ("cerbios_dashpath", "C:\\evoxdash.xbe"),
	"Debug": ("cerbios_debugsupport", False),
	"DisableLimitMem": ("cerbios_xbememlimit", False),
	"DriveSetup": ("cerbios_drivesetup", "Legacy Mode"),
	"EnableScreenshots": ("cerbios_enablescreenshots", False),
	"FanSpeed": ("cerbios_fanspeed", "Auto"),
	"Force480p": ("cerbios_force480p", False),
	"ForceFFilter": ("cerbios_flickerfilter", "System"),
	"ForceVGA": ("cerbios_forcevga", False),
	"FrontLed": (
		["cerbios_ledcolour1", "cerbios_ledcolour2", "cerbios_ledcolour3", "cerbios_ledcolour4"],
		["Green", "Green", "Green", "Green"]
	),
	"IGRCycle": (
		["cerbios_igrcycle_1", "cerbios_igrcycle_2", "cerbios_igrcycle_3", "cerbios_igrcycle_4"],
		["Left Trigger", "Right Trigger", "Black", "DPad Up"]
	),
	"IGRDash": (
		["cerbios_igrdash_1", "cerbios_igrdash_2", "cerbios_igrdash_3", "cerbios_igrdash_4"],
		["Left Trigger", "Right Trigger", "Start", "Back"]
	),
	"IGRFull": (
		["cerbios_igrfull_1", "cerbios_igrfull_2", "cerbios_igrfull_3", "cerbios_igrfull_4"],
		["Left Trigger", "Right Trigger", "Black", "Back"]
	),
	"IGRGame": (
		["cerbios_igrgame_1", "cerbios_igrgame_2", "cerbios_igrgame_3", "cerbios_igrgame_4"],
		["Left Trigger", "Right Trigger", "Black", "Start"]
	),
	"IGRShutdown": (
		["cerbios_igrshutdown_1", "cerbios_igrshutdown_2", "cerbios_igrshutdown_3", "cerbios_igrshutdown_4"],
		["Left Trigger", "Right Trigger", "DPad Up", "Back"]
	),
	"IGRScreen": (
		["cerbios_igrscreen_1", "cerbios_igrscreen_2", "cerbios_igrscreen_3", "cerbios_igrscreen_4"],
		["Left Thumb", "Right Thumb", "", ""]
	),
	"IGRMasterPort": ("cerbios_igrmasterport", "0"),
	"InAppLCDEnable": ("cerbios_lcdsupport", False),
	"LCDI2CAddr": ("cerbios_lcdi2caddr", "3C"),
	"LCDI2CProto": ("cerbios_lcdi2cproto", "HD44780 compatible (LCD2004)"),
	"NVPLLCoeff": ("cerbios_nvpllcoeff", "000000"),
	"Overclocking": ("cerbios_overclocking", False),
	"ReadOnlyC": ("cerbios_readonlyc", False),
	"ResetOnEject": ("cerbios_roeject", False),
	"RTCEnable": ("cerbios_rtcsupport", False),
	"ScreenshotHDD": ("cerbios_screenshothdd", "Master"),
	"ScreenshotPart": ("cerbios_screenshotpart", "E"),
	"TUDATARedir": ("cerbios_tudataredir", False),
	"TUDATARedirHDD": ("cerbios_tudataredirhdd", "Master"),
	"TUDATARedirPart": ("cerbios_tudataredirpart", "System"),
	"UdmaModeMaster": ("cerbios_udmamodemaster", "System"),
	"UdmaModeSlave": ("cerbios_udmamodeslave", "System"),
	"XonlineDashRedir": ("cerbios_xonlinedashredir", False)
}

# This is here as its shared with the saving function.
led_skin_mapping = {
	"Off": "O",
	"Amber": "A",
	"Green": "G",
	"Red": "R",
}

# Map friendly names to hex values
igr_button_skin_mapping = {
	"A": "0",
	"B": "1",
	"X": "2",
	"Y": "3",
	"Black": "4",
	"White": "5",
	"Left Trigger": "6",
	"Right Trigger": "7",
	"DPad Up": "8",
	"DPad Down": "9",
	"DPad Left": "A",
	"DPad Right": "B",
	"Start": "C",
	"Back": "D",
	"Left Thumb": "E",
	"Right Thumb": "F",
}

def convert_ini_to_skin(ini_key, value):
	if value.lower() in ["true", "false"]:
		return value.lower() == "true"

	if ini_key == "DriveSetup":
		drive_mapping = {
			"0": "Standard Mode",
			"1": "Legacy Mode",
			"2": "Modern Mode",
			"3": "Dual HDD Mode",
		}
		return drive_mapping.get(value, value)

	if ini_key == "FanSpeed":
		return "Auto" if value == "0" else "{}%".format(value)

	if ini_key == "ForceFFilter":
		flicker_mapping = {
			"6": "System",
			"0": "Off",
			"1": "Slight",
			"2": "Moderate",
			"3": "Balanced",
			"4": "Enhanced",
			"5": "Strong",
		}
		return flicker_mapping.get(value, "System")

	if ini_key == "FrontLed":
		led_ini_mapping = {
			"O": "Off",
			"A": "Amber",
			"G": "Green",
			"R": "Red",
		}
		return [led_ini_mapping.get(char, "Off") for char in value]

	if ini_key == "IGRMasterPort":
		igrmasterport_mapping = {
			"0": "ALL",
			"1": "Port 1",
			"2": "Port 2",
			"3": "Port 3",
			"4": "Port 4",
		}
		return igrmasterport_mapping.get(value, "ALL")

	if ini_key in ["IGRCycle", "IGRDash", "IGRFull", "IGRGame", "IGRScreen", "IGRShutdown"]:
		igr_button_mapping = {
			"0": "A",
			"1": "B",
			"2": "X",
			"3": "Y",
			"4": "Black",
			"5": "White",
			"6": "Left Trigger",
			"7": "Right Trigger",
			"8": "DPad Up",
			"9": "DPad Down",
			"A": "DPad Left",
			"B": "DPad Right",
			"C": "Start",
			"D": "Back",
			"E": "Left Thumb",
			"F": "Right Thumb",
		}
		return [igr_button_mapping.get(c.upper(), "") for c in value]

	if ini_key in ["LCDI2CAddr", "CPUMPLLCoeff", "NVPLLCoeff"]:
		return value.replace('0x', '')

	if ini_key == "LCDI2CProto":
		lcdi2cproto_mapping = {
			"0": "HD44780 compatible (LCD2004)",
			"1": "US2066 (NHD-0420CW)",
		}
		return lcdi2cproto_mapping.get(value, "HD44780 compatible (LCD2004)")

	if ini_key == "ScreenshotPart":
		screenshot_redir_part_mapping = {
			"1": "E",
			"6": "F",
			"7": "G",
		}
		return screenshot_redir_part_mapping.get(value, "E")

	if ini_key in ["UdmaModeMaster", "UdmaModeSlave"]:
		udma_mapping = {
			"0": "System",
			"1": "UDMA 1",
			"2": "UDMA 2",
			"3": "UDMA 3",
			"4": "UDMA 4",
			"5": "UDMA 5",
			"6": "UDMA 6",
		}
		return udma_mapping.get(value, "System")

	if ini_key in ["TUDATARedirHDD", "ScreenshotHDD"]:
		master_slave_hdd_mapping = {
			"0": "Master",
			"1": "Slave",
		}
		return master_slave_hdd_mapping.get(value, "Master")

	if ini_key == "TUDATARedirPart":
		tudata_redir_part_mapping = {
			"1": "System",
			"6": "F",
			"7": "G",
		}
		return tudata_redir_part_mapping.get(value, "System")

	return value

def convert_skin_to_ini(skin_key, value):
	if skin_key == "cerbios_drivesetup":
		drive_mapping = {
			"Standard Mode": "0",
			"Legacy Mode": "1",
			"Modern Mode": "2",
			"Dual HDD Mode": "3"
		}
		return drive_mapping.get(value, "1")

	if skin_key == "cerbios_fanspeed":
		return "0" if value == "Auto" else value.replace("%", "").strip()

	if skin_key == "cerbios_flickerfilter":
		flicker_mapping = {
			"System": "6",
			"Off": "0",
			"Slight": "1",
			"Moderate": "2",
			"Balanced": "3",
			"Enhanced": "4",
			"Strong": "5",
		}
		return flicker_mapping.get(value, "6")

	if skin_key == "cerbios_igrmasterport":
		igrmasterport_mapping = {
			"ALL": "0",
			"Port 1": "1",
			"Port 2": "2",
			"Port 3": "3",
			"Port 4": "4",
		}
		return igrmasterport_mapping.get(value, "0")

	if skin_key in ["cerbios_lcdi2caddr", "cerbios_cpumpllcoeff", "cerbios_nvpllcoeff"]:
		return "0x{}".format(value.upper())

	if skin_key == "cerbios_lcdi2cproto":
		lcdi2cproto_mapping = {
			"HD44780 compatible (LCD2004)": "0",
			"US2066 (NHD-0420CW)": "1",
		}
		return lcdi2cproto_mapping.get(value, "0")

	if skin_key == "cerbios_screenshotpart":
		screenshot_redir_part_mapping = {
			"E": "1",
			"F": "6",
			"G": "7",
		}
		return screenshot_redir_part_mapping.get(value, "1")

	if skin_key in ["cerbios_udmamodemaster", "cerbios_udmamodeslave"]:
		udma_mapping = {
			"System": "0",
			"UDMA 1": "1",
			"UDMA 2": "2",
			"UDMA 3": "3",
			"UDMA 4": "4",
			"UDMA 5": "5",
			"UDMA 6": "6",
		}
		return udma_mapping.get(value, "0")

	if skin_key in ["cerbios_tudataredirhdd", "cerbios_screenshothdd"]:
		master_slave_hdd_mapping = {
			"0": "Master",
			"1": "Slave",
		}
		return master_slave_hdd_mapping.get(value, "0")

	if skin_key == "cerbios_tudataredirpart":
		tudata_redir_part_mapping = {
			"System": "1",
			"F": "6",
			"G": "7",
		}
		return tudata_redir_part_mapping.get(value, "1")

	return value

def check_guisettings(path):
	guisettings_values = {}
	tree = ET.parse(path)
	root = tree.getroot()
	skinsettings = root.find("skinsettings")
	if skinsettings is not None:
		for setting in skinsettings.findall("setting"):
			name = setting.get("name")
			if name and name.startswith("Profile.cerbios_"):
				guisettings_values[name.replace("Profile.", "")] = setting.text.strip() if setting.text else ""
	return guisettings_values

# Parse the ini, configparser wont work with this ini as it doesn't have sections [blah blah] so had to so it this way.
def parse_ini_file(file_path):
	first_run = False
	reload_all = False

	if not getCondVisibility("Skin.HasSetting(cerbios_config_editor_first_run)"):
		executebuiltin("Skin.SetBool(cerbios_config_editor_first_run)")
		first_run = True

	guisettings_values = check_guisettings("P:\\guisettings.xml")
	settings = {}
	executebuiltin("Skin.Reset(cerbios_cansave)")

	enable_saving_keys = {
		"AdvCPUSupport", "ForceFFilter", "InAppLCDEnable", "LCDI2CAddr",
		"LCDI2CProto", "ResetOnEject", "TUDATARedir", "TUDATARedirHDD",
		"TUDATARedirPart", "XonlineDashRedir", "IGRCycle", "IGRDash",
		"IGRFull", "IGRGame", "IGRScreen", "IGRShutdown", "CPUMPLLCoeff",
		"NVPLLCoeff", "ReadOnlyC"
	}
	enable_saving = set()

	partition_mapping = {
		"\\Device\\Harddisk0\\Partition1\\": "E",
		"\\Device\\Harddisk0\\Partition2\\": "C",
		"\\Device\\Harddisk0\\Partition6\\": "F",
		"\\Device\\Harddisk0\\Partition7\\": "G",
		"HDD0-C": "C", "HDD0-E": "E", "HDD0-F": "F", "HDD0-G": "G"
	}

	with open(file_path, "r") as file:
		lines = file.readlines()
		reload_all = any(line.strip().startswith(";") for line in lines)
		for line in lines:
			line = line.strip()
			if not line or line.startswith(";"):
				continue
			key_value = line.split("=", 1)
			if len(key_value) != 2:
				continue
			key, value = key_value[0].strip(), key_value[1].strip()
			for raw_path, mapped_path in partition_mapping.items():
				if raw_path in value:
					value = value.replace(raw_path, mapped_path)
			skin_value = convert_ini_to_skin(key, value)
			settings[key] = skin_value
			if key in skin_mappings:
				skin_keys = skin_mappings[key][0]
				if not isinstance(skin_keys, list):
					skin_keys = [skin_keys]
				ini_values = skin_value if isinstance(skin_value, list) else [skin_value]
				refresh = first_run or reload_all
				if not refresh:
					for i, k in enumerate(skin_keys):
						expected = ini_values[i] if i < len(ini_values) else ""
						current = guisettings_values.get(k, "")
						if str(current) != str(expected):
							refresh = True
							break
				if refresh:
					apply_skin_settings({key: skin_value}, {key: skin_mappings[key]})
			if key in enable_saving_keys:
				enable_saving.add(key)

	if enable_saving == enable_saving_keys:
		executebuiltin("Skin.SetBool(cerbios_cansave)")

# Reset the config to the default values
def reset_skin_settings():
	for ini_key, (skin_key, default_value) in skin_mappings.items():
		if isinstance(default_value, list):
			type = None
			if any("cerbios_igr" in k.lower() for k in skin_key):
				type = "igr"
			elif any("cerbios_led" in k.lower() for k in skin_key):
				type = "led"
			for i, key in enumerate(skin_key):
				val = default_value[i] if i < len(default_value) else ("Off" if type == "led" else "")
				executebuiltin("Skin.SetString({}, {})".format(key, val))
		elif isinstance(default_value, bool):
			if default_value:
				executebuiltin("Skin.SetBool({})".format(skin_key))
			else:
				executebuiltin("Skin.Reset({})".format(skin_key))
		else:
			executebuiltin("Skin.SetString({}, {})".format(skin_key, default_value))
	sleep(1)

# Apply the settings from the ini so the menu matches the ini file.
def apply_skin_settings(settings, skin_mappings):
	for ini_key, (skin_key, default_value) in skin_mappings.items():
		if ini_key in settings:
			value = settings[ini_key]
			if isinstance(skin_key, list):
				type = None
				if any("cerbios_igr" in k.lower() for k in skin_key):
					type = "igr"
				elif any("cerbios_led" in k.lower() for k in skin_key):
					type = "led"
				if type:
					for i, key in enumerate(skin_key):
						val = value[i] if i < len(value) else default_value[i]
						executebuiltin("Skin.SetString({}, {})".format(key, val))
			elif isinstance(value, bool):
				if value:
					executebuiltin("Skin.SetBool({})".format(skin_key))
				else:
					executebuiltin("Skin.Reset({})".format(skin_key))
			else:
				executebuiltin("Skin.SetString({}, {})".format(skin_key, value))

# Save the setting to the config.ini only if the config is newer.
def save_skin_settings(file_path, skin_mappings, delay=0):
	sleep(delay)
	ini_content = []

	if isfile(file_path):
		with open(file_path, "r") as f:
			ini_content = f.readlines()

	settings = {}
	for ini_key, (skin_key, default_value) in skin_mappings.items():
		if isinstance(skin_key, list):
			if any("cerbios_igr" in k.lower() for k in skin_key):
				full_igr_values = [getInfoLabel("Skin.String({})".format(k)) for k in skin_key]
				settings[ini_key] = "".join([igr_button_skin_mapping.get(c, "") for c in full_igr_values])
			if any("cerbios_led" in k.lower() for k in skin_key):
				full_led_values = [getInfoLabel("Skin.String({})".format(k)) for k in skin_key]
				settings[ini_key] = "".join([led_skin_mapping.get(c, "O") for c in full_led_values])
		elif isinstance(default_value, bool):
			settings[ini_key] = "true" if getCondVisibility("Skin.HasSetting({})".format(skin_key)) else "false"
		else:
			value = getInfoLabel("Skin.String({})".format(skin_key))
			settings[ini_key] = value if value else str(default_value)

		settings[ini_key] = convert_skin_to_ini(skin_key, settings[ini_key])

	with open(file_path, "w") as ini_file:
		for key, value in settings.items():
			ini_file.write("{} = {}\n".format(key, value))

if (__name__ == "__main__"):
	arg = argv[1] if len(argv) > 1 else 'load'

	if isfile(ini_file):
		if arg == "load":
			parse_ini_file(ini_file)
		elif arg == "save":
			save_skin_settings(ini_file, skin_mappings)
			Dialog().ok('Success', "", 'Cerbios.ini has been successfully saved.')
		elif arg == "reset":
			sleep(1)
			reset_skin_settings()
			executebuiltin('Dialog.Close(1100,false)')
			Dialog().ok("Reset", "", "All Cerbios settings have been reset to default.")
			save_skin_settings(ini_file, skin_mappings)
	else:
		xbmcgui.Dialog().ok('Error', "", 'Cannot find E:\\Cerbios\\Cerbios.ini')