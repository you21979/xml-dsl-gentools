#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------

# pjw
def pjw(key):
    BitsInUnsignedInt = 4 * 8
    ThreeQuarters = long((BitsInUnsignedInt  * 3) / 4)
    OneEighth = long(BitsInUnsignedInt / 8)
    HighBits = (0xFFFFFFFF) << (BitsInUnsignedInt - OneEighth)
    value = 0
    test = 0
    for i in range(len(key)):
        value = (value << OneEighth) + ord(key[i])
        test = value & HighBits
        if test != 0:
            value = (( value ^ (test >> ThreeQuarters)) & (~HighBits));
    return (value & 0x7FFFFFFF)

