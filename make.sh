#!/bin/bash

BASE_DIR=$(cd $(dirname $0); pwd)
WORK_DIR="$BASE_DIR/build_tmp"
BUILD_DIR="$BASE_DIR/build"

VERSION='0.0.3'

FAMILYNAME="UDEAWN"
DISP_FAMILYNAME="UDEAWN"
FAMILYNAME_LIGA="UDEAWNLG"
DISP_FAMILYNAME_LIGA="UDEAWN LG"
FAMILYNAME_JPDOC="UDEAWNJPDOC"
DISP_FAMILYNAME_JPDOC="UDEAWN JPDOC"
FAMILYNAME_NF="UDEAWNNF"
DISP_FAMILYNAME_NF="UDEAWN NF"
FAMILYNAME_NF_LIGA="UDEAWNNFLG"
DISP_FAMILYNAME_NF_LIGA="UDEAWN NFLG"
FAMILYNAME_35="UDEAWN35"
DISP_FAMILYNAME_35="UDEAWN 35"
FAMILYNAME_LIGA_35="UDEAWN35LG"
DISP_FAMILYNAME_LIGA_35="UDEAWN 35LG"
FAMILYNAME_JPDOC_35="UDEAWN35JPDOC"
DISP_FAMILYNAME_JPDOC_35="UDEAWN 35JPDOC"
FAMILYNAME_NF_35="UDEAWN35NF"
DISP_FAMILYNAME_NF_35="UDEAWN 35NF"
FAMILYNAME_NF_LIGA_35="UDEAWN35NFLG"
DISP_FAMILYNAME_NF_LIGA_35="UDEAWN 35NFLG"

if [ ! -d "$BUILD_DIR" ]
then
  mkdir "$BUILD_DIR"
fi

for italic_flag in 0 1
do
  # リガチャなし版の生成
  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME" "$DISP_FAMILYNAME" 0 0 0 0 $italic_flag
  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME" "" 0
  "${BASE_DIR}/cmap_patch.sh" "$FAMILYNAME"
  "${BASE_DIR}/copyright.sh" "$FAMILYNAME"
  mv "$WORK_DIR/$FAMILYNAME"*.ttf "$BUILD_DIR"
  rm -rf "$WORK_DIR"

  # リガチャあり版の生成
#  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME_LIGA" "$DISP_FAMILYNAME_LIGA" 1 0 0 0 $italic_flag
#  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME_LIGA" "" 0
#  "${BASE_DIR}/cmap_patch.sh" "$FAMILYNAME_LIGA"
#  "${BASE_DIR}/copyright.sh" "$FAMILYNAME_LIGA"
#  mv "$WORK_DIR/$FAMILYNAME_LIGA"*.ttf "$BUILD_DIR"
#  rm -rf "$WORK_DIR"
#
#  # JPDOC版の生成
#  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME_JPDOC" "$DISP_FAMILYNAME_JPDOC" 0 1 0 0 $italic_flag
#  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME_JPDOC" "" 0
#  "${BASE_DIR}/cmap_patch.sh" "$FAMILYNAME_JPDOC"
#  "${BASE_DIR}/copyright.sh" "$FAMILYNAME_JPDOC"
#  mv "$WORK_DIR/$FAMILYNAME_JPDOC"*.ttf "$BUILD_DIR"
#  rm -rf "$WORK_DIR"
#
#  # Nerd Fonts版の生成 - リガチャなし
#  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME_NF" "$DISP_FAMILYNAME_NF" 0 0 1 0 $italic_flag
#  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME_NF" "" 0
#  "${BASE_DIR}/copyright.sh" "$FAMILYNAME_NF"
#  mv "$WORK_DIR/$FAMILYNAME_NF"*.ttf "$BUILD_DIR"
#  rm -rf "$WORK_DIR"
#
#  # Nerd Fonts版の生成 - リガチャあり
#  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME_NF_LIGA" "$DISP_FAMILYNAME_NF_LIGA" 1 0 1 0 $italic_flag
#  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME_NF_LIGA" "" 0
#  "${BASE_DIR}/copyright.sh" "$FAMILYNAME_NF_LIGA"
#  mv "$WORK_DIR/$FAMILYNAME_NF_LIGA"*.ttf "$BUILD_DIR"
#  rm -rf "$WORK_DIR"
#
#  # リガチャなし版の生成 (3:5幅)
#  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME_35" "$DISP_FAMILYNAME_35" 0 0 0 1 $italic_flag
#  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME_35" "" 1
#  "${BASE_DIR}/cmap_patch.sh" "$FAMILYNAME_35"
#  "${BASE_DIR}/copyright.sh" "$FAMILYNAME_35"
#  mv "$WORK_DIR/$FAMILYNAME_35"*.ttf "$BUILD_DIR"
#  rm -rf "$WORK_DIR"
#
#  # リガチャあり版の生成 (3:5幅)
#  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME_LIGA_35" "$DISP_FAMILYNAME_LIGA_35" 1 0 0 1 $italic_flag
#  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME_LIGA_35" "" 1
#  "${BASE_DIR}/cmap_patch.sh" "$FAMILYNAME_LIGA_35"
#  "${BASE_DIR}/copyright.sh" "$FAMILYNAME_LIGA_35"
#  mv "$WORK_DIR/$FAMILYNAME_LIGA_35"*.ttf "$BUILD_DIR"
#  rm -rf "$WORK_DIR"
#
#  # JPDOC版の生成 (3:5幅)
#  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME_JPDOC_35" "$DISP_FAMILYNAME_JPDOC_35" 0 1 0 1 $italic_flag
#  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME_JPDOC_35" "" 1
#  "${BASE_DIR}/cmap_patch.sh" "$FAMILYNAME_JPDOC_35"
#  "${BASE_DIR}/copyright.sh" "$FAMILYNAME_JPDOC_35"
#  mv "$WORK_DIR/$FAMILYNAME_JPDOC_35"*.ttf "$BUILD_DIR"
#  rm -rf "$WORK_DIR"
#
#  # Nerd Fonts版の生成 - リガチャなし (3:5幅)
#  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME_NF_35" "$DISP_FAMILYNAME_NF_35" 0 0 1 1 $italic_flag
#  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME_NF_35" "" 1
#  "${BASE_DIR}/copyright.sh" "$FAMILYNAME_NF_35"
#  mv "$WORK_DIR/$FAMILYNAME_NF_35"*.ttf "$BUILD_DIR"
#  rm -rf "$WORK_DIR"
#
#  # Nerd Fonts版の生成 - リガチャあり (3:5幅)
#  "${BASE_DIR}/generator.sh" "$VERSION" "$FAMILYNAME_NF_LIGA_35" "$DISP_FAMILYNAME_NF_LIGA_35" 1 0 1 1 $italic_flag
#  "${BASE_DIR}/os2_patch.sh" "$FAMILYNAME_NF_LIGA_35" "" 1
#  "${BASE_DIR}/copyright.sh" "$FAMILYNAME_NF_LIGA_35"
#  mv "$WORK_DIR/$FAMILYNAME_NF_LIGA_35"*.ttf "$BUILD_DIR"
#  rm -rf "$WORK_DIR"
done
