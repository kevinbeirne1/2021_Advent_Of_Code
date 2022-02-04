"""
--- Day 14: Extended Polymerization ---

The incredible pressures at this depth are starting to put a strain on your
submarine. The submarine has polymerization equipment that would produce
suitable materials to reinforce the submarine, and the nearby
volcanically-active caves should even have the necessary input elements in
sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer
formula; specifically, it offers a polymer template and a list of pair
insertion rules (your puzzle input). You just need to work out what polymer would
result after repeating the pair insertion process a few times.

For example:

    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C

The first line is the polymer template - this is the starting point of the
process.

The following section defines the pair insertion rules. A rule like AB -> C
means that when elements A and B are immediately adjacent, element C should be
inserted between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously
considers all three pairs:

 - The first pair (NN) matches the rule NN -> C, so element C is inserted
 between the first N and the second N.
 - The second pair (NC) matches the rule NC -> B, so element B is inserted
 between the N and the C.
 - The third pair (CB) matches the rule CB -> H, so element H is inserted
 between the C and the B.

Note that these pairs overlap: the second element of one pair is the first
element of the next pair. Also, because all pairs are considered
simultaneously, inserted elements are not considered to be part of a pair
until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

    Template:     NNCB
    After step 1: NCNBCHB
    After step 2: NBCCNBBBCBHCB
    After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
    After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

This polymer grows quickly. After step 5, it has length 97; After step 10,
it has length 3073. After step 10, B occurs 1749 times, C occurs 298 times,
H occurs 161 times, and N occurs 865 times; taking the quantity of the most
common element (B, 1749) and subtracting the quantity of the least common
element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most
and least common elements in the result. What do you get if you take the
quantity of the most common element and subtract the quantity of the least
common element?

"""
import re
import unittest
from collections import Counter, defaultdict
from helper_functions import read_txt_file_contents

class Polymer:

    def __init__(self, input_data):
        self.polymer, self.instructions = self.parse_input(input_data)

    @staticmethod
    def parse_input(input_data):
        starting_polymer = [letter for letter in input_data[0].strip()]
        polymer_map = {}
        for line in input_data[1:]:
            if line != "\n":
                first, second, value = re.findall(r'\w', line)
                polymer_map[(first, second)] = value
        return starting_polymer, polymer_map

    def polymerize(self, steps):
        for _ in range(steps):
            new_polymer = [self.polymer[0]]
            previous = self.polymer[0]
            for current in self.polymer[1:]:
                new_polymer.append(self.instructions[(previous, current)])
                new_polymer += [current]
                previous = current
            self.polymer = new_polymer
        return "".join(new_polymer)

    def polymer_counter(self):
        counted = Counter(self.polymer)
        return counted.most_common()

    def polymer_max_minus_min(self):
        counted = self.polymer_counter()
        max = counted[0][1]
        min = counted[-1][1]
        return max - min


class TestPolymer(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.parse_input_test_cases = [
            (
                [
                    'NNCB', 'CH -> B', 'HH -> N', 'CB -> H', 'NH -> C',
                    'HB -> C', 'HC -> B', 'HN -> C', 'NN -> C', 'BH -> H',
                    'NC -> B', 'NB -> B', 'BN -> B', 'BB -> N', 'BC -> B',
                    'CC -> N', 'CN -> C'
                ],
                (
                    ['N', 'N', 'C', 'B'],
                    {
                        ('C', 'H'): 'B', ('H', 'H'): 'N', ('C', 'B'): 'H',
                        ('N', 'H'): 'C', ('H', 'B'): 'C', ('H', 'C'): 'B',
                        ('H', 'N'): 'C', ('N', 'N'): 'C', ('B', 'H'): 'H',
                        ('N', 'C'): 'B', ('N', 'B'): 'B', ('B', 'N'): 'B',
                        ('B', 'B'): 'N', ('B', 'C'): 'B', ('C', 'C'): 'N',
                        ('C', 'N'): 'C',
                    }
                )
            ),
            (
                [
                    'NNCB\n', '\n', 'CH -> B\n', 'HH -> N\n', 'CB -> H\n', 'NH -> C\n',
                    'HB -> C\n', 'HC -> B\n', 'HN -> C\n', 'NN -> C\n', 'BH -> H\n',
                    'NC -> B\n', 'NB -> B\n', 'BN -> B\n', 'BB -> N\n', 'BC -> B\n',
                    'CC -> N\n', 'CN -> C'
                ],
                (
                    ['N', 'N', 'C', 'B'],
                    {
                        ('C', 'H'): 'B', ('H', 'H'): 'N', ('C', 'B'): 'H',
                        ('N', 'H'): 'C', ('H', 'B'): 'C', ('H', 'C'): 'B',
                        ('H', 'N'): 'C', ('N', 'N'): 'C', ('B', 'H'): 'H',
                        ('N', 'C'): 'B', ('N', 'B'): 'B', ('B', 'N'): 'B',
                        ('B', 'B'): 'N', ('B', 'C'): 'B', ('C', 'C'): 'N',
                        ('C', 'N'): 'C',
                    }
                )
            ),
        ]

        cls.polymer_instructions = [
            'NNCB', 'CH -> B', 'HH -> N', 'CB -> H', 'NH -> C',
            'HB -> C', 'HC -> B', 'HN -> C', 'NN -> C', 'BH -> H',
            'NC -> B', 'NB -> B', 'BN -> B', 'BB -> N', 'BC -> B',
            'CC -> N', 'CN -> C'
        ]

        cls.polymerize_test_cases = [
            (1, "NCNBCHB"),
            (2, "NBCCNBBBCBHCB"),
            (3, "NBBBCNCCNBBNBNBBCHBHHBCHB"),
            (4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"),
        ]

        cls.letter_count_test_case = [('B', 1749), ("N", 865), ("C", 298), ("H", 161)]

    def test_parse_input(self):
        for test_case, expected_result in self.parse_input_test_cases:
            with self.subTest():
                poly = Polymer(test_case)
                actual = poly.polymer, poly.instructions
                self.assertEqual(actual, expected_result)

    def test_polymerize(self):
        for steps, expected_result in self.polymerize_test_cases:
            with self.subTest():
                poly = Polymer(self.polymer_instructions)
                actual = poly.polymerize(steps)
                self.assertEqual(actual, expected_result)

    def test_letter_count(self):
        poly = Polymer(self.polymer_instructions)
        poly.polymerize(10)
        actual = poly.polymer_counter()
        expected = self.letter_count_test_case
        self.assertEqual(actual, expected)

    def test_max_minus_min(self):
        poly = Polymer(self.polymer_instructions)
        steps = [10, ]  # 40]
        expected_results = [1588, ]  # 2188189693529]
        for step, expected_result in zip(steps, expected_results):
            with self.subTest():
                poly.polymerize(step)
                actual = poly.polymer_max_minus_min()
                self.assertEqual(actual, expected_result)


"""
--- Part Two ---

The resulting polymer isn't nearly strong enough to reinforce the submarine. 
You'll need to run more steps of the pair insertion process; a total of 40 
steps should do it.

In the above example, the most common element is B (occurring 2192039569602 
times) and the least common element is H (occurring 3849876073 times); 
subtracting these produces 2188189693529.

Apply 40 steps of pair insertion to the polymer template and find the most 
and least common elements in the result. What do you get if you take the 
quantity of the most common element and subtract the quantity of the 
least common element?
"""



class PolymerVersion2:
    """
    First version was done by generating the new string each iteration.
    Was able to work for 10 iterations, but couldn't for 40 loops because
    of the exponential growth of the string.
    Got a hint from reddit that much like with the lanternfish in problem 6,
    I don't need to know exact string just a counter of the pairs
    """

    def __init__(self, input_data):
        self.polymer, self.child_dict = self.parse_input(input_data)

        self.segment_count = defaultdict(int)
        self.count_initial_segments()

    def count_initial_segments(self):
        previous = self.polymer[0]
        new_dict = defaultdict(int)
        for current in self.polymer[1:]:
            new_dict[(previous, current)] += 1
            previous = current
        self.segment_count = new_dict

    def polymerize(self, steps):
        for _ in range(steps):
            new_chain = defaultdict(int)

            queue = list(self.segment_count.keys())
            for segment in queue:
                amount = self.segment_count[segment]
                children = self.child_dict[segment]
                for child in children:
                    new_chain[child] += amount
            self.segment_count = new_chain

    @property
    def letter_count(self):
        letter_counter = defaultdict(int)
        for segment, amount in self.segment_count.items():
            letter_counter[segment[0]] += amount
        letter_counter[self.polymer[-1]] += 1
        return dict(letter_counter)

    @staticmethod
    def parse_input(input_data):
        starting_polymer = [letter for letter in input_data[0].strip()]
        polymer_map = {}
        for line in input_data[1:]:
            if line != "\n":
                first, second, value = re.findall(r'\w', line)
                polymer_map[(first, second)] = ((first, value), (value, second))
        return starting_polymer, polymer_map

    @property
    def max_minus_min(self):
        letter_counts = self.letter_count.values()
        return max(letter_counts) - min(letter_counts)

class TestPolymerVersion2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.parse_input_test_cases = [
            (
                [
                    'NNCB', 'CH -> B', 'HH -> N', 'CB -> H', 'NH -> C',
                    'HB -> C', 'HC -> B', 'HN -> C', 'NN -> C', 'BH -> H',
                    'NC -> B', 'NB -> B', 'BN -> B', 'BB -> N', 'BC -> B',
                    'CC -> N', 'CN -> C'
                ],
                (
                    ['N', 'N', 'C', 'B'],
                    {
                        ('C', 'H'): (('C', 'B'), ('B', 'H')),
                        ('H', 'H'): (('H', 'N'), ('N', 'H')),
                        ('C', 'B'): (('C', 'H'), ('H', 'B')),
                        ('N', 'H'): (('N', 'C'), ('C', 'H')),
                        ('H', 'B'): (('H', 'C'), ('C', 'B')),
                        ('H', 'C'): (('H', 'B'), ('B', 'C')),
                        ('H', 'N'): (('H', 'C'), ('C', 'N')),
                        ('N', 'N'): (('N', 'C'), ('C', 'N')),
                        ('B', 'H'): (('B', 'H'), ('H', 'H')),
                        ('N', 'C'): (('N', 'B'), ('B', 'C')),
                        ('N', 'B'): (('N', 'B'), ('B', 'B')),
                        ('B', 'N'): (('B', 'B'), ('B', 'N')),
                        ('B', 'B'): (('B', 'N'), ('N', 'B')),
                        ('B', 'C'): (('B', 'B'), ('B', 'C')),
                        ('C', 'C'): (('C', 'N'), ('N', 'C')),
                        ('C', 'N'): (('C', 'C'), ('C', 'N')),
                    }
                )
            ),
            (
                [
                    'NNCB\n', '\n', 'CH -> B\n', 'HH -> N\n', 'CB -> H\n', 'NH -> C\n',
                    'HB -> C\n', 'HC -> B\n', 'HN -> C\n', 'NN -> C\n', 'BH -> H\n',
                    'NC -> B\n', 'NB -> B\n', 'BN -> B\n', 'BB -> N\n', 'BC -> B\n',
                    'CC -> N\n', 'CN -> C'
                ],
                (
                    ['N', 'N', 'C', 'B'],
                    {
                        ('C', 'H'): (('C', 'B'), ('B', 'H')),
                        ('H', 'H'): (('H', 'N'), ('N', 'H')),
                        ('C', 'B'): (('C', 'H'), ('H', 'B')),
                        ('N', 'H'): (('N', 'C'), ('C', 'H')),
                        ('H', 'B'): (('H', 'C'), ('C', 'B')),
                        ('H', 'C'): (('H', 'B'), ('B', 'C')),
                        ('H', 'N'): (('H', 'C'), ('C', 'N')),
                        ('N', 'N'): (('N', 'C'), ('C', 'N')),
                        ('B', 'H'): (('B', 'H'), ('H', 'H')),
                        ('N', 'C'): (('N', 'B'), ('B', 'C')),
                        ('N', 'B'): (('N', 'B'), ('B', 'B')),
                        ('B', 'N'): (('B', 'B'), ('B', 'N')),
                        ('B', 'B'): (('B', 'N'), ('N', 'B')),
                        ('B', 'C'): (('B', 'B'), ('B', 'C')),
                        ('C', 'C'): (('C', 'N'), ('N', 'C')),
                        ('C', 'N'): (('C', 'C'), ('C', 'N')),
                    }
                )
            ),
        ]

        cls.polymer_instructions = [
            'NNCB', 'CH -> B', 'HH -> N', 'CB -> H', 'NH -> C',
            'HB -> C', 'HC -> B', 'HN -> C', 'NN -> C', 'BH -> H',
            'NC -> B', 'NB -> B', 'BN -> B', 'BB -> N', 'BC -> B',
            'CC -> N', 'CN -> C'
        ]

        cls.polymerize_test_cases = [
            (0, {'N': 2, 'C': 1, 'B': 1}),
            (1, {'N': 2, 'C': 2, 'B': 2, 'H': 1}),
            (2, {'B': 6, 'C': 4, 'N': 2, 'H': 1}),
            (3, {'B': 11, 'N': 5, 'C': 5, 'H': 4}),
            (4, {'B': 23, 'N': 11, 'C': 10, 'H': 5}),
        ]

        cls.letter_count_test_cases = [
            ({('N', 'N'): 1, ('N', 'C'): 1, ('C', 'B'): 1}, {'N': 2, 'C': 1, 'B': 1}),
            (
                {
                    ('N', 'C'): 1, ('C', 'N'): 1, ('N', 'B'): 1,
                    ('B', 'C'): 1, ('C', 'H'): 1, ('H', 'B'): 1
                },
                {'N': 2, 'C': 2, 'B': 2, 'H': 1}
            ),
            (
                {
                    ('N', 'B'): 2, ('B', 'C'): 2, ('C', 'C'): 1,
                    ('C', 'N'): 1, ('B', 'B'): 2, ('C', 'B'): 2,
                    ('B', 'H'): 1, ('H', 'C'): 1
                },
                {'B': 6, 'C': 4, 'N': 2, 'H': 1}),
            (
                {
                    ('N', 'B'): 4, ('B', 'B'): 4, ('B', 'C'): 3,
                    ('C', 'N'): 2, ('N', 'C'): 1, ('C', 'C'): 1,
                    ('B', 'N'): 2, ('C', 'H'): 2, ('H', 'B'): 3,
                    ('B', 'H'): 1, ('H', 'H'): 1
                },
                {'B': 11, 'N': 5, 'C': 5, 'H': 4}
            ),
            (
                {
                    ('N', 'B'): 9, ('B', 'B'): 9, ('B', 'N'): 6, ('B', 'C'): 4,
                    ('C', 'C'): 2, ('C', 'N'): 3, ('N', 'C'): 1, ('C', 'B'): 5,
                    ('B', 'H'): 3, ('H', 'C'): 3, ('H', 'H'): 1, ('H', 'N'): 1,
                    ('N', 'H'): 1
                },
                {'B': 23, 'N': 11, 'C': 10, 'H': 5}
            ),
        ]

        cls.segment_count_test_cases = [
            ("NNCB", {('N', 'N'): 1, ('N', 'C'): 1, ('C', 'B'): 1}),
            (
                "NCNBCHB",
                {
                    ('N', 'C'): 1, ('C', 'N'): 1, ('N', 'B'): 1,
                    ('B', 'C'): 1, ('C', 'H'): 1, ('H', 'B'): 1
                }
            ),
            (
                "NBCCNBBBCBHCB",
                {
                    ('N', 'B'): 2, ('B', 'C'): 2, ('C', 'C'): 1,
                    ('C', 'N'): 1, ('B', 'B'): 2, ('C', 'B'): 2,
                    ('B', 'H'): 1, ('H', 'C'): 1
                }
            ),
            (
                "NBBBCNCCNBBNBNBBCHBHHBCHB",
                {
                    ('N', 'B'): 4, ('B', 'B'): 4, ('B', 'C'): 3,
                    ('C', 'N'): 2, ('N', 'C'): 1, ('C', 'C'): 1,
                    ('B', 'N'): 2, ('C', 'H'): 2, ('H', 'B'): 3,
                    ('B', 'H'): 1, ('H', 'H'): 1}
            ),
            (
                "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB",
                {
                    ('N', 'B'): 9, ('B', 'B'): 9, ('B', 'N'): 6, ('B', 'C'): 4,
                    ('C', 'C'): 2, ('C', 'N'): 3, ('N', 'C'): 1, ('C', 'B'): 5,
                    ('B', 'H'): 3, ('H', 'C'): 3, ('H', 'H'): 1, ('H', 'N'): 1,
                    ('N', 'H'): 1
                }
            )
        ]

        cls.max_min_test_cases = [
            (0, 1),
            (1, 1),
            (2, 5),
            (3, 7),
            (4, 18),
            (10, 1588),
            (40, 2188189693529)
        ]

    def test_parse_input(self):
        for test_case, expected_result in self.parse_input_test_cases:
            with self.subTest():
                poly = PolymerVersion2(test_case)
                actual = poly.polymer, poly.child_dict
                self.assertEqual(actual, expected_result)

    def test_letter_count(self):
        for test_case, expected_result in self.letter_count_test_cases:
            with self.subTest():
                poly = PolymerVersion2(self.polymer_instructions)
                poly.segment_count = test_case
                actual = poly.letter_count
                self.assertEqual(actual, expected_result)

    def test_segment_count(self):
        for test_case, expected_result in self.segment_count_test_cases:
            with self.subTest():
                poly = PolymerVersion2(self.polymer_instructions)
                poly.polymer = test_case
                poly.count_initial_segments()
                actual = dict(poly.segment_count)
                self.assertEqual(actual, expected_result)

    def test_polymerize_letter_count(self):
        for test_case, expected_result in self.polymerize_test_cases:
            with self.subTest():
                poly = PolymerVersion2(self.polymer_instructions)
                poly.polymerize(test_case)
                actual = poly.letter_count
                self.assertEqual(actual, expected_result)

    def test_max_minus_min(self):
        for test_case, expected_result in self.max_min_test_cases:
            with self.subTest():
                poly = PolymerVersion2(self.polymer_instructions)
                poly.polymerize(test_case)
                actual = poly.max_minus_min
                self.assertEqual(actual, expected_result)


if __name__ == '__main__':
    polymer_data = read_txt_file_contents('14-polymer_map.txt')
    poly = Polymer(polymer_data)
    poly.polymerize(10)
    print(poly.polymer_max_minus_min())

    poly2 = PolymerVersion2(polymer_data)
    poly2.polymerize(40)
    print(poly2.max_minus_min)

    unittest.main()
