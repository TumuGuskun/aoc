from itertools import combinations

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return [list(map(int, line.split())) for line in input_file.readlines()]


@timed
def part1(rows):
    print(sum(map(lambda x: max(x) - min(x), rows)))


@timed
def part2(rows):
    print(sum(b // a for row in rows for a, b in combinations(sorted(row), 2) if b % a == 0))


if __name__ == '__main__':
    row_list = read()
    part1(row_list)
    part2(row_list)
