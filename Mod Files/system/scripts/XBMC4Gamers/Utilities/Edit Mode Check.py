import os,xbmc
xbmc.executebuiltin('Skin.reset(kioskmode)')
if os.path.isfile("Q:/system/keymaps/Enabled"): xbmc.executebuiltin('Skin.SetBool(kioskmode)')