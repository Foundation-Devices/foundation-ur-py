# CRC32 functions

TABLE = None
def crc32(buf):
    # Lazily instantiate CRC table
    global TABLE
    if TABLE == None:
        TABLE = [None] * (256 * 4)

        for i in range(256):
            c = i
            for j in range(8):
                c = (c >> 1) if (c % 2 == 0) else (0xEDB88320 ^ (c >> 1))

            TABLE[i] = c

    crc = 0xffffffff & ~0
    for byte in buf:
        crc = (crc >> 8) ^ TABLE[(crc ^ byte) & 0xFF]

    return 0xffffffff & ~crc

def crc32n(buf):
    n = crc32(buf)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')
