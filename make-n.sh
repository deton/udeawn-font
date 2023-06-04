#!/bin/bash
set -euo pipefail

BASE_DIR=$(cd $(dirname $0); pwd)
WORK_DIR="$BASE_DIR/build_tmp"
BUILD_DIR="$BASE_DIR/build"

VERSION='0.0.7'

FAMILYNAME="UDEAWNn"

if [ ! -d "$BUILD_DIR" ]
then
  mkdir "$BUILD_DIR"
fi
if [ ! -d "$WORK_DIR" ]
then
  mkdir "$WORK_DIR"
fi

if [ ! -d source/NotoEmoji ]
then
  curl -L https://fonts.google.com/download?family=Noto%20Emoji -o source/NotoEmoji.zip
  unzip -d source/NotoEmoji/ source/NotoEmoji.zip
fi

FONTS_DIRECTORIES="${BASE_DIR}/source/"
SRC_FONT_BIZUD_REGULAR='fontforge_export_BIZUDGothic-Regular.ttf'
SRC_FONT_BIZUD_BOLD='fontforge_export_BIZUDGothic-Bold.ttf'
SRC_FONT_NOTOEMOJI_REGULAR='NotoEmoji-SemiBold.ttf'
SRC_FONT_NOTOEMOJI_BOLD='NotoEmoji-Bold.ttf'

PATH_BIZUD_REGULAR=`find $FONTS_DIRECTORIES -follow -name "$SRC_FONT_BIZUD_REGULAR"`
PATH_BIZUD_BOLD=`find $FONTS_DIRECTORIES -follow -name "$SRC_FONT_BIZUD_BOLD"`
PATH_NOTOEMOJI_REGULAR=`find $FONTS_DIRECTORIES -follow -name "$SRC_FONT_NOTOEMOJI_REGULAR"`
PATH_NOTOEMOJI_BOLD=`find $FONTS_DIRECTORIES -follow -name "$SRC_FONT_NOTOEMOJI_BOLD"`

fontforge -script eaa2narrow.py "$PATH_BIZUD_REGULAR" "$FAMILYNAME" Regular "$VERSION" "$PATH_NOTOEMOJI_REGULAR"
mv "${FAMILYNAME}-Regular.ttf" "${WORK_DIR}"

fontforge -script eaa2narrow.py "$PATH_BIZUD_BOLD" "$FAMILYNAME" Bold "$VERSION" "$PATH_NOTOEMOJI_BOLD"
mv "${FAMILYNAME}-Bold.ttf" "${WORK_DIR}"

"${BASE_DIR}/os2_patch.sh" "$FAMILYNAME" "" 0
mv "$WORK_DIR/$FAMILYNAME"*.ttf "$BUILD_DIR"
rm -rf "$WORK_DIR"
