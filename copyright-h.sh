#!/bin/bash

BASE_DIR="$(cd $(dirname $0); pwd)/build_tmp"

FAMILYNAME="$1"
PREFIX="$2"

FONT_PATTERN=${PREFIX}${FAMILYNAME}'*.ttf'

COPYRIGHT='[BIZ UDGothic]
Copyright 2022 The BIZ UDGothic Project Authors (https://github.com/googlefonts/morisawa-biz-ud-gothic)

[Noto Emoji]
Copyright 2013, 2022 Google Inc. (https://github.com/googlefonts/noto-emoji)

[DejaVu Sans Mono]
DejaVu fonts 2.37 (c)2004-2016 DejaVu fonts team
Fonts are (c) Bitstream (see below). DejaVu changes are in public domain.
Glyphs imported from Arev fonts are (c) Tavmjong Bah (see below)
Copyright (c) 2003 by Bitstream, Inc. All Rights Reserved. Bitstream Vera is
a trademark of Bitstream, Inc.
Copyright (c) 2006 by Tavmjong Bah. All Rights Reserved.

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
