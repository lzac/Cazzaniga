# -*- coding: utf-8 -*-

from Crypto.Cipher import Blowfish #@UnresolvedImport

B64 = "./0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def _i(s, n):
    try:
        return s[n]
    except:
        return '\x00'

def _bytetoB64(s):
    r = ''
    k = -1

    while (k < len(s) - 1):
        k += 1
        left = (ord(_i(s, k)) << 24)
        k += 1
        left += (ord(_i(s, k)) << 16)
        k += 1
        left += (ord(_i(s, k)) << 8)
        k += 1
        left += ord(_i(s, k))

        k += 1
        right = (ord(_i(s, k)) << 24)
        k += 1
        right += (ord(_i(s, k)) << 16)
        k += 1
        right += (ord(_i(s, k)) << 8)
        k += 1
        right += ord(_i(s, k))

        for i in range(0, 6):
            r += B64[right & 0x3F]
            right = right >> 6

        for i in range(0, 6):
            r += B64[left & 0x3F]
            left = left >> 6
    return r


def _B64tobyte(s):
    r = ''
    k = -1
    if s==None:
        s = ''
    while (k < len(s) - 1):
        left = 0
        right = 0

        for i in range(0, 6):
            k += 1
            try:
                right |= B64.index(s[k]) << (i * 6)
            except:
                pass

        for i in range(0, 6):
            k += 1
            try:
                left |= B64.index(s[k]) << (i * 6)
            except:
                pass
        for i in range(0, 4):
            r += chr((left & (0xFF << ((3 - i) * 8))) >> ((3 - i) * 8))

        for i in range(0, 4):
            r += chr((right & (0xFF << ((3 - i) * 8))) >> ((3 - i) * 8))
    return r


def encrypt(data, key):
    obj = Blowfish.new(key)
    for i in range(0, (8 - len(data) % 8)):
        data += chr(0)
    return _bytetoB64(obj.encrypt(data))

def decrypt(data, key):
    obj = Blowfish.new(key)
    return obj.decrypt(_B64tobyte(data)).replace(chr(0), "")