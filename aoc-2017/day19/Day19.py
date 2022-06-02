import re

from shared.Util import timed, Point

DIR_MAP = {
    'u': Point(-1, 0),
    'd': Point(1, 0),
    'l': Point(0, -1),
    'r': Point(0, 1)
}


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: x.rstrip() + ' ' * (201 - len(x)), input_file.readlines()))


def move(position, direction, grid, letters):
    if m := re.match(r'[A-Z|-]', grid[position.x][position.y]):
        if m.string.isalpha():
            letters.append(m.string)
        return position + DIR_MAP[direction], direction
    else:
        if direction == 'u' or direction == 'd':
            for new_dir in ['l', 'r']:
                new_point = position + DIR_MAP[new_dir]
                if new_point.is_valid(upper_x=200, upper_y=200):
                    if grid[new_point.x][new_point.y] == '-':
                        return new_point, new_dir
        else:
            for new_dir in ['u', 'd']:
                new_point = position + DIR_MAP[new_dir]
                if new_point.is_valid(upper_x=200, upper_y=200):
                    if grid[new_point.x][new_point.y] == '|':
                        return new_point, new_dir


@timed
def part1(mazes):
    position = Point(0, 1)
    direction = 'd'
    count = 0
    letters = []
    while pos_dir := move(position, direction, mazes, letters):
        position, direction = pos_dir
        count += 1
    print(''.join(letters), count)


@timed
def part2(mazes):
    pass


if __name__ == '__main__':
    maze_list = read()
    part1(maze_list)
    part2(maze_list)
