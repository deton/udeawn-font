# UDEAWN font

wsltty等の端末エミュレータ向けに、East Asian Ambiguous文字等をNarrowにしたフォントです。

端末エミュレータ側が想定する幅と合わないと、テキストブラウザLynxなどで、文字が重なって読みにくいので、
UAX#11の[EastAsianWidth.txt](https://www.unicode.org/Public/UCD/latest/ucd/EastAsianWidth.txt)にある幅になるべく合わせています。

* EastAsianWidth.txtでNarrowなのに[BIZ UDゴシックではWideな文字](WidthMismatch.txt)も、FontForgeで半分幅に縮小しています。

## UDEAWNn font
BIZ UDゴシック内のEast Asian Ambiguous文字をFontForgeで半分幅に縮めたもの。
(ただし、元々半分幅に収まっている文字は、縮めずに半分領域をそのまま使用。)

一部文字はなるべく縦線が細くならないように幅を縮めていますが、
それ以外の文字は単に縮めているので、縦線が細めです。
丸数字等が縦長です。

* EastAsianWidth.txtでNarrowまたはAmbiguousで、BIZ UDゴシックに含まれない絵文字で、[NotoEmojiにある文字](WidthMismatchNotoEmoji.txt)に関して、FontForgeで半分幅に縮小して取り込んでいます。
  (でないと、fallbackフォントでWide幅で表示される場合が多いようなので)
  ![NotoEmojiから幅を縮めて取り込んでいる絵文字](https://user-images.githubusercontent.com/761487/233821627-4fcf334e-719f-4ac3-b641-4b344fbc1c89.png)

![udeawnn](https://user-images.githubusercontent.com/761487/232277599-22a81805-88a7-4e17-b689-1c011c2a9ed6.png)
(wslttyでの表示例。UDEAWNnフォントに含まれない文字は灰色背景。fallbackフォントで表示されている。)

### UDEAWNs font
UDEAWNnで取り込み対象にする絵文字に関して、Noto Emojiのかわりに
[Noto Emoji SVG](https://github.com/adobe-fonts/noto-emoji-svg/)
を使った版です。

* 絵文字が、黒白表示の際に黒が多くて少し見やすい印象。(上下のはみ出し多め)

### UDEAWNo font
取り込み対象にする絵文字に関して、
[EmojiOne Color. Black and White version](https://github.com/adobe-fonts/emojione-color)
[にある文字](WidthMismatchEmojiOne.txt)を使った版です。

* 絵文字が、Noto Emojiよりも見やすい印象。
* ただしNoto Emojiに比べて取り込み対象が4文字少ない。
* U+20E3(combining enclosing keycap)がつぶれて、中の文字が見えない

### UDEAWNd font
NotoEmojiでNarrow化時に見にくい絵文字は
[DejaVuSansMono](https://github.com/dejavu-fonts/dejavu-fonts)から取込

NotoEmojiに無い/白抜き/細かくて線が細い/枠付きなので縮めると細くなりがち、
な絵文字を、元からNarrowなDejaVuSansMonoから取込。

## UDEAWNi font
BIZ UDゴシック内のEast Asian Ambiguous文字の多くをIllusion-Nフォントにしたもの。

East Asian Ambiguous文字に関して、
+ BIZ UDゴシックで元々半分幅に収まっている文字は、半分領域をそのまま使用。
+ [Illusion-N](https://github.com/tomonic-x/Illusion)に含まれる文字は、Illusion-Nに置き換え。
+ Illusion-Nに含まれない文字は、FontForgeで半分幅に縮小。

[UDEV Gothic](https://github.com/yuru7/udev-gothic) の生成スクリプトを改造。

East Asian Ambiguous文字のリストは以下を参考に使用。
https://github.com/uwabami/locale-eaw-emoji/blob/master/EastAsianAmbiguous.txt

![udeawn](https://user-images.githubusercontent.com/761487/232278123-8aa5a254-5bc9-4d3b-9304-225521dfcf37.png)
(wslttyでの表示例。UDEAWNiフォントに含まれない文字は灰色背景。fallbackフォントで表示されている。)

## 備考
### wsltty設定
wslttyデフォルトだと、ローマ数字(Ⅲⅳ等)の表示幅が75%に縮められて少し読みにくくなるようなので、
回避したい場合は、設定ファイル(`%APPDATA%\wsltty\config`)に、`CharNarrowing=100`を追加。

### Vim設定
EastAsianWidth.txtに合わせてNarrowにすると、一部の絵文字が、Vimが想定する表示幅と合わなくなるようなので、
UDEAWNの幅に合わせるには、
cellwidth_udeawn.vimをVimの`'runtimepath'/plugin/`に置いてください。
(参考 https://github.com/rbtnn/vim-ambiwidth )

## ビルド

* OS: Ubuntu 22.04
* Tools
  * ttfautohint: 1.8.3
  * fonttools: 3.44.0
  * fontforge: 20201107

```sh
sudo apt-get install ttfautohint fontforge python2 python2-pip-whl
python2 /usr/share/python-wheels/pip-20.3.4-py2.py3-none-any.whl/pip install --no-index /usr/share/python-wheels/pip-20.3.4-py2.py3-none-any.whl
python2 -m pip install fonttools
python3 -m pip install ttfautohint-py
./make-n.sh
./make.sh
```

`pyftmerge`や`ttx`は、`$HOME/.local/bin`に入るので、
PATHに`$HOME/.local/bin`を入れている想定。

[HackGenのビルドツールインストール方法を参考](https://github.com/yuru7/HackGen#%E3%83%93%E3%83%AB%E3%83%89%E3%83%84%E3%83%BC%E3%83%AB%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E6%96%B9%E6%B3%95%E3%81%A8%E6%B3%A8%E6%84%8F%E7%82%B9)
