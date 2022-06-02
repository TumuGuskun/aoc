from collections import defaultdict

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.read().split()))


def next_coord(row, col):
    if col == 1:
        return 1, row + 1
    else:
        return row + 1, col - 1


@timed
def part1(coordinates):
    end_row, end_col, curr_code = coordinates
    curr_row = curr_col = 1
    paper = defaultdict(lambda: defaultdict(int))
    while curr_row != end_row or curr_col != end_col:
        curr_row, curr_col = next_coord(curr_row, curr_col)
        curr_code *= 252533
        curr_code %= 33554393
    print(curr_code)


@timed
def part2(coordinates):
    pass


if __name__ == '__main__':
    coordinate_list = read()
    part1(coordinate_list)
    part2(coordinate_list)
