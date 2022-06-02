from collections import defaultdict

import numpy as np

from shared.Util import timed, get_ints


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        lines = []
        for line in input_file:
            lines.append(get_ints(line))
        return lines


@timed
def part1(lines):
    xs = [x for line in lines for x in line[::2]]
    ys = [y for line in lines for y in line[1::2]]
    board = np.zeros(shape=(max(xs) + 1, max(ys) + 1))
    for x1, y1, x2, y2 in lines:
        if x1 == x2:
            if y1 > y2:
                y2, y1 = y1, y2
            board[x1, y1:y2 + 1] += 1
        elif y1 == y2:
            if x1 > x2:
                x2, x1 = x1, x2
            board[x1:x2 + 1, y1] += 1

    print(board > 1)
    print((board > 1).sum())


@timed
def part2(lines):
    board = defaultdict(lambda: defaultdict(int))
    for x1, y1, x2, y2 in lines:
        if x1 == x2:
            if y1 > y2:
                y2, y1 = y1, y2
            for yi in range(y1, y2 + 1):
                board[x1][yi] += 1
        elif y1 == y2:
            if x1 > x2:
                x2, x1 = x1, x2
            for xi in range(x1, x2 + 1):
                board[xi][y1] += 1
        else:
            if x1 > x2:
                x2, x1 = x1, x2
                y2, y1 = y1, y2
            for i in range(x2 - x1 + 1):
                j = i if y2 > y1 else -i
                board[x1 + i][y1 + j] += 1

    count = 0
    for row in board.values():
        for spot in row.values():
            if spot >= 2:
                count += 1

    print(count)


if __name__ == '__main__':
    line_list = read()
    part1(line_list)
    part2(line_list)
