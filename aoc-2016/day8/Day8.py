import os

import numpy as np

from shared.Util import timed


@timed
def read():
    np.set_printoptions(edgeitems=10, linewidth=300)
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        operations = []
        for line in map(lambda l: l.rstrip(), input_file.readlines()):
            if line.startswith('rect'):
                op, size = line.split()
                x, y = map(int, size.split('x'))
                operations.append((op, x, y))
            else:
                line = line[7:]
                op, row, _, shift = line.split()
                row = int(row.split('=')[1])
                operations.append((op, row, int(shift)))

    return operations


@timed
def part1(operations):
    grid = np.zeros(shape=(6, 50), dtype=int)
    for op, a, b in operations:
        if op == 'rect':
            x, y = a, b
            grid[0:y, 0:x] = np.ones(shape=(y, x), dtype=int)
        elif op == 'row':
            row, shift = a, b
            grid[row] = np.roll(grid[row], shift)
        elif op == 'column':
            col, shift = a, b
            grid[:, col] = np.roll(grid[:, col], shift)
    print(np.count_nonzero(grid))
    print(grid)


@timed
def part2(operations):
    pass


if __name__ == '__main__':
    operation_list = read()
    part1(operation_list)
    part2(operation_list)
