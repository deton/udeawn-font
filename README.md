# UDEAWN/UDEAWH font

## UDEAWN font
BIZ UDゴシック内のEast Asian Ambiguous文字のみをNarrowにしたもの。

East Asian Ambiguous文字に関して、
+ BIZ UDゴシックで元々半分幅に収まっている文字は、半分領域をそのまま使用。
+ [Illusion-N](https://github.com/tomonic-x/Illusion)に含まれる文字は、Illusion-Nに置き換え。
+ Illusion-Nに含まれない文字は、FontForgeで半分幅に縮小。

[UDEV Gothic](https://github.com/yuru7/udev-gothic) の生成スクリプトを改造。

East Asian Ambiguous文字のリストは以下を参考に使用。
https://github.com/uwabami/locale-eaw-emoji/blob/master/EastAsianAmbiguous.txt

![udeawn](https://user-images.githubusercontent.com/761487/222949949-fe8dfa6d-582a-4276-8d3c-bbaf7fa08059.png)

## UDEAWH font
BIZ UDゴシック内のEast Asian Ambiguous文字をFontForgeで半分幅に縮めたもの。
(ただし、元々半分幅に収まっている文字は、縮めずに半分領域をそのまま使用。)

単に縮めているので、縦線が細めです。丸数字等が縦長です。

![udeawh](https://user-images.githubusercontent.com/761487/221395252-e00bd075-fe9c-44e5-a1bc-ec54006f756c.png)

## ビルド環境

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
```

`pyftmerge`や`ttx`は、`$HOME/.local/bin`に入るので、
PATHに`$HOME/.local/bin`を入れている想定。

[HackGenのビルドツールインストール方法を参考](https://github.com/yuru7/HackGen#%E3%83%93%E3%83%AB%E3%83%89%E3%83%84%E3%83%BC%E3%83%AB%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E6%96%B9%E6%B3%95%E3%81%A8%E6%B3%A8%E6%84%8F%E7%82%B9)
