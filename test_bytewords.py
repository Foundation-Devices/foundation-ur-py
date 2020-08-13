#
# test_bytewords.py
#
# Copyright © 2020 by Foundation Devices Inc.
#
import unittest

from bytewords import Bytewords
from utils import crc32_bytes, crc32_int, data_to_hex

def check_crc32(input, expected_hex):
    checksum = crc32_int(bytes(input, 'utf8'))
    hex = '{:x}'.format(checksum)
    return hex == expected_hex

class TestUR(unittest.TestCase):
    def test_crc32(self):
        assert check_crc32("Hello, world!", "ebe6c6e6")
        assert check_crc32("Wolf", "598c84dc")


# static void test_bytewords_1() {
#     ByteVector input = {0, 1, 2, 128, 255};
#     assert(Bytewords::encode(Bytewords::style::standard, input) == "able acid also lava zero jade need echo taxi");
#     assert(Bytewords::encode(Bytewords::style::uri, input) == "able-acid-also-lava-zero-jade-need-echo-taxi");
#     assert(Bytewords::encode(Bytewords::style::minimal, input) == "aeadaolazojendeoti");

#     assert(Bytewords::decode(Bytewords::style::standard, "able acid also lava zero jade need echo taxi") == input);
#     assert(Bytewords::decode(Bytewords::style::uri, "able-acid-also-lava-zero-jade-need-echo-taxi") == input);
#     assert(Bytewords::decode(Bytewords::style::minimal, "aeadaolazojendeoti") == input);

#     // bad checksum
#     assert_throws(Bytewords::decode(Bytewords::style::standard, "able acid also lava zero jade need echo wolf"));
#     assert_throws(Bytewords::decode(Bytewords::style::uri, "able-acid-also-lava-zero-jade-need-echo-wolf"));
#     assert_throws(Bytewords::decode(Bytewords::style::minimal, "aeadaolazojendeowf"));

#     // too short
#     assert_throws(Bytewords::decode(Bytewords::style::standard, "wolf"));
#     assert_throws(Bytewords::decode(Bytewords::style::standard, ""));
# }

# static void test_bytewords_2() {
#     ByteVector input = {
#         245, 215, 20, 198, 241, 235, 69, 59, 209, 205,
#         165, 18, 150, 158, 116, 135, 229, 212, 19, 159,
#         17, 37, 239, 240, 253, 11, 109, 191, 37, 242,
#         38, 120, 223, 41, 156, 189, 242, 254, 147, 204,
#         66, 163, 216, 175, 191, 72, 169, 54, 32, 60,
#         144, 230, 210, 137, 184, 197, 33, 113, 88, 14,
#         157, 31, 177, 46, 1, 115, 205, 69, 225, 150,
#         65, 235, 58, 144, 65, 240, 133, 69, 113, 247,
#         63, 53, 242, 165, 160, 144, 26, 13, 79, 237,
#         133, 71, 82, 69, 254, 165, 138, 41, 85, 24
#     };

#     string encoded =
#         "yank toys bulb skew when warm free fair tent swan "
#         "open brag mint noon jury lion view tiny brew note "
#         "body data webs what zone bald join runs data whiz "
#         "days keys user diet news ruby whiz zoom menu surf "
#         "flew omit trip pose runs fund part even crux fern "
#         "math visa tied loud redo silk curl jugs hard beta "
#         "next cost puma drum acid junk swan free very mint "
#         "flap warm fact math flap what list free jugs yell "
#         "fish epic whiz open numb math city belt glow wave "
#         "list fuel grim free zoom open love diet gyro cats "
#         "fizz holy city puff";

#     string encoded_minimal =
#         "yktsbbswwnwmfefrttsnonbgmtnnjylnvwtybwne"
#         "bydawswtzebdjnrsdawzdsksurdtnsrywzzmmusf"
#         "fwottppersfdptencxfnmhvatdldroskcljshdba"
#         "ntctpadmadjksnfevymtfpwmftmhfpwtltfejsyl"
#         "fhecwzonnbmhcybtgwweltflgmfezmonledtgocs"
#         "fzhycypf";

#     assert(Bytewords::encode(Bytewords::style::standard, input) == encoded);
#     assert(Bytewords::encode(Bytewords::style::minimal, input) == encoded_minimal);
#     assert(Bytewords::decode(Bytewords::style::standard, encoded) == input);
#     assert(Bytewords::decode(Bytewords::style::minimal, encoded_minimal) == input);
# }

if __name__ == '__main__':
    unittest.main()