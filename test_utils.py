#
# test_utils.py
#
# Copyright © 2020 by Foundation Devices Inc.
#

from xoshiro256 import Xoshiro256
from cbor_lite import CBOREncoder

def make_message(length, seed = "Wolf"):
    rng = Xoshiro256.from_string(seed)
    return rng.next_data(length)

def make_message_ur(length, seed = "Wolf"):
    message = make_message(length, seed)
    encoder = CBOREncoder()
    encoder.encodeBytes(message)
    
    # TODO: Implement UR and add this code in
    # return UR("bytes", encoder.get_bytes())

