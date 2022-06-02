import numpy as np

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        changed = False
        points = []
        folds = []
        for line in map(lambda x: x.rstrip(), input_file):
            if line == '':
                changed = True
            elif changed:
                folds.append((0 if 'x' in line else 1, get_ints(line).pop()))
            else:
                points.append(get_ints(line))
        return points, folds


@timed
def part1(dots):
    points, folds = dots
    array = np.zeros(shape=(max(points, key=first)[0] + 1, max(points, key=second)[1] + 1))
    grid = Grid(array)

    for point in points:
        grid.set(*point, 1)

    for axis, line in folds:
        if axis == 1:
            first_half = grid.grid[:, 0:line]
            second_half = grid.grid[:, line + 1:]

            second_half = np.flip(second_half, axis=axis)

            if first_half.shape[1] > second_half.shape[1]:
                zeros = np.zeros(shape=(first_half.shape[0], first_half.shape[1] - second_half.shape[1]))
                second_half = np.append(zeros, second_half, axis=1)

                grid = Grid(first_half + second_half)
            else:
                zeros = np.zeros(shape=(first_half.shape[0], second_half.shape[1] - first_half.shape[1]))
                first_half = np.append(zeros, first_half, axis=1)

                grid = Grid(first_half + second_half)
        else:
            top_half = grid.grid[0:line, :]
            bottom_half = grid.grid[line + 1:, :]

            bottom_half = np.flip(bottom_half, axis=axis)
            if top_half.shape[0] > bottom_half.shape[0]:
                zeros = np.zeros(shape=(top_half.shape[0] - bottom_half.shape[0], top_half.shape[1]))
                bottom_half = np.append(zeros, bottom_half, axis=0)

                grid = Grid(top_half + bottom_half)
            else:
                zeros = np.zeros(shape=(bottom_half.shape[0] - top_half.shape[0], top_half.shape[1]))
                top_half = np.append(zeros, top_half, axis=0)

                grid = Grid(top_half + bottom_half)

        print(np.count_nonzero(grid.grid))
        return


@timed
def part2(dots):
    points, folds = dots
    array = np.zeros(shape=(max(points, key=first)[0] + 1, max(points, key=second)[1] + 1))
    grid = Grid(array)

    for point in points:
        grid.set(*point, 1)

    for axis, line in folds:
        if axis == 1:
            first_half = grid.grid[:, 0:line]
            second_half = grid.grid[:, line + 1:]

            second_half = np.flip(second_half, axis=axis)

            if first_half.shape[1] > second_half.shape[1]:
                zeros = np.zeros(shape=(first_half.shape[0], first_half.shape[1] - second_half.shape[1]))
                second_half = np.append(zeros, second_half, axis=1)

                grid = Grid(first_half + second_half)
            else:
                zeros = np.zeros(shape=(first_half.shape[0], second_half.shape[1] - first_half.shape[1]))
                first_half = np.append(zeros, first_half, axis=1)

                grid = Grid(first_half + second_half)
        else:
            top_half = grid.grid[0:line, :]
            bottom_half = grid.grid[line + 1:, :]

            bottom_half = np.flip(bottom_half, axis=axis)
            if top_half.shape[0] > bottom_half.shape[0]:
                zeros = np.zeros(shape=(top_half.shape[0] - bottom_half.shape[0], top_half.shape[1]))
                bottom_half = np.append(zeros, bottom_half, axis=0)

                grid = Grid(top_half + bottom_half)
            else:
                zeros = np.zeros(shape=(bottom_half.shape[0] - top_half.shape[0], top_half.shape[1]))
                top_half = np.append(zeros, top_half, axis=0)

                grid = Grid(top_half + bottom_half)

    grid = grid.grid.transpose()

    for i, row in enumerate(grid):
        line = ''
        for j, e in enumerate(row):
            line += '.' if e == 0 else '#'
        print(line)


if __name__ == '__main__':
    dot_list = read()
    part1(dot_list)
    part2(dot_list)
