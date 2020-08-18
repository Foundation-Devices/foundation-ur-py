#
# fountain_encoder.py
#
# Copyright © 2020 by Foundation Devices Inc.
#

from cbor_lite import CBOREncoder

from fountain_utils import choose_fragments
import math
from utils import split, crc32_int, xor_into, data_to_hex

import cbor_lite

class Part:
    class InvalidHeader(Exception):
        pass

    # (uint32_t seq_num, size_t seq_len, size_t message_len, uint32_t checksum, const ByteVector& data) 
    def __init__(self, seq_num, seq_len, message_len, checksum, data):
        self.seq_num = seq_num
        self.seq_len = seq_len
        self.message_len = message_len
        self.checksum = checksum
        self.data = data

    def from_cbor(cbor_buf):
        try:
            decoder = CBOREncoder(cbor_buf)
            (array_size, _) = decoder.decodeArraySize()
            if array_size != 5:
                raise InvalidHeader()
            
            n = None
            
            (n, _) = decoder.decodeUnsigned();
            if n > 0xffffffffffffffff:
                raise InvalidHeader()
            self.seq_num = n
            
            (n, _) = decoder.decodeUnsigned()
            if n > 0xffffffffffffffff:
                raise InvalidHeader()
            self.seq_len = n
            
            (n, _) = decoder.decodeUnsigned()
            if n > 0xffffffffffffffff:
                raise InvalidHeader()
            self.message_len = n
            
            (n, _) = decoder.decodeUnsigned()
            if n > 0xffffffffffffffff:
                raise InvalidHeader()
            self.checksum = n

            (data, _) = decoder.decodeBytes()
            self.data = data
        except Exception:
            raise InvalidHeader()

    def cbor(self):
        encoder = CBOREncoder()
        encoder.encodeArraySize(5)
        encoder.encodeInteger(self.seq_num)
        encoder.encodeInteger(self.seq_len)
        encoder.encodeInteger(self.message_len)
        encoder.encodeInteger(self.checksum)
        encoder.encodeBytes(self.data)
        return encoder.get_bytes()

    def seq_num(self):
        return self.seq_num

    def seq_len(self):
        return self.seq_len

    def message_len(self):
        return self.message_len

    def checksum(self):
        return self.checksum

    def data(self):
        return self.data

    def description(self):
        return "seqNum:{}, seqLen:{}, messageLen:{}, checksum:{}, data:{}".format(
            self.seq_num, self.seq_len, self.message_len, self.checksum, data_to_hex(self.data))

class FountainEncoder:
    # ByteVector& message, size_t max_fragment_len, uint32_t first_seq_num = 0, size_t min_fragment_len = 10)
    def __init__(self, message, max_fragment_len, first_seq_num = 0, min_fragment_len = 10):
        assert(len(message) <= 0xffffffff)
        self.message_len = len(message)
        self.checksum = crc32_int(message)
        self.fragment_len = FountainEncoder.find_nominal_fragment_length(self.message_len, min_fragment_len, max_fragment_len)
        self.fragments = FountainEncoder.partition_message(message, self.fragment_len)
        self.seq_num = first_seq_num
    
    @staticmethod
    def find_nominal_fragment_length(message_len, min_fragment_len, max_fragment_len):
        assert(message_len > 0)
        assert(min_fragment_len > 0)
        assert(max_fragment_len >= min_fragment_len)
        max_fragment_count = message_len // min_fragment_len
        fragment_len = None

        for fragment_count in range(1, max_fragment_count + 1):
            fragment_len = math.ceil(message_len / fragment_count)
            if fragment_len <= max_fragment_len:
                break

        assert(fragment_len != None)
        return fragment_len


    @staticmethod
    def partition_message(message, fragment_len):
        remaining = message
        fragments = []
        while len(remaining) != 0:
            (fragment, remaining) = split(remaining, fragment_len);
            padding = fragment_len - len(fragment)
            while padding > 0:
                fragment.append(0)
                padding -= 1
            fragments.append(fragment)

        return fragments

    def last_part_indexes(self):
        return self.last_part_indexes

    def seq_len(self):
        return len(self.fragments)

    # This becomes `true` when the minimum number of parts
    # to relay the complete message have been generated
    def is_complete(self):
        return self.seq_num >= self.seq_len()

    # True if only a single part will be generated.
    def is_single_part(self):
        return self.seq_len() == 1

    def next_part(self):
        self.seq_num += 1
        self.seq_num = self.seq_num % 0xffffffff  # wrap at period 2^32
        indexes = choose_fragments(self.seq_num, self.seq_len(), self.checksum)
        mixed = self.mix(indexes)
        data = bytes(mixed)
        return Part(self.seq_num, self.seq_len(), self.message_len, self.checksum, data)

    def mix(self, indexes):
        result = [0] * self.fragment_len
        for index in indexes:
            xor_into(result, self.fragments[index])
        return result
