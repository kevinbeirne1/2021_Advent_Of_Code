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
from collections import deque
from helper_functions import read_txt_file_contents


class SmokeMap:

    def __init__(self, input_data):
        self.height_dict = {(i, j): num for i, row in enumerate(input_data) for j, num in enumerate(row) if num != '\n'}
        self.height_map = numpy.array([[int(num) for num in row if num != "\n"] for row in input_data])
        self.low_points = []

    @property
    def width(self):
        return len(self.height_map[0])

    @property
    def depth(self):
        return len(self.height_map)

    @property
    def risk_level(self):
        low_values = [self.height_map[i][j] + 1 for i, j in self.low_points]
        return sum(low_values)

    def get_low_points(self):
        for y_coord in range(self.depth):
            for x_coord in range(self.width):
                if self.check_low_point(y_coord, x_coord):
                    self.low_points.append((y_coord, x_coord))
                    # self.risk_level += self.height_map[y_coord][x_coord] + 1

    def check_low_point(self, y_coord, x_coord):
        x_low = max(x_coord - 1, 0)
        x_high = min(x_coord + 2, self.width)
        y_low = max(y_coord - 1, 0)
        y_high = min(y_coord + 2, self.depth)
        x_range = self.height_map[y_coord][x_low: x_high]
        y_range = self.height_map[y_low: y_high:, x_coord]
        x_min = min(x_range)
        y_min = min(y_range)
        pt = self.height_map[y_coord][x_coord]
        pt_count = list(x_range).count(pt) == 1 and list(y_range).count(pt) == 1
        return y_min == pt == x_min and pt_count

    def get_basin_size(self, node):
        node_queue = deque([node])
        visited = set()
        size = 0
        neighbours = self.get_neighbours(node)
        node_queue += list(neighbours - visited)
        while node_queue:
            current_node = node_queue.popleft()
            if current_node in visited:
                continue
            if self.height_dict.get(current_node) not in {'9', None}:
                neighbours = self.get_neighbours(current_node)
                for node in neighbours - visited:
                    node_queue.append(node)
                size += 1
            visited |= {current_node}
        return size

    @staticmethod
    def get_neighbours(node):
        i, j = node
        return {(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)}

    def get_largest_basins(self):
        if not self.low_points:
            self.get_low_points()
        basin_sizes = []
        for low_point in self.low_points:
            basin_sizes.append(self.get_basin_size(low_point))
        three_largest_basins = sorted(basin_sizes, reverse=True)[:3]
        return three_largest_basins[0] * three_largest_basins[1] * three_largest_basins[2]


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
            # (["818", "896", "856",], (1, 1), False),
            # (["178", "896", "876",], (0, 0), True),
            # (["0000", "0100", "0209", "4567"], (3, 3), False)
        ]

        cls.neighbours_test_cases = [
            # (["0000", "9999", "0209", "4567"], (0, 0), 4),
            (
                [
                    "2199943210",
                    "3987894921",
                    "9856789892",
                    "8767896789",
                    "9899965678"
                ], (0, 1), 3
            ),
            (
                [
                    "2199943210",
                    "3987894921",
                    "9856789892",
                    "8767896789",
                    "9899965678"
                ], (0, 9), 9
            ),
            (
                [
                    "2199943210",
                    "3987894921",
                    "9856789892",
                    "8767896789",
                    "9899965678"
                ], (2, 2), 14
            ),
            (
                [
                    "2199943210",
                    "3987894921",
                    "9856789892",
                    "8767896789",
                    "9899965678"
                ], (4, 6), 9
            ),
            (
                [
                    "9899899864598765321239999546794323489012356910136789234678999765986432109874349897678921298754345856",
                    "8798788978989899992398798932986734678943869872345679129789999843497643298765456789568910129983236745",
                    "7676567899976998789977587891297945789654699964557789298999987932599954399897897893457891239765101234",
                    "6545459789765497679765476789349657898765789985668999987899876893989876988998998932378932349874323457",
                    "6435345678987984568974345678998998999997893596779789876789765689878989877569789949989864556995434567",
                    "4323234799999876789743234789997899990199952129895698975678934599769998966445679897899876769876546789",
                    "3210125899989987897654348999876789989987641016954987654699545678958986543234598786788989895989657899",
                    "4391434989878999998776567898765434878999832345693198766789956799346995432123987655677899934598978978",
                    "5989549876567899899987898997654323459876546598789239979899897890239876543099878434566789545987899769",
                    "9878998765456789788798999998765434568997687678898945989999789994345987654987654312345689656976793244",
                    "9767989654345897652649999899876685678998798899987899995697679879959998765699873201239798769865692123"
                ], (2, 95), 58
            ),
            (
                read_txt_file_contents("09-height_map.txt"), (2, 95), 58
            )
        ]

        cls.largest_basins_test_cases = [
            (
                [
                    "2199943210",
                    "3987894921",
                    "9856789892",
                    "8767896789",
                    "9899965678"
                ], 1134
            ),
            (
                read_txt_file_contents("09-height_map.txt"), 899392
            ),
        ]

    def test_risk_level(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest():
                smoke_map = SmokeMap(test_case)
                smoke_map.get_low_points()
                actual = smoke_map.risk_level
                self.assertEqual(actual, expected_result)

    def test_check_low_point(self):
        for grid, coords, expected_result in self.low_point_test_cases:
            with self.subTest():
                smoke = SmokeMap(grid)
                actual = smoke.check_low_point(*coords)
                self.assertEqual(actual, expected_result)

    def test_get_basin_size(self):
        for grid, coords, expected_result in self.neighbours_test_cases:
            with self.subTest():
                smoke = SmokeMap(grid)
                actual = smoke.get_basin_size(coords)
                self.assertEqual(actual, expected_result)

    def test_get_largest_basins(self):
        for grid, expected_result in self.largest_basins_test_cases:
            with self.subTest():
                smoke = SmokeMap(grid)
                actual = smoke.get_largest_basins()
                self.assertEqual(actual, expected_result)

if __name__ == "__main__":
    heights = read_txt_file_contents("09-height_map.txt")
    grid = SmokeMap(heights)
    grid.get_low_points()
    print(grid.risk_level)
    print(grid.get_largest_basins())
    unittest.main()
