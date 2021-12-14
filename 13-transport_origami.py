"""
--- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave. It would be nice if you
could do some kind of thermal imaging so you could tell ahead of time which
caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you
activate it, you are greeted with:

    Congratulations on your purchase! To activate this infrared thermal imaging
    camera system, please enter the code found on page 1 of the manual.

Apparently, the Elves have never used this feature. To your surprise, you
manage to find the manual; as you go to open it, page 1 falls out. It's a
large sheet of transparent paper! The transparent paper is marked with
random dots and includes instructions on how to fold it up (your puzzle
input). For example:

    6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents
the top-left coordinate. The first value, x, increases to the right. The
second value, y, increases downward. So, the coordinate 3,0 is to the right
of 0,0, and the coordinate 0,7 is below 0,0. The coordinates in this example
form the following pattern, where # is a dot on the paper and . is an empty,
unmarked position:

    ...#..#..#.
    ....#......
    ...........
    #..........
    ...#....#.#
    ...........
    ...........
    ...........
    ...........
    ...........
    .#....#.##.
    ....#......
    ......#...#
    #..........
    #.#........

Then, there is a list of fold instructions. Each instruction indicates a line
on the transparent paper and wants you to fold the paper up (for horizontal
y=... lines) or left (for vertical x=... lines). In this example, the first
fold instruction is fold along y=7, which designates the line formed by all
of the positions where y is 7 (marked here with -):

    ...#..#..#.
    ....#......
    ...........
    #..........
    ...#....#.#
    ...........
    ...........
    -----------
    ...........
    ...........
    .#....#.##.
    ....#......
    ......#...#
    #..........
    #.#........

Because this is a horizontal line, fold the bottom half up. Some of the dots
might end up overlapping after the fold is complete, but dots will never
appear exactly on a fold line. The result of doing this fold looks like this:

    #.##..#..#.
    #...#......
    ......#...#
    #...#......
    .#.#..#.###
    ...........
    ...........

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the
transparent paper is folded; after the fold is complete, those dots appear
in the top left corner (at 0,0 and 0,1). Because the paper is transparent,
the dot just below them in the result (at 0,3) remains visible, as it can
be seen through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots
merge together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

    #.##.|#..#.
    #...#|.....
    .....|#...#
    #...#|.....
    .#.#.|#.###
    .....|.....
    .....|.....

Because this is a vertical line, fold left:

    #####
    #...#
    #...#
    #...#
    #####
    .....
    .....

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the
first fold. After the first fold in the example above, 17 dots are visible -
dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on
your transparent paper?
"""
import unittest
import re
from helper_functions import read_txt_file_contents


def perform_multiple_folds(grid, fold_instructions):
    folded_grid = grid
    for fold in fold_instructions:
        folded_grid = perform_single_fold(folded_grid, fold)
    return folded_grid


def perform_single_fold(grid, fold_instruction):
    if fold_instruction[0] == 'y':
        return fold_along_y(grid, fold_instruction[1])
    else:
        return fold_along_x(grid, fold_instruction[1])


def fold_along_y(grid, fold_line):
    new_grid = set()
    for node in grid:
        x, y = node
        if int(y) < int(fold_line):
            new_grid.add(node)
        elif int(y) > int(fold_line):
            new_grid.add((x, str(int(fold_line)*2 - int(y))))
    return new_grid


def print_grid(grid):
    output = [[" " for _ in range(50)] for _ in range(7)]

    for point in grid:
        x, y = point
        output[int(y)][int(x)] = "#"
    output = ["".join(row) for row in output]
    print(*output, sep="\n")


def fold_along_x(grid, fold_line):
    new_grid = set()
    for node in grid:
        x, y = node
        if int(x) < int(fold_line):
            new_grid.add(node)
        elif int(x) > int(fold_line):
            new_grid.add((str(int(fold_line)*2 - int(x)), y))
    return new_grid


def parse_input(input_data):
    points, folds = [], []
    for line in input_data:
        point = re.findall(r'^(\d+),(\d+)', line)
        fold = re.findall(r'([xy])=(\d+)', line)
        points += point if point else []
        folds += fold if fold else []
    return points, folds


class TestGenerateGrid(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.parse_input_test_cases = [
            (
                [
                    "6,10", "0,14", "9,10", "0,3", "10,4", "4,11", "6,0", 
                    "6,12", "4,1", "0,13", "10,12", "3,4", "3,0", "8,4", 
                    "1,10", "2,14", "8,10", "9,0", "fold along y=7",
                    "fold along x=5"
                ],
                (
                    [
                        ('6', '10'), ('0', '14'), ('9', '10'), ('0', '3'),
                        ('10', '4'), ('4', '11'), ('6', '0'), ('6', '12'),
                        ('4', '1'), ('0', '13'), ('10', '12'), ('3', '4'),
                        ('3', '0'), ('8', '4'), ('1', '10'), ('2', '14'),
                        ('8', '10'), ('9', '0')
                    ],
                    [('y', '7'), ('x', '5')]
                )
            ),
            (
                [
                    "6,10\n", "0,14\n", "9,10\n", "0,3\n", "10,4\n", "4,11\n", "6,0\n",
                    "6,12\n", "4,1\n", "0,13\n", "10,12\n", "3,4\n", "3,0\n", "8,4\n",
                    "1,10\n", "2,14\n", "8,10\n", "9,0\n", "\n", "fold along y=7\n",
                    "fold along x=5"
                ],
                (
                    [
                        ('6', '10'), ('0', '14'), ('9', '10'), ('0', '3'),
                        ('10', '4'), ('4', '11'), ('6', '0'), ('6', '12'),
                        ('4', '1'), ('0', '13'), ('10', '12'), ('3', '4'),
                        ('3', '0'), ('8', '4'), ('1', '10'), ('2', '14'),
                        ('8', '10'), ('9', '0')
                    ],
                    [('y', '7'), ('x', '5')]
                )
                # [
                #     "...#..#..#.",
                #     "....#......",
                #     "...........",
                #     "#..........",
                #     "...#....#.#",
                #     "...........",
                #     "...........",
                #     "...........",
                #     "...........",
                #     "...........",
                #     ".#....#.##.",
                #     "....#......",
                #     "......#...#",
                #     "#..........",
                #     "#.#........"
                # ]
            ),
        ]

        cls.fold_y_test_cases = [
            (
                [
                    ('6', '10'), ('0', '14'), ('9', '10'), ('0', '3'),
                    ('10', '4'), ('4', '11'), ('6', '0'), ('6', '12'),
                    ('4', '1'), ('0', '13'), ('10', '12'), ('3', '4'),
                    ('3', '0'), ('8', '4'), ('1', '10'), ('2', '14'),
                    ('8', '10'), ('9', '0')
                ],
                ('y', 7),
                {('0', '0'), ('2', '0'), ('3', '0'), ('6', '0'), ('9', '0'),
                 ('0', '1'), ('4', '1'), ('6', '2'), ('10', '2'), ('0', '3'),
                 ('4', '3'), ('1', '4'), ('3', '4'), ('6', '4'), ('8', '4'),
                 ('9', '4'), ('10', '4')}
            )
        ]

        cls.fold_x_test_cases = [
            (
                {
                     ('0', '0'), ('2', '0'), ('3', '0'), ('6', '0'), ('9', '0'),
                     ('0', '1'), ('4', '1'), ('6', '2'), ('10', '2'), ('0', '3'),
                     ('4', '3'), ('1', '4'), ('3', '4'), ('6', '4'), ('8', '4'),
                     ('9', '4'), ('10', '4')
                },
                ('x', 5),
                {
                    ('0', '0'), ('0', '1'), ('0', '2'), ('0', '3'), ('0', '4'),
                    ('4', '0'), ('4', '1'), ('4', '2'), ('4', '3'), ('4', '4'),
                    ('1', '0'), ('2', '0'), ('3', '0'),
                    ('1', '4'), ('2', '4'), ('3', '4')
                }
            )
        ]

        cls.multiple_folds_test_cases = [
            (
                [
                    ('6', '10'), ('0', '14'), ('9', '10'), ('0', '3'),
                    ('10', '4'), ('4', '11'), ('6', '0'), ('6', '12'),
                    ('4', '1'), ('0', '13'), ('10', '12'), ('3', '4'),
                    ('3', '0'), ('8', '4'), ('1', '10'), ('2', '14'),
                    ('8', '10'), ('9', '0')
                ],
                [('y', 7), ('x', 5)],
                {
                    ('0', '0'), ('0', '1'), ('0', '2'), ('0', '3'), ('0', '4'),
                    ('4', '0'), ('4', '1'), ('4', '2'), ('4', '3'), ('4', '4'),
                    ('1', '0'), ('2', '0'), ('3', '0'),
                    ('1', '4'), ('2', '4'), ('3', '4')
                }
            )
        ]

    def test_parse_input(self):
        for test_case, expected_result in self.parse_input_test_cases:
            with self.subTest():
                actual = parse_input(test_case)
                self.assertEqual(actual, expected_result)

    def test_y_fold(self):
        for grid, fold, expected_result in self.fold_y_test_cases:
            with self.subTest():
                actual = perform_single_fold(grid, fold)
                self.assertEqual(actual, expected_result)

    def test_x_fold(self):
        for grid, fold, expected_result in self.fold_x_test_cases:
            with self.subTest():
                actual = perform_single_fold(grid, fold)
                self.assertEqual(actual, expected_result)

    def test_multiple_folds(self):
        for grid, folds, expected_result in self.multiple_folds_test_cases:
            actual = perform_multiple_folds(grid, folds)
            self.assertEqual(actual, expected_result)


if __name__ == "__main__":
    fold_data = read_txt_file_contents("13-fold_instructions.txt")
    points, folds = parse_input(fold_data)
    first_fold = folds[0]
    print(len(perform_single_fold(points, first_fold)))
    final_grid = perform_multiple_folds(points, folds)
    print_grid(final_grid)

    unittest.main()