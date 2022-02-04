"""
--- Day 17: Trick Shot ---
You finally decode the Elves' message. HI, the message says. You continue
searching for the sleigh keys.

Ahead of you is what appears to be a large ocean trench. Could the keys have
fallen into it? You'd better send a probe to investigate.

The probe launcher on your submarine can fire the probe with any integer
velocity in the x (forward) and y (upward, or downward if negative) directions.
For example, an initial x,y velocity like 0,10 would fire the probe straight
up, while an initial velocity like 10,-1 would fire the probe forward at a
slight downward angle.

The probe's x,y position starts at 0,0. Then, it will follow some trajectory by
moving in steps. On each step, these changes occur in the following order:

    - The probe's x position increases by its x velocity.
    - The probe's y position increases by its y velocity.
    - Due to drag, the probe's x velocity changes by 1 toward the value 0; that
    is, it decreases by 1 if it is greater than 0, increases by 1 if it is
    less than 0, or does not change if it is already 0.
    - Due to gravity, the probe's y velocity decreases by 1.

For the probe to successfully make it into the trench, the probe must be on
some trajectory that causes it to be within a target area after any step. The
submarine computer has already calculated this target area (your puzzle input).

For example:

    target area: x=20..30, y=-10..-5

This target area means that you need to find initial x,y velocity values such that
after any step, the probe's x position is at least 20 and at most 30, and the
probe's y position is at least -10 and at most -5.

Given this target area, one initial velocity that causes the probe to be within
the target area after any step is 7,2:

    .............#....#............
    .......#..............#........
    ...............................
    S........................#.....
    ...............................
    ...............................
    ...........................#...
    ...............................
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTTT
    ....................TTTTTTTT#TT
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTTT

In this diagram, S is the probe's initial position, 0,0. The x coordinate
increases to the right, and the y coordinate increases upward. In the bottom
right, positions that are within the target area are shown as T. After each
step (until the target area is reached), the position of the probe is marked
with #. (The bottom-right # is both a position the probe reaches and a
position in the target area.)


Another initial velocity that causes the probe to be within the target area
after any step is 6,3:

    ...............#..#............
    ...........#........#..........
    ...............................
    ......#..............#.........
    ...............................
    ...............................
    S....................#.........
    ...............................
    ...............................
    ...............................
    .....................#.........
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTTT
    ....................T#TTTTTTTTT
    ....................TTTTTTTTTTT


Another one is 9,0:

    S........#.....................
    .................#.............
    ...............................
    ........................#......
    ...............................
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTT#
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTTT
    ....................TTTTTTTTTTT


One initial velocity that doesn't cause the probe to be within the target area
after any step is 17,-4:

    S..............................................................
    ...............................................................
    ...............................................................
    ...............................................................
    .................#.............................................
    ....................TTTTTTTTTTT................................
    ....................TTTTTTTTTTT................................
    ....................TTTTTTTTTTT................................
    ....................TTTTTTTTTTT................................
    ....................TTTTTTTTTTT..#.............................
    ....................TTTTTTTTTTT................................
    ...............................................................
    ...............................................................
    ...............................................................
    ...............................................................
    ................................................#..............
    ...............................................................
    ...............................................................
    ...............................................................
    ...............................................................
    ...............................................................
    ...............................................................
    ..............................................................#

The probe appears to pass through the target area, but is never within it after
any step. Instead, it continues down and to the right - only the first few
steps are shown.

If you're going to fire a highly scientific probe out of a super cool probe
launcher, you might as well do it with style. How high can you make the probe
go while still reaching the target area?

In the above example, using an initial velocity of 6,9 is the best you can do,
causing the probe to reach a maximum y position of 45. (Any higher initial y
velocity causes the probe to overshoot the target area entirely.)

Find the initial velocity that causes the probe to reach the highest y position
and still eventually be within the target area after any step. What is the
highest y position it reaches on this trajectory?

"""

import re
import unittest

from math import ceil, floor, sqrt


class TargetCalculation:

    def __init__(self, target_string):
        self.target_zone = self.convert_target(target_string)

    @staticmethod
    def convert_target(target_string):
        x1, x2, y1, y2 = re.findall(r'(-?\d+)', target_string)
        x_bounds = list(range(int(x1), int(x2) + 1))
        y_bounds = list(range(int(y1), int(y2) + 1))
        return x_bounds, y_bounds

    def in_target_zone(self, node):
        return node[0] in self.target_zone[0] and node[1] in self.target_zone[1]

    def get_min_x_velocity(self):
        """
        The final x position:  x * (x+1) / 2 = y
        Setting the final x position as the minimum of the target zone, can
        then reverse the equation to solve for starting x

        Using quadratic formula
        x = -b +/- sqrt(b**2 - 4ac) / 2
            a = 1
            b = 1
            c = - min(target_zone)

        Get the ceiling of the resultant to get the nearest integer value that
        will reach zone
        """
        return ceil((-1 + sqrt(1 + 4 * 2 * min(self.target_zone[0]))) / 2)

    def get_max_y_position(self):
        """
        If a positive y starting velocity (j) is used it will always intersect
        the x-axis (ie y = 0) after j steps.
        The max starting velocity will be one where the next step after
        intersecting 0 will go to the bottom of the target zone.
        So the max Y velocity will be: (target_zone_bottom - 1)

        The heighest point it reaches will be while velocity y > 0.
        So can calculate it by j * (j + 1) /2
        """
        deepest_target_zone = abs(min(self.target_zone[1]))
        max_y_velocity = deepest_target_zone - 1
        return max_y_velocity * deepest_target_zone // 2


class TestTargetCalculation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        target_zone = 'target area: x=20..30, y=-10..-5'
        cls.target_calculator = TargetCalculation(target_zone)

        cls.in_target_test_cases = [
            ((0, 0), False),
            ((20, 0), False),
            ((19, -5), False),
            ((31, -5), False),
            ((20, -4), False),
            ((20, -11), False),
            ((20, -10), True),
            ((20, -5), True),
            ((30, -10), True),
            ((30, -5), True),
            ((25, -7), True)
        ]

        cls.get_min_x_velocity_test_cases = [
            ('target area: x=20..30, y=-10..-5', 6),
            ('target area: x=40..50, y=-10..-5', 9),
            ('target area: x=130..150, y=-10..-5', 16),
            ('target area: x=241..275, y=-75..-49', 22),
        ]

        cls.max_y_position_test_cases = [
            ('target area: x=20..30, y=-10..-5', 45),
        ]

    def test_is_class_instance(self):
        actual = type(TargetCalculation)
        self.assertIsInstance(actual, type)

    def test_raises_if_target_zone_not_passed(self):
        with self.assertRaises(TypeError):
            TargetCalculation()

    def test_target_zone_conversion(self):
        actual = self.target_calculator.target_zone
        expected = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [-10, -9, -8,  -7, -6, -5]
        self.assertEqual(actual, expected)

    def test_in_target_zone(self):
        for test_case, expected_result in self.in_target_test_cases:
            actual = self.target_calculator.in_target_zone(test_case)
            self.assertEqual(actual, expected_result)

    def test_get_min_x_velocity(self):
        for test_case, expected_result in self.get_min_x_velocity_test_cases:
            target_calc = TargetCalculation(test_case)
            actual = target_calc.get_min_x_velocity()
            self.assertEqual(actual, expected_result)

    def test_get_max_y_position(self):
        for test_case, expected_result in self.max_y_position_test_cases:
            target_calc = TargetCalculation(test_case)
            actual = target_calc.get_max_y_position()
            self.assertEqual(actual, expected_result)


"""
--- Part Two ---
Maybe a fancy trick shot isn't the best idea; after all, you only have one 
probe, so you had better not miss.

To get the best idea of what your options are for launching the probe, you 
need to find every initial velocity that causes the probe to eventually be 
within the target area after any step.

In the above example, there are 112 different initial velocity values that 
meet these criteria:

    23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
    25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
    8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
    26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
    20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
    25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
    25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
    8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
    24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
    7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
    23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
    27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
    8,-2    27,-8   30,-5   24,-7
    
How many distinct initial velocity values cause the probe to be within the 
target area after any step?
"""

class TargetCalculationPart2:

    def __init__(self, target_string):
        self.target_zone = self.convert_target(target_string)
        self._pos = [0, 0]
        self._velocity = [0, 0]

    @staticmethod
    def convert_target(target_string):
        x1, x2, y1, y2 = re.findall(r'(-?\d+)', target_string)
        x_bounds = list(range(int(x1), int(x2) + 1))
        y_bounds = list(range(int(y1), int(y2) + 1))
        return x_bounds, y_bounds

    def in_target_zone(self, node):
        return node[0] in self.target_zone[0] and node[1] in self.target_zone[1]

    def get_min_x_velocity(self):
        """
        The final x position:  x * (x+1) / 2 = y
        Setting the final x position as the minimum of the target zone, can
        then reverse the equation to solve for starting x

        Using quadratic formula
        x = -b +/- sqrt(b**2 - 4ac) / 2
            a = 1
            b = 1
            c = - min(target_zone)

        Get the ceiling of the resultant to get the nearest integer value that
        will reach zone
        """
        return ceil((-1 + sqrt(1 + 4 * 2 * min(self.target_zone[0]))) / 2)

    def get_max_x_velocity(self):
        """
        The final x position:  x * (x+1) / 2 = y
        Setting the final x position as the minimum of the target zone, can
        then reverse the equation to solve for starting x

        Using quadratic formula
        x = -b +/- sqrt(b**2 - 4ac) / 2
            a = 1
            b = 1
            c = - min(target_zone)

        Get the ceiling of the resultant to get the nearest integer value that
        will reach zone
        """
        return floor((-1 + sqrt(1 + 4 * 2 * max(self.target_zone[0]))) / 2)

    def get_max_y_position(self):
        """
        If a positive y starting velocity (j) is used it will always intersect
        the x-axis (ie y = 0) after j steps.
        The max starting velocity will be one where the next step after
        intersecting 0 will go to the bottom of the target zone.
        So the max Y velocity will be: (target_zone_bottom - 1)

        The heighest point it reaches will be while velocity y > 0.
        So can calculate it by j * (j + 1) /2
        """
        deepest_target_zone = abs(min(self.target_zone[1]))
        max_y_velocity = deepest_target_zone - 1
        return max_y_velocity * deepest_target_zone // 2

    def iterate_position(self):
        x_vel, y_vel = self._velocity
        self._pos[0] +=  x_vel
        self._pos[1] += y_vel
        self._velocity[0] = max(0, x_vel - 1)
        self._velocity[1] -= 1

    def is_valid_velocity(self, starting_velocity):
        self._pos = [0, 0]
        self._velocity = [* starting_velocity]

        while self._pos[0] <= max(self.target_zone[0]) and self._pos[1] >= min(self.target_zone[1]):
            self.iterate_position()
            if self.in_target_zone(self._pos):
                return True
        return False

    def get_low_arc_velocities(self):
        total_valid = 0
        lower_x_limit = self.get_max_x_velocity() + 1
        upper_x_limit = ceil(max(self.target_zone[0]) / 2) + 1
        lower_y_limit = min(self.target_zone[1])
        upper_y_limit = self.get_max_y_position()
        for i in range(lower_x_limit, upper_x_limit):
            for j in range(lower_y_limit, upper_y_limit):
                if self.is_valid_velocity((i, j)):
                    total_valid += 1
        return  total_valid

    def get_high_arc_velocities(self):
        total_valid = 0
        upper_x_limit = self.get_max_x_velocity() + 1
        lower_x_limit = self.get_min_x_velocity()
        lower_y_limit = -20
        upper_y_limit = self.get_max_y_position()
        for i in range(lower_x_limit, upper_x_limit):
            for j in range(lower_y_limit, upper_y_limit):
                if self.is_valid_velocity((i, j)):
                    total_valid += 1
                    # print(i, j)
        return total_valid

    def single_step_velocities(self):
        return len(self.target_zone[0]) * len(self.target_zone[1])

    def total_valid_velocities(self):
        return self.get_low_arc_velocities() + self.get_high_arc_velocities() + self.single_step_velocities()

class TestAmountOfVelocities(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.high_arc_velocities_test_cases = [
            ('target area: x=20..30, y=-10..-5', 21),
        ]

        cls.first_step_velocities_test_cases = [
            ('target area: x=20..30, y=-10..-5', 66),
        ]

        cls.get_max_x_velocity_test_cases = [
            ('target area: x=20..30, y=-10..-5', 7),
            ('target area: x=40..50, y=-10..-5', 9),
            ('target area: x=130..150, y=-10..-5', 16),
            ('target area: x=241..275, y=-75..-49', 22),
        ]

        cls.low_arc_velocities_test_cases = [
            ('target area: x=20..30, y=-10..-5', 25),
        ]

        cls.total_valid_velocities = [
            ('target area: x=20..30, y=-10..-5', 112),
            ("target area: x=241..275, y=-75..-49", 1566)
        ]

        cls.target_area = 'target area: x=20..30, y=-10..-5'

        cls.iterate_position_test_cases = [
            (((8, 3), 1), [8, 3]),
            (((8, 3), 2), [15, 5]),
            (((8, 3), 3), [21, 6]),
            (((8, 3), 4), [26, 6]),
            (((8, 3), 5), [30, 5]),
            (((8, 3), 6), [33, 3]),
            (((8, 3), 7), [35, 0]),
            (((8, 3), 8), [36, -4]),
            (((1, 3), 1), [1, 3]),
            (((1, 3), 2), [1, 5]),
            (((1, 3), 5), [1, 5]),
            (((1, 3), 6), [1, 3]),

        ]

        cls.valid_velocity_test_cases = [
            ((1, 1), False),
            ((8, 1), True),
            ((8, -2), True),

        ]
    def test_get_max_x_velocity(self):
        for test_case, expected_result in self.get_max_x_velocity_test_cases:
            target_calc = TargetCalculationPart2(test_case)
            actual = target_calc.get_max_x_velocity()
            self.assertEqual(actual, expected_result)

    def test_single_step_velocities(self):
        for test_case, expected_result in self.first_step_velocities_test_cases:
            target_calc = TargetCalculationPart2(test_case)
            actual = target_calc.single_step_velocities()
            self.assertEqual(actual, expected_result)

    def test_high_arc_velocities(self):
        for test_case, expected_result in self.high_arc_velocities_test_cases:
            target_calc = TargetCalculationPart2(test_case)
            actual = target_calc.get_high_arc_velocities()
            self.assertEqual(actual, expected_result)

    def test_iterate_position(self):
        target_calc = TargetCalculationPart2(self.target_area)
        for test_case, expected_result in self.iterate_position_test_cases:
            velocity, steps = test_case
            target_calc._velocity = [*velocity]
            target_calc._pos = [0, 0]
            for _ in range(steps):
                target_calc.iterate_position()
            actual = target_calc._pos
            self.assertEqual(actual, expected_result)

    def test_is_valid_velocity(self):
        target_calc = TargetCalculationPart2(self.target_area)
        for test_case, expected_result in self.valid_velocity_test_cases:
            actual = target_calc.is_valid_velocity(test_case)
            self.assertEqual(actual, expected_result)

    def test_inbetween_velocities(self):
        target_calc = TargetCalculationPart2(self.target_area)
        for test_case, expected_result in self.low_arc_velocities_test_cases:
            actual = target_calc.get_low_arc_velocities()
            self.assertEqual(actual, expected_result)

    def test_total_valid_velocities(self):
        for test_case, expected_result in self.total_valid_velocities:
            target_calc = TargetCalculationPart2(test_case)

            actual = target_calc.total_valid_velocities()
            self.assertEqual(actual, expected_result)


if __name__=="__main__":
    target_area = "target area: x=241..275, y=-75..-49"
    target_calc = TargetCalculation(target_area)
    print(target_calc.get_max_y_position())
    target_calc_part_2 = TargetCalculationPart2(target_area)
    # print(target_calc_part_2.inbetween_velocities())

    unittest.main()