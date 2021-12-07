"""
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents
constantly produce large, opaque clouds, so it would be best to avoid them if
possible.

They tend to form in lines; the submarine helpfully produces a list of nearby
lines of vents (your puzzle input) for you to review. For example:

    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2
where x1,y1 are the coordinates of one end the line segment and x2,y2 are
the coordinates of the other end. These line segments include the points at
both ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either
x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce
the following diagram:

    .......1..
    ..1....1..
    ..1....1..
    .......1..
    .112111211
    ..........
    ..........
    ..........
    ..........
    222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9.
Each position is shown as the number of lines which cover that point or . if no
line covers that point. The top-left pair of 1s, for example, comes from
2,2 ->2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9
and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points
where at least two lines overlap. In the above example, this is anywhere in the
diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two
lines overlap?
"""
import re
import unittest
from helper_functions import read_txt_file_contents


class VentMapper:
    def __init__(self):
        self.dangerous_nodes = 0
        graph_size = 1000
        self.vent_graph = [[0 for _ in range(graph_size)] for _ in range(graph_size)]

    @staticmethod
    def parse_vent_vector(vent_vector):
        """Take a string of numbers and output a corresponding list of numbers"""
        split_vent_vector = re.findall(r'(\d+)', vent_vector)
        return [int(num) for num in split_vent_vector]

    def add_multiple_vents(self, vent_vectors_list):
        for raw_vent_vector in vent_vectors_list:
            vent_vector = self.parse_vent_vector(raw_vent_vector)
            self.add_single_vent(*vent_vector)

    def add_single_vent(self, x_1, y_1, x_2, y_2):
        if x_1 < x_2:
            x_coords = range(x_1, x_2 + 1)
        elif x_2 < x_1:
            x_coords = reversed(range(x_2, x_1 + 1))
        else:
            x_coords = [x_1] * (abs(y_1 - y_2) + 1)

        if y_1 < y_2:
            y_coords = range(y_1, y_2 + 1)
        elif y_2 < y_1:
            y_coords = reversed(range(y_2, y_1 + 1))
        else:
            y_coords = [y_1] * (abs(x_1 - x_2) + 1)

        for i, j in zip(x_coords, y_coords):
            self.update_single_node(i, j)

    def update_single_node(self, x_index, y_index):
        self.vent_graph[x_index][y_index] += 1
        if self.vent_graph[x_index][y_index] == 2:
            self.dangerous_nodes += 1

    def __str__(self):
        stringified_graph = '\n'.join([str(row) for row in self.vent_graph])
        return f"{stringified_graph}"

"""
--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you
the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in 
your list will only ever be horizontal, vertical, or a diagonal line at
exactly 45 degrees. In other words:

    An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
    
Considering all lines from the above example would now produce the following diagram:

    1.1....11.
    .111...2..
    ..2.1.111.
    ...1.2.2..
    .112313211
    ...1.2....
    ..1...1...
    .1.....1..
    1.......1.
    222111....
    
You still need to determine the number of points where at least two lines overlap. 
In the above example, this is still anywhere in the diagram with a 2 or larger - 
now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""


class TestVentMapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (
                [
                    '0, 9 -> 5, 9',
                    '8, 0 -> 0, 8',
                    '9, 4 -> 3, 4',
                    '2, 2 -> 2, 1',
                    '7, 0 -> 7, 4',
                    '6, 4 -> 2, 0',
                    '0, 9 -> 2, 9',
                    '3, 4 -> 1, 4',
                    '0, 0 -> 8, 8',
                    '5, 5 -> 8, 2',
                ], 12),
        ]

    def setUp(self) -> None:
        self.vent_graph = VentMapper()

    def test_calculate_dangerous_vent_positions(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest():
                self.vent_graph.add_multiple_vents(test_case)
                actual = self.vent_graph.dangerous_nodes
                self.assertEqual(actual, expected_result)


if __name__ == "__main__":
    vent_data = read_txt_file_contents("05-vent_lines.txt")
    vent_map = VentMapper()
    vent_map.add_multiple_vents(vent_data)
    print(vent_map.dangerous_nodes)
    unittest.main()
