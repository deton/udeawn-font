#!/bin/bash
set -euo pipefail

BASE_DIR=$(cd $(dirname $0); pwd)
WORK_DIR="$BASE_DIR/build_tmp"
BUILD_DIR="$BASE_DIR/build"

VERSION='0.0.5'

FAMILYNAME="UDEAWN"
DISP_FAMILYNAME="UDEAWN"

if [ ! -d "$BUILD_DIR" ]
then
  mkdir "$BUILD_DIR"
fi

for italic_flag in 0 1
do
  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME" "$DISP_FAMILYNAME" $italic_flag
  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME" "" 0
  "${BASE_DIR}/cmap_patch.sh" "$FAMILYNAME"
  "${BASE_DIR}/copyright.sh" "$FAMILYNAME"
  mv "$WORK_DIR/$FAMILYNAME"*.ttf "$BUILD_DIR"
  rm -rf "$WORK_DIR"
done
