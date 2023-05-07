#!/usr/bin/fontforge
# stdinで(0x付きで)指定した文字コードのグリフが
# フォントファイルに含まれるかどうかをstdoutに出力する。
#   例: fontforge -script chkwidth.py source/NotoEmoji/static/NotoEmoji-Regular.ttf | \
#       cut -f1 -d' ' | \
#       fontforge -script chkexist.py source/fontforge_export_BIZUDGothic-Regular.ttf
import sys
import fontforge


def main(fontfile):
    font = fontforge.open(fontfile)
    for line in sys.stdin:
        ucode = int(line, base=16)
        if ucode in font and font[ucode].isWorthOutputting():
            print(f"0x{ucode:x} 1 {chr(ucode)}")
        else:
            print(f"0x{ucode:x} 0 {chr(ucode)}")
    font.close()


if __name__ == '__main__':
    # fontfile
    main(sys.argv[1])
