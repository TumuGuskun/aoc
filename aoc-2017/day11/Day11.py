from fractions import Fraction
from math import sqrt

from shared.Util import timed, Point

directions = {
    'n': Point(0, 1),
    'nw': Point(-1, 1),
    'ne': Point(1, 1),
    's': Point(0, -1),
    'sw': Point(-1, -1),
    'se': Point(1, -1),
}


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(input_file.read().split(','))


@timed
def part1(steps):
    start = Point(0, 0)
    maximum = start
    for step in steps:
        start += directions[step]
        maximum = max(maximum, start)
    print(max(abs(start.x), abs(start.y)))
    print(max(abs(maximum.x), abs(maximum.y)))


@timed
def part2(steps):
    pass


if __name__ == '__main__':
    step_list = read()
    part1(step_list)
    part2(step_list)
