from copy import copy
from queue import Queue
from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return Grid(input_file.readlines())


@timed
def part1(inputs):
    inputs = copy(inputs)
    flashes = 0
    for _ in range(100):
        flash_list = Queue()
        for (i, j), e in coordinate(inputs):
            if e < 9:
                inputs.grid[i, j] += 1
            else:
                inputs.grid[i, j] = 0
                flash_list.put((i, j))
                flashes += 1

        while not flash_list.empty():
            curr_flash = flash_list.get()
            for (i, j), _ in inputs.neighbors(*curr_flash):
                if inputs.grid[i, j] == 9:
                    inputs.grid[i, j] = 0
                    flash_list.put((i, j))
                    flashes += 1
                elif inputs.grid[i, j] != 0:
                    inputs.grid[i, j] += 1
    print(flashes)


@timed
def part2(inputs):
    steps = 0
    while True:
        steps += 1
        flash_list = Queue()
        zeroed = set()
        for p, v in coordinate(inputs):
            if v < 9:
                inputs.set(*p, v + 1)
            else:
                inputs.set(*p, 0)
                flash_list.put(p)
                zeroed.add(p)

        while not flash_list.empty():
            curr_flash = flash_list.get()
            for p, v in inputs.neighbors(*curr_flash):
                if v == 9:
                    inputs.set(*p, 0)
                    flash_list.put(p)
                    zeroed.add(p)
                elif p not in zeroed:
                    inputs.inc(*p)

        if len(zeroed) == inputs.size:
            print(steps)
            return


if __name__ == '__main__':
    input_list = read()
    part1(input_list)
    part2(input_list)
