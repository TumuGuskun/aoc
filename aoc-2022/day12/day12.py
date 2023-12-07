import os
import numpy as np
from copy import copy
from queue import Queue

from shared.gum import gum_choose
from shared.util import timed
from shared.grid import Grid


@timed
def read() -> Grid:
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        numbered = []
        for line in input_file.readlines():
            numbered.append(list(map(lambda c: ord(c) - 96, line.strip())))
        return Grid(numbered)


@timed
def part1(map: Grid) -> None:
    queue = Queue()
    seen = set()

    end = map.find(-27)
    start = map.find(-13)
    map.set_point(*start, value=1)
    map.set_point(*end, 26)

    queue.put((start, [start]))
    seen.add(start)
    while not queue.empty():
        curr_indices, path = queue.get()
        curr_value = map.get_point(*curr_indices)
        if curr_indices == end:
            print(len(path) - 1)
            break
        for neighbor_index, neighbor_value in map.get_adjacents(*curr_indices):
            if neighbor_index in seen:
                continue
            if neighbor_value <= curr_value + 1:
                neighbor_path = path[:] + [neighbor_index]
                queue.put((neighbor_index, neighbor_path))
                seen.add(neighbor_index)


@timed
def part2(map: Grid):
    possible_starts = np.where(map.grid == 1)
    smol = 437

    end = map.find(-27)
    map.set_point(*end, 26)
    for i in range(len(possible_starts[0])):
        queue = Queue()
        seen = set()

        possible_start = (possible_starts[0][i], possible_starts[1][i])
        map.set_point(*possible_start, value=1)

        queue.put((possible_start, [possible_start]))
        seen.add(possible_start)
        while not queue.empty():
            curr_indices, path = queue.get()
            curr_value = map.get_point(*curr_indices)
            if curr_indices == end:
                if (possible_dist := len(path) - 1) < smol:
                    smol = possible_dist
                break
            for neighbor_index, neighbor_value in map.get_adjacents(*curr_indices):
                if neighbor_index in seen:
                    continue
                if neighbor_value <= curr_value + 1:
                    neighbor_path = path[:] + [neighbor_index]
                    queue.put((neighbor_index, neighbor_path))
                    seen.add(neighbor_index)
    print(smol)


if __name__ == "__main__":
    map_list = read()
    part1(copy(map_list))
    part2(copy(map_list))
