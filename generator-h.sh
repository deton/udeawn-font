#!/bin/bash
set -euo pipefail

BASE_DIR=$(cd $(dirname $0); pwd)

WORK_DIR="$BASE_DIR/build_tmp"
if [ ! -d "$WORK_DIR" ]
then
  mkdir "$WORK_DIR"
fi

VERSION="$1"
FAMILYNAME="$2"

FONTS_DIRECTORIES="${BASE_DIR}/source/"

SRC_FONT_BIZUD_REGULAR='fontforge_export_BIZUDGothic-Regular.ttf'
SRC_FONT_BIZUD_BOLD='fontforge_export_BIZUDGothic-Bold.ttf'
SRC_FONT_EMOJIONE='EmojiOneBW.otf'

PATH_BIZUD_REGULAR=`find $FONTS_DIRECTORIES -follow -name "$SRC_FONT_BIZUD_REGULAR"`
PATH_BIZUD_BOLD=`find $FONTS_DIRECTORIES -follow -name "$SRC_FONT_BIZUD_BOLD"`
PATH_EMOJIONE=`find $FONTS_DIRECTORIES -follow -name "$SRC_FONT_EMOJIONE"`

MODIFIED_FONT_BIZUD_REGULAR='modified_bizud_regular.ttf'
MODIFIED_FONT_BIZUD_BOLD='modified_bizud_bold.ttf'

if [ -z "$SRC_FONT_BIZUD_REGULAR" -o -z "$SRC_FONT_BIZUD_BOLD" ]
then
  echo 'ソースフォントファイルが存在しない'
  exit 1
fi

fontforge -script eaa2narrow.py "$PATH_BIZUD_REGULAR" "$FAMILYNAME" Regular "$VERSION" "$PATH_EMOJIONE"
mv "${FAMILYNAME}-Regular.ttf" "${WORK_DIR}"

fontforge -script eaa2narrow.py "$PATH_BIZUD_BOLD" "$FAMILYNAME" Bold "$VERSION" "$PATH_EMOJIONE"
mv "${FAMILYNAME}-Bold.ttf" "${WORK_DIR}"

#for f in `ls "${WORK_DIR}/${FAMILYNAME}"*.ttf`
#do
#  python3 -m ttfautohint -l 6 -r 45 -a nnn -D latn -f none -S -W -X "13-" -I "$f" "${f}_hinted"
#done

#mv "${WORK_DIR}/${FAMILYNAME}-Regular.ttf_hinted" "${WORK_DIR}/${MODIFIED_FONT_BIZUD_REGULAR}"
#mv "${WORK_DIR}/${FAMILYNAME}-Bold.ttf_hinted" "${WORK_DIR}/${MODIFIED_FONT_BIZUD_BOLD}"
