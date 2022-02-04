"""
--- Day 15: Chiton ---

You've almost reached the exit of the cave, but the walls are getting closer
together. Your submarine can barely still fit, though; the main problem is
that the walls of the cave are covered in chitons, and it would be best not
to bump any of them.

The cavern is large, but has a very low ceiling, restricting your motion to two
dimensions. The shape of the cavern resembles a square; a quick scan of chiton
density produces a map of risk level throughout the cave (your puzzle input).
For example:

    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581

You start in the top left position, your destination is the bottom right
position, and you cannot move diagonally. The number at each position is its
risk level; to determine the total risk of an entire path, add up the risk
levels of each position you enter (that is, don't count the risk level of your
starting position unless you enter it; leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. In this example, a path
with the lowest total risk is highlighted here:

    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581

The total risk of this path is 40 (the starting position is never entered, so
its risk is not counted).

What is the lowest total risk of any path from the top left to the bottom right?
"""

import unittest
from collections import defaultdict
from queue import PriorityQueue
from helper_functions import read_txt_file_contents

"""
Create a min_map the same size as grid with everything == infinity

Start at (0, 0)
iterate through the neighbours (using helper function to get the neighbours)
    - if path_distance < neighbour_value -> neighbour_value == path_distance
"""


def min_chiton_risk(risk_map, tiled=False):
    """
    Solve using a Dijkstra algorithm to get to shortest distance between two
    points on a graph
    """
    if not risk_map:
        return 0
    if isinstance(risk_map[0], str):
        risk_map = parse_input(risk_map)
    if tiled:
        # print(risk_map)
        risk_map = increment_array(risk_map)
    depth = len(risk_map)
    width = len(risk_map[0])
    node_queue = PriorityQueue()
    node_queue.put((0, (0, 0)))
    # for node in [(10, (1, 0)), (4, (4, 3)), (5, (2, 4)), ]:
    #     node_queue.put(node)
    costs = defaultdict(lambda: float('inf'))
    visited = set()
    while not node_queue.empty():
        cost, current_node = node_queue.get()
        if current_node in visited:
            continue
        visited.add(current_node)

        if costs[current_node] > cost:
            costs[current_node] = cost
        neighbours = get_neighbours(current_node, depth, width)
        for neighbour in neighbours:

            i, j = neighbour
            potential_cost = cost + risk_map[i][j]
            if potential_cost < costs[neighbour]:
                costs[neighbour] = potential_cost
            if neighbour not in visited:
                node_queue.put((costs[neighbour], neighbour))
    return costs[depth - 1, width - 1]


def parse_input(risk_map):
    risk_map = [[int(num) for num in row if num.isdigit()] for row in risk_map ]
    return risk_map


def get_neighbours(node, depth, width):
    x_vals = [-1, 0, 1]
    y_vals = [-1, 0, 1]
    i, j = node
    neighbours = []
    for x in x_vals:
        for y in y_vals:

            if depth > i + x >= 0 and width > j + y >= 0 and abs(x) != abs(y):
                neighbours.append((x + i, y + j))
    return neighbours


def increment_array(input_array):
    width = len(input_array[0])
    depth = len(input_array)

    output = [[None for _ in range(width * 5)] for _ in range(depth * 5)]
    for row, row_list in enumerate(input_array):
        for col, val in enumerate(row_list):
            for i in range(5):
                for j in range(5):
                    col_index = col + i * width
                    row_index = row + j * depth
                    new_value = (val + i + j) % 9

                    output[row_index][col_index] = new_value if new_value != 0 else 9

    return output


class TestGetNeighbours(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        one_by_three = [[0]] * 3
        three_by_one = [[0] * 3]
        three_by_three = [[0] * 3] * 3

        cls.test_cases = [
            ([[]], (0, 0), []),
            ([[0]], (0, 0), []),
            (three_by_one, (0, 0), [(0, 1)]),
            (three_by_one, (0, 1), [(0, 0), (0, 2)]),
            (three_by_one, (0, 2), [(0, 1)]),
            (one_by_three, (0, 0), [(1, 0)]),
            (one_by_three, (1, 0), [(0, 0), (2, 0)]),
            (one_by_three, (2, 0), [(1, 0)]),
            (three_by_three, (0, 0), [(0, 1), (1, 0)]),
            (three_by_three, (1, 0), [(0, 0), (2, 0), (1, 1)]),
            (three_by_three, (2, 0), [(2, 1), (1, 0)]),
            (three_by_three, (0, 1), [(0, 0), (0, 2), (1, 1)]),
            (three_by_three, (1, 1), [(0, 1), (1, 0), (2, 1), (1, 2)]),
            (three_by_three, (2, 1), [(2, 0), (2, 2), (1, 1)]),
            (three_by_three, (2, 0), [(1, 0), (2, 1)]),
            (three_by_three, (2, 1), [(2, 0), (2, 2), (1, 1)]),
            (three_by_three, (2, 2), [(1, 2), (2, 1)]),
        ]

    def test_get_neighbours(self):
        for grid, node, expected_result in self.test_cases:
            with self.subTest(f"Test case: {grid} - {node}"):
                depth = len(grid)
                width = len(grid[0])
                actual = get_neighbours(node, depth, width)
                result = all(item in actual for item in expected_result)
                self.assertTrue(result)
                self.assertEqual(len(actual), len(expected_result))


class TestChiton(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [

            ([], 0),
            ([[1]], 0),
            ([
                 [1, 2],
                 [1, 3],
             ], 4),
            ([
                 [1, 1, 6],
             ], 7),
            ([
                 [1],
                 [1],
                 [2]
             ], 3),
            ([
                 [1, 1, 6],
                 [1, 3, 8],
                 [2, 1, 3]
             ], 7),
            ([
                 [1, 1, 6, 3],
                 [1, 3, 8, 1],
                 [2, 1, 3, 6],
             ], 13),
            (['116\n', '138\n', '213'], 7),
            ([
                 "1163751742",
                 "1381373672",
                 "2136511328",
                 "3694931569",
                 "7463417111",
                 "1319128137",
                 "1359912421",
                 "3125421639",
                 "1293138521",
                 "2311944581"
             ], 40)

        ]

        cls.tiled_test_cases = [
            ([
                 "1163751742",
                 "1381373672",
                 "2136511328",
                 "3694931569",
                 "7463417111",
                 "1319128137",
                 "1359912421",
                 "3125421639",
                 "1293138521",
                 "2311944581"
             ], 315),

        ]

        cls.parse_input_test_cases = [
            (['116\n', '138\n', '213'], [
                 [1, 1, 6],
                 [1, 3, 8],
                 [2, 1, 3]
             ]),

        ]

    def test_parse_input(self):
        for test_case, expected_result in self.parse_input_test_cases:
            with self.subTest():
                actual = parse_input(test_case)
                self.assertEqual(actual, expected_result)

    def test_chiton(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest(f"Test Case: {test_case}"):
                actual = min_chiton_risk(test_case)
                self.assertEqual(actual, expected_result)

    def test_tiled_chiton(self):
        for test_case, expected_result in self.tiled_test_cases:
            actual = min_chiton_risk(test_case, True)
            self.assertEqual(actual, expected_result)


class TestIncrementArray(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_cases = [
            ([[9]],
             [
                 [9, 1, 2, 3, 4],
                 [1, 2, 3, 4, 5],
                 [2, 3, 4, 5, 6],
                 [3, 4, 5, 6, 7],
                 [4, 5, 6, 7, 8],


             ]),
            ([[8]],
             [
                 [8, 9, 1, 2, 3],
                 [9, 1, 2, 3, 4],
                 [1, 2, 3, 4, 5],
                 [2, 3, 4, 5, 6],
                 [3, 4, 5, 6, 7],

             ]),
            ([[1, 2]],
             [
                 [1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
                 [2, 3, 3, 4, 4, 5, 5, 6, 6, 7],
                 [3, 4, 4, 5, 5, 6, 6, 7, 7, 8],
                 [4, 5, 5, 6, 6, 7, 7, 8, 8, 9],
                 [5, 6, 6, 7, 7, 8, 8, 9, 9, 1],

             ]),
            (
                [
                    "1163751742",
                    "1381373672",
                    "2136511328",
                    "3694931569",
                    "7463417111",
                    "1319128137",
                    "1359912421",
                    "3125421639",
                    "1293138521",
                    "2311944581"
                ],
                [
                    "11637517422274862853338597396444961841755517295286",
                    "13813736722492484783351359589446246169155735727126",
                    "21365113283247622439435873354154698446526571955763",
                    "36949315694715142671582625378269373648937148475914",
                    "74634171118574528222968563933317967414442817852555",
                    "13191281372421239248353234135946434524615754563572",
                    "13599124212461123532357223464346833457545794456865",
                    "31254216394236532741534764385264587549637569865174",
                    "12931385212314249632342535174345364628545647573965",
                    "23119445813422155692453326671356443778246755488935",
                    "22748628533385973964449618417555172952866628316397",
                    "24924847833513595894462461691557357271266846838237",
                    "32476224394358733541546984465265719557637682166874",
                    "47151426715826253782693736489371484759148259586125",
                    "85745282229685639333179674144428178525553928963666",
                    "24212392483532341359464345246157545635726865674683",
                    "24611235323572234643468334575457944568656815567976",
                    "42365327415347643852645875496375698651748671976285",
                    "23142496323425351743453646285456475739656758684176",
                    "34221556924533266713564437782467554889357866599146",
                    "33859739644496184175551729528666283163977739427418",
                    "35135958944624616915573572712668468382377957949348",
                    "43587335415469844652657195576376821668748793277985",
                    "58262537826937364893714847591482595861259361697236",
                    "96856393331796741444281785255539289636664139174777",
                    "35323413594643452461575456357268656746837976785794",
                    "35722346434683345754579445686568155679767926678187",
                    "53476438526458754963756986517486719762859782187396",
                    "34253517434536462854564757396567586841767869795287",
                    "45332667135644377824675548893578665991468977611257",
                    "44961841755517295286662831639777394274188841538529",
                    "46246169155735727126684683823779579493488168151459",
                    "54698446526571955763768216687487932779859814388196",
                    "69373648937148475914825958612593616972361472718347",
                    "17967414442817852555392896366641391747775241285888",
                    "46434524615754563572686567468379767857948187896815",
                    "46833457545794456865681556797679266781878137789298",
                    "64587549637569865174867197628597821873961893298417",
                    "45364628545647573965675868417678697952878971816398",
                    "56443778246755488935786659914689776112579188722368",
                    "55172952866628316397773942741888415385299952649631",
                    "57357271266846838237795794934881681514599279262561",
                    "65719557637682166874879327798598143881961925499217",
                    "71484759148259586125936169723614727183472583829458",
                    "28178525553928963666413917477752412858886352396999",
                    "57545635726865674683797678579481878968159298917926",
                    "57944568656815567976792667818781377892989248891319",
                    "75698651748671976285978218739618932984172914319528",
                    "56475739656758684176786979528789718163989182927419",
                    "67554889357866599146897761125791887223681299833479"
                ]
            )

        ]

    def test_increment_array(self):
        for test_case, expected_result in self.test_cases:
            with self.subTest():
                if isinstance(test_case[0], str):
                    test_case = parse_input(test_case)
                actual = increment_array(test_case)
                if isinstance(expected_result[0], str):
                    expected_result = parse_input(expected_result)
                self.assertEqual(actual, expected_result)

"""
--- Part Two ---
Now that you know how to find low-risk paths in the cave, you can try to 
find your way out.

The entire cave is actually five times larger in both dimensions than you 
thought; the area you originally scanned is just one tile in a 5x5 tile 
area that forms the full map. Your original map tile repeats to the right 
and downward; each time the tile repeats to the right or downward, all of 
its risk levels are 1 higher than the tile immediately up or left of it. 
However, risk levels above 9 wrap back around to 1. So, if your original 
map had some position with a risk level of 8, then that same position on 
each of the 25 total tiles would be as follows:

8 9 1 2 3
9 1 2 3 4
1 2 3 4 5
2 3 4 5 6
3 4 5 6 7

Each single digit above corresponds to the example position with a value 
of 8 on the top-left tile. Because the full map is actually five times 
larger in both dimensions, that position appears a total of 25 times, 
once in each duplicated tile, with the values shown above.

Here is the full five-times-as-large version of the first example above, 
with the original map in the top left corner highlighted:

11637517422274862853338597396444961841755517295286
13813736722492484783351359589446246169155735727126
21365113283247622439435873354154698446526571955763
36949315694715142671582625378269373648937148475914
74634171118574528222968563933317967414442817852555
13191281372421239248353234135946434524615754563572
13599124212461123532357223464346833457545794456865
31254216394236532741534764385264587549637569865174
12931385212314249632342535174345364628545647573965
23119445813422155692453326671356443778246755488935
22748628533385973964449618417555172952866628316397
24924847833513595894462461691557357271266846838237
32476224394358733541546984465265719557637682166874
47151426715826253782693736489371484759148259586125
85745282229685639333179674144428178525553928963666
24212392483532341359464345246157545635726865674683
24611235323572234643468334575457944568656815567976
42365327415347643852645875496375698651748671976285
23142496323425351743453646285456475739656758684176
34221556924533266713564437782467554889357866599146
33859739644496184175551729528666283163977739427418
35135958944624616915573572712668468382377957949348
43587335415469844652657195576376821668748793277985
58262537826937364893714847591482595861259361697236
96856393331796741444281785255539289636664139174777
35323413594643452461575456357268656746837976785794
35722346434683345754579445686568155679767926678187
53476438526458754963756986517486719762859782187396
34253517434536462854564757396567586841767869795287
45332667135644377824675548893578665991468977611257
44961841755517295286662831639777394274188841538529
46246169155735727126684683823779579493488168151459
54698446526571955763768216687487932779859814388196
69373648937148475914825958612593616972361472718347
17967414442817852555392896366641391747775241285888
46434524615754563572686567468379767857948187896815
46833457545794456865681556797679266781878137789298
64587549637569865174867197628597821873961893298417
45364628545647573965675868417678697952878971816398
56443778246755488935786659914689776112579188722368
55172952866628316397773942741888415385299952649631
57357271266846838237795794934881681514599279262561
65719557637682166874879327798598143881961925499217
71484759148259586125936169723614727183472583829458
28178525553928963666413917477752412858886352396999
57545635726865674683797678579481878968159298917926
57944568656815567976792667818781377892989248891319
75698651748671976285978218739618932984172914319528
56475739656758684176786979528789718163989182927419
67554889357866599146897761125791887223681299833479

Equipped with the full map, you can now find a path from the top left corner 
to the bottom right corner with the lowest total risk:

11637517422274862853338597396444961841755517295286
13813736722492484783351359589446246169155735727126
21365113283247622439435873354154698446526571955763
36949315694715142671582625378269373648937148475914
74634171118574528222968563933317967414442817852555
13191281372421239248353234135946434524615754563572
13599124212461123532357223464346833457545794456865
31254216394236532741534764385264587549637569865174
12931385212314249632342535174345364628545647573965
23119445813422155692453326671356443778246755488935
22748628533385973964449618417555172952866628316397
24924847833513595894462461691557357271266846838237
32476224394358733541546984465265719557637682166874
47151426715826253782693736489371484759148259586125
85745282229685639333179674144428178525553928963666
24212392483532341359464345246157545635726865674683
24611235323572234643468334575457944568656815567976
42365327415347643852645875496375698651748671976285
23142496323425351743453646285456475739656758684176
34221556924533266713564437782467554889357866599146
33859739644496184175551729528666283163977739427418
35135958944624616915573572712668468382377957949348
43587335415469844652657195576376821668748793277985
58262537826937364893714847591482595861259361697236
96856393331796741444281785255539289636664139174777
35323413594643452461575456357268656746837976785794
35722346434683345754579445686568155679767926678187
53476438526458754963756986517486719762859782187396
34253517434536462854564757396567586841767869795287
45332667135644377824675548893578665991468977611257
44961841755517295286662831639777394274188841538529
46246169155735727126684683823779579493488168151459
54698446526571955763768216687487932779859814388196
69373648937148475914825958612593616972361472718347
17967414442817852555392896366641391747775241285888
46434524615754563572686567468379767857948187896815
46833457545794456865681556797679266781878137789298
64587549637569865174867197628597821873961893298417
45364628545647573965675868417678697952878971816398
56443778246755488935786659914689776112579188722368
55172952866628316397773942741888415385299952649631
57357271266846838237795794934881681514599279262561
65719557637682166874879327798598143881961925499217
71484759148259586125936169723614727183472583829458
28178525553928963666413917477752412858886352396999
57545635726865674683797678579481878968159298917926
57944568656815567976792667818781377892989248891319
75698651748671976285978218739618932984172914319528
56475739656758684176786979528789718163989182927419
67554889357866599146897761125791887223681299833479

The total risk of this path is 315 (the starting position is still never 
entered, so its risk is not counted).

Using the full map, what is the lowest total risk of any path from the top
left to the bottom right?
"""


if __name__ == "__main__":
    cave_map = read_txt_file_contents("15-cave_map.txt")
    print(min_chiton_risk(cave_map))
    print(min_chiton_risk(cave_map, tiled=True))

    unittest.main()
