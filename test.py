#
# test.py
#
# Copyright © 2020 by Foundation Devices Inc.
#

import unittest

from bytewords import Bytewords
from utils import crc32_bytes, crc32_int, data_to_hex, bytes_to_int, string_to_bytes
from xoshiro256 import Xoshiro256
from random_sampler import RandomSampler
from fountain_utils import shuffled

def check_crc32(input, expected_hex):
    checksum = crc32_int(bytes(input, 'utf8'))
    hex = '{:x}'.format(checksum)
    return hex == expected_hex

class TestUR(unittest.TestCase):
    def test_crc32(self):
        assert check_crc32("Hello, world!", "ebe6c6e6")
        assert check_crc32("Wolf", "598c84dc")

    def test_bytewords_1(self):
        input = bytes([0, 1, 2, 128, 255])
        assert(Bytewords.encode(Bytewords.Style.standard, input) == "able acid also lava zero jade need echo taxi")
        assert(Bytewords.encode(Bytewords.Style.uri, input) == "able-acid-also-lava-zero-jade-need-echo-taxi")
        assert(Bytewords.encode(Bytewords.Style.minimal, input) == "aeadaolazojendeoti")

        assert(Bytewords.decode(Bytewords.Style.standard, "able acid also lava zero jade need echo taxi") == input)
        assert(Bytewords.decode(Bytewords.Style.uri, "able-acid-also-lava-zero-jade-need-echo-taxi") == input)
        assert(Bytewords.decode(Bytewords.Style.minimal, "aeadaolazojendeoti") == input)

        # bad checksum
        with self.assertRaises(ValueError):
            Bytewords.decode(Bytewords.Style.standard, "able acid also lava zero jade need echo wolf")
        with self.assertRaises(ValueError):
            Bytewords.decode(Bytewords.Style.uri, "able-acid-also-lava-zero-jade-need-echo-wolf")
        with self.assertRaises(ValueError):
            Bytewords.decode(Bytewords.Style.minimal, "aeadaolazojendeowf")

        # too short
        with self.assertRaises(ValueError):
            Bytewords.decode(Bytewords.Style.standard, "wolf")
        with self.assertRaises(ValueError):
            Bytewords.decode(Bytewords.Style.standard, "")

    def test_bytewords_2(self):
        input = bytes([
            245, 215, 20, 198, 241, 235, 69, 59, 209, 205,
            165, 18, 150, 158, 116, 135, 229, 212, 19, 159,
            17, 37, 239, 240, 253, 11, 109, 191, 37, 242,
            38, 120, 223, 41, 156, 189, 242, 254, 147, 204,
            66, 163, 216, 175, 191, 72, 169, 54, 32, 60,
            144, 230, 210, 137, 184, 197, 33, 113, 88, 14,
            157, 31, 177, 46, 1, 115, 205, 69, 225, 150,
            65, 235, 58, 144, 65, 240, 133, 69, 113, 247,
            63, 53, 242, 165, 160, 144, 26, 13, 79, 237,
            133, 71, 82, 69, 254, 165, 138, 41, 85, 24
        ])

        encoded = \
            "yank toys bulb skew when warm free fair tent swan " + \
            "open brag mint noon jury lion view tiny brew note " + \
            "body data webs what zone bald join runs data whiz " + \
            "days keys user diet news ruby whiz zoom menu surf " + \
            "flew omit trip pose runs fund part even crux fern " + \
            "math visa tied loud redo silk curl jugs hard beta " + \
            "next cost puma drum acid junk swan free very mint " + \
            "flap warm fact math flap what list free jugs yell " + \
            "fish epic whiz open numb math city belt glow wave " + \
            "list fuel grim free zoom open love diet gyro cats " + \
            "fizz holy city puff"

        encoded_minimal = \
            "yktsbbswwnwmfefrttsnonbgmtnnjylnvwtybwne" + \
            "bydawswtzebdjnrsdawzdsksurdtnsrywzzmmusf" + \
            "fwottppersfdptencxfnmhvatdldroskcljshdba" + \
            "ntctpadmadjksnfevymtfpwmftmhfpwtltfejsyl" + \
            "fhecwzonnbmhcybtgwweltflgmfezmonledtgocs" + \
            "fzhycypf"

        assert(Bytewords.encode(Bytewords.Style.standard, input) == encoded)
        assert(Bytewords.encode(Bytewords.Style.minimal, input) == encoded_minimal)
        assert(Bytewords.decode(Bytewords.Style.standard, encoded) == input)
        assert(Bytewords.decode(Bytewords.Style.minimal, encoded_minimal) == input)


    def test_rng_1(self):
        rng = Xoshiro256.from_string("Wolf")
        numbers = []
        for i in range(100):
            numbers.append(rng.next() % 100)

        expected_numbers = [42, 81, 85, 8, 82, 84, 76, 73, 70, 88, 2, 74, 40, 48, 77, 54, 88, 7, 5, 88, 37, 25, 82, 13, 69, 59, 30, 39, 11, 82, 19, 99, 45, 87, 30, 15, 32, 22, 89, 44, 92, 77, 29, 78, 4, 92, 44, 68, 92, 69, 1, 42, 89, 50, 37, 84, 63, 34, 32, 3, 17, 62, 40, 98, 82, 89, 24, 43, 85, 39, 15, 3, 99, 29, 20, 42, 27, 10, 85, 66, 50, 35, 69, 70, 70, 74, 30, 13, 72, 54, 11, 5, 70, 55, 91, 52, 10, 43, 43, 52]
        assert(numbers == expected_numbers)

    def test_rng_2(self):
        checksum = bytes_to_int(crc32_bytes(string_to_bytes("Wolf")))
        rng = Xoshiro256.from_crc32(checksum)
        numbers  = []
        for i in range(100):
            numbers.append(rng.next() % 100)

        expected_numbers = [88, 44, 94, 74, 0, 99, 7, 77, 68, 35, 47, 78, 19, 21, 50, 15, 42, 36, 91, 11, 85, 39, 64, 22, 57, 11, 25, 12, 1, 91, 17, 75, 29, 47, 88, 11, 68, 58, 27, 65, 21, 54, 47, 54, 73, 83, 23, 58, 75, 27, 26, 15, 60, 36, 30, 21, 55, 57, 77, 76, 75, 47, 53, 76, 9, 91, 14, 69, 3, 95, 11, 73, 20, 99, 68, 61, 3, 98, 36, 98, 56, 65, 14, 80, 74, 57, 63, 68, 51, 56, 24, 39, 53, 80, 57, 51, 81, 3, 1, 30]
        assert(numbers == expected_numbers)

    def test_rng_3(self):
        rng = Xoshiro256.from_string("Wolf")
        numbers = []
        for i in range(100):
            numbers.append(rng.next_int(1, 10))

        expected_numbers = [6, 5, 8, 4, 10, 5, 7, 10, 4, 9, 10, 9, 7, 7, 1, 1, 2, 9, 9, 2, 6, 4, 5, 7, 8, 5, 4, 2, 3, 8, 7, 4, 5, 1, 10, 9, 3, 10, 2, 6, 8, 5, 7, 9, 3, 1, 5, 2, 7, 1, 4, 4, 4, 4, 9, 4, 5, 5, 6, 9, 5, 1, 2, 8, 3, 3, 2, 8, 4, 3, 2, 1, 10, 8, 9, 3, 10, 8, 5, 5, 6, 7, 10, 5, 8, 9, 4, 6, 4, 2, 10, 2, 1, 7, 9, 6, 7, 4, 2, 5]
        assert(numbers == expected_numbers)

    # TODO: test_find_fragment_length() goes here

    def test_random_sampler(self):
        probs = [ 1, 2, 4, 8 ]
        sampler = RandomSampler(probs)
        rng = Xoshiro256.from_string("Wolf")
        samples = []
        f = lambda: rng.next_double()
        for i in range(500):
            samples.append(sampler.next(f))

        expected_samples = [3, 3, 3, 3, 3, 3, 3, 0, 2, 3, 3, 3, 3, 1, 2, 2, 1, 3, 3, 2, 3, 3, 1, 1, 2, 1, 1, 3, 1, 3, 1, 2, 0, 2, 1, 0, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 2, 3, 2, 2, 3, 3, 3, 3, 2, 3, 3, 0, 3, 3, 3, 3, 1, 2, 3, 3, 2, 2, 2, 1, 2, 2, 1, 2, 3, 1, 3, 0, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 1, 3, 3, 2, 0, 2, 2, 3, 1, 1, 2, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 3, 1, 2, 1, 1, 3, 1, 3, 2, 2, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 1, 2, 3, 3, 1, 3, 2, 3, 3, 3, 2, 3, 1, 3, 0, 3, 2, 1, 1, 3, 1, 3, 2, 3, 3, 3, 3, 2, 0, 3, 3, 1, 3, 0, 2, 1, 3, 3, 1, 1, 3, 1, 2, 3, 3, 3, 0, 2, 3, 2, 0, 1, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 0, 2, 3, 3, 3, 3, 2, 1, 1, 1, 2, 1, 3, 3, 3, 2, 2, 3, 3, 1, 2, 3, 0, 3, 2, 3, 3, 3, 3, 0, 2, 2, 3, 2, 2, 3, 3, 3, 3, 1, 3, 2, 3, 3, 3, 3, 3, 2, 2, 3, 1, 3, 0, 2, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 2, 2, 2, 3, 1, 1, 3, 2, 2, 0, 3, 2, 1, 2, 1, 0, 3, 3, 3, 2, 2, 3, 2, 1, 2, 0, 0, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 1, 1, 3, 2, 2, 3, 1, 1, 0, 1, 3, 2, 3, 3, 2, 3, 3, 2, 3, 3, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 1, 2, 3, 3, 2, 2, 2, 2, 3, 3, 2, 0, 2, 1, 3, 3, 3, 3, 0, 3, 3, 3, 3, 2, 2, 3, 1, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 2, 1, 3, 3, 3, 3, 2, 2, 0, 1, 2, 3, 2, 0, 3, 3, 3, 3, 3, 3, 1, 3, 3, 2, 3, 2, 2, 3, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 2, 1, 3, 3, 3, 3, 1, 2, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 1, 2, 3, 2, 1, 1, 3, 3, 2, 3, 3, 2, 3, 3, 0, 0, 1, 3, 3, 2, 3, 3, 3, 3, 1, 3, 3, 0, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 2]
        assert(samples == expected_samples)

    def test_shuffle(self):
        rng = Xoshiro256.from_string("Wolf")
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = []
        for i in range(10):
            result.append(shuffled(values.copy(), rng))

        expectedResult = [
            [6, 4, 9, 3, 10, 5, 7, 8, 1, 2],
            [10, 8, 6, 5, 1, 2, 3, 9, 7, 4],
            [6, 4, 5, 8, 9, 3, 2, 1, 7, 10],
            [7, 3, 5, 1, 10, 9, 4, 8, 2, 6],
            [8, 5, 7, 10, 2, 1, 4, 3, 9, 6],
            [4, 3, 5, 6, 10, 2, 7, 8, 9, 1],
            [5, 1, 3, 9, 4, 6, 2, 10, 7, 8],
            [2, 1, 10, 8, 9, 4, 7, 6, 3, 5],
            [6, 7, 10, 4, 8, 9, 2, 3, 1, 5],
            [10, 2, 1, 7, 9, 5, 6, 3, 4, 8]
        ]
        assert(result == expectedResult)

if __name__ == '__main__':
    unittest.main()