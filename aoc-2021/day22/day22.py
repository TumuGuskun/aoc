from functools import cache

import numpy as np

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return [(1 if line.startswith('on') else 0, tuple(get_ints(line))) for line in input_file]


@timed
def part1(steps):
    grid = np.zeros((101, 101, 101), dtype=int)

    for step, bounds in filter(lambda x: min(x[1]) >= -50 and max(x[1]) <= 50, steps):
        x1, x2, y1, y2, z1, z2 = map(lambda x: x + 50, bounds)
        grid[x1:x2 + 1, y1:y2 + 1, z1:z2 + 1] = step

    print(np.count_nonzero(grid))


@timed
def part2(steps):
    print(sum(on_in(i, tuple(steps), step) for i, step in enumerate(steps)))


def on_in(i, steps, step):
    step, (x1, x2, y1, y2, z1, z2) = step
    count = step * (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
    for j, (b_step, (b_x1, b_x2, b_y1, b_y2, b_z1, b_z2)) in enumerate(steps[:i]):
        if ((new_x1 := max(x1, b_x1)) <= (new_x2 := min(x2, b_x2))
                and (new_y1 := max(y1, b_y1)) <= (new_y2 := min(y2, b_y2))
                and (new_z1 := max(z1, b_z1)) <= (new_z2 := min(z2, b_z2))):
            count -= on_in(j, steps, (b_step, (new_x1, new_x2, new_y1, new_y2, new_z1, new_z2)))

    return count


if __name__ == '__main__':
    step_list = read()
    part1(step_list)
    part2(step_list)
