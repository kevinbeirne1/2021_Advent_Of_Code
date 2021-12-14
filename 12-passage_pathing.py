"""
--- Day 12: Passage Pathing ---

With your submarine's subterranean subsystems subsisting suboptimally, the only
way you're getting out of this cave anytime soon is by finding a path yourself.
Not just a path - the only way to know if you've found the best path is to
find all of them.

Fortunately, the sensors are still mostly working, and so you build a rough map
of the remaining caves (your puzzle input). For example:

start-A
start-b
A-c
A-b
b-d
A-end
b-end

This is a list of how all of the caves are connected. You start in the cave
named start, and your destination is the cave named end. An entry like b-d
means that cave b is connected to cave d - that is, you can move between them.

So, the above cave system looks roughly like this:

        start
        /   \
    c--A-----b--d
        \   /
         end

Your goal is to find the number of distinct paths that start at start, end at
end, and don't visit small caves more than once. There are two types of caves:
big caves (written in uppercase, like A) and small caves (written in lowercase,
like b). It would be a waste of time to visit any small cave more than once,
but big caves are large enough that it might be worth visiting them multiple
times. So, all paths you find should visit small caves at most once, and can
visit big caves any number of times.

Given these rules, there are 10 paths through this example cave system:

    start,A,b,A,c,A,end
    start,A,b,A,end
    start,A,b,end
    start,A,c,A,b,A,end
    start,A,c,A,b,end
    start,A,c,A,end
    start,A,end
    start,b,A,c,A,end
    start,b,A,end
    start,b,end

(Each line in the above list corresponds to a single path; the caves visited by
that path are listed in the order they are visited and separated by commas.)

Note that in this cave system, cave d is never visited by any path: to do so,
cave b would need to be visited twice (once on the way to cave d and a second
time when returning from cave d), and since cave b is small, this is not
allowed.

Here is a slightly larger example:

    dc-end
    HN-start
    start-kj
    dc-start
    dc-HN
    LN-dc
    HN-end
    kj-sa
    kj-HN
    kj-dc

The 19 paths through it are as follows:

    start,HN,dc,HN,end
    start,HN,dc,HN,kj,HN,end
    start,HN,dc,end
    start,HN,dc,kj,HN,end
    start,HN,end
    start,HN,kj,HN,dc,HN,end
    start,HN,kj,HN,dc,end
    start,HN,kj,HN,end
    start,HN,kj,dc,HN,end
    start,HN,kj,dc,end
    start,dc,HN,end
    start,dc,HN,kj,HN,end
    start,dc,end
    start,dc,kj,HN,end
    start,kj,HN,dc,HN,end
    start,kj,HN,dc,end
    start,kj,HN,end
    start,kj,dc,HN,end
    start,kj,dc,end

Finally, this even larger example has 226 paths through it:

    fs-end
    he-DX
    fs-he
    start-DX
    pj-DX
    end-zg
    zg-sl
    zg-pj
    pj-he
    RW-he
    fs-DX
    pj-RW
    zg-RW
    start-pj
    he-WI
    zg-he
    pj-fs
    start-RW

How many paths through this cave system are there that visit small caves at most once?
"""
import unittest
from collections import deque, defaultdict
from helper_functions import read_txt_file_contents
import re

"""
Start at 'start' add nodes connected to start to a queue
loop through the connected nodes
at each node 
    - add that node to 'visited' list and remove from the queue

at each node loop through the connected nodes
    if lower case and in 'visited' drop that node from the queue
if node == 'end' => path_count += 1
"""


class Cave:

    def __init__(self, input_data):
        self.cave_map = self.create_cave_map(input_data)
        # self.visited = set()
        # self.queue = deque(self.cave_map['start'])
        # self.calculate_no_of_paths('start')

    @staticmethod
    def create_cave_map(input_data):
        cave_map = defaultdict(set)
        for line in input_data:
            a, b = re.findall(r'(\w+)-(\w+)', line)[0]
            if a != 'end' and b != 'start':
                cave_map[a].add(b)
            if a != 'start' and b != 'end':
                cave_map[b].add(a)
        return cave_map

    def calculate_no_of_paths(self, current_node='start', seen=None):
        paths = 0
        if current_node == 'end':
            return 1

        if not seen:
            seen = set()

        if current_node.islower() and current_node in seen:
            return 0

        for node in self.cave_map[current_node]:
            child_visited = seen | {current_node}
            paths += self.calculate_no_of_paths(node, child_visited)
        return paths

    def calculate_no_of_paths_part_2(self, current_node='start', seen=None, visited_twice=False, ):
        paths = 0
        if current_node == 'end':
            return 1

        if not seen:
            seen = set()

        if current_node.islower() and current_node in seen:
            if not visited_twice:
                visited_twice = True
            else:
                return 0

        for node in self.cave_map[current_node]:
            child_visited = seen | {current_node}
            paths += self.calculate_no_of_paths_part_2(node, child_visited, visited_twice)
        return paths

"""
--- Part Two ---
After reviewing the available paths, you realize you might have time to visit 
a single small cave twice. Specifically, big caves can be visited any number 
of times, a single small cave can be visited at most twice, and the remaining 
small caves can be visited at most once. However, the caves named start and 
end can only be visited exactly once each: once you leave the start cave, you 
may not return to it, and once you reach the end cave, the path must end 
immediately.

Now, the 36 possible paths through the first example above are:

    start,A,b,A,b,A,c,A,end
    start,A,b,A,b,A,end
    start,A,b,A,b,end
    start,A,b,A,c,A,b,A,end
    start,A,b,A,c,A,b,end
    start,A,b,A,c,A,c,A,end
    start,A,b,A,c,A,end
    start,A,b,A,end
    start,A,b,d,b,A,c,A,end
    start,A,b,d,b,A,end
    start,A,b,d,b,end
    start,A,b,end
    start,A,c,A,b,A,b,A,end
    start,A,c,A,b,A,b,end
    start,A,c,A,b,A,c,A,end
    start,A,c,A,b,A,end
    start,A,c,A,b,d,b,A,end
    start,A,c,A,b,d,b,end
    start,A,c,A,b,end
    start,A,c,A,c,A,b,A,end
    start,A,c,A,c,A,b,end
    start,A,c,A,c,A,end
    start,A,c,A,end
    start,A,end
    start,b,A,b,A,c,A,end
    start,b,A,b,A,end
    start,b,A,b,end
    start,b,A,c,A,b,A,end
    start,b,A,c,A,b,end
    start,b,A,c,A,c,A,end
    start,b,A,c,A,end
    start,b,A,end
    start,b,d,b,A,c,A,end
    start,b,d,b,A,end
    start,b,d,b,end
    start,b,end
    
The slightly larger example above now has 103 paths through it, and the even 
larger example now has 3509 paths through it.

Given these new rules, how many paths through this cave system are there?
"""


class TestCreateCaveMap(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.cave_map_test_cases = [
            (['start-A', 'start-b', 'A-c', 'A-b', 'b-d', 'A-end', 'b-end'],
             {
                 'start': {'A', 'b'},
                 'A': {'b', 'c', 'end'},
                 'b': {'d', 'A', 'end'},
                 'c': {'A'},
                 'd': {'b'},
             }),
            (['dc-end', 'HN-start', 'start-kj', 'dc-start', 'dc-HN',
              'LN-dc', 'HN-end', 'kj-sa', 'kj-HN', 'kj-dc'],
             {
                 'start': {'HN', 'kj', 'dc'},
                 'HN': {'end', 'kj', 'dc'},
                 'kj': {'dc', 'sa', 'HN'},

                 'dc': {'end', 'LN', 'kj', 'HN'},

                 'LN': {'dc'},
                 'sa': {'kj'}
             }),
            #
            # {
            #     'start': deque(['A', 'b']),
            #     'A': deque(['b', 'c', 'end']),
            #     'b': deque(['d', 'A', 'end']),
            #     'c': deque(['A']),
            #     'd': deque(['b']),
            # }),
            # (['dc-end', 'HN-start', 'start-kj', 'dc-start', 'dc-HN',
            #   'LN-dc', 'HN-end', 'kj-sa', 'kj-HN', 'kj-dc'],
            #  {
            #      'start': deque(['HN', 'kj', 'dc']),
            #      'HN': deque(['end', 'kj', 'dc']),
            #      'kj': deque(['dc', 'sa', 'HN']),
            #
            #      'dc': deque(['end', 'LN', 'kj', 'HN']),
            #
            #      'LN': deque(['dc']),
            #      'sa': deque(['kj'])
            #  }),
        ]

    def test_create_cave_map(self):
        for test_case, expected_result in self.cave_map_test_cases:
            with self.subTest():
                cave = Cave(test_case)
                actual = cave.cave_map
                # for key in actual:
                #     print(key, actual[key], expected_result))
                self.assertEqual(actual, expected_result)


class TestPathCount(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            (['start-A', 'A-end'], 1),
            (['start-A', 'start-B', 'A-end', 'B-end'], 2),
            (['start-A', 'start-b', 'A-end', 'A-b', 'b-end'], 5),
            (['start-A', 'start-b', 'A-c', 'A-b', 'b-d', 'A-end', 'b-end'], 10),
            (['start-A', 'A-b', 'b-end', 'start-c', 'c-b'], 2),

            (['dc-end', 'HN-start', 'start-kj', 'dc-start', 'dc-HN',
              'LN-dc', 'HN-end', 'kj-sa', 'kj-HN', 'kj-dc'], 19),
            (['fs-end', 'he-DX', 'fs-he', 'start-DX', 'pj-DX', 'end-zg', 'zg-sl', 'zg-pj', 'pj-he', 'RW-he', 'fs-DX',
              'pj-RW', 'zg-RW', 'start-pj', 'he-WI', 'zg-he', 'pj-fs', 'start-RW'], 226)

        ]
        cls.part_2_test_cases = [
            (['start-A', 'start-b', 'A-c', 'A-b', 'b-d', 'A-end', 'b-end'], 36),
            (['dc-end', 'HN-start', 'start-kj', 'dc-start', 'dc-HN',
              'LN-dc', 'HN-end', 'kj-sa', 'kj-HN', 'kj-dc'], 103),
            (['fs-end', 'he-DX', 'fs-he', 'start-DX', 'pj-DX', 'end-zg', 'zg-sl', 'zg-pj', 'pj-he', 'RW-he', 'fs-DX',
              'pj-RW', 'zg-RW', 'start-pj', 'he-WI', 'zg-he', 'pj-fs', 'start-RW'], 3509)

        ]

    def test_path_count(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest():
                cave = Cave(test_case)
                actual = cave.calculate_no_of_paths()
                self.assertEqual(actual, expected_result)

    def test_path_count_part_2(self):
        for test_case, expected_result in self.part_2_test_cases:
            with self.subTest():
                cave = Cave(test_case)
                actual = cave.calculate_no_of_paths_part_2()
                self.assertEqual(actual, expected_result)


if __name__ == '__main__':
    cave_data = read_txt_file_contents("12-cave_map.txt")
    cave = Cave(cave_data)
    print(cave.calculate_no_of_paths())
    print(cave.calculate_no_of_paths_part_2())
    unittest.main()
