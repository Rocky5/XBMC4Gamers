'''
    Script by Rocky5
    Used to check for the Birthday_Dates file and set up a birthday.
    Usage:
        You place a file called Birthday_Dates in the root of the XBMC4Gamers directory (next to the default.xbe) with a structure like:
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
        Obviously, if you're American your dates would be 30-12, etc.
'''

import os
import xbmcgui
import xbmc

def load_birthday_dates(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

def set_birthday_strings(birthday_values):
    for i in range(0, len(birthday_values), 2):
        try:
            birthday_label = birthday_values[i]
            birthday_date = birthday_values[i + 1]
            if "Birthday" in birthday_label:
                birthday_number = birthday_label.split()[-1]
                xbmc.executebuiltin('Skin.SetString(Birthday_Date_{}, {})'.format(birthday_number, birthday_date))
        except IndexError:
            pass

def main():
    print "| Scripts/XBMC4Gamers/Utilities/Check Birthday Dates.py loaded."
    birthday_date_file = xbmc.translatePath("special://xbmc/Birthday_Dates")

    if os.path.isfile(birthday_date_file):
        birthday_date_values = load_birthday_dates(birthday_date_file)
        set_birthday_strings(birthday_date_values)
        # os.remove(birthday_date_file)
    else:
        print "Birthday_Dates file does not exist."

if __name__ == "__main__":
    main()
