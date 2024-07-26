import os
import xbmc

def toggle_kiosk_mode():
	xbmc.executebuiltin('Skin.reset(kioskmode)')
	if os.path.isfile("Q:/system/keymaps/Enabled"):
		xbmc.executebuiltin('Skin.SetBool(kioskmode)')

if __name__ == "__main__":
	toggle_kiosk_mode()
