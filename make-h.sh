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

if [ ! -d source/NotoEmoji ]
then
  curl -L https://fonts.google.com/download?family=Noto%20Emoji -o source/NotoEmoji.zip
  unzip -d source/NotoEmoji/ source/NotoEmoji.zip
fi

"${BASE_DIR}/generator-h.sh" "$VERSION" "$FAMILYNAME"
"${BASE_DIR}/os2_patch.sh" "$FAMILYNAME" "" 0
mv "$WORK_DIR/$FAMILYNAME"*.ttf "$BUILD_DIR"
rm -rf "$WORK_DIR"
