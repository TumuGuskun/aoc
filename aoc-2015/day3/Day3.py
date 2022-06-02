from shared.Util import timed, Point
from collections import defaultdict


MAP = {
    '<': Point(-1, 0),
    '>': Point(1, 0),
    'v': Point(0, -1),
    '^': Point(0, 1)
}


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.read()


@timed
def part1(directions):
    spots = defaultdict(int)
    spots[Point(0, 0)] += 1
    curr_spot = Point(0, 0)
    for direction in directions:
        curr_spot += MAP[direction]
        spots[curr_spot] += 1

    print(len(spots))


@timed
def part2(directions):
    spots = defaultdict(int)
    spots[Point(0, 0)] += 2
    santa_spot = Point(0, 0)
    robo_spot = Point(0, 0)
    for i, direction in enumerate(directions):
        if i % 2 == 0:
            santa_spot += MAP[direction]
            spots[santa_spot] += 1
        else:
            robo_spot += MAP[direction]
            spots[robo_spot] += 1

    print(len(spots))


if __name__ == '__main__':
    direction_list = read()
    part1(direction_list)
    part2(direction_list)
