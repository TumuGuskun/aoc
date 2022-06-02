from copy import copy
from queue import PriorityQueue

import numpy as np

from shared.Util import *
from shared.bfs import BFS


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return Grid(input_file.readlines())


@timed
def part1(lines):
    endx, endy = lines.grid.shape

    queue = PriorityQueue()
    seen = set()
    queue.put((0, (0, 0), [(0, 0)]))
    seen.add((0, 0))

    while not queue.empty():
        curr_weight, curr_node, path = queue.get()
        if curr_node == (endx - 1, endy - 1):
            break
        else:
            for neighbor, weight in lines.adjacents(*curr_node):
                if neighbor not in seen:
                    queue.put((weight + curr_weight, neighbor, path[:] + [neighbor]))
                    seen.add(neighbor)

    print(sum(lines.get(*p) for p in path) - lines.get(0, 0))


@timed
def part2(lines):
    bigg = np.array([[20] * lines.grid.shape[1] * 5])
    for j in range(5):
        new_lines = copy(lines)
        for _ in range(j):
            new_lines.grid += 1
            new_lines.grid[new_lines.grid == 10] = 1
        for i in range(1, 5):
            new_side = copy(lines)
            for _ in range(i + j):
                new_side.grid += 1
                new_side.grid[new_side.grid == 10] = 1
            new_lines.grid = np.append(new_lines.grid, new_side.grid, axis=1)
        bigg = np.append(bigg, new_lines.grid, axis=0)

    lines.grid = bigg

    endx, endy = lines.grid.shape

    queue = PriorityQueue()
    seen = set()
    queue.put((1, (1, 0), [(1, 0)]))
    seen.add((1, 0))

    while not queue.empty():
        curr_weight, curr_node, path = queue.get()
        if curr_node == (endx - 1, endy - 1):
            break
        else:
            for neighbor, weight in lines.adjacents(*curr_node):
                if neighbor not in seen:
                    queue.put((weight + curr_weight, neighbor, path[:] + [neighbor]))
                    seen.add(neighbor)

    print(sum(lines.get(*p) for p in path) - lines.get(1, 0))


if __name__ == '__main__':
    line_list = read()
    part1(line_list)
    part2(line_list)
