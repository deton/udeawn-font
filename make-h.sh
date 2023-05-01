#!/bin/bash
set -euo pipefail

BASE_DIR=$(cd $(dirname $0); pwd)
WORK_DIR="$BASE_DIR/build_tmp"
BUILD_DIR="$BASE_DIR/build"

VERSION='0.0.7'

FAMILYNAME="UDEAWH"

if [ ! -d "$BUILD_DIR" ]
then
  mkdir "$BUILD_DIR"
fi

if [ ! -d source/NotoEmoji ]
then
  curl -L https://fonts.google.com/download?family=Noto%20Emoji -o source/NotoEmoji.zip
  unzip -d source/NotoEmoji/ source/NotoEmoji.zip
fi

if [ ! -d source/dejavu-fonts-ttf-2.37 ]
then
  curl -L https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip -o source/dejavu-fonts-ttf-2.37.zip
  unzip -d source/ source/dejavu-fonts-ttf-2.37.zip
fi

"${BASE_DIR}/generator-h.sh" "$VERSION" "$FAMILYNAME"
"${BASE_DIR}/os2_patch.sh" "$FAMILYNAME" "" 0
"${BASE_DIR}/copyright-h.sh" "$FAMILYNAME"
mv "$WORK_DIR/$FAMILYNAME"*.ttf "$BUILD_DIR"
rm -rf "$WORK_DIR"
