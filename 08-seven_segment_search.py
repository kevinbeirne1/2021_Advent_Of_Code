"""--- Day 8: Seven Segment Search ---

You barely reach the safety of the cave when the whale smashes into the cave
mouth, collapsing it. Sensors indicate another exit to this cave at a much
greater depth, so you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice
that the four-digit seven-segment displays in your submarine are
malfunctioning; they must have been damaged during the escape. You'll be in a
lot of trouble without them, so you'd better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of
seven segments named a through g:

      0:      1:      2:      3:      4:
     aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
     ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
     gggg    ....    gggg    gggg    ....

       5:      6:      7:      8:      9:
      aaaa    aaaa    aaaa    aaaa    aaaa
     b    .  b    .  .    c  b    c  b    c
     b    .  b    .  .    c  b    c  b    c
      dddd    dddd    ....    dddd    dddd
     .    f  e    f  .    f  e    f  .    f
     .    f  e    f  .    f  e    f  .    f
      gggg    gggg    ....    gggg    gggg

So, to render a 1, only segments c and f would be turned on; the rest would be
off. To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up
on each display. The submarine is still trying to display numbers by producing
output on signal wires a through g, but those wires are connected to segments
randomly. Worse, the wire/segment connections are mixed up separately for each
four-digit display! (All of the digits within a display use the same
connections, though.)

So, you might know that only signal wires b and g are turned on, but that
doesn't mean segments b and g are turned on: the only digit that uses two
segments is 1, so it must mean segments c and f are meant to be on. With just
that information, you still can't tell which wire (b/g) goes to which segment
(c/f). For that, you'll need to collect more information.

For each display, you watch the changing signals for a while, make a note of
all ten unique signal patterns you see, and then write down a single four digit
output value (your puzzle input). Using the signal patterns, you should be
able to work out which pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf

(The entry is wrapped here to two lines so it fits; in your notes, it will all
be on a single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally
the four digit output value. Within an entry, the same wire/segment
connections are used (but you don't know what the connections actually are).
The unique signal patterns correspond to the ten different ways the submarine
tries to render a digit using the current wire/segment connections. Because 7
is the only digit that uses three segments, dab in the above example means
that to render a 7, signal lines d, a, and b are on. Because 4 is the only
digit that uses four segments, eafb means that to render a 4, signal lines e,
a, f, and b are on.

Using this information, you should be able to work out which combination of
signal wires corresponds to each of the ten digits. Then, you can decode the
four digit output value. Unfortunately, in the above example, all of the
digits in the output value (cdfeb fcadb cdfeb cdbaf) use five segments and
are more difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

    be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
    fdgacbe cefdb cefbgd gcbe
    edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
    fcgedb cgb dgebacf gc
    fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
    cg cg fdcagb cbg
    fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
    efabcd cedba gadfec cb
    aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
    gecf egdcabf bgf bfgea
    fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
    gebdcfa ecba ca fadegcb
    dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
    cefg dcbef fcge gbcadfe
    bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
    ed bcgafe cdgba cbgef e
    gadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
    gbdfcae bgc cg cgb
    gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
    fgae cfgab fg bagce

Because the digits 1, 4, 7, and 8 each use a unique number of segments, you
should be able to tell which combinations of signals correspond to those
digits. Counting only digits in the output values (the part after | on each
line), in the above example, there are 26 instances of digits that use a
unique number of segments (highlighted above).

"""
from collections import Counter

from helper_functions import read_txt_file_contents
import unittest
import re


def display_wiring(input_data):
    # displays = {0: 6, 1: 2, 2: 5, 3: 5, 4: 4, 5: 5, 6: 6, 7: 3, 8: 7, 9: 6}
    # display_list = [6, 2, 5, 5, 5, 5, 6, 3, 7, 6]
    no_of_digits = 0
    for line in input_data:
        output = re.findall(r'(\w+)', line)[-4:]
        no_of_digits += len([digit for digit in output if len(digit) in [2, 3, 4, 7]])
    return no_of_digits


"""
--- Part Two ---
Through a little deduction, you should now be able to determine the remaining 
digits. Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf

After some careful analysis, the mapping between signal wires and segments 
only make sense in the following configuration:

     dddd
    e    a
    e    a
     ffff
    g    b
    g    b
     cccc
     
So, the unique signal patterns would correspond to the following digits:

    acedgfb: 8
    cdfbe: 5
    gcdfa: 2
    fbcad: 3
    dab: 7
    cefabd: 9
    cdfgeb: 6
    eafb: 4
    cagedb: 0
    ab: 1
    
Then, the four digits of the output value can be decoded:

    cdfeb: 5
    fcadb: 3
    cdfeb: 5
    cdbaf: 3
    
Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, 
the output value of each entry can be determined:

    fdgacbe cefdb cefbgd gcbe: 8394
    fcgedb cgb dgebacf gc: 9781
    cg cg fdcagb cbg: 1197
    efabcd cedba gadfec cb: 9361
    gecf egdcabf bgf bfgea: 4873
    gebdcfa ecba ca fadegcb: 8418
    cefg dcbef fcge gbcadfe: 4548
    ed bcgafe cdgba cbgef: 1625
    gbdfcae bgc cg cgb: 8717
    fgae cfgab fg bagce: 4315
    
Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the 
four-digit output values. What do you get if you add up all of the output 
values?
"""


class Wiring:

    word_lengths = {2: 1, 4: 4, 3: 7, 7: 8}

    def __init__(self, input_data):
        self.input_data = re.findall(r'(\w+)', input_data)
        self.display_digits = [set()] * 10
        self.codeword_output = [False] * 14

    def assign_digit(self, word, digit, word_index):
        self.display_digits[digit] = word
        self.codeword_output[word_index] = digit

    def decode_word(self):
        for _ in range(2):
            for i, codeword in enumerate(self.input_data):
                set_word, len_word = set(codeword), len(codeword)
                if len_word in [2, 3, 4, 7]:
                    digit = self.word_lengths[len_word]
                    self.assign_digit(set_word, digit, i)
                elif len_word == 6:
                    if self.display_digits[4] and not self.display_digits[4] - set_word:
                        self.assign_digit(set_word, 9, i)
                    elif self.display_digits[7] and not self.display_digits[7] - set_word:
                        self.assign_digit(set_word, 0, i)
                    elif self.display_digits[7] and self.display_digits[4]:
                        self.assign_digit(set_word, 6, i)

                elif len_word == 5:
                    if self.display_digits[1] and not self.display_digits[1] - set_word:
                        self.assign_digit(set_word, 3, i)
                    elif self.display_digits[1] and self.display_digits[4] and not (self.display_digits[4] - self.display_digits[1]) - set_word:
                        self.assign_digit(set_word, 5, i)
                    elif self.display_digits[1] and self.display_digits[9]:
                        self.assign_digit(set_word, 2, i)
        return self.concatenate_number

    @property
    def concatenate_number(self):
        last_four_digits = self.codeword_output[-4:][::-1]
        return sum([num * 10 ** i for i, num in zip(range(4), last_four_digits)])


def display_wiring_part_2(input_data):
    sum_of_digits = 0
    # digits = []
    for line in input_data:
        parsed_line = Wiring(line)
        digit = parsed_line.decode_word()
        sum_of_digits += digit
    return sum_of_digits


def display_wiring_alternate_part_2(input_data):
    """
    Saw on reddit. If assign each segment a value based on how many times it's
    used when doing all digits 0-9. Then assign each digit a number equal to
    the sum of each segment value in it

    segment_values:

             top - 8
    tl - 6            tr - 8
             mid - 7
    bl - 4            br - 9
             bot - 7

    Digit_values:
    0 - 42, 1 - 17, 2 - 34, 3 - 39, 4 - 30,
    5 - 37, 6 - 41, 7 - 25, 8 - 49, 9 - 45

    The first 10 words supplied correspond to digits 0-9, so if do a Counter
    on those. Iterating through the output words can then get a value for each
    word and use that to decode it
    """
    digit_map = {42: '0', 17: '1', 34: '2', 39: '3', 30: '4', 37: '5', 41: '6', 25: '7', 49: '8', 45: '9'}
    decoded_outputs = []
    for line in input_data:
        codewords, output = line.split("|")
        raw_output = re.findall(r'(\w+)', output)
        decoded_output = ""
        segment_counter = Counter(codewords)
        for word in raw_output:
            word_value = sum((segment_counter[letter] for letter in word))
            decoded_output += digit_map[word_value]
        decoded_outputs.append(int(decoded_output))
    return sum(decoded_outputs)


class TestDisplayWiring(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (["be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",], 2),
            (["edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",], 3),
            (["fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",], 3),
            (["fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",], 1),
            (["aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",], 3),
            (["fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",], 4),
            (["dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",], 3),
            (["bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",], 1),
            (["egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",], 4),
            (["gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",], 2),
            ([
                 "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
                 "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
                 "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
                 "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
                 "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
                 "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
                 "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
                 "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
                 "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
                 "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
             ], 26),
        ]

    def test_display_wiring(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest(f"test case - {test_case}"):
                actual = display_wiring(test_case)
                self.assertEqual(actual, expected_result)


class TestDisplayWiringPart2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        be      1
        cfbegad 8
        cbdgef  9
        fgaecd
        cgeb    4
        fdcge
        agebfd
        fecdb   3
        fabcd
        edb     7
        fdgacbe 8
        cefdb   3
        cefbgd  9
        gcbe    4

         dddd
             be
       gc    be
         gc--
             be
             be

        """


        cls.test_cases = [
            (["cfe dgebc bfcage fbeag efgcb eafcbdg gfedba faecdg cbaf fc | cfe ebgaf cbfa cbgfade"], 7548),
            (["abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg | cf abcefg acdeg acdfg"], 1023),
            (["abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg | cf abcefg abcefg abcefg"], 1000),
            (["abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg | abcefg abcefg abcefg fc"], 1),

            (["abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg | cf abcefg acdeg acdfg"], 1023),
            (["be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",], 8394),
            (["edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",], 9781),
            (["fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",], 1197),
            (["fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",], 9361),
            (["aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",], 4873),
            (["fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",], 8418),
            (["dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",], 4548),
            (["bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",], 1625),
            (["egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",], 8717),
            (["gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",], 4315),
            ([
                 "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
                 "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
                 "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
                 "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
                 "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
                 "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
                 "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
                 "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
                 "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
                 "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
             ], 61229),
        ]
        cls.functions_to_test = [
            display_wiring_part_2,
            display_wiring_alternate_part_2,
        ]

    def test_display_wiring(self):
        for test_case, expected_result in self.test_cases:
            for function_to_test in self.functions_to_test:
                with self.subTest(f"test case - {test_case}"):
                    actual = function_to_test(test_case)
                    self.assertEqual(actual, expected_result)


if __name__ == "__main__":
    wiring_info = read_txt_file_contents("08-display_wiring.txt")
    """
    errors at
    expected actual index 
    7548 7048 23
    8082 8080 35
    2587 87 93
    4151 4101 104
    7247 7047 155
    5762 760 158
    
    """
    print(wiring_info[23])
    print(display_wiring(wiring_info))
    print(display_wiring_part_2(wiring_info))
    print(display_wiring_alternate_part_2(wiring_info))
    unittest.main()
