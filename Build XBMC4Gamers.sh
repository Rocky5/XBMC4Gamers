#!/bin/bash
VERSION=$(cat version.txt)

red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
magenta=`tput setaf 5`
cyan=`tput setaf 6`
white=`tput setaf 7`

reset=`tput sgr0`

# Create array of all folders we want to remove
REMOVE_FILES=(./XBMC/plugins \
    ./XBMC/sounds\ 
    ./XBMC/userdata\ 
    ./XBMC/visualisations\ 
    ./XBMC/web\ 
    ./XBMC/system/keymaps\ 
    ./XBMC/system/cdrip\ 
    ./XBMC/system/scrapers\ 
    ./XBMC/system/players/mplayer/codecs\ 
    ./XBMC/scripts\ 
    ./XBMC/skin \
    ./XBMC/screensavers \
    "./XBMC/system/filezilla server.xml" \
    ./XBMC/copying.txt \
    ./XBMC/keymapping.txt \
    ./XBMC/media/icon.png \
    ./XBMC/media/Splash_2007.png \
    ./XBMC/media/Splash_2008.png \
    ./XBMC/media/weather.rar)

COPY_SYSTEM_FILES=(./XBMC/media \
    ./XBMC/language \
    ./XBMC/screenshots \
    ./XBMC/UserData)

echo "#############################################"
echo "#"
echo "# Welcome to the ${blue}XBMC4Gamers${reset} build script."
echo "#"
echo "# Shell script by:"
echo "#     ${blue}Dominic Hock (Subtixx)${reset}"
echo "#"
echo "# XBMC4Gamers Version:"
echo "#     ${blue}$VERSION${reset}"
echo "#"
echo "#############################################"

# Check for XBMC folder and XBMC/system folder existance
if [ ! -d "./XBMC" ]; then
    echo "${red}ERROR: Place a fresh copy of XBMC into this folder and try again.${reset}"
    exit 1
fi

if [ ! -d "./XBMC/system" ]; then
    echo "${red}ERROR: Place a fresh copy of XBMC into this folder and try again.${reset}"
    exit 1
fi

echo "${green}Building XBMC4Gamers...${reset}"

echo "${green}Removing unneeded files...${reset}"
# Remove all files we don't need
for i in "${REMOVE_FILES[@]}"
do
    if [ -e "$i" ]; then
        echo "Removing $i"
        rm -r "$i"
    fi
done

echo "${green}Copying system files...${reset}"
for i in "${COPY_SYSTEM_FILES[@]}"
do
    if [ -e "$i" ]; then
        echo "Copying $i"
        cp -a "$i" "./XBMC/system/"
    fi
done

echo "${green}Copying XBMC4Gamers mod files...${reset}"

cp -a "./Mod Files/." "./XBMC/"
cp "./changes.txt" "./XBMC/system/SystemInfo/changes.txt"

echo "${green}Setting variables...${reset}"

if [ ! -e "./XBMC/skins/Profile/language/English/strings.po" ]; then
    echo "${red}ERROR: Place a fresh copy of XBMC into this folder and try again.${reset}"
    rm -r "./XBMC"
    exit 1
fi

sed -i "s/0.0.000/$VERSION/g" "./XBMC/skins/Profile/language/English/strings.po"

if [ ! -d "./XBMC/skins/Manage Profiles" ]; then
    mkdir -p "./XBMC/skins/Manage Profiles/language/English"
fi

if [ ! -d "./XBMC/skins/DVD2Xbox Skin" ]; then
    mkdir -p "./XBMC/skins/DVD2Xbox Skin/language/English"
fi

cp "./XBMC/skins/Profile/language/English/strings.po" "./XBMC/skins/Manage Profiles/language/English/strings.po"
cp "./XBMC/skins/Profile/language/English/strings.po" "./XBMC/skins/DVD2Xbox Skin/language/English/strings.po"

# cp "Source/default.xbe" "./XBMC/default.xbe"

mv "./XBMC" "./XBMC4Gamers"

echo "${green}Done!${reset}"