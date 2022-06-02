from day2.directions import STANDARD_DIRECTIONS, FANCY_DIRECTIONS
from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: x.rstrip().lower(), input_file.readlines()))


@timed
def part1(directions):
    code = []
    curr = 5
    for number in directions:
        for direction in number:
            curr = STANDARD_DIRECTIONS[curr][direction]
        code.append(curr)

    print(''.join(map(str, code)))


@timed
def part2(directions):
    code = []
    curr = 5
    for number in directions:
        for direction in number:
            curr = FANCY_DIRECTIONS[curr][direction]
        code.append(curr)

    print(''.join(map(str, code)).upper())


if __name__ == '__main__':
    direction_list = read()
    part1(direction_list)
    part2(direction_list)
