#!/bin/bash
set -euo pipefail

BASE_DIR=$(cd $(dirname $0); pwd)
WORK_DIR="$BASE_DIR/build_tmp"
BUILD_DIR="$BASE_DIR/build"

VERSION='0.0.6'

FAMILYNAME="UDEAWH"

if [ ! -d "$BUILD_DIR" ]
then
  mkdir "$BUILD_DIR"
fi

"${BASE_DIR}/generator-h.sh" "$VERSION" "$FAMILYNAME"
"${BASE_DIR}/os2_patch.sh" "$FAMILYNAME" "" 0
"${BASE_DIR}/copyright-h.sh" "$FAMILYNAME"
mv "$WORK_DIR/$FAMILYNAME"*.ttf "$BUILD_DIR"
rm -rf "$WORK_DIR"
