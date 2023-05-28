#!/usr/bin/fontforge
# East Asian Ambiguousなグリフの幅を半分に縮める
#   Usage: fontforge -script eaa2narrow.py <srcfont.ttf> <fontfamily> <fontstyle> <version> [emojifont.ttf] [emojifont2.ttf]
#   Ex: fontforge -script eaa2narrow.py source/fontforge_export_BIZUDGothic-Regular.ttf UDEAWNo Regular 0.0.1 source/EmojiOneBW.otf source/NotoEmoji/static/NotoEmoji-SemiBold.ttf
import datetime
import math
import sys
import fontforge
import psMat

# 幅を縮小後に残しておく、左右side bearing(余白)の合計値。
# 小さすぎる(60)と、U+2030(‰)がwslttyのCharNarrowing=75設定で縮められる場合あり
# XXX:大きくしても(512)、ローマ数字(U+2161 Ⅱ等)は上記設定で縮められる模様
SIDE_BEARING = 60

# East Asian Ambiguousのリスト
# のうち、BIZ UDゴシックで元々半分幅に収まっている文字
eaw_useright = (0x2018, 0x201C)
eaw_useleft = (0x00B0, 0x2019, 0x201D, 0x2032, 0x2033)
# https://github.com/uwabami/locale-eaw-emoji/blob/master/EastAsianAmbiguous.txt
eaw_array = (
    0x00A1, 0x00A4, 0x00A7, 0x00A8, 0x00AA, 0x00AD, 0x00AE, 0x00B0, 0x00B1,
    0x00B2, 0x00B3, 0x00B4, 0x00B6, 0x00B7, 0x00B8, 0x00B9, 0x00BA, 0x00BC,
    0x00BD, 0x00BE, 0x00BF, 0x00C6, 0x00D0, 0x00D7, 0x00D8, 0x00DE, 0x00DF,
    0x00E0, 0x00E1, 0x00E6, 0x00E8, 0x00E9, 0x00EA, 0x00EC, 0x00ED, 0x00F0,
    0x00F2, 0x00F3, 0x00F7, 0x00F8, 0x00F9, 0x00FA, 0x00FC, 0x00FE, 0x0101,
    0x0111, 0x0113, 0x011B, 0x0126, 0x0127, 0x012B, 0x0131, 0x0132, 0x0133,
    0x0138, 0x013F, 0x0140, 0x0141, 0x0142, 0x0144, 0x0148, 0x0149, 0x014A,
    0x014B, 0x014D, 0x0152, 0x0153, 0x0166, 0x0167, 0x016B, 0x01CE, 0x01D0,
    0x01D2, 0x01D4, 0x01D6, 0x01D8, 0x01DA, 0x01DC, 0x0251, 0x0261, 0x02C4,
    0x02C7, 0x02C9, 0x02CA, 0x02CB, 0x02CD, 0x02D0, 0x02D8, 0x02D9, 0x02DA,
    0x02DB, 0x02DD, 0x02DF, 0x0391, 0x0392, 0x0393, 0x0394, 0x0395, 0x0396,
    0x0397, 0x0398, 0x0399, 0x039A, 0x039B, 0x039C, 0x039D, 0x039E, 0x039F,
    0x03A0, 0x03A1, 0x03A3, 0x03A4, 0x03A5, 0x03A6, 0x03A7, 0x03A8, 0x03A9,
    0x03B1, 0x03B2, 0x03B3, 0x03B4, 0x03B5, 0x03B6, 0x03B7, 0x03B8, 0x03B9,
    0x03BA, 0x03BB, 0x03BC, 0x03BD, 0x03BE, 0x03BF, 0x03C0, 0x03C1, 0x03C3,
    0x03C4, 0x03C5, 0x03C6, 0x03C7, 0x03C8, 0x03C9, 0x0401, 0x0410, 0x0411,
    0x0412, 0x0413, 0x0414, 0x0415, 0x0416, 0x0417, 0x0418, 0x0419, 0x041A,
    0x041B, 0x041C, 0x041D, 0x041E, 0x041F, 0x0420, 0x0421, 0x0422, 0x0423,
    0x0424, 0x0425, 0x0426, 0x0427, 0x0428, 0x0429, 0x042A, 0x042B, 0x042C,
    0x042D, 0x042E, 0x042F, 0x0430, 0x0431, 0x0432, 0x0433, 0x0434, 0x0435,
    0x0436, 0x0437, 0x0438, 0x0439, 0x043A, 0x043B, 0x043C, 0x043D, 0x043E,
    0x043F, 0x0440, 0x0441, 0x0442, 0x0443, 0x0444, 0x0445, 0x0446, 0x0447,
    0x0448, 0x0449, 0x044A, 0x044B, 0x044C, 0x044D, 0x044E, 0x044F, 0x0451,
    0x2010, 0x2013, 0x2014, 0x2015, 0x2016, 0x2018, 0x2019, 0x201C, 0x201D,
    0x2020, 0x2021, 0x2022, 0x2024, 0x2025, 0x2026, 0x2027, 0x2030, 0x2032,
    0x2033, 0x2035, 0x203B, 0x203E, 0x2074, 0x207F, 0x2080, 0x2081, 0x2082,
    0x2083, 0x2084, 0x20AC, 0x2103, 0x2105, 0x2109, 0x2113, 0x2116, 0x2121,
    0x2122, 0x2126, 0x212B, 0x2153, 0x2154, 0x215B, 0x215C, 0x215D, 0x215E,
    0x2160, 0x2161, 0x2162, 0x2163, 0x2164, 0x2165, 0x2166, 0x2167, 0x2168,
    0x2169, 0x216A, 0x216B, 0x2170, 0x2171, 0x2172, 0x2173, 0x2174, 0x2175,
    0x2176, 0x2177, 0x2178, 0x2179, 0x2189, 0x2190, 0x2191, 0x2192, 0x2193,
    0x2194, 0x2195, 0x2196, 0x2197, 0x2198, 0x2199, 0x21B8, 0x21B9, 0x21D2,
    0x21D4, 0x21E7, 0x2200, 0x2202, 0x2203, 0x2207, 0x2208, 0x220B, 0x220F,
    0x2211, 0x2215, 0x221A, 0x221D, 0x221E, 0x221F, 0x2220, 0x2223, 0x2225,
    0x2227, 0x2228, 0x2229, 0x222A, 0x222B, 0x222C, 0x222E, 0x2234, 0x2235,
    0x2236, 0x2237, 0x223C, 0x223D, 0x2248, 0x224C, 0x2252, 0x2260, 0x2261,
    0x2264, 0x2265, 0x2266, 0x2267, 0x226A, 0x226B, 0x226E, 0x226F, 0x2282,
    0x2283, 0x2286, 0x2287, 0x2295, 0x2299, 0x22A5, 0x22BF, 0x2312, 0x2460,
    0x2461, 0x2462, 0x2463, 0x2464, 0x2465, 0x2466, 0x2467, 0x2468, 0x2469,
    0x246A, 0x246B, 0x246C, 0x246D, 0x246E, 0x246F, 0x2470, 0x2471, 0x2472,
    0x2473, 0x2474, 0x2475, 0x2476, 0x2477, 0x2478, 0x2479, 0x247A, 0x247B,
    0x247C, 0x247D, 0x247E, 0x247F, 0x2480, 0x2481, 0x2482, 0x2483, 0x2484,
    0x2485, 0x2486, 0x2487, 0x2488, 0x2489, 0x248A, 0x248B, 0x248C, 0x248D,
    0x248E, 0x248F, 0x2490, 0x2491, 0x2492, 0x2493, 0x2494, 0x2495, 0x2496,
    0x2497, 0x2498, 0x2499, 0x249A, 0x249B, 0x249C, 0x249D, 0x249E, 0x249F,
    0x24A0, 0x24A1, 0x24A2, 0x24A3, 0x24A4, 0x24A5, 0x24A6, 0x24A7, 0x24A8,
    0x24A9, 0x24AA, 0x24AB, 0x24AC, 0x24AD, 0x24AE, 0x24AF, 0x24B0, 0x24B1,
    0x24B2, 0x24B3, 0x24B4, 0x24B5, 0x24B6, 0x24B7, 0x24B8, 0x24B9, 0x24BA,
    0x24BB, 0x24BC, 0x24BD, 0x24BE, 0x24BF, 0x24C0, 0x24C1, 0x24C2, 0x24C3,
    0x24C4, 0x24C5, 0x24C6, 0x24C7, 0x24C8, 0x24C9, 0x24CA, 0x24CB, 0x24CC,
    0x24CD, 0x24CE, 0x24CF, 0x24D0, 0x24D1, 0x24D2, 0x24D3, 0x24D4, 0x24D5,
    0x24D6, 0x24D7, 0x24D8, 0x24D9, 0x24DA, 0x24DB, 0x24DC, 0x24DD, 0x24DE,
    0x24DF, 0x24E0, 0x24E1, 0x24E2, 0x24E3, 0x24E4, 0x24E5, 0x24E6, 0x24E7,
    0x24E8, 0x24E9, 0x24EB, 0x24EC, 0x24ED, 0x24EE, 0x24EF, 0x24F0, 0x24F1,
    0x24F2, 0x24F3, 0x24F4, 0x24F5, 0x24F6, 0x24F7, 0x24F8, 0x24F9, 0x24FA,
    0x24FB, 0x24FC, 0x24FD, 0x24FE, 0x24FF, 0x2500, 0x2501, 0x2502, 0x2503,
    0x2504, 0x2505, 0x2506, 0x2507, 0x2508, 0x2509, 0x250A, 0x250B, 0x250C,
    0x250D, 0x250E, 0x250F, 0x2510, 0x2511, 0x2512, 0x2513, 0x2514, 0x2515,
    0x2516, 0x2517, 0x2518, 0x2519, 0x251A, 0x251B, 0x251C, 0x251D, 0x251E,
    0x251F, 0x2520, 0x2521, 0x2522, 0x2523, 0x2524, 0x2525, 0x2526, 0x2527,
    0x2528, 0x2529, 0x252A, 0x252B, 0x252C, 0x252D, 0x252E, 0x252F, 0x2530,
    0x2531, 0x2532, 0x2533, 0x2534, 0x2535, 0x2536, 0x2537, 0x2538, 0x2539,
    0x253A, 0x253B, 0x253C, 0x253D, 0x253E, 0x253F, 0x2540, 0x2541, 0x2542,
    0x2543, 0x2544, 0x2545, 0x2546, 0x2547, 0x2548, 0x2549, 0x254A, 0x254B,
    0x2550, 0x2551, 0x2552, 0x2553, 0x2554, 0x2555, 0x2556, 0x2557, 0x2558,
    0x2559, 0x255A, 0x255B, 0x255C, 0x255D, 0x255E, 0x255F, 0x2560, 0x2561,
    0x2562, 0x2563, 0x2564, 0x2565, 0x2566, 0x2567, 0x2568, 0x2569, 0x256A,
    0x256B, 0x256C, 0x256D, 0x256E, 0x256F, 0x2570, 0x2571, 0x2572, 0x2573,
    0x2580, 0x2581, 0x2582, 0x2583, 0x2584, 0x2585, 0x2586, 0x2587, 0x2588,
    0x2589, 0x258A, 0x258B, 0x258C, 0x258D, 0x258E, 0x258F, 0x2592, 0x2593,
    0x2594, 0x2595, 0x25A0, 0x25A1, 0x25A3, 0x25A4, 0x25A5, 0x25A6, 0x25A7,
    0x25A8, 0x25A9, 0x25B2, 0x25B3, 0x25B6, 0x25B7, 0x25BC, 0x25BD, 0x25C0,
    0x25C1, 0x25C6, 0x25C7, 0x25C8, 0x25CB, 0x25CE, 0x25CF, 0x25D0, 0x25D1,
    0x25E2, 0x25E3, 0x25E4, 0x25E5, 0x25EF, 0x2605, 0x2606, 0x2609, 0x260E,
    0x260F, 0x261C, 0x261E, 0x2640, 0x2642, 0x2660, 0x2661, 0x2662, 0x2663,
    0x2664, 0x2665, 0x2666, 0x2667, 0x2668, 0x2669, 0x266A, 0x266C, 0x266D,
    0x266F, 0x269E, 0x269F, 0x26BF, 0x26C6, 0x26C7, 0x26C8, 0x26C9, 0x26CA,
    0x26CB, 0x26CC, 0x26CD, 0x26CF, 0x26D0, 0x26D1, 0x26D2, 0x26D3, 0x26D5,
    0x26D6, 0x26D7, 0x26D8, 0x26D9, 0x26DA, 0x26DB, 0x26DC, 0x26DD, 0x26DE,
    0x26DF, 0x26E0, 0x26E1, 0x26E3, 0x26E8, 0x26E9, 0x26EB, 0x26EC, 0x26ED,
    0x26EE, 0x26EF, 0x26F0, 0x26F1, 0x26F4, 0x26F6, 0x26F7, 0x26F8, 0x26F9,
    0x26FB, 0x26FC, 0x26FE, 0x26FF, 0x273D, 0x2776, 0x2777, 0x2778, 0x2779,
    0x277A, 0x277B, 0x277C, 0x277D, 0x277E, 0x277F, 0x2B56, 0x2B57, 0x2B58,
    0x2B59, 0x3248, 0x3249, 0x324A, 0x324B, 0x324C, 0x324D, 0x324E, 0x324F,
    0xFFFD,
    0x0001F100, 0x0001F101, 0x0001F102, 0x0001F103, 0x0001F104, 0x0001F105,
    0x0001F106, 0x0001F107, 0x0001F108, 0x0001F109, 0x0001F10A, 0x0001F110,
    0x0001F111, 0x0001F112, 0x0001F113, 0x0001F114, 0x0001F115, 0x0001F116,
    0x0001F117, 0x0001F118, 0x0001F119, 0x0001F11A, 0x0001F11B, 0x0001F11C,
    0x0001F11D, 0x0001F11E, 0x0001F11F, 0x0001F120, 0x0001F121, 0x0001F122,
    0x0001F123, 0x0001F124, 0x0001F125, 0x0001F126, 0x0001F127, 0x0001F128,
    0x0001F129, 0x0001F12A, 0x0001F12B, 0x0001F12C, 0x0001F12D, 0x0001F130,
    0x0001F131, 0x0001F132, 0x0001F133, 0x0001F134, 0x0001F135, 0x0001F136,
    0x0001F137, 0x0001F138, 0x0001F139, 0x0001F13A, 0x0001F13B, 0x0001F13C,
    0x0001F13D, 0x0001F13E, 0x0001F13F, 0x0001F140, 0x0001F141, 0x0001F142,
    0x0001F143, 0x0001F144, 0x0001F145, 0x0001F146, 0x0001F147, 0x0001F148,
    0x0001F149, 0x0001F14A, 0x0001F14B, 0x0001F14C, 0x0001F14D, 0x0001F14E,
    0x0001F14F, 0x0001F150, 0x0001F151, 0x0001F152, 0x0001F153, 0x0001F154,
    0x0001F155, 0x0001F156, 0x0001F157, 0x0001F158, 0x0001F159, 0x0001F15A,
    0x0001F15B, 0x0001F15C, 0x0001F15D, 0x0001F15E, 0x0001F15F, 0x0001F160,
    0x0001F161, 0x0001F162, 0x0001F163, 0x0001F164, 0x0001F165, 0x0001F166,
    0x0001F167, 0x0001F168, 0x0001F169, 0x0001F170, 0x0001F171, 0x0001F172,
    0x0001F173, 0x0001F174, 0x0001F175, 0x0001F176, 0x0001F177, 0x0001F178,
    0x0001F179, 0x0001F17A, 0x0001F17B, 0x0001F17C, 0x0001F17D, 0x0001F17E,
    0x0001F17F, 0x0001F180, 0x0001F181, 0x0001F182, 0x0001F183, 0x0001F184,
    0x0001F185, 0x0001F186, 0x0001F187, 0x0001F188, 0x0001F189, 0x0001F18A,
    0x0001F18B, 0x0001F18C, 0x0001F18D, 0x0001F18F, 0x0001F190, 0x0001F19B,
    0x0001F19C, 0x0001F19D, 0x0001F19E, 0x0001F19F, 0x0001F1A0, 0x0001F1A1,
    0x0001F1A2, 0x0001F1A3, 0x0001F1A4, 0x0001F1A5, 0x0001F1A6, 0x0001F1A7,
    0x0001F1A8, 0x0001F1A9, 0x0001F1AA, 0x0001F1AB, 0x0001F1AC)

# EastAsianWidth.txtで;Wや;FでないのにBIZ UDゴシックではWideになっている文字
expect_narrow = (
    0x01CD, 0x01D1, 0x2051, 0x213B, 0x217A, 0x217B, 0x217F, 0x2318, 0x23A7,
    0x23A8, 0x23A9, 0x23AB, 0x23AC, 0x23AD, 0x23BE, 0x23BF, 0x23C0, 0x23C1,
    0x23C2, 0x23C3, 0x23C4, 0x23C5, 0x23C6, 0x23C7, 0x23C8, 0x23C9, 0x23CA,
    0x23CB, 0x23CC, 0x23CE, 0x2423, 0x24EA, 0x2600, 0x2601, 0x2602, 0x2603,
    0x2616, 0x2617, 0x261D, 0x261F, 0x2713, 0x2756, 0x27A1, 0x29BF, 0x2B05,
    0x2B06, 0x2B07)

# Narrowにしてマージする絵文字リスト。
# EastAsianWidth.txtで;Wや;FでないのにNotoEmojiではWideになっている文字
emojis = (
    0x203c, 0x2049, 0x20e3, 0x2122, 0x2139, 0x2194, 0x2195, 0x2196, 0x2197,
    0x2198, 0x2199, 0x21a9, 0x21aa, 0x2328, 0x23cf, 0x23ed, 0x23ee, 0x23ef,
    0x23f1, 0x23f2, 0x23f8, 0x23f9, 0x23fa, 0x24c2, 0x25b6, 0x25c0,
    # medium squareの縮小率に合わせてsmall squareを縮小するのでmedium->small順
    0x25fb, 0x25fc, 0x25aa, 0x25ab,
    0x2600, 0x2601, 0x2602, 0x2603, 0x2604, 0x260e,
    0x2611, 0x2618, 0x261d, 0x2620, 0x2622, 0x2623, 0x2626, 0x262a, 0x262e,
    0x262f, 0x2638, 0x2639, 0x263a, 0x2640, 0x2642, 0x265f, 0x2660, 0x2663,
    0x2665, 0x2666, 0x2668, 0x267b, 0x267e, 0x2692, 0x2694, 0x2695, 0x2696,
    0x2697, 0x2699, 0x269b, 0x269c, 0x26a0, 0x26a7, 0x26b0, 0x26b1, 0x26c8,
    0x26cf, 0x26d1, 0x26d3, 0x26e9, 0x26f0, 0x26f1, 0x26f4, 0x26f7, 0x26f8,
    0x26f9, 0x2702, 0x2708, 0x2709, 0x270c, 0x270d, 0x270f, 0x2712, 0x2714,
    0x2716, 0x271d, 0x2721, 0x2733, 0x2734, 0x2744, 0x2747, 0x2763, 0x2764,
    0x27a1, 0x2934, 0x2935, 0x2b05, 0x2b06, 0x2b07,
    0x1f170, 0x1f171, 0x1f17e, 0x1f17f, 0x1f1e6, 0x1f1e7, 0x1f1e8, 0x1f1e9,
    0x1f1ea, 0x1f1eb, 0x1f1ec, 0x1f1ed, 0x1f1ee, 0x1f1ef, 0x1f1f0, 0x1f1f1,
    0x1f1f2, 0x1f1f3, 0x1f1f4, 0x1f1f5, 0x1f1f6, 0x1f1f7, 0x1f1f8, 0x1f1f9,
    0x1f1fa, 0x1f1fb, 0x1f1fc, 0x1f1fd, 0x1f1fe, 0x1f1ff, 0x1f321, 0x1f324,
    0x1f325, 0x1f326, 0x1f327, 0x1f328, 0x1f329, 0x1f32a, 0x1f32b, 0x1f32c,
    0x1f336, 0x1f37d, 0x1f396, 0x1f397, 0x1f399, 0x1f39a, 0x1f39b, 0x1f39e,
    0x1f39f, 0x1f3cb, 0x1f3cc, 0x1f3cd, 0x1f3ce, 0x1f3d4, 0x1f3d5, 0x1f3d6,
    0x1f3d7, 0x1f3d8, 0x1f3d9, 0x1f3da, 0x1f3db, 0x1f3dc, 0x1f3dd, 0x1f3de,
    0x1f3df, 0x1f3f3, 0x1f3f5, 0x1f3f7, 0x1f43f, 0x1f441, 0x1f4fd, 0x1f549,
    0x1f54a, 0x1f56f, 0x1f570, 0x1f573, 0x1f574, 0x1f575, 0x1f576, 0x1f577,
    0x1f578, 0x1f579, 0x1f587, 0x1f58a, 0x1f58b, 0x1f58c, 0x1f58d, 0x1f590,
    0x1f5a5, 0x1f5a8, 0x1f5b1, 0x1f5b2, 0x1f5bc, 0x1f5c2, 0x1f5c3, 0x1f5c4,
    0x1f5d1, 0x1f5d2, 0x1f5d3, 0x1f5dc, 0x1f5dd, 0x1f5de, 0x1f5e1, 0x1f5e3,
    0x1f5e8, 0x1f5ef, 0x1f5f3, 0x1f5fa, 0x1f6cb, 0x1f6cd, 0x1f6ce, 0x1f6cf,
    0x1f6e0, 0x1f6e1, 0x1f6e2, 0x1f6e3, 0x1f6e4, 0x1f6e5, 0x1f6e9, 0x1f6f0,
    0x1f6f3)


def add_variationSelector(f):
    """
    Variation Selectorに空グリフを追加する。
    wslttyで四角入りXが重なって表示されないように。
    """
    f.selection.select(0x0020)  # space
    f.copy()
    # emoji用(0xFE0E,0xFE0F)と、doc/ivs.txt で使われているもの
    for ucode in (*range(0xFE00, 0xFE10), *range(0xE0100, 0xE0105)):
        f.selection.select(ucode)
        f.paste()
        f[ucode].width = 0


def narrow(g, halfWidth):
    """文字幅をNarrowに収まるように縮める"""
    xmin, ymin, xmax, ymax = g.boundingBox()
    boxw = xmax - xmin
    if boxw > halfWidth:
        # side bearing(余白)を加える
        scalex = halfWidth / (boxw + SIDE_BEARING)
        g.transform(psMat.scale(scalex, 1))
    g.width = halfWidth
    centerInWidth(g)


def g_warningsign(f, g, halfWidth):
    # !の幅は縮めずに△の下側左右端の位置を移動することで幅を縮める。
    # 全体の幅を縮めると!も細くなって見にくくなるので。

    def identify_parts(layer):
        # 各部品(三角外枠, 三角内枠, 棒, 点)のcontourを特定して返す。
        # (emojifontごとに、どのcontourが外側白三角に該当するかが異なるので)
        partsymax = []
        for c in layer:
            xmin, ymin, xmax, ymax = c.boundingBox()
            partsymax.append((c, ymax))
        partsymax.sort(key=lambda x: x[1], reverse=True)
        return [x[0] for x in partsymax]

    xmin, ymin, xmax, ymax = g.boundingBox()
    boxw = xmax - xmin
    if boxw <= halfWidth:
        return
    # expect: ((xmax - dx) - (xmin + dx) + SIDE_BEARING) <= halfWidth
    dx = (xmax - xmin + SIDE_BEARING - halfWidth) / 2
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    layer = g.layers[g.activeLayer]
    ctriout, ctriin, cbar, cdot = identify_parts(layer)
    # 上下にはみ出ている
    if ymin < -f.descent:  # fはUDEAWN。g.fontはemojifont
        dy = -f.descent - ymin
        # 三角枠を上に移動して、下端を枠に収める
        ctriout.transform(psMat.translate(0, dy))
        ctriin.transform(psMat.translate(0, dy))
        ymax += dy
    dya = 0
    if ymax > f.ascent:
        dya = f.ascent - ymax
    for c in (ctriout, ctriin):  # 三角枠
        for p in c:
            if p.y < cy:  # 下側端を左右内寄りに移動
                if p.x < cx:
                    p.x += dx
                else:
                    p.x -= dx
            else:  # 上端がはみ出ないように下に移動
                p.y += dya

    # !が上寄りなので少し下に移動する。
    # 三角内枠の下線と、点の間隔が、棒と点の間隔と同じになるよう移動。
    # (XXX:少し下げすぎかも?)
    xminb, yminb, xmaxb, ymaxb = cbar.boundingBox()
    xmind, ymind, xmaxd, ymaxd = cdot.boundingBox()
    ydiffref = yminb - ymaxd
    xmint, ymint, xmaxt, ymaxt = ctriin.boundingBox()
    ydiff = ymind - ymint
    if ydiff > ydiffref:
        dy = ydiff - ydiffref
        cdot.transform(psMat.translate(0, -dy))
        cbar.transform(psMat.translate(0, -dy))

    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def add_emoji(f, halfWidth, emojifontfile, emojilist, overwrite=False):
    """
    Ambiguous幅な絵文字や、
    fallbackフォントでWide幅だが、EastAsianWidth.txtで;Wでも;Fでもない絵文字を
    Narrowにしてコピペする
    """

    def getydiff():
        g = emojifont[0x26d3]  # chains(⛓)
        xmin, ymin, xmax, ymax = g.boundingBox()
        boxh = ymax - ymin
        # ymax位置をf.ascent+余白の位置に配置
        # expect: f.ascent - (ymax + ydiff) = (emojifont.em - boxh) / 2
        ydiff = f.ascent - ymax - (emojifont.em - boxh) / 2
        cy = (ymax + ymin) / 2 + ydiff
        return ydiff, cy

    if not emojifontfile:
        return
    emojifont = fontforge.open(emojifontfile)
    emojifont.em = f.em  # EmojiOneBWは拡大
    ydiff, cy = getydiff()
    trcen = psMat.translate(0, -cy)
    # regional indicator symbol letter群用のscale。
    # 文字ごとにscaleがばらばらだとIだけ太くて違和感があるのでそろえる。
    regional_indicator_scale = halfWidth / maxboxwidth(emojifont, range(0x1f1e6, 0x1f200))
    for ucode in emojilist:
        if not overwrite and ucode in f:
            continue  # 既に含まれているグリフは上書きしない
        if ucode not in emojifont:
            continue
        g = emojifont[ucode]
        g.transform(psMat.translate(0, ydiff))
        if ucode == 0x25fb:  # white medium square(◻)
            scalewms = scalexy(g, halfWidth)
        elif ucode == 0x25fc:  # black medium square(◼)
            scalebms = scalexy(g, halfWidth)
        elif ucode == 0x25ab:  # white small square(▫)
            scalexy(g, halfWidth, scale=scalewms)
        elif ucode == 0x25aa:  # black small square(▪)
            scalexy(g, halfWidth, scale=scalebms)
        elif ucode in (0x2611, 0x2716):
            # ballot box with check(☑), heavy multiplication x(✖)
            scalexy(g, halfWidth)  # 縦方向も横方向と同様に縮める
        elif ucode == 0x26a0:  # warning sign(⚠)
            g_warningsign(f, g, halfWidth)
        else:
            xmin, ymin, xmax, ymax = g.boundingBox()
            boxh = ymax - ymin
            if boxh > f.em:  # 上下がはみ出る場合、収まるように縮める
                g.transform(trcen)  # 縮小で下にずれないように上下中央に移動
                g.transform(psMat.scale(1, f.em / boxh))
                g.transform(psMat.inverse(trcen))
            if ucode in range(0x1f1e6, 0x1f200):
                # regional indicator symbol letter群は固定scaleで幅を縮める
                g.transform(psMat.scale(regional_indicator_scale, 1))
                g.width = halfWidth
                centerInWidth(g)
            else:
                narrow(g, halfWidth)
        emojifont.selection.select(ucode)
        emojifont.copy()
        f.selection.select(ucode)
        f.paste()
    emojifont.close()


def add_emoji2(f, halfWidth, emojifontfile2):
    """EmojiOneBWに含まれない絵文字等をNotoEmojiから取込"""
    if not emojifontfile2:
        return
    # EmojiOneBWのU+20E3(combining enclosing keycap)はつぶれて、
    # 中の文字が見えないので、Noto Emojiから取り込み。
    emoji2list = (0x20e3, 0x265f, 0x267e, 0x2695, 0x26a7)
    add_emoji(f, halfWidth, emojifontfile2, emoji2list, overwrite=True)


def g_twoDotLeader(f, halfWidth):
    if 0x2025 not in f:
        return
    g = f[0x2025]  # two dot leader(‥)
    layer = g.layers[g.activeLayer]
    c0 = layer[0]
    xmin0, ymin, xmax, ymax = c0.boundingBox()
    c1 = layer[1]
    xmin1, ymin, xmax, ymax = c1.boundingBox()
    # 点の間隔をつめる
    dx = - round((xmin1 - xmin0) / 2)
    c1.transform(psMat.translate(dx, 0))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_threeDotLeader(f, halfWidth):
    if 0x2026 not in f:
        return
    g = f[0x2026]  # three dot leader(…)
    layer = g.layers[g.activeLayer]
    c0 = layer[0]
    xmin0, ymin, xmax, ymax = c0.boundingBox()
    c1 = layer[1]
    xmin1, ymin, xmax, ymax = c1.boundingBox()
    # 点の間隔をつめる。XXX: つまりすぎて少し見にくい気も
    dx = - round((xmin1 - xmin0) / 2)
    c1.transform(psMat.translate(dx, 0))
    c2 = layer[2]
    c2.transform(psMat.translate(dx * 2, 0))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_whiteStar(g, halfWidth, *, scaleinfactor=0.8, scaleyfactor=0):
    layer = g.layers[g.activeLayer]
    # 外側と内側の星で別の縮小率を使うので、ずれを回避するため、
    # bbox中心を原点に移動してから縮小したのち位置を戻す。(参考:cica.py)
    xmin, ymin, xmax, ymax = layer.boundingBox()
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    scale0 = halfWidth / (xmax - xmin + SIDE_BEARING)
    if scaleyfactor == 0:
        scaley = 1
    else:
        scaley = scale0 * scaleyfactor
    trcen = psMat.translate(-cx, -cy)
    layer.transform(trcen)
    layer[0].transform(psMat.scale(scale0, scaley))
    # 線が細くなりすぎないように、内側の星は外側(の縮小率)よりも縮める
    scale1 = scale0 * scaleinfactor
    layer[1].transform(psMat.scale(scale1, scaley * scaleinfactor))
    layer.transform(psMat.inverse(trcen))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_infinity(f, halfWidth):
    # 左右端の線が細くなって見にくくならないように。
    # XXX:少し太すぎでバランス悪いかも
    g = f[0x221E]  # infinity(∞)
    layer = g.layers[g.activeLayer]
    xmin0, ymin0, xmax0, ymax0 = layer[0].boundingBox()  # 外側
    xmin1, ymin1, xmax1, ymax1 = layer[1].boundingBox()  # 内側左
    xmin2, ymin2, xmax2, ymax2 = layer[2].boundingBox()  # 内側右
    boxw0 = xmax0 - xmin0
    scale0 = halfWidth / (boxw0 + SIDE_BEARING)
    # print(scale0)  # Regular: 0.58, Bold: 0.57
    linewidth = ymax0 - ymax2
    centerwidth = xmin2 - xmax1
    cx = (xmin0 + xmax0) / 2
    cy = (ymin0 + ymax0) / 2
    trcen = psMat.translate(-cx, -cy)
    layer.transform(trcen)
    layer[0].transform(psMat.scale(scale0, 1))

    # 内側
    boxw2 = xmax2 - xmin2
    # expect: boxw0 * scale0 = linewidth + boxw1 * scale1 + centerwidth + boxw2 * scale2 + linewidth
    # 左右同じとして、boxw1 = boxw2, scale1 = scale2
    #     → boxw0 * scale0 = (boxw2 * scale2) * 2 + linewidth * 2 + centerwidth
    scale2 = (boxw0 * scale0 - linewidth * 2 - centerwidth) / (boxw2 * 2)
    # print(scale2)  # Regular: 0.45, Bold: 0.38
    layer[2].transform(psMat.scale(scale2, 1))
    layer[1].transform(psMat.scale(scale2, 1))
    # 中央に寄りすぎなので調整
    xmin0, ymin0, xmax0, ymax0 = layer[0].boundingBox()
    xmin2, ymin2, xmax2, ymax2 = layer[2].boundingBox()
    # expect: xmax2 + dx + linewidth = xmax0
    dx = xmax0 - xmax2 - linewidth
    layer[2].transform(psMat.translate(dx, 1))
    layer[1].transform(psMat.translate(-dx, 1))
    layer.transform(psMat.inverse(trcen))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_degreeCelsius(g, halfWidth):
    # 丸が縦長すぎて見にくくならないように
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    scalex = halfWidth / (xmax - xmin + SIDE_BEARING)
    # 丸の内側を外側よりも縮めて線が細くなりすぎないようにする
    cin = layer[1].dup()
    xmin1, ymin1, xmax1, ymax1 = cin.boundingBox()
    cx = (xmin1 + xmax1) / 2
    cy = (ymin1 + ymax1) / 2
    cin.transform(psMat.translate(-cx, -cy))
    cin.transform(psMat.scale(scalex * 0.8, 0.8))

    layer.transform(psMat.scale(scalex, 1))
    # 丸の内側を、外側の位置に移動して、置き換え
    xmin0, ymin0, xmax0, ymax0 = layer[0].boundingBox()
    cx = (xmin0 + xmax0) / 2
    cy = (ymin0 + ymax0) / 2
    cin.transform(psMat.translate(cx, cy))
    layer[1] = cin
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_angstrom(f, halfWidth):
    g_degreeCelsius(f[0x212B], halfWidth)  # angstrom sign(Å)


def g_proportional(f, halfWidth):
    g = f[0x221D]  # proportional(∝)
    layer = g.layers[g.activeLayer]
    xmin0, ymin0, xmax0, ymax0 = layer[0].boundingBox()  # 外側
    xmin1, ymin1, xmax1, ymax1 = layer[1].boundingBox()  # 内側
    boxw0 = xmax0 - xmin0
    scale0 = halfWidth / (boxw0 + SIDE_BEARING)
    linewidth = ymax0 - ymax1
    cx = (xmin0 + xmax0) / 2
    cy = (ymin0 + ymax0) / 2
    trcen = psMat.translate(-cx, -cy)
    layer.transform(trcen)
    layer[0].transform(psMat.scale(scale0, 1))
    layer[1].transform(psMat.scale(scale0 * 0.8, 1))
    # 中央に寄りすぎなので調整
    xmin0, ymin0, xmax0, ymax0 = layer[0].boundingBox()
    xmin1, ymin1, xmax1, ymax1 = layer[1].boundingBox()
    # expect: xmin0 + linewidth = xmin1 - dx
    dx = xmin1 - xmin0 - linewidth
    layer[1].transform(psMat.translate(-dx, 1))
    layer.transform(psMat.inverse(trcen))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_circle(g, halfWidth):
    # 線が細くなって見にくくならないように。
    layer = g.layers[g.activeLayer]
    xmin0, ymin0, xmax0, ymax0 = layer[0].boundingBox()  # 外側
    xmin1, ymin1, xmax1, ymax1 = layer[1].boundingBox()  # 内側
    boxw0 = xmax0 - xmin0
    scale0 = halfWidth / (boxw0 + SIDE_BEARING)
    linewidth = ymax0 - ymax1
    cx = (xmin0 + xmax0) / 2
    cy = (ymin0 + ymax0) / 2
    trcen = psMat.translate(-cx, -cy)
    layer.transform(trcen)
    layer[0].transform(psMat.scale(scale0, scale0))

    # 内側
    boxw1 = xmax1 - xmin1
    # expect: boxw0 * scale0 = linewidth + boxw1 * scale1 + linewidth
    scale1 = (boxw0 * scale0 - linewidth * 2) / boxw1
    layer[1].transform(psMat.scale(scale1, scale1))
    layer.transform(psMat.inverse(trcen))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_bullseye(f, halfWidth):
    # もとからnarrowなfisheyeと同じ線幅になるように縮める
    gref = f[0x25C9]  # fisheye(◉)
    layerref = gref.layers[gref.activeLayer]
    xminref1, yminref1, xmaxref1, ymaxref1 = layerref[1].boundingBox()  # 外側
    xminref2, yminref2, xmaxref2, ymaxref2 = layerref[2].boundingBox()  # 内側
    boxwref = xmaxref1 - xminref1
    linewidth = ymaxref1 - ymaxref2

    g = f[0x25CE]  # bullseye(◎)
    layer = g.layers[g.activeLayer]
    xmin2, ymin2, xmax2, ymax2 = layer[2].boundingBox()  # 外側の輪
    xmin3, ymin3, xmax3, ymax3 = layer[3].boundingBox()
    xmin0, ymin0, xmax0, ymax0 = layer[0].boundingBox()  # 内側の輪
    xmin1, ymin1, xmax1, ymax1 = layer[1].boundingBox()
    boxw2 = xmax2 - xmin2
    scale2 = halfWidth / (boxw2 + SIDE_BEARING)
    cx = (xmin2 + xmax2) / 2
    cy = (ymin2 + ymax2) / 2
    trcen = psMat.translate(-cx, -cy)
    layer.transform(trcen)
    layer[2].transform(psMat.scale(scale2, scale2))

    # 線の幅が合うようなscaleを算出して縮める
    boxw3 = xmax3 - xmin3
    # expect: boxw2 * scale2 = linewidth + boxw3 * scale3 + linewidth
    scale3 = (boxw2 * scale2 - linewidth * 2) / boxw3
    layer[3].transform(psMat.scale(scale3, scale3))
    layer[0].transform(psMat.scale(scale2, scale2))
    boxw0 = xmax0 - xmin0
    boxw1 = xmax1 - xmin1
    scale1 = (boxw0 * scale2 - linewidth * 2) / boxw1
    layer[1].transform(psMat.scale(scale1, scale1))
    layer.transform(psMat.inverse(trcen))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_circledBullet(f, halfWidth):
    # もとからnarrowなfisheyeと同じ文字幅、線幅になるように縮める
    gref = f[0x25C9]  # fisheye(◉)
    layerref = gref.layers[gref.activeLayer]
    xminref1, yminref1, xmaxref1, ymaxref1 = layerref[1].boundingBox()  # 外側
    xminref2, yminref2, xmaxref2, ymaxref2 = layerref[2].boundingBox()  # 内側
    boxwref = xmaxref1 - xminref1
    linewidth = ymaxref1 - ymaxref2

    g = f[0x29BF]  # circled bullet(⦿)
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    boxw = xmax - xmin
    scale = boxwref / boxw
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    trcen = psMat.translate(-cx, -cy)
    layer.transform(trcen)
    layer[0].transform(psMat.scale(scale, scale))  # 最内の黒円
    layer[1].transform(psMat.scale(scale, scale))  # 最外円

    # 線の幅が合うようなscaleを算出して縮める
    xmin2, ymin2, xmax2, ymax2 = layer[2].boundingBox()
    boxw2 = xmax2 - xmin2
    # expect: boxw * scale = linewidth + boxw2 * scale2 + linewidth
    scale2 = (boxw * scale - linewidth * 2) / boxw2
    layer[2].transform(psMat.scale(scale2, scale2))
    layer.transform(psMat.inverse(trcen))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def scalexy(g, halfWidth, *, scale=0, scaleyfactor=1):
    """縦方向も横方向と同様に縮める"""
    xmin, ymin, xmax, ymax = g.boundingBox()
    boxw = xmax - xmin
    if scale == 0:
        scalex = halfWidth / (boxw + SIDE_BEARING)
    elif boxw < halfWidth * 0.9:
        # XXX:NotoEmojiのsmall squareを縮めすぎると見にくいのでそのままにする。
        # medium squareはhalfWidth幅に縮小済なのでその幅より0.9未満ならば、
        # 縮めずそのままにする。
        scalex = 1
    else:
        scalex = scale
    scaley = scalex * scaleyfactor
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    trcen = psMat.translate(-cx, -cy)
    g.transform(trcen)  # 中心を原点に移動。でないと高さ位置が低くなる
    g.transform(psMat.scale(scalex, scaley))
    g.transform(psMat.inverse(trcen))
    g.width = halfWidth
    centerInWidth(g)
    return scalex


def g_romanNumeralTwo(f, halfWidth):
    g = f[0x2161]  # roman numeral two(Ⅱ)
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    xmin1, ymin1, xmax1, ymax1 = layer[1].boundingBox()  # 内側四角
    scalex = halfWidth / (xmax - xmin + SIDE_BEARING)
    layer.transform(psMat.scale(scalex, 1))
    # 線が細くなりすぎないように、内側の四角の各点のx座標を調整する
    c0 = layer[0]  # 外側
    c1 = layer[1]  # 内側四角
    xmin1, ymin1, xmax1, ymax1 = c1.boundingBox()
    linewidth = c0[0].y - c1[0].y
    for p in c1:
        if p.x <= xmin1:
            c1xmin = c0[-2].x + linewidth
            p.x = c1xmin
        else:
            c1xmax = c0[3].x - linewidth
            p.x = c1xmax
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)

    g = f[0x2171]  # small roman numeral two(ⅱ)
    # 線が細くなりすぎないように、移動だけで幅を縮める
    layer = g.layers[g.activeLayer]
    dx = c1xmin - xmin1
    layer[0].transform(psMat.translate(dx, 0))
    layer[1].transform(psMat.translate(dx, 0))
    dx = c1xmax - xmax1
    layer[2].transform(psMat.translate(dx, 0))
    layer[3].transform(psMat.translate(dx, 0))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_romanNumeralThree(f, halfWidth):
    g = f[0x2162]  # roman numeral three(Ⅲ)
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    xminb1, yminb1, xmaxb1, ymaxb1 = layer[1].boundingBox()  # 内側四角左
    xminb2, yminb2, xmaxb2, ymaxb2 = layer[2].boundingBox()  # 内側四角右
    scalex = halfWidth / (xmax - xmin + SIDE_BEARING)
    layer.transform(psMat.scale(scalex, 1))
    # 線が細くなりすぎないように、内側の四角の各点のx座標を調整する
    c0 = layer[0]  # 外側
    c1 = layer[1]  # 内側四角左
    xmin1, ymin1, xmax1, ymax1 = c1.boundingBox()
    linewidth = c0[0].y - c1[0].y
    dx = 0
    for p in c1:
        if p.x <= xmin1:
            c1xmin = c0[-2].x + linewidth
            dx = c1xmin - p.x
            p.x += dx
        else:
            p.x -= dx / 2
            c1xmax = p.x
    c2 = layer[2]  # 内側四角右
    xmin2, ymin2, xmax2, ymax2 = c2.boundingBox()
    for p in c2:
        if p.x >= xmax2:
            p.x -= dx
            c2xmax = p.x
        else:
            p.x += dx / 2
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)

    g = f[0x2172]  # small roman numeral three(ⅲ)
    # 線が細くなりすぎないように、移動だけで幅を縮める
    layer = g.layers[g.activeLayer]
    dx = c1xmin - xminb1
    layer[0].transform(psMat.translate(dx, 0))
    layer[1].transform(psMat.translate(dx, 0))
    dx = c1xmax - xmaxb1
    layer[2].transform(psMat.translate(dx, 0))
    layer[3].transform(psMat.translate(dx, 0))
    dx = c2xmax - xmaxb2
    layer[4].transform(psMat.translate(dx, 0))
    layer[5].transform(psMat.translate(dx, 0))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_nearlyEqual(f, halfWidth):
    # 単に幅を縮めると、丸が縦長になって見にくいので、位置移動だけで変形
    gref = f[0x003D]  # equal(=)
    xminref, ymin, xmaxref, ymax = gref.boundingBox()
    g = f[0x2252]  # nearly equals(≒)
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    # =部分の端の点を移動
    for p in layer[0] + layer[1]:
        if p.x <= xmin:
            p.x = xminref
        elif p.x >= xmax:
            p.x = xmaxref
    # 上側の丸
    c2 = layer[2]
    xmin2, ymin, xmax2, ymax = c2.boundingBox()
    offset = (xmin2 - xmin) / 2  # /2 半分に縮小
    dx = xminref + offset - xmin2
    c2.transform(psMat.translate(dx, 0))
    # 下側の丸
    c3 = layer[3]
    xmin3, ymin, xmax3, ymax = c3.boundingBox()
    dx = xmaxref - offset - xmax3
    c3.transform(psMat.translate(dx, 0))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth


def trimleft(g, halfWidth):
    """左半分の点を、halfWidthに収まるように右に移動する"""
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    # expect: xmax - (xmin + dx) + SIDE_BEARING <= halfWidth
    dx = xmax - xmin + SIDE_BEARING - halfWidth
    # 左半分の点を右に移動
    for p in layer[0]:
        if p.x < halfWidth:
            p.x += dx
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def trimright(g, halfWidth):
    """右半分の点を、halfWidthに収まるように左に移動する"""
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    # expect: (xmax - dx) - xmin + SIDE_BEARING <= halfWidth
    dx = xmax - xmin + SIDE_BEARING - halfWidth
    # 右半分の点を左に移動
    for p in layer[0]:
        if p.x > halfWidth:
            p.x -= dx
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def trimboth(g, halfWidth, side_bearing):
    """xmin,xmaxの点を、halfWidthに収まるように右左に移動する"""
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    # expect: (xmax - dx) - (xmin + dx) + side_bearing <= halfWidth
    dx = (xmax - xmin + side_bearing - halfWidth) / 2
    for c in layer:
        for p in c:
            if p.x <= xmin + side_bearing:
                p.x += dx
            # XXX: ±の+のxmaxが1単位だけ-のxmaxより小さいのでside_bearing幅まで
            elif p.x >= xmax - side_bearing:
                p.x -= dx
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)
    return dx


def g_arrowdblb(f, halfWidth):
    # 斜め線が細くなりすぎないように、矢じり間隔を短くした上で、幅を縮める
    gref = f[0x2194]  # arrowboth(↔)
    layer = gref.layers[gref.activeLayer]
    xminref, yminref, xmaxref, ymaxref = gref.boundingBox()
    # 左右の矢じり間隔
    leftxmax = 0
    rightxmin = halfWidth
    for p in layer[0]:
        if p.y == ymaxref:
            if p.x < halfWidth / 2:
                if leftxmax < p.x:
                    leftxmax = p.x
            else:
                if rightxmin > p.x:
                    rightxmin = p.x
    diff = rightxmin - leftxmax

    g = f[0x21D4]  # arrowdblboth(⇔)
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    leftxmax = 0
    rightxmin = halfWidth * 2
    for p in layer[0]:
        if p.x < halfWidth:
            if leftxmax < p.x:
                leftxmax = p.x
        else:
            if rightxmin > p.x:
                rightxmin = p.x
    # expect: rightxmin - (leftxmax + dx) = diff
    dx = rightxmin - leftxmax - diff
    # 左半分の点を右に移動
    for c in layer:
        for p in c:
            if p.x <= halfWidth:
                p.x += dx

    xmin, ymin, xmax, ymax = layer.boundingBox()
    scalex = halfWidth / (xmax - xmin + SIDE_BEARING)
    layer.transform(psMat.scale(scalex, 1))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_arrowupdn(f, halfWidth):
    f.selection.select(0x2191)  # arrowup(↑)
    f.copy()
    f.selection.select(0x2195)
    f.paste()
    g = f[0x2195]
    layer = g.layers[g.activeLayer]
    c = layer[0]
    gd = f[0x2193]  # arrowdown(↓)
    layerd = gd.layers[gd.activeLayer]
    cd = layerd[0]
    # 下向き矢じりに置き換える
    c[4:6] = [p for p in cd[2:]]
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_blackarrowlr(f, halfWidth):
    # 幅を縮めた後に矢柄を短くして、矢じりを大きくして見やすくする
    # (単にtrimleft()すると矢柄がほとんど無くなる)
    g = f[0x27A1]  # black rightwards arrow(➡)
    narrow(g, halfWidth)
    layer = g.layers[g.activeLayer]
    c = layer[0]
    # 左上部分の水平線と垂直線が同じ長さになるように、点c[-1]のxを小さくする
    ah = c[0].y - c[-1].y
    # expect: c[-1].x - c[-2].x = ah
    c[-1].x = c[-2].x + ah
    c[0].x = c[-1].x
    # 左下部分
    c[-4].x = c[-3].x + ah
    c[-5].x = c[-4].x
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)

    g = f[0x2B05]  # leftwards black arrow(⬅)
    narrow(g, halfWidth)
    layer = g.layers[g.activeLayer]
    c = layer[0]
    # 右上部分の水平線と垂直線が同じ長さになるように、点c[-1]のxを小さくする
    ah = c[0].y - c[1].y
    # expect: c[2].x - c[1].x = ah
    c[1].x = c[2].x - ah
    c[0].x = c[1].x
    # 右下部分
    c[4].x = c[3].x - ah
    c[5].x = c[4].x
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_kome(f, halfWidth):
    g = f[0x203B]  # reference mark(※)
    layer = g.layers[g.activeLayer]
    # 単純化のため、bbox中心を原点に移動してからX縮小・丸の移動後に位置を戻す
    xmin, ymin, xmax, ymax = layer.boundingBox()
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    trcen = psMat.translate(-cx, -cy)
    layer.transform(trcen)
    scalex = halfWidth / (xmax - xmin + SIDE_BEARING)
    xmin0, ymin0, xmax0, ymax0 = layer[0].boundingBox()
    # X部分の幅を縮める。XXX: 線が細くなって見にくくなる
    layer[0].transform(psMat.scale(scalex, 1))
    xmin0s, ymin0, xmax0, ymax0 = layer[0].boundingBox()
    dx = xmin0s - xmin0
    layer[1].transform(psMat.translate(dx, 0))  # 左丸を移動
    layer[3].transform(psMat.translate(-dx, 0))  # 右丸を移動
    layer.transform(psMat.inverse(trcen))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_therefore(f, halfWidth):
    # 丸の移動だけで幅を縮める。丸が縦長になると少し見にくいので
    g = f[0x2234]  # therefore(∴)
    layer = g.layers[g.activeLayer]
    # 単純化のため、bbox中心を原点に移動してから丸の移動後に位置を戻す
    xmin, ymin, xmax, ymax = layer.boundingBox()
    scalex = halfWidth / (xmax - xmin + SIDE_BEARING)
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    trcen = psMat.translate(-cx, -cy)
    layer.transform(trcen)
    xmin, ymin, xmax, ymax = layer.boundingBox()
    dx = xmax - xmax * scalex
    layer[1].transform(psMat.translate(dx, 0))  # 左丸を移動
    layer[2].transform(psMat.translate(-dx, 0))  # 右丸を移動
    layer.transform(psMat.inverse(trcen))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_because(f, halfWidth):
    g = f[0x2235]  # because(∵)
    layer = g.layers[g.activeLayer]
    xmin, ymin, xmax, ymax = layer.boundingBox()
    scalex = halfWidth / (xmax - xmin + SIDE_BEARING)
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    trcen = psMat.translate(-cx, -cy)
    layer.transform(trcen)
    xmin, ymin, xmax, ymax = layer.boundingBox()
    dx = xmax - xmax * scalex
    layer[1].transform(psMat.translate(dx, 0))  # 左丸を移動
    layer[2].transform(psMat.translate(-dx, 0))  # 右丸を移動
    layer.transform(psMat.inverse(trcen))
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def g_triangleDU(f, halfWidth):
    scaleyfactor = 1.1  # 少しでも大きくなるように少しだけ縦長にする
    # black up-pointing triangle(▲)
    scalexy(f[0x25B2], halfWidth, scaleyfactor=scaleyfactor)
    # black down-pointing triangle(▼)
    scalexy(f[0x25BC], halfWidth, scaleyfactor=scaleyfactor)
    # white up-pointing triangle(△)
    g_whiteStar(f[0x25B3], halfWidth, scaleinfactor=0.9, scaleyfactor=scaleyfactor)
    # white down-pointing triangle(▽)
    g_whiteStar(f[0x25BD], halfWidth, scaleinfactor=0.9, scaleyfactor=scaleyfactor)

    # 斜め線が細くなって見にくいので補正
    g = f[0x25BD]  # white down-pointing triangle(▽)
    layer = g.layers[g.activeLayer]
    # 計算を単純にするため外側三角の下点端が原点に来るように移動
    tip0 = layer[0][2]
    transy = psMat.translate(0, -tip0.y)
    layer.transform(psMat.compose(transy, psMat.translate(-tip0.x, 0)))

    c0 = layer[0]
    c1 = layer[1]
    d = c0[0].y - c1[0].y

    # 平行線の距離(d)と、相似な三角形の辺の比が同じことを使って、
    # 内側三角の上辺左右端のdxと、下点端のdyを計算する。
    # 外側contour(c0)は左上の点から時計回り。
    # 内側contour(c1)は左上の点から反時計回り。
    # 相似三角形1: c0下点(原点) -- c0右上点 -- c0右上点から垂線を下ろしたx軸上点
    #              (0, 0) -- (c0[1].x, c0[1].y) -- (c0[1].x, 0)
    # 相似三角形2: c0下点(原点) -- c1下点+dy -- c1+(dx,dy)線から原点への垂線交点
    #              (0, 0) -- (0, c11y) -- (c1nx, c1ny)
    # 原点と相似三角形2の3点目の距離をdにしたい。
    #     (0, 0) -- (c0[1].x, c0[1].y) : (0, 0) -- (c0[1].x, 0)
    #   = (0, 0) -- (0, c11y)          : (0, 0) -- (c1nx, c1ny)
    # →
    #     sqrt(c0[1].x ** 2 + c0[1].y ** 2) : c0[1].x
    #   = c11y : d
    c11y = d * math.sqrt(c0[1].x ** 2 + c0[1].y ** 2) / c0[1].x
    # 内側三角の右上がりの辺の傾きは外側に合わせて平行にする。
    #   c0[1].y / c0[1].x = (c1[2].y - c11y) / c12x
    c12x = c0[1].x * (c1[2].y - c11y) / c0[1].y
    dy = c11y - c1[1].y
    dxright = c12x - c1[2].x
    dxleft = -dxright

    # 内側三角の左上点を右に移動
    c1[0].x += dxleft
    # 内側三角の右上点を左に移動
    c1[2].x += dxright
    # 内側三角の下点を上に移動
    c1[1].y += dy

    # y方向位置を戻す。x方向は後でcenterInWidth()で中央に寄せる
    layer.transform(psMat.inverse(transy))

    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)

    # white up-pointing triangle(△)
    g = f[0x25B3]
    layer = g.layers[g.activeLayer]
    c1 = layer[1]
    c1[0].y -= dy
    c1[1].x += dxleft
    c1[2].x += dxright
    g.setLayer(layer, g.activeLayer)
    g.width = halfWidth
    centerInWidth(g)


def maxboxwidth(f, ucoderange, eaw_array=None):
    maxboxw = 0
    for ucode in ucoderange:
        if ucode not in f:
            continue
        if eaw_array and ucode not in eaw_array:
            continue
        g = f[ucode]
        if not g.isWorthOutputting():
            continue
        xmin, ymin, xmax, ymax = g.boundingBox()
        boxw = xmax - xmin
        if maxboxw < boxw:
            maxboxw = boxw
    return maxboxw


def narrow_withscale(f, halfWidth, scalex, ucoderange):
    for ucode in ucoderange:
        if ucode not in f:
            continue
        if ucode not in eaw_array:
            continue
        g = f[ucode]
        if not g.isWorthOutputting():
            continue
        #w = g.width
        #if w <= halfWidth:
        #    continue
        g.transform(psMat.scale(scalex, 1))
        g.width = halfWidth


def g_greek(f, halfWidth):
    """Ambiguousなギリシャ文字をNarrowにする"""
    # ギリシャ文字群のbboxの最大幅
    maxboxw = maxboxwidth(f, range(0x0370, 0x0400), eaw_array)
    # scalex=0.5だと細すぎる印象があるのでなるべく大きくなるようにしたい。
    # かといって文字ごとにscaleがばらばらだと大きさがそろわず読みにくい。
    # ただし、0.53 (=1024/1921)なので0.5と違いがわからない程度
    scalex = halfWidth / maxboxw
    # Unicode Block: Greek and Coptic
    narrow_withscale(f, halfWidth, scalex, range(0x0370, 0x0400))


def g_cyrillic(f, halfWidth):
    """Ambiguousなキリル文字をNarrowにする"""
    # キリル文字群のbboxの最大幅
    maxboxw = maxboxwidth(f, range(0x0400, 0x0500), eaw_array)
    scalex = halfWidth / maxboxw  # 0.55
    # Unicode Block: Cyrillic
    narrow_withscale(f, halfWidth, scalex, range(0x0400, 0x0500))


def g_boxDrawing(f, halfWidth):
    """罫線素片を縦線が細くならないようにNarrowにする"""
    for u in (0x2502, 0x2503):
        g = f[u]
        g.width = halfWidth
        centerInWidth(g)
    for u in range(0x252C, 0x254C):
        if u in f:
            dx = trimboth(f[u], halfWidth, 0)
    narrowCenter = halfWidth / 2
    for u in range(0x250C, 0x252C):
        if u not in f:
            continue
        g = f[u]
        layer = g.layers[g.activeLayer]
        for c in layer:
            for p in c:
                if p.x <= 0:
                    p.x += dx
                elif p.x >= halfWidth * 2:
                    p.x -= dx
        g.setLayer(layer, g.activeLayer)
        g.transform(psMat.translate(-narrowCenter, 0))
        g.width = halfWidth


def centerInWidth(g):
    w = g.width
    b = round((g.left_side_bearing + g.right_side_bearing) / 2)
    g.left_side_bearing = b
    g.right_side_bearing = b
    g.width = w  # g.widthが縮む場合があるので再設定


def main(fontfile, fontfamily, fontstyle, version, emojifontfile, emojifontfile2):
    font = fontforge.open(fontfile)

    # 半角スペースから幅を取得
    halfWidth = font[0x0020].width

    add_variationSelector(font)
    add_emoji(font, halfWidth, emojifontfile, emojis)
    add_emoji2(font, halfWidth, emojifontfile2)

    # East Asian Ambiguousなグリフの幅を半分にする。
    g_greek(font, halfWidth)
    g_cyrillic(font, halfWidth)
    g_twoDotLeader(font, halfWidth)
    g_threeDotLeader(font, halfWidth)
    g_whiteStar(font[0x2606], halfWidth)  # white star(☆)
    g_nearlyEqual(font, halfWidth)
    g_kome(font, halfWidth)
    g_therefore(font, halfWidth)
    g_because(font, halfWidth)
    g_triangleDU(font, halfWidth)
    g_arrowdblb(font, halfWidth)
    g_arrowupdn(font, halfWidth)
    g_infinity(font, halfWidth)
    g_proportional(font, halfWidth)
    g_degreeCelsius(font[0x2103], halfWidth)  # degree celsius(℃)
    g_angstrom(font, halfWidth)
    g_circle(font[0x25CB], halfWidth)  # circle(○)
    g_circle(font[0x25EF], halfWidth)  # large circle(◯)
    g_circle(font[0x25A1], halfWidth)  # white squre(□)
    g_circle(font[0x25C7], halfWidth)  # white diamond(◇)
    g_bullseye(font, halfWidth)
    g_circledBullet(font, halfWidth)
    scalexy(font[0x25CF], halfWidth)  # black circle(●)
    scalexy(font[0x25A0], halfWidth)  # black squre(■)
    scalexy(font[0x25C6], halfWidth)  # black diamond(◆)
    g_romanNumeralTwo(font, halfWidth)
    g_romanNumeralThree(font, halfWidth)
    g_boxDrawing(font, halfWidth)
    trimboth(font[0x00B1], halfWidth, SIDE_BEARING)  # plusminus(±)
    trimboth(font[0x00F7], halfWidth, SIDE_BEARING)  # divide(÷)
    trimboth(font[0x2260], halfWidth, SIDE_BEARING)  # notequal(≠)
    trimboth(font[0x22A5], halfWidth, SIDE_BEARING)  # perpendicular(⊥)
    trimboth(font[0x2640], halfWidth, SIDE_BEARING)  # female(♀)
    trimright(font[0x2190], halfWidth)  # arrowleft(←)
    trimleft(font[0x2192], halfWidth)  # arrowright(→)
    trimleft(font[0x21D2], halfWidth)  # arrowdblright(⇒) XXX:寸詰りでバランス悪
    trimleft(font[0x2203], halfWidth)  # existential(∃)
    #trimright(font[0x2208], halfWidth)  # element(∈) 曲がり部分に段差ができる
    #trimleft(font[0x220B], halfWidth)  # suchthat(∋) 曲がり部分に段差ができる
    trimright(font[0x221F], halfWidth)  # orthogonal(∟)
    g_blackarrowlr(font, halfWidth)

    # 元々半分幅な文字は縮めると細すぎるので縮めずそのまま使う。
    # 右半分だけにする
    for ucode in eaw_useright:
        g = font[ucode]
        if not g.isWorthOutputting():
            continue
        if g.width > halfWidth:
            g.transform(psMat.translate(-halfWidth, 0))
            g.width = halfWidth

    # 左半分だけにする
    for ucode in eaw_useleft:
        g = font[ucode]
        if not g.isWorthOutputting():
            continue
        if g.width > halfWidth:
            g.width = halfWidth

    for ucode in eaw_array + expect_narrow:
        if ucode not in font:
            continue
        g = font[ucode]
        if not g.isWorthOutputting():
            continue
        if g.width <= halfWidth:
            continue
        if 0x2500 <= ucode <= 0x259F:  # Box Drawing, Block Elements
            g.transform(psMat.scale(0.5, 1))
            g.width = halfWidth
            continue
        narrow(g, halfWidth)

    # 修正後のフォントファイルを保存
    copyright = open(f'copyright-{fontfamily}.txt').read()
    uniqueid = f"{fontfamily} : {datetime.datetime.now().strftime('%d-%m-%Y')}"

    # TTF名設定 - 英語
    font.appendSFNTName(0x409, 0, copyright)
    font.appendSFNTName(0x409, 1, fontfamily)
    font.appendSFNTName(0x409, 2, fontstyle)
    font.appendSFNTName(0x409, 3, uniqueid)
    font.appendSFNTName(0x409, 4, fontfamily + " " + fontstyle)
    font.appendSFNTName(0x409, 5, version)
    font.appendSFNTName(0x409, 6, fontfamily + "-" + fontstyle)
    # TTF名設定 - 日本語
    font.appendSFNTName(0x411, 0, copyright)
    font.appendSFNTName(0x411, 1, fontfamily)
    font.appendSFNTName(0x411, 2, fontstyle)
    font.appendSFNTName(0x411, 3, uniqueid)
    font.appendSFNTName(0x411, 4, fontfamily + " " + fontstyle)
    font.appendSFNTName(0x411, 5, version)
    font.appendSFNTName(0x411, 6, fontfamily + "-" + fontstyle)

    # 修正後のフォントファイルを保存
    font.generate(f"{fontfamily}-{fontstyle}.ttf")
    font.close()


if __name__ == '__main__':
    # fontfile, fontfamily, fontstyle, version, emojifontfile, emojifontfile2
    if len(sys.argv) > 6:
        emojifontfile2 = sys.argv[6]
    else:
        emojifontfile2 = None
    if len(sys.argv) > 5:
        emojifontfile = sys.argv[5]
    else:
        emojifontfile = None
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], emojifontfile, emojifontfile2)
