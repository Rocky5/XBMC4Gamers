#!/bin/bash

FOLDER_NAME="update-files"
OUTPUT_ZIP="XBMC4Gamers-update-files.zip"
VERSION=$(cat version.txt)

red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
magenta=`tput setaf 5`
cyan=`tput setaf 6`
white=`tput setaf 7`

reset=`tput sgr0`

echo "#############################################"
echo "#"
echo "# Welcome to the ${blue}XBMC4Gamers${reset} updater script."
echo "#"
echo "# Shell script by:"
echo "#     ${blue}Dominic Hock (Subtixx)${reset}"
echo "#"
echo "# XBMC4Gamers Version:"
echo "#     ${blue}$VERSION${reset}"
echo "#"
echo "#############################################"

echo "${green}Building XBMC4Gamers...${reset}"

echo "${green}Copying XBMC4Gamers mod files...${reset}"

cp -a "./Mod Files/." "./update-files/"
cp "./changes.txt" "./update-files/system/SystemInfo/changes.txt"

rm "./update-files/system/UserData/profiles.xml"

echo "${green}Setting variables...${reset}"

if [ ! -e "./update-files/skins/Profile/language/English/strings.po" ]; then
    echo "${red}ERROR: Place a fresh copy of XBMC into this folder and try again.${reset}"
    rm -r "./XBMC"
    exit 1
fi

sed -i "s/0.0.000/$VERSION/g" "./update-files/skins/Profile/language/English/strings.po"

if [ ! -d "./update-files/skins/Manage Profiles" ]; then
    mkdir "./update-files/skins/Manage Profiles"
fi

if [ ! -d "./update-files/skins/DVD2Xbox Skin" ]; then
    mkdir "./update-files/skins/DVD2Xbox Skin"
fi

cp "./update-files/skins/Profile/language/English/strings.po" "./update-files/skins/Manage Profiles/language/English/strings.po"
cp "./update-files/skins/Profile/language/English/strings.po" "./update-files/skins/DVD2Xbox Skin/language/English/strings.po"

# cp "Source/default.xbe" "./update-files/default.xbe"

# Create zip file
echo "${green}Creating zip file...${reset}"

7z a -tzip -mx=7 -r -y "./Other/update build/updater/Update Files/update-files.zip" "*" -mx=7 -r -y
7z a -tzip -mx=7 -r -y "./XBMC4Gamers-update-files.zip" "../Other/update build/*"

rm "./Other/update build/updater/Update Files/update-files.zip"
rm -r "update-files"

echo "${green}Done!${reset}"