"""
--- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically active;
small hydrothermal vents release smoke into the caves that slowly settles
like rain.

If you can model how the smoke flows through the caves, you might be able to
avoid it and be that much safer. The submarine generates a heightmap of the
floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the
following heightmap:

    2199943210
    3987894921
    9856789892
    8767896789
    9899965678

Each number corresponds to the height of a particular location, where 9 is the
highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than
any of its adjacent locations. Most locations have four adjacent locations
(up, down, left, and right); locations on the edge or corner of the map have
three or two adjacent locations, respectively. (Diagonal locations do not count
as adjacent.)

In the above example, there are four low points, all highlighted: two are in
the first row (a 1 and a 0), one is in the third row (a 5), and one is in the
bottom row (also a 5). All other locations on the heightmap have some lower
adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the
risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels
of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk
levels of all low points on your heightmap?

"""

import unittest
import numpy
from helper_functions import read_txt_file_contents


class SmokeMap:

    def __init__(self, input_data):
        self.heights = numpy.array([[int(num) for num in row if num != "\n"] for row in input_data])
        self.risk_level = 0

    @property
    def width(self):
        return len(self.heights[0])

    @property
    def depth(self):
        return len(self.heights)

    def check_risk(self):
        for y_coord in range(self.depth):
        # for y_coord in range(2, 3):
            for x_coord in range(self.width):
            # for x_coord in range(2, 3):
                if self.check_low_point(y_coord, x_coord):
                    # print(y_coord, x_coord)
                    self.risk_level += self.heights[y_coord][x_coord] + 1

    def check_low_point(self, y_coord, x_coord):
        x_low = max(x_coord - 1, 0)
        x_high = min(x_coord + 2, self.width)
        y_low = max(y_coord - 1, 0)
        y_high = min(y_coord + 2, self.depth)
        x_range = self.heights[y_coord][x_low: x_high]
        y_range = self.heights[y_low: y_high:, x_coord]
        x_min = min(x_range)
        y_min = min(y_range)
        pt = self.heights[y_coord][x_coord]
        pt_count = list(x_range).count(pt) == 1 and list(y_range).count(pt) == 1
        # print(y_min == self.heights[y_coord][x_coord] == x_min)
        return y_min == pt == x_min and pt_count
        pass


class TestRiskLevels(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (
                [
                    "2199943210",
                    "3987894921",
                    "9856789892",
                    "8767896789",
                    "9899965678"
                ], 15
            ),
            (["219",
              "398",
              "985"], 8),
            (["878",
              "856",
              "876",], 6),
            (["828", "856", "876",], 3),
        ]

        cls.low_point_test_cases = [
            (["878", "856", "876",], (1, 1), True),
            (["818", "896", "856",], (1, 1), False),
            (["178", "896", "876",], (0, 0), True),
            (["0000", "0100", "0209", "4567"], (3, 3), False)
        ]

    def test_risk_level(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest():
                process = SmokeMap(test_case)
                process.check_risk()
                actual = process.risk_level
                # print(*actual, sep="\n")
                self.assertEqual(actual, expected_result)

    @unittest.skip
    def test_check_low_point(self):
        for grid, coords, expected_result in self.low_point_test_cases:
            with self.subTest():
                smoke = SmokeMap(grid)
                # print(smoke.heights[:, 1])
                actual = smoke.check_low_point(*coords)
                self.assertEqual(actual, expected_result)

if __name__ == "__main__":
    heights = read_txt_file_contents("09-height_map.txt")
    grid = SmokeMap(heights)
    grid.check_risk()
    print(grid.risk_level)
    unittest.main()
