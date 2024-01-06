'''
	Script by Rocky5
	Used to check for the Birthday_Dates file and setup a birthday.
	Usage:
		You place a file called Birthday_Dates in the root of the XBMC4Gamers directory (Next to the default.xbe) with a sructure like.
		Birthday 1
		10-12
		Birthday 2
		1-1
		Birthday 3
		1-11
		Birthday 4
		12-26
		Birthday 5
		5-30
		Obviously if your American your dates would be 30-12 eg....
'''
import os
import xbmcgui
import xbmc
print "| Scripts\XBMC4Gamers\Utilities\Check Birthday Dates.py loaded."
Birthday_Date_File	= xbmc.translatePath("special://xbmc/Birthday_Dates")
if os.path.isfile(Birthday_Date_File):
	tmp = open(Birthday_Date_File,"r")
	Birthday_Date_Values = [ i.rstrip() for i in tmp.readlines()]
	tmp.close()
	try:
		Birthday_Number1	= Birthday_Date_Values[0]
	except:
		pass
	try:
		Birthday_Number2	= Birthday_Date_Values[2]
	except:
		pass
	try:
		Birthday_Number3	= Birthday_Date_Values[4]
	except:
		pass
	try:
		Birthday_Number4	= Birthday_Date_Values[6]
	except:
		pass
	try:
		Birthday_Number5	= Birthday_Date_Values[8]
	except:
		pass
	try:
		if Birthday_Number1 == "Birthday 1":
			try:
				Birthday_Date_Start		= Birthday_Date_Values[1]
				xbmc.executebuiltin('Skin.SetString(Birthday_Date_1,'+Birthday_Date_Start+')')
			except:
				pass
	except:
		pass
	try:
		if Birthday_Number2 == "Birthday 2":
			try:
				Birthday_Date_Start		= Birthday_Date_Values[3]
				xbmc.executebuiltin('Skin.SetString(Birthday_Date_2,'+Birthday_Date_Start+')')
			except:
				pass
	except:
		pass
	try:
		if Birthday_Number3 == "Birthday 3":
			try:
				Birthday_Date_Start		= Birthday_Date_Values[5]
				xbmc.executebuiltin('Skin.SetString(Birthday_Date_3,'+Birthday_Date_Start+')')
			except:
				pass
	except:
		pass
	try:
		if Birthday_Number4 == "Birthday 4":
			try:
				Birthday_Date_Start		= Birthday_Date_Values[7]
				xbmc.executebuiltin('Skin.SetString(Birthday_Date_4,'+Birthday_Date_Start+')')
			except:
				pass
	except:
		pass
	try:
		if Birthday_Number5 == "Birthday 5":
			try:
				Birthday_Date_Start		= Birthday_Date_Values[9]
				xbmc.executebuiltin('Skin.SetString(Birthday_Date_5,'+Birthday_Date_Start+')')
			except:
				pass
	except:
		pass
	#os.remove(Birthday_Date_File)
else:
	pass