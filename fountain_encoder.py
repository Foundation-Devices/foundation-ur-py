#
# fountain_encoder.py
#
# Copyright © 2020 by Foundation Devices Inc.
#

import math
from utils import split

import cbor_lite

class FountainEncoder:
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
            self.cbor = None
            self.description = None

        def from_cbor(cbor):
            try:
                # auto i = cbor.begin();
                # auto end = cbor.end();
                # size_t array_size;
                # CborLite::decodeArraySize(i, end, array_size);
                # if(array_size != 5) { throw InvalidHeader(); }
                
                # uint64_t n;
                
                # CborLite::decodeUnsigned(i, end, n);
                # if(n > std::numeric_limits<decltype(seq_num_)>::max()) { throw InvalidHeader(); }
                # seq_num_ = n;
                
                # CborLite::decodeUnsigned(i, end, n);
                # if(n > std::numeric_limits<decltype(seq_len_)>::max()) { throw InvalidHeader(); }
                # seq_len_ = n;
                
                # CborLite::decodeUnsigned(i, end, n);
                # if(n > std::numeric_limits<decltype(message_len_)>::max()) { throw InvalidHeader(); }
                # message_len_ = n;
                
                # CborLite::decodeUnsigned(i, end, n);
                # if(n > std::numeric_limits<decltype(checksum_)>::max()) { throw InvalidHeader(); }
                # checksum_ = n;

                # CborLite::decodeBytes(i, end, data_);
                pass
            except Exception:
                raise InvalidHeader()

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

    # ByteVector& message, size_t max_fragment_len, uint32_t first_seq_num = 0, size_t min_fragment_len = 10)
    def __init__(self, message, max_fragment_len, first_seq_num = 0,min_fragment_len = 10):
        pass
    
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

    def seq_num(self):
        return self.seq_num

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

    def next_part():
        pass

    def _mix(indexes):
        pass
