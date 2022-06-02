import numpy as np

from shared.Util import timed

DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return np.array(list(map(lambda x: np.array(list(x.rstrip())), input_file.readlines())))


def get_neighbors(i, j, rows, dist=0):
    neighbors = 0
    for direction in DIRECTIONS:
        curr_dist = 0
        del_i, del_j = direction
        curr_i, curr_j = i + del_i, j + del_j
        while 0 <= curr_i < len(rows) and 0 <= curr_j < len(rows) and curr_dist < dist:
            seat = rows[curr_i, curr_j]
            if seat == '#':
                neighbors += 1
                break
            elif seat == '.':
                break
            curr_i += del_i
            curr_j += del_j
            curr_dist += 1
    return neighbors


@timed
def part1(rows):
    new_rows = rows.copy()

    for _ in range(100):
        for i, j in np.ndindex(rows.shape):
            seat = rows[i, j]
            neighbors = get_neighbors(i, j, rows, 1)
            if seat == '#':
                new_rows[i, j] = '#' if 1 < neighbors < 4 else '.'
            else:
                new_rows[i, j] = '#' if neighbors == 3 else '.'
        rows, new_rows = new_rows, rows

    print(np.count_nonzero(rows == '#'))


@timed
def part2(rows):
    new_rows = rows.copy()
    w, h = rows.shape
    rows[0, 0] = '#'
    rows[0, w - 1] = '#'
    rows[h - 1, 0] = '#'
    rows[h - 1, w - 1] = '#'

    for _ in range(100):
        for i, j in np.ndindex(rows.shape):
            seat = rows[i, j]
            neighbors = get_neighbors(i, j, rows, 1)
            if (i, j) in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
                new_rows[i, j] = '#'
            else:
                if seat == '#':
                    new_rows[i, j] = '#' if 1 < neighbors < 4 else '.'
                else:
                    new_rows[i, j] = '#' if neighbors == 3 else '.'
        rows, new_rows = new_rows, rows

    print(np.count_nonzero(rows == '#'))


if __name__ == '__main__':
    line_list = read()
    part1(line_list)
    part2(line_list)
