from shared.Util import *
from shared.point import Point


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(f'day17/{file_name}') as input_file:
        return get_ints(input_file.read())


@timed
def part1(spaces):
    print(spaces)
    x1, x2, y1, y2 = spaces

    vels = []
    for xv in range(25):
        for yv in range(75, 125):
            point = Point(0, 0, xv, yv)

            max_height = 0
            while point.y >= y1 and point.x <= x2:
                point.move()
                max_height = max(point.y, max_height)
                point.v_x -= 1 if point.v_x > 0 else (-1 if point.v_x < 0 else 0)
                point.v_y -= 1
                if point.x in range(x1, x2) and point.y in range(y1, y2):
                    vels.append((max_height, xv, yv))
                    break

    print(max(vels))


@timed
def part2(spaces):
    x1, x2, y1, y2 = spaces

    velocities = set()
    for xv in range(23, 287):
        for yv in range(-101, 101):
            point = Point(0, 0, xv, yv)

            while point.y >= y1:
                point.move()
                point.v_x = max(point.v_x - 1, 0)
                point.v_y -= 1
                if point.x in range(x1, x2 + 1) and point.y in range(y1, y2 + 1):
                    velocities.add((xv, yv))
                    break

    print(len(velocities))


if __name__ == '__main__':
    space_list = read()
    part1(space_list)
    part2(space_list)
