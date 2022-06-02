import numpy as np

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return Grid(input_file.readlines())


@timed
def part1(cucumbers):
    dim1, dim2 = cucumbers.grid.shape
    moved = 1
    steps = 0
    while moved:
        moved = 0
        new_grid = np.array([['.'] * dim2] * dim1)
        for y, x in np.argwhere(cucumbers.grid == '>'):
            new_x = (x + 1) % dim2
            if cucumbers.get(y, new_x) == '.':
                new_grid[y, new_x] = '>'
                moved += 1
            else:
                new_grid[y, x] = '>'

        for y, x in np.argwhere(cucumbers.grid == 'v'):
            new_y = (y + 1) % dim1
            if cucumbers.get(new_y, x) != 'v' and new_grid[new_y, x] == '.':
                new_grid[new_y, x] = 'v'
                moved += 1
            else:
                new_grid[y, x] = 'v'

        steps += 1
        cucumbers.grid = new_grid

    print(steps)


@timed
def part2(cucumbers):
    pass


if __name__ == '__main__':
    cucumber_list = read()
    part1(cucumber_list)
    part2(cucumber_list)
