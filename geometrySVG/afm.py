"""
The following code comes from a matplotlib module afm.py (adobe font metrics)
that is used to calculate the dimensions of a given string. The code is
nearly identical to the original, although I have edited it slightly, to fix
a bug caused calculating the height of a string in the function
get_str_bbox_and_descent.
"""

import sys
import os
import re
uni2type1 = {9416: 'uni24C8', 229: 'aring', 8864: 'uni22A0', 8850: 'uni2292', 8221: 'quotedblright', 978: 'uni03D2', 8725: 'uni2215', 976: 'uni03D0', 86: 'V', 36: 'dollar', 12318: 'uni301E', 981: 'uni03D5', 52: 'four', 9632: 'uni25A0', 316: 'uni013C', 315: 'uni013B', 318: 'uni013E', 221: 'Yacute', 9694: 'uni25DE', 319: 'uni013F', 9562: 'uni255A', 9734: 'uni2606', 384: 'uni0180', 8887: 'uni22B7', 1103: 'uni044F', 8885: 'uni22B5', 8884: 'uni22B4', 8878: 'uni22AE', 8882: 'uni22B2', 8881: 'uni22B1', 8880: 'uni22B0', 9677: 'uni25CD', 974: 'uni03CE', 973: 'uni03CD', 972: 'uni03CC', 971: 'uni03CB', 970: 'uni03CA', 8888: 'uni22B8', 8905: 'uni22C9', 1097: 'uni0449', 8413: 'uni20DD', 8412: 'uni20DC', 8411: 'uni20DB', 8753: 'uni2231', 9679: 'uni25CF', 12398: 'uni306E', 977: 'uni03D1', 417: 'uni01A1', 8407: 'uni20D7', 982: 'uni03D6', 8755: 'uni2233', 8402: 'uni20D2', 8401: 'uni20D1', 8400: 'uni20D0', 80: 'P', 8894: 'uni22BE', 8893: 'uni22BD', 8892: 'uni22BC', 8891: 'uni22BB', 95: 'underscore', 968: 'uni03C8', 967: 'uni03C7', 808: 'uni0328', 965: 'uni03C5', 964: 'uni03C4', 963: 'uni03C3', 962: 'uni03C2', 961: 'uni03C1', 960: 'uni03C0', 8208: 'uni2010', 304: 'uni0130', 307: 'uni0133', 306: 'uni0132', 309: 'uni0135', 308: 'uni0134', 311: 'uni0137', 310: 'uni0136', 313: 'uni0139', 312: 'uni0138', 8772: 'uni2244', 8858: 'uni229A', 9585: 'uni2571', 632: 'uni0278', 8761: 'uni2239', 112: 'p', 12313: 'uni3019', 9675: 'uni25CB', 987: 'uni03DB', 988: 'uni03DC', 986: 'uni03DA', 991: 'uni03DF', 989: 'uni03DD', 317: 'uni013D', 8714: 'uni220A', 8716: 'uni220C', 8715: 'uni220B', 8718: 'uni220E', 8717: 'uni220D', 8719: 'uni220F', 8908: 'uni22CC', 213: 'Otilde', 9701: 'uni25E5', 10038: 'uni2736', 8240: 'perthousand', 48: 'zero', 10139: 'uni279B', 305: 'dotlessi', 8825: 'uni2279', 352: 'Scaron', 382: 'zcaron', 8664: 'uni21D8', 232: 'egrave', 625: 'uni0271', 426: 'uni01AA', 9010: 'uni2332', 167: 'section', 9700: 'uni25E4', 206: 'Icircumflex', 241: 'ntilde', 1054: 'uni041E', 38: 'ampersand', 1052: 'uni041C', 1050: 'uni041A', 8875: 'uni22AB', 8667: 'uni21DB', 729: 'dotaccent', 1046: 'uni0416', 1047: 'uni0417', 1044: 'uni0414', 1045: 'uni0415', 1042: 'uni0412', 1043: 'uni0413', 176: 'degree', 1041: 'uni0411', 75: 'K', 9707: 'uni25EB', 9711: 'uni25EF', 1048: 'uni0418', 1049: 'uni0419', 8803: 'uni2263', 8814: 'uni226E', 8785: 'uni2251', 712: 'uni02C8', 8802: 'uni2262', 226: 'acircumflex', 8883: 'uni22B3', 8801: 'uni2261', 9108: 'uni2394', 197: 'Aring', 8800: 'uni2260', 8788: 'uni2254', 1078: 'uni0436', 8807: 'uni2267', 107: 'k', 8904: 'uni22C8', 8810: 'uni226A', 8991: 'uni231F', 732: 'smalltilde', 8705: 'uni2201', 8704: 'uni2200', 8707: 'uni2203', 701: 'uni02BD', 8709: 'uni2205', 8708: 'uni2204', 192: 'Agrave', 8710: 'uni2206', 8713: 'uni2209', 8712: 'uni2208', 8813: 'uni226D', 8804: 'uni2264', 9789: 'uni263D', 8792: 'uni2258', 723: 'uni02D3', 722: 'uni02D2', 721: 'uni02D1', 720: 'uni02D0', 9697: 'uni25E1', 247: 'divide', 725: 'uni02D5', 724: 'uni02D4', 244: 'ocircumflex', 9508: 'uni2524', 1082: 'uni043A', 9420: 'uni24CC', 126: 'asciitilde', 8889: 'uni22B9', 9426: 'uni24D2', 8478: 'uni211E', 8477: 'uni211D', 9437: 'uni24DD', 8474: 'uni211A', 8476: 'uni211C', 8475: 'uni211B', 9670: 'uni25C6', 383: 'uni017F', 378: 'uni017A', 380: 'uni017C', 379: 'uni017B', 838: 'uni0346', 8945: 'uni22F1', 8944: 'uni22F0', 50: 'two', 8856: 'uni2298', 9425: 'uni24D1', 69: 'E', 605: 'uni025D', 353: 'scaron', 8994: 'uni2322', 9699: 'uni25E3', 8895: 'uni22BF', 70: 'F', 1088: 'uni0440', 9566: 'uni255E', 8890: 'uni22BA', 373: 'uni0175', 372: 'uni0174', 375: 'uni0177', 374: 'uni0176', 91: 'bracketleft', 368: 'uni0170', 371: 'uni0173', 370: 'uni0172', 94: 'asciicircum', 377: 'uni0179', 9616: 'uni2590', 9698: 'uni25E2', 8473: 'uni2119', 8472: 'uni2118', 9676: 'uni25CC', 102: 'f', 186: 'ordmasculine', 8859: 'uni229B', 8865: 'uni22A1', 8465: 'uni2111', 8464: 'uni2110', 8467: 'uni2113', 8466: 'uni2112', 181: 'mu', 8833: 'uni2281', 182: 'paragraph', 57: 'nine', 9708: 'uni25EC', 118: 'v', 1036: 'uni040C', 275: 'uni0113', 8912: 'uni22D0', 8652: 'uni21CC', 8651: 'uni21CB', 8650: 'uni21CA', 8869: 'uni22A5', 8655: 'uni21CF', 8654: 'uni21CE', 8653: 'uni21CD', 8249: 'guilsinglleft', 92: 'backslash', 8836: 'uni2284', 8782: 'uni224E', 8781: 'uni224D', 8783: 'uni224F', 8778: 'uni224A', 8839: 'uni2287', 8780: 'uni224C', 8779: 'uni224B', 8637: 'uni21BD', 8838: 'uni2286', 783: 'uni030F', 781: 'uni030D', 782: 'uni030E', 779: 'uni030B', 780: 'uni030C', 778: 'uni030A', 622: 'uni026E', 621: 'uni026D', 54: 'six', 618: 'uni026A', 620: 'uni026C', 9665: 'uni25C1', 8406: 'uni20D6', 1115: 'uni045B', 1116: 'uni045C', 9579: 'uni256B', 1114: 'uni045A', 1119: 'uni045F', 1118: 'uni045E', 65: 'A', 9577: 'uni2569', 1112: 'uni0458', 1113: 'uni0459', 1106: 'uni0452', 1107: 'uni0453', 9570: 'uni2562', 1105: 'uni0451', 1110: 'uni0456', 1111: 'uni0457', 1108: 'uni0454', 1109: 'uni0455', 238: 'icircumflex', 775: 'uni0307', 772: 'uni0304', 773: 'uni0305', 617: 'uni0269', 616: 'uni0268', 768: 'uni0300', 769: 'uni0301', 613: 'uni0265', 612: 'uni0264', 615: 'uni0267', 614: 'uni0266', 609: 'uni0261', 608: 'uni0260', 611: 'uni0263', 610: 'uni0262', 97: 'a', 8711: 'uni2207', 8775: 'uni2247', 8774: 'uni2246', 8769: 'uni2241', 8768: 'uni2240', 8771: 'uni2243', 8770: 'uni2242', 8978: 'uni2312', 731: 'ogonek', 8777: 'uni2249', 8776: 'uni2248', 12336: 'uni3030', 113: 'q', 8642: 'uni21C2', 8641: 'uni21C1', 8640: 'uni21C0', 8647: 'uni21C7', 8646: 'uni21C6', 8645: 'uni21C5', 8644: 'uni21C4', 8799: 'uni225F', 8492: 'uni212C', 8648: 'uni21C8', 9319: 'uni2467', 243: 'oacute', 655: 'uni028F', 654: 'uni028E', 623: 'uni026F', 652: 'uni028C', 651: 'uni028B', 650: 'uni028A', 9488: 'uni2510', 242: 'ograve', 235: 'edieresis', 8910: 'uni22CE', 8911: 'uni22CF', 8607: 'uni219F', 44: 'comma', 8906: 'uni22CA', 1065: 'uni0429', 966: 'uni03C6', 1063: 'uni0427', 1062: 'uni0426', 1061: 'uni0425', 1060: 'uni0424', 1059: 'uni0423', 1058: 'uni0422', 1057: 'uni0421', 1056: 'uni0420', 9317: 'uni2465', 9424: 'uni24D0', 9316: 'uni2464', 1072: 'uni0430', 245: 'otilde', 9825: 'uni2661', 9430: 'uni24D6', 9318: 'uni2466', 9429: 'uni24D5', 8602: 'uni219A', 9496: 'uni2518', 8886: 'uni22B6', 9313: 'uni2461', 9428: 'uni24D4', 9312: 'uni2460', 9450: 'uni24EA', 187: 'guillemotright', 234: 'ecircumflex', 62: 'greater', 8209: 'uni2011', 250: 'uacute', 9314: 'uni2462', 76: 'L', 8226: 'bullet', 676: 'uni02A4', 679: 'uni02A7', 184: 'cedilla', 674: 'uni02A2', 8213: 'uni2015', 8900: 'uni22C4', 8901: 'uni22C5', 8877: 'uni22AD', 8903: 'uni22C7', 8896: 'uni22C0', 8214: 'uni2016', 8898: 'uni22C2', 8899: 'uni22C3', 9423: 'uni24CF', 1071: 'uni042F', 1070: 'uni042E', 1069: 'uni042D', 255: 'ydieresis', 108: 'l', 172: 'logicalnot', 9418: 'uni24CA', 647: 'uni0287', 646: 'uni0286', 645: 'uni0285', 644: 'uni0284', 643: 'uni0283', 642: 'uni0282', 641: 'uni0281', 636: 'uni027C', 9828: 'uni2664', 161: 'exclamdown', 9668: 'uni25C4', 649: 'uni0289', 648: 'uni0288', 922: 'uni039A', 8211: 'endash', 9792: 'uni2640', 8420: 'uni20E4', 1139: 'uni0473', 8417: 'uni20E1', 9794: 'uni2642', 952: 'uni03B8', 953: 'uni03B9', 224: 'agrave', 948: 'uni03B4', 949: 'uni03B5', 950: 'uni03B6', 951: 'uni03B7', 944: 'uni03B0', 945: 'uni03B1', 946: 'uni03B2', 947: 'uni03B3', 9557: 'uni2555', 196: 'Adieresis', 223: 'germandbls', 214: 'Odieresis', 32: 'space', 294: 'uni0126', 295: 'uni0127', 292: 'uni0124', 293: 'uni0125', 290: 'uni0122', 291: 'uni0123', 288: 'uni0120', 289: 'uni0121', 8217: 'quoteright', 9568: 'uni2560', 9558: 'uni2556', 251: 'ucircumflex', 9569: 'uni2561', 9553: 'uni2551', 9650: 'uni25B2', 9552: 'uni2550', 9571: 'uni2563', 9555: 'uni2553', 71: 'G', 9572: 'uni2564', 9554: 'uni2552', 8216: 'quoteleft', 9573: 'uni2565', 9586: 'uni2572', 9576: 'uni2568', 9574: 'uni2566', 87: 'W', 8522: 'uni214A', 303: 'uni012F', 301: 'uni012D', 302: 'uni012E', 299: 'uni012B', 300: 'uni012C', 9564: 'uni255C', 298: 'uni012A', 8841: 'uni2289', 81: 'Q', 8992: 'uni2320', 8993: 'uni2321', 103: 'g', 957: 'uni03BD', 958: 'uni03BE', 959: 'uni03BF', 8834: 'uni2282', 8837: 'uni2285', 954: 'uni03BA', 955: 'uni03BB', 956: 'uni03BC', 8488: 'uni2128', 9655: 'uni25B7', 119: 'w', 770: 'uni0302', 990: 'uni03DE', 9690: 'uni25DA', 771: 'uni0303', 1123: 'uni0463', 1122: 'uni0462', 12312: 'uni3018', 9492: 'uni2514', 63: 'question', 9651: 'uni25B3', 9441: 'uni24E1', 49: 'one', 8202: 'uni200A', 8824: 'uni2278', 730: 'ring', 405: 'uni0195', 8210: 'figuredash', 8940: 'uni22EC', 825: 'uni0339', 824: 'uni0338', 823: 'uni0337', 822: 'uni0336', 821: 'uni0335', 819: 'uni0333', 818: 'uni0332', 817: 'uni0331', 816: 'uni0330', 449: 'uni01C1', 448: 'uni01C0', 451: 'uni01C3', 450: 'uni01C2', 9043: 'uni2353', 776: 'uni0308', 8728: 'uni2218', 8729: 'uni2219', 8726: 'uni2216', 8727: 'uni2217', 8724: 'uni2214', 777: 'uni0309', 9737: 'uni2609', 8723: 'uni2213', 8720: 'uni2210', 8721: 'uni2211', 8773: 'uni2245', 66: 'B', 9686: 'uni25D6', 237: 'iacute', 742: 'uni02E6', 743: 'uni02E7', 744: 'uni02E8', 745: 'uni02E9', 8733: 'uni221D', 8734: 'uni221E', 376: 'Ydieresis', 8732: 'uni221C', 8919: 'uni22D7', 8730: 'uni221A', 82: 'R', 9436: 'uni24DC', 831: 'uni033F', 830: 'uni033E', 828: 'uni033C', 827: 'uni033B', 826: 'uni033A', 98: 'b', 8842: 'uni228A', 8923: 'uni22DB', 9556: 'uni2554', 1131: 'uni046B', 1130: 'uni046A', 114: 'r', 9435: 'uni24DB', 199: 'Ccedilla', 8722: 'minus', 9434: 'uni24DA', 1008: 'uni03F0', 1009: 'uni03F1', 8364: 'uni20AC', 8822: 'uni2276', 9408: 'uni24C0', 354: 'uni0162', 355: 'uni0163', 286: 'uni011E', 285: 'uni011D', 284: 'uni011C', 283: 'uni011B', 356: 'uni0164', 357: 'uni0165', 321: 'Lslash', 360: 'uni0168', 361: 'uni0169', 9673: 'uni25C9', 741: 'uni02E5', 8643: 'uni21C3', 9412: 'uni24C4', 9442: 'uni24E2', 8823: 'uni2277', 314: 'uni013A', 8450: 'uni2102', 218: 'Uacute', 8983: 'uni2317', 8455: 'uni2107', 8735: 'uni221F', 253: 'yacute', 12306: 'uni3012', 219: 'Ucircumflex', 349: 'uni015D', 34: 'quotedbl', 9689: 'uni25D9', 8832: 'uni2280', 8879: 'uni22AF', 189: 'onehalf', 8731: 'uni221B', 222: 'Thorn', 8742: 'uni2226', 77: 'M', 9658: 'uni25BA', 9315: 'uni2463', 9014: 'uni2336', 56: 'eight', 8758: 'uni2236', 215: 'multiply', 8460: 'uni210C', 8458: 'uni210A', 8649: 'uni21C9', 96: 'grave', 8462: 'uni210E', 279: 'uni0117', 364: 'uni016C', 277: 'uni0115', 362: 'uni016A', 367: 'uni016F', 274: 'uni0112', 365: 'uni016D', 366: 'uni016E', 212: 'Ocircumflex', 8965: 'uni2305', 109: 'm', 9439: 'uni24DF', 281: 'uni0119', 280: 'uni0118', 8355: 'uni20A3', 8356: 'uni20A4', 8359: 'uni20A7', 8840: 'uni2288', 9411: 'uni24C3', 9500: 'uni251C', 8845: 'uni228D', 8751: 'uni222F', 8750: 'uni222E', 8749: 'uni222D', 8748: 'uni222C', 8747: 'uni222B', 8746: 'uni222A', 9563: 'uni255B', 217: 'Ugrave', 9438: 'uni24DE', 8250: 'guilsinglright', 9482: 'uni250A', 209: 'Ntilde', 633: 'uni0279', 191: 'questiondown', 9580: 'uni256C', 195: 'Atilde', 626: 'uni0272', 627: 'uni0273', 624: 'uni0270', 231: 'ccedilla', 630: 'uni0276', 631: 'uni0277', 628: 'uni0274', 629: 'uni0275', 8786: 'uni2252', 1055: 'uni041F', 8784: 'uni2250', 90: 'Z', 8790: 'uni2256', 8791: 'uni2257', 169: 'copyright', 8789: 'uni2255', 1085: 'uni043D', 1086: 'uni043E', 1087: 'uni043F', 165: 'yen', 1053: 'uni041D', 1083: 'uni043B', 1084: 'uni043C', 8624: 'uni21B0', 8625: 'uni21B1', 8626: 'uni21B2', 8627: 'uni21B3', 8628: 'uni21B4', 8629: 'uni21B5', 8630: 'uni21B6', 8631: 'uni21B7', 8632: 'uni21B8', 201: 'Eacute', 8977: 'uni2311', 8976: 'uni2310', 8847: 'uni228F', 9691: 'uni25DB', 8634: 'uni21BA', 8635: 'uni21BB', 8636: 'uni21BC', 8215: 'uni2017', 8638: 'uni21BE', 8639: 'uni21BF', 8988: 'uni231C', 72: 'H', 659: 'uni0293', 8706: 'uni2202', 8868: 'uni22A4', 8990: 'uni231E', 8754: 'uni2232', 8795: 'uni225B', 8796: 'uni225C', 9433: 'uni24D9', 8794: 'uni225A', 1080: 'uni0438', 1081: 'uni0439', 8797: 'uni225D', 8798: 'uni225E', 1076: 'uni0434', 88: 'X', 127: 'uni007F', 1079: 'uni0437', 207: 'Idieresis', 1073: 'uni0431', 1074: 'uni0432', 1075: 'uni0433', 8876: 'uni22AC', 8909: 'uni22CD', 9635: 'uni25A3', 124: 'bar', 9403: 'uni24BB', 894: 'uni037E', 635: 'uni027B', 104: 'h', 634: 'uni027A', 639: 'uni027F', 637: 'uni027D', 638: 'uni027E', 8743: 'uni2227', 8196: 'uni2004', 8741: 'uni2225', 8740: 'uni2224', 8739: 'uni2223', 8738: 'uni2222', 8737: 'uni2221', 8736: 'uni2220', 120: 'x', 8995: 'uni2323', 9561: 'uni2559', 9560: 'uni2558', 8745: 'uni2229', 8744: 'uni2228', 252: 'udieresis', 669: 'uni029D', 170: 'ordfeminine', 8907: 'uni22CB', 9021: 'uni233D', 1064: 'uni0428', 9414: 'uni24C6', 8925: 'uni22DD', 9415: 'uni24C7', 348: 'uni015C', 347: 'uni015B', 346: 'uni015A', 8874: 'uni22AA', 351: 'uni015F', 350: 'uni015E', 123: 'braceleft', 9413: 'uni24C5', 1040: 'uni0410', 938: 'uni03AA', 9410: 'uni24C2', 940: 'uni03AC', 939: 'uni03AB', 175: 'macron', 941: 'uni03AD', 943: 'uni03AF', 660: 'uni0294', 661: 'uni0295', 662: 'uni0296', 663: 'uni0297', 656: 'uni0290', 657: 'uni0291', 658: 'uni0292', 227: 'atilde', 194: 'Acircumflex', 9072: 'uni2370', 9409: 'uni24C1', 664: 'uni0298', 665: 'uni0299', 216: 'Oslash', 670: 'uni029E', 67: 'C', 8220: 'quotedblleft', 667: 'uni029B', 668: 'uni029C', 937: 'uni03A9', 936: 'uni03A8', 83: 'S', 9417: 'uni24C9', 929: 'uni03A1', 928: 'uni03A0', 33: 'exclam', 933: 'uni03A5', 932: 'uni03A4', 935: 'uni03A7', 381: 'Zcaron', 8499: 'uni2133', 8498: 'uni2132', 345: 'uni0159', 344: 'uni0158', 8503: 'uni2137', 8197: 'uni2005', 8501: 'uni2135', 8500: 'uni2134', 698: 'uni02BA', 8243: 'uni2033', 337: 'uni0151', 336: 'uni0150', 343: 'uni0157', 61: 'equal', 341: 'uni0155', 340: 'uni0154', 115: 's', 9023: 'uni233F', 240: 'eth', 9406: 'uni24BE', 8681: 'uni21E9', 8288: 'uni2060', 200: 'Egrave', 9565: 'uni255D', 9421: 'uni24CD', 8673: 'uni21E1', 8633: 'uni21B9', 45: 'hyphen', 446: 'uni01BE', 443: 'uni01BB', 46: 'period', 236: 'igrave', 442: 'uni01BA', 8854: 'uni2296', 8855: 'uni2297', 8852: 'uni2294', 8853: 'uni2295', 58: 'colon', 8851: 'uni2293', 8848: 'uni2290', 8849: 'uni2291', 813: 'uni032D', 814: 'uni032E', 815: 'uni032F', 810: 'uni032A', 811: 'uni032B', 812: 'uni032C', 8989: 'uni231D', 202: 'Ecircumflex', 9431: 'uni24D7', 9693: 'uni25DD', 8482: 'trademark', 193: 'Aacute', 162: 'cent', 1093: 'uni0445', 9838: 'uni266E', 9837: 'uni266D', 9835: 'uni266B', 969: 'uni03C9', 8195: 'uni2003', 8263: 'uni2047', 322: 'lslash', 934: 'uni03A6', 8259: 'uni2043', 9484: 'uni250C', 8256: 'uni2040', 9567: 'uni255F', 9419: 'uni24CB', 1138: 'uni0472', 1094: 'uni0446', 1140: 'uni0474', 1141: 'uni0475', 9480: 'uni2508', 9824: 'uni2660', 9478: 'uni2506', 9474: 'uni2502', 99: 'c', 9472: 'uni2500', 78: 'N', 8870: 'uni22A6', 8679: 'uni21E7', 8496: 'uni2130', 8194: 'uni2002', 728: 'breve', 1090: 'uni0442', 211: 'Oacute', 8863: 'uni229F', 9671: 'uni25C7', 8861: 'uni229D', 8862: 'uni229E', 171: 'guillemotleft', 809: 'uni0329', 9445: 'uni24E5', 287: 'uni011F', 804: 'uni0324', 805: 'uni0325', 806: 'uni0326', 807: 'uni0327', 801: 'uni0321', 802: 'uni0322', 110: 'n', 8242: 'uni2032', 8809: 'uni2269', 8808: 'uni2268', 774: 'uni0306', 8811: 'uni226B', 8682: 'uni21EA', 358: 'uni0166', 8251: 'uni203B', 437: 'uni01B5', 239: 'idieresis', 700: 'uni02BC', 432: 'uni01B0', 125: 'braceright', 55: 'seven', 699: 'uni02BB', 282: 'uni011A', 10747: 'uni29FB', 166: 'brokenbar', 8246: 'uni2036', 9664: 'uni25C0', 342: 'uni0156', 8917: 'uni22D5', 600: 'uni0258', 249: 'ugrave', 8918: 'uni22D6', 8913: 'uni22D1', 8244: 'uni2034', 8915: 'uni22D3', 8914: 'uni22D2', 8252: 'uni203C', 8766: 'uni223E', 703: 'uni02BF', 8921: 'uni22D9', 8920: 'uni22D8', 9661: 'uni25BD', 9662: 'uni25BE', 9663: 'uni25BF', 1051: 'uni041B', 183: 'periodcentered', 9660: 'uni25BC', 414: 'uni019E', 411: 'uni019B', 410: 'uni019A', 8199: 'uni2007', 913: 'uni0391', 912: 'uni0390', 915: 'uni0393', 914: 'uni0392', 917: 'uni0395', 916: 'uni0394', 919: 'uni0397', 918: 'uni0396', 921: 'uni0399', 920: 'uni0398', 9672: 'uni25C8', 9320: 'uni2468', 163: 'sterling', 8939: 'uni22EB', 924: 'uni039C', 923: 'uni039B', 926: 'uni039E', 925: 'uni039D', 927: 'uni039F', 73: 'I', 993: 'uni03E1', 992: 'uni03E0', 8985: 'uni2319', 8843: 'uni228B', 9653: 'uni25B5', 9654: 'uni25B6', 8938: 'uni22EA', 9401: 'uni24B9', 1102: 'uni044E', 409: 'uni0199', 8806: 'uni2266', 89: 'Y', 8866: 'uni22A2', 208: 'Eth', 9839: 'uni266F', 8212: 'emdash', 9787: 'uni263B', 9405: 'uni24BD', 8926: 'uni22DE', 864: 'uni0360', 9559: 'uni2557', 8927: 'uni22DF', 8922: 'uni22DA', 8924: 'uni22DC', 865: 'uni0361', 105: 'i', 9407: 'uni24BF', 866: 'uni0362', 9790: 'uni263E', 653: 'uni028D', 8793: 'uni2259', 803: 'uni0323', 8805: 'uni2265', 8225: 'daggerdbl', 121: 'y', 266: 'uni010A', 177: 'plusminus', 60: 'less', 8622: 'uni21AE', 789: 'uni0315', 8971: 'uni230B', 8623: 'uni21AF', 8618: 'uni21AA', 8620: 'uni21AC', 8619: 'uni21AB', 507: 'uni01FB', 508: 'uni01FC', 8762: 'uni223A', 506: 'uni01FA', 511: 'uni01FF', 509: 'uni01FD', 510: 'uni01FE', 9575: 'uni2567', 9696: 'uni25E0', 260: 'uni0104', 261: 'uni0105', 262: 'uni0106', 263: 'uni0107', 256: 'uni0100', 257: 'uni0101', 258: 'uni0102', 259: 'uni0103', 8248: 'uni2038', 8201: 'uni2009', 8200: 'uni2008', 264: 'uni0108', 265: 'uni0109', 673: 'uni02A1', 8763: 'uni223B', 8812: 'uni226C', 9644: 'uni25AC', 9427: 'uni24D3', 8672: 'uni21E0', 8675: 'uni21E3', 220: 'Udieresis', 8674: 'uni21E2', 68: 'D', 8677: 'uni21E5', 9761: 'uni2621', 8657: 'uni21D1', 8254: 'uni203E', 8902: 'uni22C6', 8676: 'uni21E4', 269: 'uni010D', 270: 'uni010E', 271: 'uni010F', 53: 'five', 84: 'T', 267: 'uni010B', 268: 'uni010C', 9733: 'uni2605', 9827: 'uni2663', 8678: 'uni21E6', 9398: 'uni24B6', 8897: 'uni22C1', 248: 'oslash', 180: 'acute', 496: 'uni01F0', 100: 'd', 338: 'OE', 8931: 'uni22E3', 204: 'Igrave', 8968: 'uni2308', 8969: 'uni2309', 8617: 'uni21A9', 116: 't', 8979: 'uni2313', 931: 'uni03A3', 8612: 'uni21A4', 8615: 'uni21A7', 8614: 'uni21A6', 8609: 'uni21A1', 8608: 'uni21A0', 8611: 'uni21A3', 8610: 'uni21A2', 41: 'parenright', 9578: 'uni256A', 9692: 'uni25DC', 9422: 'uni24CE', 1068: 'uni042C', 9440: 'uni24E0', 1067: 'uni042B', 1033: 'uni0409', 1032: 'uni0408', 9447: 'uni24E7', 9652: 'uni25B4', 1066: 'uni042A', 8846: 'uni228E', 1025: 'uni0401', 228: 'adieresis', 1027: 'uni0403', 39: 'quotesingle', 1029: 'uni0405', 1028: 'uni0404', 1031: 'uni0407', 1030: 'uni0406', 8860: 'uni229C', 8966: 'uni2306', 8787: 'uni2253', 8229: 'twodotenleader', 8497: 'uni2131', 8666: 'uni21DA', 8756: 'uni2234', 8757: 'uni2235', 421: 'uni01A5', 8759: 'uni2237', 8752: 'uni2230', 716: 'uni02CC', 47: 'slash', 416: 'uni01A0', 8230: 'ellipsis', 8857: 'uni2299', 8760: 'uni2238', 35: 'numbersign', 8616: 'uni21A8', 8765: 'uni223D', 431: 'uni01AF', 8767: 'uni223F', 429: 'uni01AD', 427: 'uni01AB', 246: 'odieresis', 8764: 'uni223C', 8829: 'uni227D', 640: 'uni0280', 79: 'O', 8830: 'uni227E', 8613: 'uni21A5', 8916: 'uni22D4', 9684: 'uni25D4', 8831: 'uni227F', 1077: 'uni0435', 8962: 'uni2302', 9833: 'uni2669', 9443: 'uni24E3', 10016: 'uni2720', 8872: 'uni22A8', 8873: 'uni22A9', 1034: 'uni040A', 8871: 'uni22A7', 339: 'oe', 1035: 'uni040B', 1038: 'uni040E', 8867: 'uni22A3', 111: 'o', 1039: 'uni040F', 203: 'Edieresis', 9685: 'uni25D5', 43: 'plus', 1101: 'uni044D', 9788: 'uni263C', 8934: 'uni22E6', 8835: 'uni2283', 9612: 'uni258C', 8606: 'uni219E', 9444: 'uni24E4', 8502: 'uni2136', 8224: 'dagger', 9399: 'uni24B7', 8603: 'uni219B', 8933: 'uni22E5', 51: 'three', 8459: 'uni210B', 9524: 'uni2534', 9400: 'uni24B8', 8970: 'uni230A', 733: 'hungarumlaut', 40: 'parenleft', 328: 'uni0148', 329: 'uni0149', 8484: 'uni2124', 8485: 'uni2125', 8486: 'uni2126', 8487: 'uni2127', 320: 'uni0140', 8489: 'uni2129', 9669: 'uni25C5', 323: 'uni0143', 324: 'uni0144', 325: 'uni0145', 326: 'uni0146', 327: 'uni0147', 8461: 'uni210D', 8260: 'fraction', 8241: 'uni2031', 8598: 'uni2196', 8245: 'uni2035', 9446: 'uni24E6', 363: 'uni016B', 9402: 'uni24BA', 9834: 'uni266A', 278: 'uni0116', 8469: 'uni2115', 174: 'registered', 74: 'J', 9695: 'uni25DF', 9678: 'uni25CE', 10045: 'uni273D', 168: 'dieresis', 8491: 'uni212B', 276: 'uni0114', 8493: 'uni212D', 8494: 'uni212E', 8495: 'uni212F', 330: 'uni014A', 331: 'uni014B', 332: 'uni014C', 333: 'uni014D', 334: 'uni014E', 335: 'uni014F', 606: 'uni025E', 9448: 'uni24E8', 273: 'uni0111', 9449: 'uni24E9', 210: 'Ograve', 106: 'j', 8597: 'uni2195', 8596: 'uni2194', 8599: 'uni2197', 8247: 'uni2037', 8593: 'uni2191', 8592: 'uni2190', 8595: 'uni2193', 8594: 'uni2192', 10746: 'uni29FA', 10003: 'uni2713', 122: 'z', 8601: 'uni2199', 8600: 'uni2198', 9831: 'uni2667', 230: 'ae', 1096: 'uni0448', 59: 'semicolon', 9830: 'uni2666', 911: 'uni038F', 1092: 'uni0444', 1095: 'uni0447', 910: 'uni038E', 1089: 'uni0441', 908: 'uni038C', 1091: 'uni0443', 906: 'uni038A', 592: 'uni0250', 593: 'uni0251', 594: 'uni0252', 595: 'uni0253', 596: 'uni0254', 64: 'at', 598: 'uni0256', 599: 'uni0257', 359: 'uni0167', 601: 'uni0259', 8844: 'uni228C', 9826: 'uni2662', 793: 'uni0319', 792: 'uni0318', 9404: 'uni24BC', 1026: 'uni0402', 8943: 'uni22EF', 205: 'Iacute', 8941: 'uni22ED', 8942: 'uni22EE', 785: 'uni0311', 784: 'uni0310', 8680: 'uni21E8', 786: 'uni0312', 37: 'percent', 791: 'uni0317', 790: 'uni0316', 8662: 'uni21D6', 8663: 'uni21D7', 8660: 'uni21D4', 8661: 'uni21D5', 8658: 'uni21D2', 8659: 'uni21D3', 8656: 'uni21D0', 8504: 'uni2138', 8816: 'uni2270', 8817: 'uni2271', 8818: 'uni2272', 8819: 'uni2273', 8820: 'uni2274', 8821: 'uni2275', 93: 'bracketright', 8665: 'uni21D9', 8671: 'uni21DF', 8669: 'uni21DD', 8670: 'uni21DE', 198: 'AE', 942: 'uni03AE', 8826: 'uni227A', 8827: 'uni227B', 8828: 'uni227C', 42: 'asterisk', 225: 'aacute', 8815: 'uni226F', 8930: 'uni22E2', 902: 'uni0386', 8928: 'uni22E0', 8929: 'uni22E1', 85: 'U', 8935: 'uni22E7', 8932: 'uni22E4', 903: 'uni0387', 794: 'uni031A', 233: 'eacute', 8936: 'uni22E8', 8937: 'uni22E9', 9432: 'uni24D8', 602: 'uni025A', 603: 'uni025B', 604: 'uni025C', 101: 'e', 296: 'uni0128', 607: 'uni025F', 9829: 'uni2665', 254: 'thorn', 297: 'uni0129', 9532: 'uni253C', 9687: 'uni25D7', 117: 'u', 904: 'uni0388', 905: 'uni0389', 597: 'uni0255', 369: 'uni0171', 900: 'uni0384', 901: 'uni0385', 1098: 'uni044A', 9516: 'uni252C', 1100: 'uni044C', 1099: 'uni044B'}


# Convert string the a python type

# some afm files have floats where we are expecting ints -- there is
# probably a better way to handle this (support floats, round rather
# than truncate).  But I don't know what the best approach is now and
# this change to _to_int should at least prevent mpl from crashing on
# these JDH (2009-11-06)


def _to_int(x):
    return int(float(x))


_to_float = float


def _to_str(x):
    return x.decode('utf8')


def _to_list_of_ints(s):
    s = s.replace(b',', b' ')
    return [_to_int(val) for val in s.split()]


def _to_list_of_floats(s):
    return [_to_float(val) for val in s.split()]


def _to_bool(s):
    if s.lower().strip() in (b'false', b'0', b'no'):
        return False
    else:
        return True


def _sanity_check(fh):
    """
    Check if the file at least looks like AFM.
    If not, raise :exc:`RuntimeError`.
    """

    # Remember the file position in case the caller wants to
    # do something else with the file.
    pos = fh.tell()
    try:
        line = next(fh)
    finally:
        fh.seek(pos, 0)

    # AFM spec, Section 4: The StartFontMetrics keyword [followed by a
    # version number] must be the first line in the file, and the
    # EndFontMetrics keyword must be the last non-empty line in the
    # file. We just check the first line.
    if not line.startswith(b'StartFontMetrics'):
        raise RuntimeError('Not an AFM file')


def _parse_header(fh):
    """
    Reads the font metrics header (up to the char metrics) and returns
    a dictionary mapping *key* to *val*.  *val* will be converted to the
    appropriate python type as necessary; e.g.:

        * 'False'->False
        * '0'->0
        * '-168 -218 1000 898'-> [-168, -218, 1000, 898]

    Dictionary keys are

      StartFontMetrics, FontName, FullName, FamilyName, Weight,
      ItalicAngle, IsFixedPitch, FontBBox, UnderlinePosition,
      UnderlineThickness, Version, Notice, EncodingScheme, CapHeight,
      XHeight, Ascender, Descender, StartCharMetrics

    """
    headerConverters = {
        b'StartFontMetrics': _to_float,
        b'FontName': _to_str,
        b'FullName': _to_str,
        b'FamilyName': _to_str,
        b'Weight': _to_str,
        b'ItalicAngle': _to_float,
        b'IsFixedPitch': _to_bool,
        b'FontBBox': _to_list_of_ints,
        b'UnderlinePosition': _to_int,
        b'UnderlineThickness': _to_int,
        b'Version': _to_str,
        b'Notice': _to_str,
        b'EncodingScheme': _to_str,
        b'CapHeight': _to_float,  # Is the second version a mistake, or
        b'Capheight': _to_float,  # do some AFM files contain 'Capheight'? -JKS
        b'XHeight': _to_float,
        b'Ascender': _to_float,
        b'Descender': _to_float,
        b'StdHW': _to_float,
        b'StdVW': _to_float,
        b'StartCharMetrics': _to_int,
        b'CharacterSet': _to_str,
        b'Characters': _to_int,
        }

    d = {}
    for line in fh:
        line = line.rstrip()
        if line.startswith(b'Comment'):
            continue
        lst = line.split(b' ', 1)

        key = lst[0]
        if len(lst) == 2:
            val = lst[1]
        else:
            val = b''

        try:
            d[key] = headerConverters[key](val)
        except ValueError:
            print('Value error parsing header in AFM:',
                  key, val, file=sys.stderr)
            continue
        except KeyError:
            print('Found an unknown keyword in AFM header (was %r)' % key,
                  file=sys.stderr)
            continue
        if key == b'StartCharMetrics':
            return d
    raise RuntimeError('Bad parse')


def _parse_char_metrics(fh):
    """
    Return a character metric dictionary.  Keys are the ASCII num of
    the character, values are a (*wx*, *name*, *bbox*) tuple, where
    *wx* is the character width, *name* is the postscript language
    name, and *bbox* is a (*llx*, *lly*, *urx*, *ury*) tuple.

    This function is incomplete per the standard, but thus far parses
    all the sample afm files tried.
    """

    ascii_d = {}
    name_d = {}
    for line in fh:
        # We are defensively letting values be utf8. The spec requires
        # ascii, but there are non-compliant fonts in circulation
        line = _to_str(line.rstrip())  # Convert from byte-literal
        if line.startswith('EndCharMetrics'):
            return ascii_d, name_d
        # Split the metric line into a dictionary, keyed by metric identifiers
        vals = dict(s.strip().split(' ', 1) for s in line.split(';') if s)
        # There may be other metrics present, but only these are needed
        if not {'C', 'WX', 'N', 'B'}.issubset(vals):
            raise RuntimeError('Bad char metrics line: %s' % line)
        num = _to_int(vals['C'])
        wx = _to_float(vals['WX'])
        name = vals['N']
        bbox = _to_list_of_floats(vals['B'])
        bbox = list(map(int, bbox))
        # Workaround: If the character name is 'Euro', give it the
        # corresponding character code, according to WinAnsiEncoding (see PDF
        # Reference).
        if name == 'Euro':
            num = 128
        if num != -1:
            ascii_d[num] = (wx, name, bbox)
        name_d[name] = (wx, bbox)
    raise RuntimeError('Bad parse')


def _parse_kern_pairs(fh):
    """
    Return a kern pairs dictionary; keys are (*char1*, *char2*) tuples and
    values are the kern pair value.  For example, a kern pairs line like
    ``KPX A y -50``

    will be represented as::

      d[ ('A', 'y') ] = -50

    """

    line = next(fh)
    if not line.startswith(b'StartKernPairs'):
        raise RuntimeError('Bad start of kern pairs data: %s' % line)

    d = {}
    for line in fh:
        line = line.rstrip()
        if not line:
            continue
        if line.startswith(b'EndKernPairs'):
            next(fh)  # EndKernData
            return d
        vals = line.split()
        if len(vals) != 4 or vals[0] != b'KPX':
            raise RuntimeError('Bad kern pairs line: %s' % line)
        c1, c2, val = _to_str(vals[1]), _to_str(vals[2]), _to_float(vals[3])
        d[(c1, c2)] = val
    raise RuntimeError('Bad kern pairs parse')


def _parse_composites(fh):
    """
    Return a composites dictionary.  Keys are the names of the
    composites.  Values are a num parts list of composite information,
    with each element being a (*name*, *dx*, *dy*) tuple.  Thus a
    composites line reading:

      CC Aacute 2 ; PCC A 0 0 ; PCC acute 160 170 ;

    will be represented as::

      d['Aacute'] = [ ('A', 0, 0), ('acute', 160, 170) ]

    """
    d = {}
    for line in fh:
        line = line.rstrip()
        if not line:
            continue
        if line.startswith(b'EndComposites'):
            return d
        vals = line.split(b';')
        cc = vals[0].split()
        name, numParts = cc[1], _to_int(cc[2])
        pccParts = []
        for s in vals[1:-1]:
            pcc = s.split()
            name, dx, dy = pcc[1], _to_float(pcc[2]), _to_float(pcc[3])
            pccParts.append((name, dx, dy))
        d[name] = pccParts

    raise RuntimeError('Bad composites parse')


def _parse_optional(fh):
    """
    Parse the optional fields for kern pair data and composites

    return value is a (*kernDict*, *compositeDict*) which are the
    return values from :func:`_parse_kern_pairs`, and
    :func:`_parse_composites` if the data exists, or empty dicts
    otherwise
    """
    optional = {
        b'StartKernData': _parse_kern_pairs,
        b'StartComposites':  _parse_composites,
        }

    d = {b'StartKernData': {}, b'StartComposites': {}}
    for line in fh:
        line = line.rstrip()
        if not line:
            continue
        key = line.split()[0]

        if key in optional:
            d[key] = optional[key](fh)

    l = (d[b'StartKernData'], d[b'StartComposites'])
    return l


def parse_afm(fh):
    """
    Parse the Adobe Font Metics file in file handle *fh*. Return value
    is a (*dhead*, *dcmetrics_ascii*, *dmetrics_name*, *dkernpairs*,
    *dcomposite*) tuple where
    *dhead* is a :func:`_parse_header` dict,
    *dcmetrics_ascii* and *dcmetrics_name* are the two resulting dicts
    from :func:`_parse_char_metrics`,
    *dkernpairs* is a :func:`_parse_kern_pairs` dict (possibly {}) and
    *dcomposite* is a :func:`_parse_composites` dict (possibly {})
    """
    _sanity_check(fh)
    dhead = _parse_header(fh)
    dcmetrics_ascii, dcmetrics_name = _parse_char_metrics(fh)
    doptional = _parse_optional(fh)
    return dhead, dcmetrics_ascii, dcmetrics_name, doptional[0], doptional[1]


class AFM(object):

    def __init__(self, fh):
        """
        Parse the AFM file in file object *fh*
        """
        (dhead, dcmetrics_ascii, dcmetrics_name, dkernpairs, dcomposite) = \
            parse_afm(fh)
        self._header = dhead
        self._kern = dkernpairs
        self._metrics = dcmetrics_ascii
        self._metrics_by_name = dcmetrics_name
        self._composite = dcomposite

    def get_bbox_char(self, c, isord=False):
        if not isord:
            c = ord(c)
        wx, name, bbox = self._metrics[c]
        return bbox

    def string_width_height(self, s):
        """
        Return the string width (including kerning) and string height
        as a (*w*, *h*) tuple.
        """
        if not len(s):
            return 0, 0
        totalw = 0
        namelast = None
        miny = 1e9
        maxy = 0
        for c in s:
            if c == '\n':
                continue
            wx, name, bbox = self._metrics[ord(c)]
            l, b, w, h = bbox

            # find the width with kerning
            try:
                kp = self._kern[(namelast, name)]
            except KeyError:
                kp = 0
            totalw += wx + kp

            # find the max y
            thismax = b + h
            if thismax > maxy:
                maxy = thismax

            # find the min y
            thismin = b
            if thismin < miny:
                miny = thismin
            namelast = name

        return totalw, maxy - miny

    def get_str_bbox_and_descent(self, s):
        """
        Return the string bounding box
        """
        if not len(s):
            return 0, 0, 0, 0
        totalw = 0
        namelast = None
        miny = 1e9
        maxy = 0
        left = 0
        if not isinstance(s, str):
            s = _to_str(s)
        for c in s:
            if c == '\n':
                continue
            name = uni2type1.get(ord(c), 'question')
            try:
                wx, bbox = self._metrics_by_name[name]
            except KeyError:
                name = 'question'
                wx, bbox = self._metrics_by_name[name]
            l, b, w, h = bbox
            if l < left:
                left = l
            # find the width with kerning
            try:
                kp = self._kern[(namelast, name)]
            except KeyError:
                kp = 0
            totalw += wx + kp

            # find the max y
            thismax = h
            if thismax > maxy:
                maxy = thismax

            # find the min y
            thismin = b
            if thismin < miny:
                miny = thismin
            namelast = name

        return left, miny, totalw, maxy, -miny

    def get_str_bbox(self, s):
        """
        Return the string bounding box
        """
        return self.get_str_bbox_and_descent(s)[:4]

    def get_name_char(self, c, isord=False):
        """
        Get the name of the character, i.e., ';' is 'semicolon'
        """
        if not isord:
            c = ord(c)
        wx, name, bbox = self._metrics[c]
        return name

    def get_width_char(self, c, isord=False):
        """
        Get the width of the character from the character metric WX
        field
        """
        if not isord:
            c = ord(c)
        wx, name, bbox = self._metrics[c]
        return wx

    def get_width_from_char_name(self, name):
        """
        Get the width of the character from a type1 character name
        """
        wx, bbox = self._metrics_by_name[name]
        return wx

    def get_height_char(self, c, isord=False):
        """
        Get the height of character *c* from the bounding box.  This
        is the ink height (space is 0)
        """
        if not isord:
            c = ord(c)
        wx, name, bbox = self._metrics[c]
        return bbox[-1]

    def get_kern_dist(self, c1, c2):
        """
        Return the kerning pair distance (possibly 0) for chars *c1*
        and *c2*
        """
        name1, name2 = self.get_name_char(c1), self.get_name_char(c2)
        return self.get_kern_dist_from_name(name1, name2)

    def get_kern_dist_from_name(self, name1, name2):
        """
        Return the kerning pair distance (possibly 0) for chars
        *name1* and *name2*
        """
        return self._kern.get((name1, name2), 0)

    def get_fontname(self):
        "Return the font name, e.g., 'Times-Roman'"
        return self._header[b'FontName']

    def get_fullname(self):
        "Return the font full name, e.g., 'Times-Roman'"
        name = self._header.get(b'FullName')
        if name is None:  # use FontName as a substitute
            name = self._header[b'FontName']
        return name

    def get_familyname(self):
        "Return the font family name, e.g., 'Times'"
        name = self._header.get(b'FamilyName')
        if name is not None:
            return name

        # FamilyName not specified so we'll make a guess
        name = self.get_fullname()
        extras = (r'(?i)([ -](regular|plain|italic|oblique|bold|semibold|'
                  r'light|ultralight|extra|condensed))+$')
        return re.sub(extras, '', name)

    @property
    def family_name(self):
        return self.get_familyname()

    def get_weight(self):
        "Return the font weight, e.g., 'Bold' or 'Roman'"
        return self._header[b'Weight']

    def get_angle(self):
        "Return the fontangle as float"
        return self._header[b'ItalicAngle']

    def get_capheight(self):
        "Return the cap height as float"
        return self._header[b'CapHeight']

    def get_xheight(self):
        "Return the xheight as float"
        return self._header[b'XHeight']

    def get_underline_thickness(self):
        "Return the underline thickness as float"
        return self._header[b'UnderlineThickness']

    def get_horizontal_stem_width(self):
        """
        Return the standard horizontal stem width as float, or *None* if
        not specified in AFM file.
        """
        return self._header.get(b'StdHW', None)

    def get_vertical_stem_width(self):
        """
        Return the standard vertical stem width as float, or *None* if
        not specified in AFM file.
        """
        return self._header.get(b'StdVW', None)
