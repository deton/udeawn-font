#!/bin/bash

BASE_DIR="$(cd $(dirname $0); pwd)/build_tmp"

FAMILYNAME="$1"
PREFIX="$2"

FONT_PATTERN=${PREFIX}${FAMILYNAME}'*.ttf'

COPYRIGHT='[BIZ UDGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[EmojiOne Color. Black and White version]
Copyright 2016 Adobe Systems Incorporated (https://github.com/adobe-fonts/emojione-color)

[UDEAWN]
Copyright (c) 2023 KIHARA, Hideto'

for P in ${BASE_DIR}/${FONT_PATTERN}
do
  ttx -t name -t post "$P"
  mv "${P%%.ttf}.ttx" ${BASE_DIR}/tmp.ttx
  cat ${BASE_DIR}/tmp.ttx | perl -pe "s?###COPYRIGHT###?$COPYRIGHT?" > "${P%%.ttf}.ttx"

  mv "$P" "${P}_orig"
  ttx -m "${P}_orig" "${P%%.ttf}.ttx"
done

rm -f "${BASE_DIR}/"*.ttx
