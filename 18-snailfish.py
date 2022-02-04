"""
--- Day 18: Snailfish ---
You descend into the ocean trench and encounter some snailfish. They say they
saw the sleigh keys! They'll even tell you which direction the keys went if
you help one of the smaller snailfish with his math homework.

Snailfish numbers aren't like regular numbers. Instead, every snailfish number
is a pair - an ordered list of two elements. Each element of the pair can be
either a regular number or another pair.

Pairs are written as [x,y], where x and y are the elements within the pair.
Here are some example snailfish numbers, one snailfish number per line:

    [1,2]
    [[1,2],3]
    [9,[8,7]]
    [[1,9],[8,5]]
    [[[[1,2],[3,4]],[[5,6],[7,8]]],9]
    [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
    [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]

This snailfish homework is about addition. To add two snailfish numbers, form a
pair from the left and right parameters of the addition operator. For example,
[1,2] + [[3,4],5] becomes [[1,2],[[3,4],5]].

There's only one problem: snailfish numbers must always be reduced, and the
process of adding two snailfish numbers can result in snailfish numbers that
need to be reduced.

To reduce a snailfish number, you must repeatedly do the first action in this
list that applies to the snailfish number:

    - If any pair is nested inside four pairs, the leftmost such pair explodes.
    - If any regular number is 10 or greater, the leftmost such regular number
      splits.

Once no action in the above list applies, the snailfish number is reduced.

During reduction, at most one action applies, after which the process returns
to the top of the list of actions. For example, if split produces a pair that
meets the explode criteria, that pair explodes before other splits occur.

To explode a pair, the pair's left value is added to the first regular number
to the left of the exploding pair (if any), and the pair's right value is added
to the first regular number to the right of the exploding pair (if any).
Exploding pairs will always consist of two regular numbers. Then, the entire
exploding pair is replaced with the regular number 0.

Here are some examples of a single explode action:

    - [[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4] (the 9 has no regular
    number to its left, so it is not added to any regular number).
    - [7,[6,[5,[4,[3,2]]]]] becomes [7,[6,[5,[7,0]]]] (the 2 has no regular
    number to its right, and so it is not added to any regular number).
    - [[6,[5,[4,[3,2]]]],1] becomes [[6,[5,[7,0]]],3].
    - [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]] becomes
    [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] (the pair [3,2] is unaffected because the
    pair [7,3] is further to the left; [3,2] would explode on the next action).
    - [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]] becomes [[3,[2,[8,0]]],[9,[5,[7,0]]]].

To split a regular number, replace it with a pair; the left element of the pair
should be the regular number divided by two and rounded down, while the right
element of the pair should be the regular number divided by two and rounded up.
For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.

Here is the process of finding the reduced result of
[[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]:

    - after addition: [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
    - after explode:  [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
    - after explode:  [[[[0,7],4],[15,[0,13]]],[1,1]]
    - after split:    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
    - after split:    [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
    - after explode:  [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

Once no reduce actions apply, the snailfish number that remains is the actual
result of the addition operation: [[[[0,7],4],[[7,8],[6,0]]],[8,1]].

The homework assignment involves adding up a list of snailfish numbers (your
puzzle input). The snailfish numbers are each listed on a separate line. Add
the first snailfish number and the second, then add that result and the third,
then add that result and the fourth, and so on until all numbers in the list
have been used once.

For example, the final sum of this list is [[[[1,1],[2,2]],[3,3]],[4,4]]:

    [1,1]
    [2,2]
    [3,3]
    [4,4]
The final sum of this list is [[[[3,0],[5,3]],[4,4]],[5,5]]:

    [1,1]
    [2,2]
    [3,3]
    [4,4]
    [5,5]
The final sum of this list is [[[[5,0],[7,4]],[5,5]],[6,6]]:

    [1,1]
    [2,2]
    [3,3]
    [4,4]
    [5,5]
    [6,6]

Here's a slightly larger example:

    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    [7,[5,[[3,8],[1,4]]]]
    [[2,[2,2]],[8,[8,1]]]
    [2,9]
    [1,[[[9,3],9],[[9,0],[0,7]]]]
    [[[5,[7,4]],7],1]
    [[[[4,2],2],6],[8,7]]

The final sum [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] is found
after adding up the above snailfish numbers:

      [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
    + [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    = [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]

      [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]
    + [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
    = [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]

      [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
    + [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
    = [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]

      [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]
    + [7,[5,[[3,8],[1,4]]]]
    = [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]

      [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]
    + [[2,[2,2]],[8,[8,1]]]
    = [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]

      [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]
    + [2,9]
    = [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]

      [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]
    + [1,[[[9,3],9],[[9,0],[0,7]]]]
    = [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]

      [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]
    + [[[5,[7,4]],7],1]
    = [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]

      [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]
    + [[[[4,2],2],6],[8,7]]
    = [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

To check whether it's the right answer, the snailfish teacher only checks the
magnitude of the final sum. The magnitude of a pair is 3 times the magnitude of
its left element plus 2 times the magnitude of its right element. The magnitude
of a regular number is just that number.

For example, the magnitude of [9,1] is 3*9 + 2*1 = 29; the magnitude of
[1,9] is 3*1 + 2*9 = 21. Magnitude calculations are recursive: the magnitude of
[[9,1],[1,9]] is 3*29 + 2*21 = 129.

Here are a few more magnitude examples:

    [[1,2],[[3,4],5]] becomes 143.
    [[[[0,7],4],[[7,8],[6,0]]],[8,1]] becomes 1384.
    [[[[1,1],[2,2]],[3,3]],[4,4]] becomes 445.
    [[[[3,0],[5,3]],[4,4]],[5,5]] becomes 791.
    [[[[5,0],[7,4]],[5,5]],[6,6]] becomes 1137.
    [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] becomes 3488.

So, given this example homework assignment:

    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]

The final sum is:

    [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]

The magnitude of this final sum is 4140.

Add up all of the snailfish numbers from the homework assignment in the order
they appear. What is the magnitude of the final sum?

"""

import  unittest
from math import ceil, floor

from helper_functions import read_txt_file_contents

class Node:

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.parent = None

        if isinstance(self.left, Node):
            self.left.parent = self
        if isinstance(self.right, Node):
            self.right.parent = self

    def __str__(self):
        return f'[{self.left},{self.right}]'

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        left_string = repr(self.left) if isinstance(self.left, Node) else self.left
        right_string = repr(self.right) if isinstance(self.right, Node) else self.right
        return f'Node({left_string}, {right_string})'

    def is_leaf(self):
        return not (isinstance(self.left, Node) or isinstance(self.right, Node))


class Snailfish:

    def __init__(self, snail_string):
        self.pairs = self.snail_string_to_node(snail_string)

    def __str__(self):
        return f"{self.pairs}"

    @staticmethod
    def snail_string_to_node(input_string):
        snail_string = input_string.replace ('[', 'Node(')
        snail_string = snail_string.replace(']', ')')
        return eval(snail_string)

    def explode(self, current_node=None, depth=None):
        if not current_node:
            current_node = self.pairs
            depth = 0
        depth = depth + 1

        if isinstance(current_node.left, Node):
            if not current_node.left.is_leaf():
                self.explode(current_node.left, depth)
            if current_node.left.is_leaf() and depth >= 4:
                self.update_nearest_left_adjacent(current_node.left)
                self.update_nearest_right_adjacent(current_node.left)
                current_node.left = 0
                # print(f'exploded - {self}')

        if isinstance(current_node.right, Node):
            if not current_node.right.is_leaf():
                self.explode(current_node.right, depth)
            if current_node.right.is_leaf() and depth >= 4:
                self.update_nearest_left_adjacent(current_node.right)
                self.update_nearest_right_adjacent(current_node.right)

                current_node.right = 0
                # print(f'exploded - {self}')

    def split(self, current_node=None, already_split=False):
        if not current_node:
            current_node = self.pairs
        if already_split:
            return True

        if isinstance(current_node.left, int) and not already_split:
            if (old_left := current_node.left) > 9:
                new_left = floor(old_left / 2)
                new_right = ceil(old_left / 2)
                current_node.left = Node(new_left, new_right)
                current_node.left.parent = current_node
                # print(f'split - {self}')

                return True
        else:
            already_split = self.split(current_node.left, already_split)


        if isinstance(current_node.right, int) and not already_split:
            if (old_right := current_node.right) > 9:
                new_left = floor(old_right / 2)
                new_right = ceil(old_right / 2)
                current_node.right = Node(new_left, new_right)
                current_node.right.parent = current_node
                # print(f'split - {self}')

                return True

        else:
            already_split = self.split(current_node.right, already_split)
        return already_split


    @staticmethod
    def update_nearest_left_adjacent(node):
        parent = node.parent
        current_node = node
        while parent.left is current_node:
            if parent.parent == None:
                return None
            current_node, parent = parent, parent.parent

        left_node = parent.left
        if isinstance(left_node, int):
            parent.left += node.left
            return parent.left

        while not isinstance(left_node.right, int):
            left_node = left_node.right

        left_node.right += node.left
        return left_node.right

    @staticmethod
    def update_nearest_right_adjacent(node):
        parent = node.parent
        current_node = node
        while parent.right is current_node:
            if parent.parent == None:
                return None

            current_node, parent = parent, parent.parent
        right_node = parent.right
        if isinstance(right_node, int):
            parent.right += node.right
            return parent.right

        while not isinstance(right_node.left, int):
            right_node = right_node.left

        right_node.left += node.right
        return right_node.left

    def reduce_snail(self):
        # old_self = str(self)
        old_self = None
        self.explode()
        while old_self != str(self):
            old_self = str(self)
            self.split()
            self.explode()
            # old_self = s
        # for _ in range(64):
        #     self.split()
        #     self.explode()

    def __add__(self, other):
        other_snail = Snailfish(other)
        self.pairs = Node(self.pairs, other_snail.pairs)
        self.reduce_snail()
        return str(self.pairs)

    def magnitude(self, current_node=None):
        if current_node == None:
            current_node = self.pairs
        if isinstance(current_node, int):
            return current_node
        left = self.magnitude(current_node.left) * 3
        right = self.magnitude(current_node.right) * 2
        return left + right


def parse_snail_list(snail_list):
    main_snail = Snailfish(snail_list[0])
    for snail in snail_list[1:]:
        main_snail.__add__(snail)
    return main_snail.magnitude()

def parse_snail_list_part_2(snail_list):
    largest_magnitude = 0
    for i, snail in enumerate(snail_list):
        for comparision_snail in snail_list[i + 1:]:
            normal = parse_snail_list([snail, comparision_snail])
            largest_magnitude = normal if normal > largest_magnitude else largest_magnitude
            reverse = parse_snail_list([comparision_snail, snail])
            largest_magnitude = reverse if reverse > largest_magnitude else largest_magnitude
    return largest_magnitude


class TestNode(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.is_leaf_test_cases = [
            (Node(1, 2), True),
            (Node(1, Node(1, 2)), False),
            (Node(Node(1,2), Node(3, 4)), False),
            (Node(1, Node(3, 4)), False),
            # (None, False)

        ]

        cls.str_test_cases = [
            (Node(1, 2), '[1,2]'),
            (Node(Node(1, 2), 3), '[[1,2],3]'),
            (Node(Node(1, 9), Node(8, 5)), '[[1,9],[8,5]]'),
            (
                Node(Node(Node(Node(1, 2), Node(3, 4)), Node(Node(5, 6), Node(7, 8))), 9),
                '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]'),
        ]

        cls.repr_test_cases = [
            (Node(1, 2), 'Node(1, 2)'),
            (Node(Node(1, 2), 3), 'Node(Node(1, 2), 3)'),
            (Node(Node(1, 9), Node(8, 5)), 'Node(Node(1, 9), Node(8, 5))'),
        ]

        cls.eq_test_cases = [
            (Node(1, 5), Node(1, 5)),
            (
                Node(Node(Node(1, 2), Node(3, 4)), Node(Node(5, 6), Node(7, 8))),
                Node(Node(Node(1, 2), Node(3, 4)), Node(Node(5, 6), Node(7, 8))),
            )
        ]

        cls.neq_test_cases = [
            (Node(1, 5), Node(2, 5)),
            (Node(1, 5), Node(2, Node(3, 4))),
        ]

    def test_node_is_class(self):
        self.assertIsInstance(Node, type)

    def test_node_creation_assigns_left_property(self):
        node = Node(1, 5)
        actual = node.left
        self.assertEqual(actual, 1)

    def test_node_creation_assigns_right_property(self):
        node = Node(1, 5)
        actual = node.right
        self.assertEqual(actual, 5)

    def test_raises_if_no_parameters_passed(self):
        with self.assertRaises(TypeError):
            Node()

    def test_raises_without_left_parameter_passed(self):
        with self.assertRaises(TypeError):
            Node(right=2)

    def test_raises_without_right_parameter_passed(self):
        with self.assertRaises(TypeError):
            Node(left=2)

    def test_str(self):
        for test_case, expected_result in self.str_test_cases:
            actual = str(test_case)
            self.assertEqual(actual, expected_result)

    def test_repr(self):
        for test_case, expected_result in self.repr_test_cases:
            actual = repr(test_case)
            self.assertEqual(actual, expected_result)

    def test_eq(self):
        for test_case, expected_result in self.eq_test_cases:
            self.assertEqual(test_case, expected_result)

    def test_neq(self):
        for test_case, expected_result in self.neq_test_cases:
            self.assertNotEqual(test_case, expected_result)

    def test_is_leaf(self):
        for test_case, expected_result in self.is_leaf_test_cases:
            actual = Node.is_leaf(test_case)
            self.assertEqual(actual, expected_result)

    def test_has_parent_property(self):
        node = Node(1, 2)
        actual = node.parent
        self.assertEqual(actual, None)

    def test_left_child_assigns_parent_property(self):
        child = Node(1, 2)
        node = Node(child, 3)
        actual = child.parent
        self.assertEqual(actual, node)

    def test_right_child_assigns_parent_property(self):
        child = Node(1, 2)
        node = Node(5, child)
        actual = child.parent
        self.assertEqual(actual, node)

    def test_grandchild_has_correct_parent_property(self):
        grandchild = Node(1, 2)
        child = Node(Node(3, 4), grandchild)
        node = Node(child, Node(5, 6))
        actual = grandchild.parent.parent
        self.assertEqual(node, actual)


class TestSnailfish(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.creation_test_cases = [
            ('[1,2]', Node(1, 2)),
            ('[[1,2],3]', Node(Node(1, 2), 3)),
            ('[9,[8,7]]', Node(9, Node(8, 7))),
            ('[[1,9],[8,5]]', Node(Node(1, 9), Node(8,5))),
            (
                '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]',
                Node(Node(Node(Node(1, 2), Node(3, 4)), Node(Node(5, 6), Node(7, 8))), 9),
            ),

            (
                '[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]',
                Node(Node(Node(9, Node(3, 8)), Node(Node(0, 9), 6)), Node(Node(Node(3,7), Node(4, 9)), 3))
            )
        ]

        cls.str_test_cases = [
            (Node(1, 2), '[1,2]'),
            (Node(Node(1, 2), 3) ,'[[1,2],3]'),
            (Node(9, Node(8, 7)), '[9,[8,7]]'),
            (Node(Node(1, 9), Node(8,5)), '[[1,9],[8,5]]'),
            (
                Node(Node(Node(Node(1, 2), Node(3, 4)), Node(Node(5, 6), Node(7, 8))), 9),
                '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]',

            ),

            (
                Node(Node(Node(9, Node(3, 8)), Node(Node(0, 9), 6)), Node(Node(Node(3,7), Node(4, 9)), 3)),
                '[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]',
            )
        ]

    def test_snailfish_is_class(self):
        self.assertIsInstance(Snailfish, type)

    def test_raises_without_parameters(self):
        with self.assertRaises(TypeError):
            Snailfish()

    def test_creations_assigns_pairs_property(self):
        for test_case, expected_result in self.creation_test_cases:
            snailfish = Snailfish(test_case)
            actual = snailfish.pairs
            self.assertEqual(actual, expected_result)

    def test_str(self):
        for test_case, expected_result in self.str_test_cases:
            actual = str(test_case)
            self.assertEqual(actual, expected_result)


class TestSnailStringToNode(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ('[1,2]', Node(1, 2)),
            ('[[1,2],3]', Node(Node(1, 2), 3)),
            ('[9,[8,7]]', Node(9, Node(8, 7))),
            ('[[1,9],[8,5]]', Node(Node(1, 9), Node(8,5))),
            (
                '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]',
                Node(Node(Node(Node(1, 2), Node(3, 4)), Node(Node(5, 6), Node(7, 8))), 9),
            ),

            (
                '[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]',
                Node(Node(Node(9, Node(3, 8)), Node(Node(0, 9), 6)), Node(Node(Node(3,7), Node(4, 9)), 3))
            )
        ]

    def test_snail_string_to_node(self):
        for test_case, expected_result in self.test_cases:
            actual = Snailfish.snail_string_to_node(test_case)
            self.assertEqual(actual, expected_result)


class TestReduceSnailfish(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.explode_test_cases = [
            ('[1,2]', '[1,2]'),
            ('[[1,2],3]', '[[1,2],3]'),

            ('[[[[1,2],3],4],5]', '[[[[1,2],3],4],5]'),
            ('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]'),
            ('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]'),
            ('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]'),
            (
                '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]',
                '[[[[0,7],4],[15,[0,13]]],[1,1]]'
            ),
            ('[[[[[9,8],[1, 6]],2],3],4]', '[[[[9,0],8],3],4]'),
            (
                '[[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]]',
                '[[[[13,14],[7,15]],[[14,15],[16,2]]],[[[0,11],[6,11]],[[10,10],[5,0]]]]'
            )



        ]

        cls.split_test_cases = [
            ('[10,1]', '[[5,5],1]'),
            ('[1,10]', '[1,[5,5]]'),
            ('[11,13]', '[[5,6],13]'),
            ('[[[1,2],[15,5]],[10,[3,4]]]', "[[[1,2],[[7,8],5]],[10,[3,4]]]"),
            (
                '[[[[0,7],4],[15,[0,13]]],[1,1]]',
                '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'
            ),
        ]

        cls.reduce_test_cases = [
            ('[10,1]', '[[5,5],1]'),
            (
                '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]',
                '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'
            ),
            (
                '[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]',
                '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'
            ),

        ]

    def test_explode(self):
        for test_case, expected_result in self.explode_test_cases:
            snail = Snailfish(test_case)
            snail.explode()
            actual = str(snail)
            self.assertEqual(actual, expected_result)

    def test_split(self):
        for test_case, expected_result in self.split_test_cases:
            snail = Snailfish(test_case)
            snail.split()
            actual = str(snail)
            self.assertEqual(actual, expected_result)

    def test_split_sets_left_child_parent(self):
        snail = Snailfish('[11,1]')
        node = snail.pairs
        snail.split()

        actual = node.left.parent
        expected = node
        self.assertEqual(actual, expected)

    def test_split_sets_right_child_parent(self):
        snail = Snailfish('[1,11]')
        node = snail.pairs
        snail.split()

        actual = node.right.parent
        expected = node
        self.assertEqual(actual, expected)

    def test_reduce_snail(self):
        for test_case, expected_result in self.reduce_test_cases:
            snail = Snailfish(test_case)
            snail.reduce_snail()
            actual = str(snail)
            self.assertEqual(actual, expected_result)


class TestUpdateNearestLeft(unittest.TestCase):

    def test_update_nearest_left_single_level_no_left_nodes(self):
        node = Node(0, 11)
        Node(node, Node(1, 2))
        expected = None
        actual = Snailfish.update_nearest_left_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_left_two_level_no_left_nodes(self):
        node = Node(0, 11)
        Node(Node(node, 2), Node(1, 2))
        expected = None
        actual = Snailfish.update_nearest_left_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_left_adjacent_no_left_child(self):
        node = Node(0, 11)
        Node(2, node)
        expected = 2
        actual = Snailfish.update_nearest_left_adjacent(node)

        self.assertEqual(actual, expected)


    def test_update_nearest_left_adjacent_single_level(self):
        node = Node(0, 11)
        Node(Node(1, 2), node)
        expected = 2
        actual = Snailfish.update_nearest_left_adjacent(node)

        self.assertEqual(actual, expected)

    def test_update_nearest_left_adjacent_two_left_levels(self):
        node = Node(0, 11)
        Node(Node(1, Node(2, 3)), node)
        expected = 3
        actual = Snailfish.update_nearest_left_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_left_adjacent_two_right_levels(self):
        node = Node(0, 11)
        Node(1, Node(node, Node(2, 3)))
        expected = 1
        actual = Snailfish.update_nearest_left_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_left_adjacent_two_left_and_right_levels(self):
        node = Node(0, 11)
        Node(Node(1, Node(5, 4)), Node(node, Node(2, 3)))
        expected = 4
        actual = Snailfish.update_nearest_left_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_left_adjacent_single_level_changes_snail(self):
        node = Node(5, 11)
        snail = Node(Node(1, 2), node)
        expected_value = 7
        actual_value = Snailfish.update_nearest_left_adjacent(node)
        self.assertEqual(actual_value, expected_value)

        expected_snail = Node(Node(1, 7), Node(5, 11))

        self.assertEqual(snail, expected_snail)

    def test_update_nearest_left_adjacent_two_left_levels_changes_snail(self):
        node = Node(5, 11)
        Node(Node(1, Node(2, 3)), node)
        expected = 8
        actual = Snailfish.update_nearest_left_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_left_adjacent_two_right_levels_changes_snail(self):
        node = Node(5, 11)
        Node(1, Node(node, Node(2, 3)))
        expected = 6
        actual = Snailfish.update_nearest_left_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_left_adjacent_two_left_and_right_levels_changes_snail(self):
        node = Node(5, 11)
        Node(Node(1, Node(5, 4)), Node(node, Node(2, 3)))
        expected = 9
        actual = Snailfish.update_nearest_left_adjacent(node)
        self.assertEqual(actual, expected)


class TestUpdateNearestRight(unittest.TestCase):

    def test_update_nearest_right_single_level_no_right_nodes(self):
        node = Node(0, 11)
        Node(Node(1, 2), node)
        expected = None
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_two_level_no_right_nodes(self):
        node = Node(0, 11)
        Node(Node(1, 2), Node(2, node))
        expected = None
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_no_right_child_level(self):
        node = Node(11, 0)
        Node(node, 3)
        expected = 3
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_single_level(self):
        node = Node(11, 0)
        Node(node, Node(3, 2))
        expected = 3
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_two_right_levels(self):
        node = Node(11, 0)
        Node(node, Node(Node(3, 2), 1))
        expected = 3
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_two_left_levels(self):
        node = Node(11, 0)
        Node(1, Node(node, Node(2, 3)))
        Node(Node(Node(2, 3), node), 1)
        expected = 1
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_two_left_and_right_levels(self):
        node = Node(11, 0)
        Node(Node(1, Node(5, 4)), Node(node, Node(2, 3)))
        Node(Node(Node(2, 3), node), Node(Node(5, 4), 1))
        expected = 5
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_no_right_child_level_changes_snail(self):
        node = Node(11, 4)
        Node(node, 3)
        expected = 7
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_single_level_changes_snail(self):
        node = Node(11, 5)
        Node(node, Node(3, 2))
        expected = 8
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_two_right_levels_changes_snail(self):
        node = Node(11, 3)
        Node(node, Node(Node(3, 2), 1))
        expected = 6
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_two_left_levels_changes_snail(self):
        node = Node(11, 2)
        Node(1, Node(node, Node(2, 3)))
        Node(Node(Node(2, 3), node), 1)
        expected = 3
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    def test_update_nearest_right_adjacent_two_left_and_right_levels_changes_snail(self):
        node = Node(11, 5)
        Node(Node(1, Node(5, 4)), Node(node, Node(2, 3)))
        Node(Node(Node(2, 3), node), Node(Node(5, 4), 1))
        expected = 10
        actual = Snailfish.update_nearest_right_adjacent(node)
        self.assertEqual(actual, expected)

    # def test_update_nearest_right_adjacent_single_level_changes_snail(self):
    #     node = Node(5, 11)
    #     snail = Node(Node(1, 2), node)
    #     expected_value = 7
    #     actual_value = Snailfish.update_nearest_right_adjacent(node)
    #     self.assertEqual(actual_value, expected_value)
    #
    #     expected_snail = Node(Node(1, 7), Node(5, 11))
    #
    #     self.assertEqual(snail, expected_snail)
    #
    # def test_update_nearest_right_adjacent_two_right_levels_changes_snail(self):
    #     node = Node(5, 11)
    #     Node(Node(1, Node(2, 3)), node)
    #     expected = 8
    #     actual = Snailfish.update_nearest_right_adjacent(node)
    #     self.assertEqual(actual, expected)
    #
    # def test_update_nearest_right_adjacent_two_right_levels_changes_snail(self):
    #     node = Node(5, 11)
    #     Node(1, Node(node, Node(2, 3)))
    #     expected = 6
    #     actual = Snailfish.update_nearest_right_adjacent(node)
    #     self.assertEqual(actual, expected)
    #
    # def test_update_nearest_right_adjacent_two_right_and_right_levels_changes_snail(self):
    #     node = Node(5, 11)
    #     Node(Node(1, Node(5, 4)), Node(node, Node(2, 3)))
    #     expected = 9
    #     actual = Snailfish.update_nearest_right_adjacent(node)
    #     self.assertEqual(actual, expected)


class TestSnailfishAdd(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (('[1,1]','[2,2]'), '[[1,1],[2,2]]'),
            (
                (
                    '[1,1]',
                    '[2,2]',
                    '[3,3]',
                    '[4,4]',
                ),
                '[[[[1,1],[2,2]],[3,3]],[4,4]]'
            ),
            (
                (
                    '[[[[4,3],4],4],[7,[[8,4],9]]]',
                    '[1,1]'
                ),
                '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

            ),
            (
                (
                    '[1,1]',
                    '[2,2]',
                    '[3,3]',
                    '[4,4]',
                    '[5,5]',
                ),
                '[[[[3,0],[5,3]],[4,4]],[5,5]]'
            ),
            (
                (
                    '[1,1]',
                    '[2,2]',
                    '[3,3]',
                    '[4,4]',
                    '[5,5]',
                    '[6,6]',
                ),
                '[[[[5,0],[7,4]],[5,5]],[6,6]]'
            ),
            (
                (
                    '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
                    '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
                ),
                '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'
            ),
            (
                (
                    '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]',
                    '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]'
                ),
                '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]'
            ),
            (
                (
                    '[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]',
                    '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]'
                ),
                '[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]'
            ),
            (
                (
                    '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
                    '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
                    '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
                    '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
                    '[7,[5,[[3,8],[1,4]]]]',
                    '[[2,[2,2]],[8,[8,1]]]',
                    '[2,9]',
                    '[1,[[[9,3],9],[[9,0],[0,7]]]]',
                    '[[[5,[7,4]],7],1]',
                    '[[[[4,2],2],6],[8,7]]'
                ),
                '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
            ),
        ]

    def test_snailfish_add(self):
        for test_case, expected_result in self.test_cases:
            snail = Snailfish(test_case[0])

            for other_snail in test_case[1:]:
                snail + other_snail

            snail.explode()
            actual = str(snail)

            self.assertEqual(actual, expected_result)


class TestMagnitude(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ('[9,1]', 29),
            ('[1,9]', 21),
            ('[[9,1],[1,9]]', 129),
            ('[[1,2],[[3,4],5]]', 143),
            ('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', 1384),
            ('[[[[1,1],[2,2]],[3,3]],[4,4]]', 445),
            ('[[[[3,0],[5,3]],[4,4]],[5,5]]', 791),
            ('[[[[5,0],[7,4]],[5,5]],[6,6]]', 1137),
            ('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', 3488),
            ('[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]', 4140),
        ]

    def test_magnitude(self):
        for test_case, expected_result in self.test_cases:
            snail = Snailfish(test_case)
            actual = snail.magnitude()
            self.assertEqual(actual, expected_result)


class TestParseSnailList(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (
                (
                    '[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]',
                    '[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]',
                    '[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]',
                    '[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]',
                    '[7,[5,[[3,8],[1,4]]]]',
                    '[[2,[2,2]],[8,[8,1]]]',
                    '[2,9]',
                    '[1,[[[9,3],9],[[9,0],[0,7]]]]',
                    '[[[5,[7,4]],7],1]',
                    '[[[[4,2],2],6],[8,7]]'
                ), 3488
            ),
            (
                (
                    '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n',
                    '[[[5,[2,8]],4],[5,[[9,9],0]]]\n',
                    '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n',
                    '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n',
                    '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n',
                    '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n',
                    '[[[[5,4],[7,7]],8],[[8,3],8]]\n',
                    '[[9,3],[[9,9],[6,[4,9]]]]\n',
                    '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n',
                    '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'
                ), 4140
            ),
        ]

    def test_parse_snail_list(self):
        for test_case, expected_result in self.test_cases:
            actual = parse_snail_list(test_case)
            self.assertEqual(actual, expected_result)

class TestParseSnailListPart2(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (
                (
                    '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n',
                    '[[[5,[2,8]],4],[5,[[9,9],0]]]\n',
                    '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n',
                    '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n',
                    '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n',
                    '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n',
                    '[[[[5,4],[7,7]],8],[[8,3],8]]\n',
                    '[[9,3],[[9,9],[6,[4,9]]]]\n',
                    '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n',
                    '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'
                ), 3993
            ),
        ]

    def test_parse_snail_list_part_2(self):
        for test_case, expected_result in self.test_cases:
            actual = parse_snail_list_part_2(test_case)
            self.assertEqual(actual, expected_result)

"""
--- Part Two ---
You notice a second question on the back of the homework assignment:

What is the largest magnitude you can get from adding only two of the snailfish
 numbers?

Note that snailfish addition is not commutative - that is, x + y and y + x can 
produce different results.

Again considering the last example homework assignment above:

    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    
The largest magnitude of the sum of any two snailfish numbers in this list is 
3993. 
This is the magnitude of [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]] + 
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]], which reduces to 
[[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]].

What is the largest magnitude of any sum of two different snailfish numbers 
from the homework assignment?
"""

if __name__ == "__main__":
    raw_snailfish = read_txt_file_contents("18-snailfish_numbers.txt")
    print(parse_snail_list(raw_snailfish))
    print(parse_snail_list_part_2(raw_snailfish))
    unittest.main()
