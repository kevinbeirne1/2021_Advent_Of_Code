"""
--- Day 2: Dive! ---
Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1,
down 2, or up 3:

    forward X increases the horizontal position by X units.
    down X increases the depth by X units.
    up X decreases the depth by X units.

Note that since you're on a submarine, down and up affect your depth, and so
they have the opposite result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You
should probably figure out where it's going. For example:

    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2

Your horizontal position and depth both start at 0. The steps above would then
modify them as follows:

    forward 5 adds 5 to your horizontal position, a total of 5.
    down 5 adds 5 to your depth, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13.
    up 3 decreases your depth by 3, resulting in a value of 2.
    down 8 adds 8 to your depth, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15.

After following these instructions, you would have a horizontal position of 15
and a depth of 10. (Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the
planned course. What do you get if you multiply your final horizontal position
by your final depth?
"""

from helper_functions import read_txt_file_contents
import unittest
import re


def calculate_submarine_instructions(instruction_list):
    """
    depth, horizontal_pos = 0, 0
    Iterate through the list
    regex to separate the word and number
    if forward => horiz += number
    if down => depth += number
    if up => depth -= number
    """
    depth = 0
    horizontal_position = 0
    for instruction in instruction_list:
        direction, amount = re.match(r"(\w+)\s(\d+)", instruction).groups()
        amount = int(amount)
        if direction == "up":
            depth -= amount
        elif direction == "down":
            depth += amount
        else:
            horizontal_position += amount
    return depth * horizontal_position


"""
--- Part Two ---
Based on your calculations, the planned course doesn't seem to make any sense. 
You find the submarine manual and discover that the process is actually 
slightly more complicated.

In addition to horizontal position and depth, you'll also need to track a third 
value, aim, which also starts at 0. The commands also mean something entirely 
different than you first thought:

    down X increases your aim by X units.
    up X decreases your aim by X units.
    forward X does two things:
    It increases your horizontal position by X units.
    It increases your depth by your aim multiplied by X.
    
Again note that since you're on a submarine, down and up do the opposite of 
what you might expect: "down" means aiming in the positive direction.

Now, the above example does something different:

    - forward 5 adds 5 to your horizontal position, a total of 5. Because your 
      aim is 0, your depth does not change.
    - down 5 adds 5 to your aim, resulting in a value of 5.
    - forward 8 adds 8 to your horizontal position, a total of 13. Because your 
      aim is 5, your depth increases by 8*5=40.
    - up 3 decreases your aim by 3, resulting in a value of 2.
    - down 8 adds 8 to your aim, resulting in a value of 10.
    - forward 2 adds 2 to your horizontal position, a total of 15. Because your 
      aim is 10, your depth increases by 2*10=20 to a total of 60.
      
After following these new instructions, you would have a horizontal position of 
15 and a depth of 60. (Multiplying these produces 900.)

Using this new interpretation of the commands, calculate the horizontal position 
and depth you would have after following the planned course. What do you get if 
you multiply your final horizontal position by your final depth?
"""


def calculate_submarine_instructions_part2(instruction_list):
    """
    depth, horizontal_pos, aim = 0, 0, 0
    Iterate through the list
    regex to separate the word and number
    if forward =>
        horiz += number
        depth += number * aim
    if down => aim += number
    if up => aim -= number
    """
    depth = 0
    horizontal_position = 0
    aim = 0
    for instruction in instruction_list:
        direction, amount = re.match(r"(\w+)\s(\d+)", instruction).groups()
        amount = int(amount)
        if direction == "up":
            aim -= amount
        elif direction == "down":
            aim += amount
        else:
            horizontal_position += amount
            depth += aim * amount
    return depth * horizontal_position


class TestCalculateSubmarineInstructions(unittest.TestCase):

    def test_returns_integer(self):
        actual = calculate_submarine_instructions([])
        self.assertIsInstance(actual, int)

    def test_is_able_to_interpret_up(self):
        instructions = ['up 6', 'forward 1']
        actual = calculate_submarine_instructions(instructions)
        self.assertEqual(actual, -6)

    def test_is_able_to_interpret_down(self):
        instructions = ['down 6', 'forward 1']
        actual = calculate_submarine_instructions(instructions)
        self.assertEqual(actual, 6)

    def test_is_able_to_interpret_forward(self):
        instructions= ['forward 6', 'down 1']
        actual = calculate_submarine_instructions(instructions)
        self.assertEqual(actual, 6)

    def test_multiple_ups(self):
        instructions = ['up 6', 'up 5', 'up 4', 'forward 1']
        actual = calculate_submarine_instructions(instructions)
        self.assertEqual(actual, -15)

    def test_multiple_downs(self):
        instructions = ['down 6', 'down 5', 'down 4', 'forward 1']
        actual = calculate_submarine_instructions(instructions)
        self.assertEqual(actual, 15)

    def test_multiple_forwards(self):
        instructions = ['forward 6', 'forward 5', 'forward 4', 'down 1']
        actual = calculate_submarine_instructions(instructions)
        self.assertEqual(actual, 15)

    def test_combined_instructions(self):
        instructions = [
            'forward 5',
            'down 5',
            'forward 8',
            'up 3',
            'down 8',
            'forward 2',
        ]
        actual = calculate_submarine_instructions(instructions)
        self.assertEqual(actual, 150)


class TestCalculateSubmarineInstructionsPart2(unittest.TestCase):

    def test_combined_instructions(self):
        instructions = [
            'forward 5',
            'down 5',
            'forward 8',
            'up 3',
            'down 8',
            'forward 2',
        ]
        actual = calculate_submarine_instructions_part2(instructions)
        self.assertEqual(actual, 900)


if __name__ == "__main__":
    direction_data = read_txt_file_contents("02-directions.txt")
    print(calculate_submarine_instructions(direction_data))
    print(calculate_submarine_instructions_part2(direction_data))
    unittest.main()
