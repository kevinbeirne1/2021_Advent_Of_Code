"""
--- Day 4: Giant Squid ---

You're already almost 1.5km (almost a mile) below the surface of the ocean,
already so deep that you can't see any sunlight. What you can see, however,
is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards
on which it appears. (Numbers may not appear on all boards.) If all numbers
in any row or any column of a board are marked, that board wins. (Diagonals
don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the
giant squid) pass the time. It automatically generates a random order in which
to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners,
but the boards are marked as follows (shown here adjacent to each other to save space):

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

Finally, 24 is drawn:

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

At this point, the third board wins because it has at least one complete row or column of marked
numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked
numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that
was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will
your final score be if you choose that board?

"""
from helper_functions import read_txt_file_contents
import unittest
from collections import defaultdict
import re


def calculate_bingo_winner(input_data):
    """
    Brute Force Method
    Loop through the numbers
    Loop through the boards
    Check if any board has won
    If won => sum the remaining
    return the sum * the winning number
    """
    drawn_numbers, boards, board_sums, board_dicts = \
        generate_boards_and_numbers_from_input(input_data)

    for drawn_number in drawn_numbers:
        for i, board in enumerate(boards):
            if index := board_dicts[i].get(drawn_number):
                board[index[0]][index[1]] = -1
                board_sums[i] -= drawn_number
                if board_wins(board):
                    return drawn_number * board_sums[i]


def board_wins(board):
    """
    Check if a row or column in a board sums to -5
    return true if it does or false otherwise
    """
    transposed_board = zip(*board)
    return any(True for row in board if sum(row) == -5) or \
        any(True for row in transposed_board if sum(row) == -5)


def split_list_and_convert_to_int(number_string):
    "Convert a string to a list of numbers"
    split_number_string = re.findall(r'(\d+)', number_string)
    return [int(number) for number in split_number_string]


def create_board_dictionary(board):
    "Create a dictionary for each board of its numbers and their indices"
    board_dict = defaultdict(int)
    for i, row in enumerate(board):
        for j, number in enumerate(row):
            board_dict[number] = [i, j]
    return board_dict


def calculate_board_sum(board):
    """Create a variable that holds the sum of the numbers in a board"""
    return sum(sum(row) for row in board)


def generate_boards_and_numbers_from_input(input_data):
    """
    Take the string of data from the txt file and convert to
    a list of board arrays, and a numbers drawn list
    """
    drawn_numbers = split_list_and_convert_to_int(input_data[0])
    boards = []
    board_sums = []
    board_dicts = []
    for i, num_list in enumerate(input_data[1::6]):
        board = [split_list_and_convert_to_int(row) for row in input_data[i*6 + 2: i*6 + 7]]
        boards.append(board)
        board_sums.append(calculate_board_sum(board))
        board_dicts.append(create_board_dictionary(board))

    return drawn_numbers, boards, board_sums, board_dicts


"""
--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant 
squid win.

You aren't sure how many bingo boards a giant squid could play at once, so 
rather than waste time counting its arms, the safe thing to do is to figure out 
which board will win last and choose that one. That way, no matter which boards 
it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 
is eventually called and its middle column is completely marked. If you were to 
keep playing until this point, the second board would have a sum of unmarked 
numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?

"""


def calculate_bingo_winner_part_2(input_data):
    """
    Brute Force Method
    Loop through the numbers
    Loop through the boards
    Check if any board has won
    If won => sum the remaining
    return the sum * the winning number
    """
    drawn_numbers, boards, board_sums, board_dicts = \
        generate_boards_and_numbers_from_input(input_data)
    last_winner = 0
    winning_boards = defaultdict(int)

    for drawn_number in drawn_numbers:
        for i, board in enumerate(boards):
            if index := board_dicts[i].get(drawn_number):

                if not winning_boards[i]:
                    board[index[0]][index[1]] = -1
                    board_sums[i] -= drawn_number
                    if board_wins(board):
                        winning_boards[i] = True
                        last_winner = drawn_number * board_sums[i]
    return last_winner


class TestCalculateBingoWinner(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ([
                "7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1",
                "\n",
                "22 13 17 11  0",
                "8  2 23  4 24",
                "21  9 14 16  7",
                "6 10  3 18  5",
                "1 12 20 15 19",
                "\n",
                "3 15  0  2 22",
                "9 18 13 17  5",
                "19  8  7 25 23",
                "20 11 10 24  4",
                "14 21 16 12  6",
                "\n",
                "14 21 17 24  4",
                "10 16 15  9 19",
                "18  8 23 26 20",
                "22 11 13  6  5",
                "2  0 12  3  7",
            ], 4512)
        ]

    def test_calculate_bingo_winner(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest():
                actual = calculate_bingo_winner(test_case)
                self.assertEqual(actual, expected_result)


class TestCalculateBingoWinnerPart2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ([
                "7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1",
                "\n",
                "22 13 17 11  0",
                "8  2 23  4 24",
                "21  9 14 16  7",
                "6 10  3 18  5",
                "1 12 20 15 19",
                "\n",
                "3 15  0  2 22",
                "9 18 13 17  5",
                "19  8  7 25 23",
                "20 11 10 24  4",
                "14 21 16 12  6",
                "\n",
                "14 21 17 24  4",
                "10 16 15  9 19",
                "18  8 23 26 20",
                "22 11 13  6  5",
                "2  0 12  3  7",
            ], 1924)
        ]

    def test_calculate_bingo_winner(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest():
                actual = calculate_bingo_winner_part_2(test_case)
                self.assertEqual(actual, expected_result)


class TestGenerateBoardsAndNumbersFromInput(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (
                [
                    "42, 32, 13, 22, 91, 2\n",
                    "\n",
                    "90  8  2 34 41\n",
                    "11 67 74 71 62\n",
                    "47 42 44  1 17\n",
                    "21 55 12 91  6\n",
                    "60 69 75 92 56\n",
                    "\n",
                    '49 29 60 45 31\n',
                    '94 51 73 33 67\n',
                    '21 92 53 95 96\n',
                    ' 2 55 52  8 87\n',
                    ' 4 36 76 83 42\n'
                ],
                ([42, 32, 13, 22, 91, 2],
                    [
                        [
                            [90, 8, 2, 34, 41],
                            [11, 67, 74, 71, 62],
                            [47, 42, 44, 1, 17],
                            [21, 55, 12, 91, 6],
                            [60, 69, 75, 92, 56],
                        ],
                        [
                            [49, 29, 60, 45, 31],
                            [94, 51, 73, 33, 67],
                            [21, 92, 53, 95, 96],
                            [2, 55, 52, 8, 87],
                            [4, 36, 76, 83, 42]
                        ]
                    ],
                    [1148, 1334],
                    [
                    {90: [0, 0], 8: [0, 1], 2: [0, 2], 34: [0, 3], 41: [0, 4], 11: [1, 0], 67: [1, 1], 74: [1, 2],
                     71: [1, 3], 62: [1, 4], 47: [2, 0], 42: [2, 1], 44: [2, 2], 1: [2, 3], 17: [2, 4], 21: [3, 0],
                     55: [3, 1], 12: [3, 2], 91: [3, 3], 6: [3, 4], 60: [4, 0], 69: [4, 1], 75: [4, 2], 92: [4, 3],
                     56: [4, 4]},
                     {49: [0, 0], 29: [0, 1], 60: [0, 2], 45: [0, 3], 31: [0, 4], 94: [1, 0], 51: [1, 1], 73: [1, 2],
                      33: [1, 3], 67: [1, 4], 21: [2, 0], 92: [2, 1], 53: [2, 2], 95: [2, 3], 96: [2, 4], 2: [3, 0],
                      55: [3, 1], 52: [3, 2], 8: [3, 3], 87: [3, 4], 4: [4, 0], 36: [4, 1], 76: [4, 2], 83: [4, 3],
                      42: [4, 4]},

                    ]
                )
            )
        ]

    def test_generate_boards_and_numbers_from_input(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest():
                actual = generate_boards_and_numbers_from_input(test_case)
                self.assertEqual(actual, expected_result)


class TestBoardWins(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ([
                [-1, -1, -1, -1, -1],
                [11, 67, 74, 71, 62],
                [47, 42, 44, 1, 17],
                [21, 55, 12, 91, 6],
                [60, 69, 75, 92, 56],
            ], True),
            ([
                 [11, 67, 74, 71, 62],
                 [11, 67, 74, 71, 62],
                 [47, 42, 44, 1, 17],
                 [21, 55, 12, 91, 6],
                 [60, 69, 75, 92, 56],
             ], False),
            ([
                [-1, 8, 2, 34, 41],
                [-1, 67, 74, 71, 62],
                [-1, 42, 44, 1, 17],
                [-1, 55, 12, 91, 6],
                [-1, 69, 75, 92, 56],
            ], True),
            ([
                 [11, 67, 74, 71, 62],
                 [47, 42, 44, 1, 17],
                 [-1, -1, -1, -1, -1],
                 [21, 55, 12, 91, 6],
                 [60, 69, 75, 92, 56],
             ], True),
            ([
                 [1, -1, 8, 2, 34],
                 [1, -1, 67, 74, 71],
                 [1, -1, 42, 44, 1],
                 [1, -1, 55, 12, 91],
                 [1, -1, 69, 75, 92],
             ], True),
        ]

    def test_check_board_wins(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest():
                actual = board_wins(test_case)
                self.assertEqual(actual, expected_result)





if __name__ == "__main__":
    bingo_data = read_txt_file_contents("04-bingo_results.txt")
    print(calculate_bingo_winner(bingo_data))
    print(calculate_bingo_winner_part_2(bingo_data))
    unittest.main()

test = read_txt_file_contents("04-bingo_results.txt")
print(*generate_boards_and_numbers_from_input(test[:72]), sep='\n')
