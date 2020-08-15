#
# utils.py
#
# Copyright © 2020 by Foundation Devices Inc.
#

from crc32 import crc32, crc32n

def crc32_bytes(buf):
    checksum = crc32n(buf)
    return checksum

def crc32_int(buf):
    return crc32(buf)

def data_to_hex(buf):
    return buf.hex()

def int_to_bytes(n):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

def bytes_to_int(buf):
    return int.from_bytes(buf, 'big')

def string_to_bytes(s):
    return bytes(s, 'utf8')

def is_ur_type(ch):
    if 'a' <= ch and ch <= 'z':
         return True
    if '0' <= ch and ch <= '9':
        return True
    if ch == '-':
        return True
    return False

def partition(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]
