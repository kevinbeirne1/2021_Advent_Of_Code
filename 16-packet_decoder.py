"""
--- Day 16: Packet Decoder ---
As you leave the cave and reach open waters, you receive a transmission from
the Elves back on the ship.

The transmission was sent using the Buoyancy Interchange Transmission System
(BITS), a method of packing numeric expressions into a binary sequence. Your
submarine's computer has saved the transmission in hexadecimal (your puzzle
input).

The first step of decoding the message is to convert the hexadecimal
representation into binary. Each character of hexadecimal corresponds to four
bits of binary data:

    0 = 0000
    1 = 0001
    2 = 0010
    3 = 0011
    4 = 0100
    5 = 0101
    6 = 0110
    7 = 0111
    8 = 1000
    9 = 1001
    A = 1010
    B = 1011
    C = 1100
    D = 1101
    E = 1110
    F = 1111

The BITS transmission contains a single packet at its outermost layer which
itself contains many other packets. The hexadecimal representation of this
packet might encode a few extra 0 bits at the end; these are not part of the
transmission and should be ignored.

Every packet begins with a standard header: the first three bits encode the
packet version, and the next three bits encode the packet type ID. These two
values are numbers; all numbers encoded in any packet are represented as binary
with the most significant bit first. For example, a version encoded as the
binary sequence 100 represents the number 4.

Packets with type ID 4 represent a literal value. Literal value packets encode
a single binary number. To do this, the binary number is padded with leading
zeroes until its length is a multiple of four bits, and then it is broken into
groups of four bits. Each group is prefixed by a 1 bit except the last group,
which is prefixed by a 0 bit. These groups of five bits immediately follow the
packet header. For example, the hexadecimal string D2FE28 becomes:

    110100101111111000101000
    VVVTTTAAAAABBBBBCCCCC

Below each bit is a label indicating its purpose:

    - The three bits labeled V (110) are the packet version, 6.
    - The three bits labeled T (100) are the packet type ID, 4, which means the
    packet is a literal value.
    - The five bits labeled A (10111) start with a 1 (not the last group, keep
    reading) and contain the first four bits of the number, 0111.
    - The five bits labeled B (11110) start with a 1 (not the last group, keep
    reading) and contain four more bits of the number, 1110.
    - The five bits labeled C (00101) start with a 0 (last group, end of
    packet) and contain the last four bits of the number, 0101.
    - The three unlabeled 0 bits at the end are extra due to the hexadecimal
    representation and should be ignored.

So, this packet represents a literal value with binary representation
011111100101, which is 2021 in decimal.

Every other type of packet (any packet with a type ID other than 4) represent
an operator that performs some calculation on one or more sub-packets contained
within. Right now, the specific operations aren't important; focus on parsing
the hierarchy of sub-packets.

An operator packet contains one or more packets. To indicate which subsequent
binary data represents its sub-packets, an operator packet can use one of two
modes indicated by the bit immediately after the packet header; this is called
the length type ID:

    - If the length type ID is 0, then the next 15 bits are a number that
    represents the total length in bits of the sub-packets contained by this
    packet.
    - If the length type ID is 1, then the next 11 bits are a number that
    represents the number of sub-packets immediately contained by this packet.

Finally, after the length type ID bit and the 15-bit or 11-bit field, the
sub-packets appear.

For example, here is an operator packet (hexadecimal string 38006F45291200)
with length type ID 0 that contains two sub-packets:

    00111000000000000110111101000101001010010001001000000000
    VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB

    - The three bits labeled V (001) are the packet version, 1.
    - The three bits labeled T (110) are the packet type ID, 6, which means the
    packet is an operator.
    - The bit labeled I (0) is the length type ID, which indicates that the
    length is a 15-bit number representing the number of bits in the sub-packets.
    - The 15 bits labeled L (000000000011011) contain the length of the
    sub-packets in bits, 27.
    - The 11 bits labeled A contain the first sub-packet, a literal value
    representing the number 10.
    - The 16 bits labeled B contain the second sub-packet, a literal value
    representing the number 20.

After reading 11 and 16 bits of sub-packet data, the total length indicated in
L (27) is reached, and so parsing of this packet stops.

As another example, here is an operator packet (hexadecimal string
EE00D40C823060) with length type ID 1 that contains three sub-packets:

    11101110000000001101010000001100100000100011000001100000
    VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC

    - The three bits labeled V (111) are the packet version, 7.
    - The three bits labeled T (011) are the packet type ID, 3, which means the
    packet is an operator.
    - The bit labeled I (1) is the length type ID, which indicates that the
    length is a 11-bit number representing the number of sub-packets.
    - The 11 bits labeled L (00000000011) contain the number of sub-packets, 3.
    - The 11 bits labeled A contain the first sub-packet, a literal value
    representing the number 1.
    - The 11 bits labeled B contain the second sub-packet, a literal value
    representing the number 2.
    - The 11 bits labeled C contain the third sub-packet, a literal value
    representing the number 3.

After reading 3 complete sub-packets, the number of sub-packets indicated in L
(3) is reached, and so parsing of this packet stops.

For now, parse the hierarchy of the packets throughout the transmission and add
up all of the version numbers.

Here are a few more examples of hexadecimal-encoded transmissions:

    - 8A004A801A8002F478 represents an operator packet (version 4) which
    contains an operator packet (version 1) which contains an operator packet
    (version 5) which contains a literal value (version 6); this packet has a
    version sum of 16.
    - 620080001611562C8802118E34 represents an operator packet (version 3)
    which contains two sub-packets; each sub-packet is an operator packet that
    contains two literal values. This packet has a version sum of 12.
    - C0015000016115A2E0802F182340 has the same structure as the previous
    example, but the outermost packet uses a different length type ID. This
    packet has a version sum of 23.
    - A0016C880162017C3686B18A3D4780 is an operator packet that contains an
    operator packet that contains an operator packet that contains five
    literal values; it has a version sum of 31.

Decode the structure of your hexadecimal-encoded BITS transmission; what do you
get if you add up the version numbers in all packets?
"""

import unittest
from collections import namedtuple
from math import ceil
from helper_functions import read_txt_file_contents
import numpy as np

def hex_to_bin(hex_string):
    hex_digits = {
        "0": '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
    }
    output = ""
    for letter in hex_string:
        output += hex_digits[letter]
    return output


LiteralCode = namedtuple('LiteralCode', ['version', 'operator', 'numbers', 'block_length'])
FixedLength = namedtuple('FixedLength', ['version', 'operator', 'id', 'length', 'sub_packets', 'block_length'])
VariableLength = namedtuple('VariableLength', ['version', 'operator', 'id', 'no_of_sub_packets', 'sub_packets', 'block_length'])


def decode_binary_string(input_string, version_sum=None):
    if not version_sum:
        version_sum = 0
    version = int(input_string[:3], 2)
    version_sum += version
    operator = int(input_string[3: 6], 2)
    remainder = input_string[6:]
    if operator == 4:
        decoded_literal = decode_literal(remainder)
        preamble_length = 6
        block_length = preamble_length + (len(decoded_literal) * 5)//4
        # padded_block_length = ceil(block_length / 8) * 8

        return version_sum, LiteralCode(version, operator, int(decoded_literal, 2), block_length)
    else:
        length_id = int(remainder[0])
        preamble_length = 7

        if length_id == 0:
            # Fixed length sub_packet
            packet_length_bin = remainder[1:16]
            packet_length_int = int(packet_length_bin, 2)
            packets_string = remainder[16: 16 + packet_length_int]
            packet_data = []
            while packets_string:
                version_sum, packet = decode_binary_string(packets_string, version_sum)
                packets_string = packets_string[packet.block_length:]
                packet_data.append(packet)
                # break
                pass
            block_length = preamble_length + len(packet_length_bin) + packet_length_int
            # padded_block_length = ceil(block_length / 8) * 8
            return version_sum, FixedLength(version, operator, length_id, packet_length_int, packet_data, block_length)
        else:
            packet_amount_bin = remainder[1:12]
            packet_amount_int = int(packet_amount_bin, 2)
            packet_string = remainder[12:]
            block_length = preamble_length + len(packet_amount_bin)
            packets = []
            for _ in range(packet_amount_int):
                version_sum, packet = decode_binary_string(packet_string, version_sum)
                packets.append(packet)
                packet_length = packet.block_length
                packet_string = packet_string[packet_length:]
                block_length += packet_length
            return version_sum, VariableLength(version, operator, length_id, packet_amount_int, packets, block_length)
    padded_block_length = ceil(block_length / 8) * 8
    print(padded_block_length)


def decode_literal(input_string):
    number = ""
    i = 0
    while True:
        index = i + 4*i
        new_block = input_string[index: index + 5]
        last_digit = new_block[0]
        number += new_block[1:] if len(new_block) == 5 else ""
        i += 1

        if last_digit == "0":
            # output_string = input_string[index + 5:]
            break

    return number


def decode_hex_part_1(hex_string):
    bin_string = hex_to_bin(hex_string)
    version, packet = decode_binary_string(bin_string)
    return version


class TestDecodeLiteral(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            # ("11010001010", ("110", '100', '1010')),
            # ("1101001101001010", ("110", '100', '10101010')),
            # ("110100101111111000101000", ('110', '100', "011111100101"))
            ("01010", "1010"),
            ("1101001010", "10101010"),
            ("101111111000101000", "011111100101"),
            ("010100101001000100100", "1010"),
        ]

    def test_literal_tuple_type(self):
        actual = (issubclass(LiteralCode, tuple))
        self.assertTrue(actual)

    def test_literal_tuple_fields(self):
        expected = ('version', 'operator', 'numbers', 'block_length')
        actual = LiteralCode._fields
        self.assertEqual(actual, expected)

    def test_decode_literal(self):
        for test_case, expected_result in self.test_cases:
            actual = decode_literal(test_case)
            self.assertEqual(actual, expected_result)


class TestFixedLengthCode(unittest.TestCase):

    def test_fixed_length_tuple_type(self):
        actual = (issubclass(FixedLength, tuple))
        self.assertTrue(actual)

    def test_fixed_length_tuple_fields(self):
        expected = ('version', 'operator', 'id', 'length', 'sub_packets', 'block_length')
        actual = FixedLength._fields
        self.assertEqual(actual, expected)


class TestVariableLengthCode(unittest.TestCase):

    def test_fixed_length_tuple_type(self):
        actual = (issubclass(VariableLength, tuple))
        self.assertTrue(actual)

    def test_variable_length_tuple_fields(self):
        expected = ('version', 'operator', 'id', 'no_of_sub_packets', 'sub_packets', 'block_length')
        actual = VariableLength._fields
        self.assertEqual(actual, expected)


class TestHexToBin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ("", ""),
            (
                'EE00D40C823060',
                '11101110000000001101010000001100100000100011000001100000'
            ),
            (
                '38006F45291200',
                '00111000000000000110111101000101001010010001001000000000'
            )
        ]

    def test_decode_hex(self):
        for test_case, expected_result in self.test_cases:
            actual = hex_to_bin(test_case)
            self.assertEqual(actual, expected_result)


class TestDecodeBinaryString(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ("11110001010", LiteralCode(7, 4, 10, 11)),
            ("1011001101001010", LiteralCode(5, 4, 170, 16)),
            ("100100101111111000101000", LiteralCode(4, 4, 2021, 21)),
            ("110100101111111000101000", LiteralCode(6, 4, 2021, 21)),
            (
                "00111000000000000110111101000101001010010001001000000000",
                FixedLength(1, 6, 0, 27, [LiteralCode(6, 4, 10, 11), LiteralCode(2, 4, 20, 16)], 49)
            ),
            (
                "11101110000000001101010000001100100000100011000001100000",
                VariableLength(7, 3, 1, 3, [
                    LiteralCode(2, 4, 1, 11),
                    LiteralCode(4, 4, 2, 11),
                    LiteralCode(1, 4, 3, 11)
                ], 51),
                # ('variable', "00000000011", '01010000001100100000100011000001100000')
            )
        ]

        cls.version_sum_test_cases = [
            ("11110001010", 7),
            ("1011001101001010", 5),
            ("100100101111111000101000", 4),
            ("110100101111111000101000", 6),
            (
                "00111000000000000110111101000101001010010001001000000000",
                9
            ),
            (
                "11101110000000001101010000001100100000100011000001100000",
                14,
                # ('variable', "00000000011", '01010000001100100000100011000001100000')
            )
        ]

    def test_version_sum(self):
        for test_case, expected_result in self.version_sum_test_cases:
            actual, _ = decode_binary_string(test_case)
            self.assertEqual(actual, expected_result)

    def test_decode_binary_string(self):
        for test_case, expected_result in self.test_cases:
            _, actual = decode_binary_string(test_case)
            # print(actual)
            # print(expected_result)
            self.assertEqual(actual, expected_result)


class TestDecodeHex(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ('8A004A801A8002F478', 16),
            ('620080001611562C8802118E34', 12),
            ('C0015000016115A2E0802F182340', 23),
            ('A0016C880162017C3686B18A3D4780', 31),
        ]

    def test_decode_hex(self):
        for test_case, expected_result in self.test_cases:
            actual = decode_hex_part_1(test_case)
            self.assertEqual(actual, expected_result)

"""
--- Part Two ---
Now that you have the structure of your transmission decoded, you can calculate
the value of the expression it represents.

Literal values (type ID 4) represent a single number as described above. The 
remaining type IDs are more interesting:

    - Packets with type ID 0 are sum packets - their value is the sum of the 
    values of their sub-packets. If they only have a single sub-packet, their 
    value is the value of the sub-packet.
    - Packets with type ID 1 are product packets - their value is the result of
    multiplying together the values of their sub-packets. If they only have a 
    single sub-packet, their value is the value of the sub-packet.
    - Packets with type ID 2 are minimum packets - their value is the minimum 
    of the values of their sub-packets.
    - Packets with type ID 3 are maximum packets - their value is the maximum 
    of the values of their sub-packets.
    - Packets with type ID 5 are greater than packets - their value is 1 if the
    value of the first sub-packet is greater than the value of the second 
    sub-packet; otherwise, their value is 0. These packets always have exactly 
    two sub-packets.
    - Packets with type ID 6 are less than packets - their value is 1 if the 
    value of the first sub-packet is less than the value of the second 
    sub-packet; otherwise, their value is 0. These packets always have exactly
    two sub-packets.
    - Packets with type ID 7 are equal to packets - their value is 1 if the 
    value of the first sub-packet is equal to the value of the second 
    sub-packet; otherwise, their value is 0. These packets always have exactly
    two sub-packets.
    
Using these rules, you can now work out the value of the outermost packet in 
your BITS transmission.

For example:

    - C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
    - 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
    - 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
    - CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
    - D8005AC2A8F0 produces 1, because 5 is less than 15.
    - F600BC2D8F produces 0, because 5 is not greater than 15.
    - 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
    - 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
"""


def decode_hex_part_2(hex_string):
    bin_string = hex_to_bin(hex_string)
    packet, length = decode_binary_string_part_2(bin_string)
    return packet


def decode_binary_string_part_2(input_string):
    operator = int(input_string[3: 6], 2)
    remainder = input_string[6:]
    if operator == 4:
        decoded_literal = decode_literal(remainder)
        preamble_length = 6
        block_length = preamble_length + (len(decoded_literal) * 5)//4
        return int(decoded_literal, 2), block_length
    else:
        length_id = int(remainder[0])
        preamble_length = 7

        if length_id == 0:
            # Fixed length sub_packet
            packet_length_bin = remainder[1:16]
            packet_length_int = int(packet_length_bin, 2)
            packets_string = remainder[16: 16 + packet_length_int]
            packet_data = []
            while packets_string:
                packet, length = decode_binary_string_part_2(packets_string)
                packets_string = packets_string[length:]
                packet_data.append(packet)

            block_length = preamble_length + len(packet_length_bin) + packet_length_int

            return parse_packets(operator, packet_data), block_length

        else:
            packet_amount_bin = remainder[1:12]
            packet_amount_int = int(packet_amount_bin, 2)
            packet_string = remainder[12:]
            block_length = preamble_length + len(packet_amount_bin)
            packets = []
            for _ in range(packet_amount_int):
                packet, packet_length = decode_binary_string_part_2(packet_string)
                packets.append(packet)
                packet_string = packet_string[packet_length:]
                block_length += packet_length
            return parse_packets(operator, packets), block_length


def parse_packets(operator, packets):
    if operator == 0:
        return sum(packets)
    if operator == 1:
        return np.prod(np.array(packets))
    if operator == 2:
        return min(packets)
    if operator == 3:
        return max(packets)
    if operator == 5:
        return 1 if packets[0] > packets[1] else 0
    if operator == 6:
        return 1 if packets[0] < packets[1] else 0
    if operator == 7:
        return 1 if packets[0] == packets[1] else 0


class TestParsePackets(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ((0, [2, 3, 4, 5]), 14),
            ((0, [9]), 9),
            ((1, [2, 3, 4, 5]), 120),
            ((1, [5]), 5),
            ((2, [2, 3, 4, 5]), 2),
            ((2, [6, 5, 3, 7]), 3),
            ((2, [5]), 5),
            ((3, [2, 3, 4, 5]), 5),
            ((3, [9, 5, 3, 7]), 9),
            ((3, [5]), 5),
            ((5, [5, 3]), 1),
            ((5, [5, 5]), 0),
            ((5, [3, 5]), 0),
            ((6, [5, 3]), 0),
            ((6, [5, 5]), 0),
            ((6, [3, 5]), 1),
            ((7, [5, 3]), 0),
            ((7, [5, 5]), 1),
            ((7, [3, 5]), 0),
        ]

    def test_parse_packets(self):
        for test_case, expected_result in self.test_cases:
            actual = parse_packets(*test_case)
            self.assertEqual(actual, expected_result)

# @unittest.skip
class TestDecodeBinaryStringPart2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ("11110001010", (10, 11)),
            ("1011001101001010", (170, 16)),
            ("100100101111111000101000", (2021, 21)),
            (
                "00100000000000000110111101000101001010010001001000000000",
                # FixedLength(1, 1, 0, 27, [10, 20], 49)
                (30, 49)

            ),
            (
                "00100100000000000110111101000101001010010001001000000000",
                # FixedLength(1, 1, 0, 27, [10, 20], 49)
                (200, 49)

            ),
            (
                "00101000000000000110111101000101001010010001001000000000",
                # FixedLength(1, 2, 0, 27, [10, 20], 49)
                (10, 49)

            ),
            (
                "00101100000000000110111101000101001010010001001000000000",
                # FixedLength(1, 3, 0, 27, [10, 20], 49)
                (20, 49)
            ),
            (
                "00110100000000000110111101000101001010010001001000000000",
                # FixedLength(1, 5, 0, 27, [10, 20], 49)
                (0, 49)

            ),
            (
                "00111000000000000110111101000101001010010001001000000000",
                # FixedLength(1, 6, 0, 27, [10, 20], 49)
                (1, 49)

            ),
            (
                "00111100000000000110111101000101001010010001001000000000",
                # FixedLength(1, 7, 0, 27, [10, 20], 49)
                (0, 49)

            ),
            (
                "11101110000000001101010000001100100000100011000001100000",
                # VariableLength(7, 3, 1, 3, [1, 2, 3], 51),
                (3, 51)
            )
        ]

    def test_decode_binary_string_part_2(self):
        for test_case, expected_result in self.test_cases:
            actual = decode_binary_string_part_2(test_case)
            # print(actual, expected_result)
            self.assertEqual(actual, expected_result)


class TestDecodeHexPart2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ("C200B40A82", 3),
            ("04005AC33890", 54),
            ("880086C3E88112", 7),
            ("CE00C43D881120", 9),
            ("D8005AC2A8F0", 1),
            ("F600BC2D8F", 0),
            ("9C005AC2F8F0", 0),
            ("9C0141080250320F1802104A08", 1)
        ]

    def test_decode_hex_part_2(self):
        for test_case, expected_result in self.test_cases:
            actual = decode_hex_part_2(test_case)
            self.assertEqual(actual, expected_result)

if __name__ == "__main__":
    # print(hex_to_bin('8A004A801A8002F478'))
    # print(hex_to_bin('A0016C880162017C3686B18A3D4780'))
    transmission = read_txt_file_contents('16-bits_transmission.txt')[0]
    print(decode_hex_part_1(transmission))
    print(decode_hex_part_2(transmission))

    unittest.main()
