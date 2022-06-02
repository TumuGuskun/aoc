import sys
from functools import cache
from itertools import permutations
from queue import Queue

import numpy as np

from shared.Util import timed

MAZE = None


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        global MAZE
        MAZE = np.array(list(map(lambda x: list(x.rstrip()), input_file.readlines())))


def get_neighbors(x, y, maze):
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return filter(lambda z: maze[z[0], z[1]] in '01234567.', neighbors)


@cache
def dist_between(a, b):
    x, y = np.argwhere(MAZE == a)[0]
    queue = Queue()
    queue.put((x, y, 0))
    seen = set()
    seen.add((x, y))
    while not queue.empty():
        curr_x, curr_y, depth = queue.get()
        if MAZE[curr_x, curr_y] == b:
            return depth
        else:
            for next_x, next_y in get_neighbors(curr_x, curr_y, MAZE):
                if (next_x, next_y) not in seen:
                    queue.put((next_x, next_y, depth + 1))
                    seen.add((next_x, next_y))


@timed
def part1(lines):
    min_distance = float('inf')
    for order in permutations('1234567'):
        prev_node = '0'
        distance = 0
        for node in order:
            low = min(prev_node, node)
            high = max(prev_node, node)
            distance += dist_between(low, high)
            prev_node = node
        min_distance = min(distance, min_distance)
    print(min_distance)


@timed
def part2(lines):
    min_distance = float('inf')
    for order in permutations('1234567'):
        order = list(order) + ['0']
        prev_node = '0'
        distance = 0
        for node in order:
            low = min(prev_node, node)
            high = max(prev_node, node)
            distance += dist_between(low, high)
            prev_node = node
        min_distance = min(distance, min_distance)
    print(min_distance)


if __name__ == '__main__':
    line_list = read()
    part1(line_list)
    part2(line_list)
