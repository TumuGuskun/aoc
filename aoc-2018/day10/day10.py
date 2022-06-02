import re

from shared.Util import timed, Point, get_ints


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        points = []
        for line in input_file.readlines():
            search = get_ints(line)
            points.append((search[:2], search[2:]))
        return points


@timed
def part1(points):
    points = [Point(x, y, v_x, v_y) for ((x, y), (v_x, v_y)) in points]
    count = 0
    while True:
        max_x = max(p.x for p in points)
        min_x = min(p.x for p in points)
        max_y = max(p.y for p in points)
        min_y = min(p.y for p in points)

        if max_y - min_y == 9:
            for j in range(min_y, max_y + 1):
                line = ''
                for i in range(min_x, max_x + 1):
                    line += '#' if Point(i, j) in points else '.'
                print(line)
            print(count)
            return

        for point in points:
            point.move()

        count += 1


@timed
def part2(points):
    pass


if __name__ == '__main__':
    point_list = read()
    part1(point_list)
    part2(point_list)
