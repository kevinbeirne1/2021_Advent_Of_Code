"""

--- Day 3: Binary Diagnostic ---
The submarine has been making some odd creaking noises, so you ask it to
produce a diagnostic report just in case.

The diagnostic report (your puzzle input) consists of a list of binary numbers
which, when decoded properly, can tell you many useful things about the
conditions of the submarine. The first parameter to check is the power
consumption.

You need to use the binary numbers in the diagnostic report to generate two new
binary numbers (called the gamma rate and the epsilon rate). The power
consumption can then be found by multiplying the gamma rate by the epsilon
rate.

Each bit in the gamma rate can be determined by finding the most common bit in
the corresponding position of all numbers in the diagnostic report. For
example, given the following diagnostic report:

    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010

Considering only the first bit of each number, there are five 0 bits and seven
1 bits. Since the most common bit is 1, the first bit of the gamma rate is 1.

The most common second bit of the numbers in the diagnostic report is 0, so the
second bit of the gamma rate is 0.

The most common value of the third, fourth, and fifth bits are 1, 1, and 0,
respectively, and so the final three bits of the gamma rate are 110.

So, the gamma rate is the binary number 10110, or 22 in decimal.

The epsilon rate is calculated in a similar way; rather than use the most
common bit, the least common bit from each position is used. So, the epsilon
rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the epsilon
rate (9) produces the power consumption, 198.

Use the binary numbers in your diagnostic report to calculate the gamma rate
and epsilon rate, then multiply them together. What is the power consumption of
the submarine? (Be sure to represent your answer in decimal, not binary.)

"""

import unittest
from collections import defaultdict
from helper_functions import read_txt_file_contents


def most_common_bit(numbers_list):
    """
    create a dictionary of bit_index: count_of_1_bit
    iterate through the list
    iterate through the bit
    if bit == 1 => dict[bit_index] += 1
    iterate through the dictionary:
    if bit_count > len(array // 2)
    """
    bit_index_count = defaultdict(int)
    for binary_number in numbers_list:
        for i, bit in enumerate(binary_number):
            bit_index_count[i] += 1 if bit == "1" else 0
    binary_number_length = len(numbers_list[-1]) if numbers_list != [] else 0
    numbers_list_length = len(numbers_list)
    gamma = [
        "1" if bit_index_count[i] > numbers_list_length // 2 else "0"
        for i in range(binary_number_length)
    ]
    epsilon = [
        "0" if bit_index_count[i] > numbers_list_length // 2 else "1"
        for i in range(binary_number_length)
    ]

    gamma = "".join(gamma)
    epsilon = "".join(epsilon)
    return int(gamma, 2) * int(epsilon, 2)


"""
--- Part 2 ---
Next, you should verify the life support rating, which can be determined by 
multiplying the oxygen generator rating by the CO2 scrubber rating.

Both the oxygen generator rating and the CO2 scrubber rating are values that 
can be found in your diagnostic report - finding them is the tricky part. 
Both values are located using a similar process that involves filtering out 
values until only one remains. Before searching for either rating value, start 
with the full list of binary numbers from your diagnostic report and consider 
just the first bit of those numbers. Then:

Keep only numbers selected by the bit criteria for the type of rating value for 
which you are searching. Discard numbers which do not match the bit criteria.
If you only have one number left, stop; this is the rating value for which you 
are searching.

Otherwise, repeat the process, considering the next bit to the right.
The bit criteria depends on which type of rating value you want to find:

To find oxygen generator rating, determine the most common value (0 or 1) in 
the current bit position, and keep only numbers with that bit in that position.
If 0 and 1 are equally common, keep values with a 1 in the position being 
considered.

To find CO2 scrubber rating, determine the least common value (0 or 1) in the 
current bit position, and keep only numbers with that bit in that position. If
0 and 1 are equally common, keep values with a 0 in the position being 
considered.

For example, to determine the oxygen generator rating value using the same 
example diagnostic report from above:

- Start with all 12 numbers and consider only the first bit of each number. 
    - There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers 
    with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, 
    and 11001.
- Then, consider the second bit of the 7 remaining numbers: 
    - There are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers 
    with a 0 in the second position: 10110, 10111, 10101, and 10000.
- In the third position, 
    - three of the four numbers have a 1, so keep those three: 10110, 
    10111, and 10101.
- In the fourth position, two of the three numbers have a 1, so keep those 
two: 10110 and 10111.
- In the fifth position, there are an equal number of 0 bits and 1 bits (one 
each). So, to find the oxygen generator rating, keep the number with a 1 in 
that position: 10111.
As there is only one number left, stop; the oxygen generator rating is 10111, 
or 23 in decimal.

Then, to determine the CO2 scrubber rating value from the same example above:

Start again with all 12 numbers and consider only the first bit of each number. 
There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0
in the first position: 00100, 01111, 00111, 00010, and 01010.

Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits 
(2) than 0 bits (3), so keep only the 2 numbers with a 1 in the second position: 
01111 and 01010.
In the third position, there are an equal number of 0 bits and 1 bits (one each). 
So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 
01010.
As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 
in decimal.
Finally, to find the life support rating, multiply the oxygen generator rating 
(23) by the CO2 scrubber rating (10) to get 230.

Use the binary numbers in your diagnostic report to calculate the oxygen 
generator rating and CO2 scrubber rating, then multiply them together. What is 
the life support rating of the submarine? (Be sure to represent your answer in 
decimal, not binary.)
"""


def most_common_bit_part2(numbers_list):
    """
    create a dictionary of bit_index: count_of_1_bit
    iterate through the list
    iterate through the bit
    if bit == 1 => dict[bit_index] += 1
    iterate through the dictionary:
    if bit_count > len(array // 2)
    """
    oxygen_list, carbon_list = numbers_list, numbers_list
    for i in range(len(numbers_list[0].strip())):
        carbon_list = filter_carbon(carbon_list, i)
        oxygen_list = filter_oxygen(oxygen_list, i)
    return int(oxygen_list[0], 2) * int(carbon_list[0], 2)


def filter_oxygen(numbers_list, bit_index):
    most_bit = single_most_common_bit_calculator(numbers_list, bit_index)
    oxygen_filter = [num for num in numbers_list if num[bit_index] == most_bit]
    return oxygen_filter


def filter_carbon(numbers_list, bit_index):
    most_bit = single_most_common_bit_calculator(numbers_list, bit_index)
    carbon_filter = [num for num in numbers_list if num[bit_index] != most_bit]
    return carbon_filter if carbon_filter else numbers_list


def single_most_common_bit_calculator(numbers_list, bit_index):
    """
    create a dictionary of bit_index: count_of_1_bit
    iterate through the list
    iterate through the bit
    if bit == 1 => dict[bit_index] += 1
    iterate through the dictionary:
    if bit_count > len(array // 2)
    """
    bit_index_count = 0
    for binary_number in numbers_list:
        bit_index_count += 1 if binary_number[bit_index] == "1" else 0
    most_bit = "1" if bit_index_count * 2 >= len(numbers_list) else "0"
    return most_bit


class TestMostCommonBit(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (["10"], 2),
            (["10", "01", "00"], 0),
            (["10", "01", "11"], 0),
            (["10", "10", "10"], 2),
            (
                [
                    "00100",
                    "11110",
                    "10110",
                    "10111",
                    "10101",
                    "01111",
                    "00111",
                    "11100",
                    "10000",
                    "11001",
                    "00010",
                    "01010",
                ],
                198,
            ),
            (
                [
                    "011001101000\n",
                    "010101111100\n",
                    "000000111101\n",
                    "001001001010\n",
                    "010011000001",
                ],
                3346776,
            ),
        ]

    def test_most_common_bit(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest(f"test case: {test_case}"):
                actual = most_common_bit(test_case)
                self.assertEqual(actual, expected_result)


class TestMostCommonBitPart2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (
                [
                    "00100",
                    "11110",
                    "10110",
                    "10111",
                    "10101",
                    "01111",
                    "00111",
                    "11100",
                    "10000",
                    "11001",
                    "00010",
                    "01010",
                ],
                230,
            ),
            (
                [
                    "011001101000\n",
                    "010101111100\n",
                    "010011000001",
                    "000000111101\n",
                    "001001001010\n",

                ],
                85644

            )
        ]

    def test_most_common_bit_part_2(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest(f"test case: {test_case}"):
                actual = most_common_bit_part2(test_case)
                self.assertEqual(actual, expected_result)


class TestFilterOxygen(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (
                ([
                    "00100",
                    "11110",
                    "10110",
                    "10111",
                    "10101",
                    "01111",
                    "00111",
                    "11100",
                    "10000",
                    "11001",
                    "00010",
                    "01010",
                ], 0),
                ["11110", "10110", "10111", "10101", "11100", "10000", "11001"],

            ),
            (
                (["11110", "10110", "10111", "10101", "11100", "10000", "11001"], 1),
                ["10110", "10111", "10101", "10000"]
            ),
            (
                (["10110", "10111", "10101", "10000"], 2),
                ["10110", "10111", "10101"]
            ),
            (
                (["10110", "10111", "10101"], 3),
                ["10110", "10111"]
            ),
            (
                (["10110", "10111", ], 4),
                ["10111", ]
            ),
            (
                (["10111", ], 4),
                ["10111", ]
            ),
        ]

    def test_filter_oxygen(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest(f"test case: {test_case}"):
                actual = filter_oxygen(*test_case)
                self.assertEqual(actual, expected_result)


class TestFilterCarbon(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (
                ([
                    "00100",
                    "11110",
                    "10110",
                    "10111",
                    "10101",
                    "01111",
                    "00111",
                    "11100",
                    "10000",
                    "11001",
                    "00010",
                    "01010",
                ], 0),
                ["00100", "01111", "00111", "00010", "01010"],

            ),
            (
                (["00100", "01111", "00111", "00010", "01010"], 1),
                ["01111", "01010"]
            ),
            (
                (["01111", "01010"], 2),
                ["01010", ]
            ),
            (
                (["01010", ], 3),
                ["01010", ]
            ),
            (
                (["01010", ], 4),
                ["01010", ]
            ),
        ]

    def test_filter_carbon(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest(f"test case: {test_case}"):
                actual = filter_carbon(*test_case)
                self.assertEqual(actual, expected_result)


if __name__ == "__main__":
    diagnostic_data = read_txt_file_contents("03-diagnostic_data.txt")
    print(most_common_bit(diagnostic_data))
    print(most_common_bit_part2(diagnostic_data))
    unittest.main()
