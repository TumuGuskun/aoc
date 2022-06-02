from collections import defaultdict

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        enhance_map = input_file.readline().rstrip()
        enhance_map = enhance_map.replace('#', '1').replace('.', '0')
        input_file.readline()
        grid = defaultdict(lambda: defaultdict(lambda: '0'))
        for (i, j), v in coordinate(list(map(lambda x: x.rstrip(), input_file.readlines()))):
            grid[i][j] = '0' if v == '.' else '1'

        return enhance_map, grid


@timed
def part1(maps):
    enhance_map, grid = maps

    for _ in range(2):
        fill_char = '0' if _ % 2 == 0 else '1'
        new_grid = defaultdict(lambda: defaultdict(lambda: fill_char))
        i_range = range(min(grid.keys()) - 1, max(grid.keys()) + 2)
        j_range = range(min(map(min, grid.values())) - 1, max(map(max, grid.values())) + 2)
        for i in i_range:
            for j in j_range:
                new_grid[i][j] = enhance_map[enhance_index(i, j, grid)]

        grid = new_grid

    print(sum(1 for row in grid.values() for v in row.values() if v == '1'))


def enhance_index(i, j, grid):
    return int(''.join([grid[i - 1][j - 1], grid[i - 1][j], grid[i - 1][j + 1],
                        grid[i][j - 1],     grid[i][j],     grid[i][j + 1],
                        grid[i + 1][j - 1], grid[i + 1][j], grid[i + 1][j + 1]]), 2)


def print_grid(grid):
    for i in range(min(grid.keys()), max(grid.keys()) + 1):
        line = ''
        for j in range(min(map(min, grid.values())), max(map(max, grid.values())) + 1):
            line += '# ' if grid[i][j] == '1' else '. '
        print(line)


@timed
def part2(maps):
    enhance_map, grid = maps

    for _ in range(50):
        fill_char = '0' if _ % 2 == 0 else '1'
        new_grid = defaultdict(lambda: defaultdict(lambda: fill_char))
        i_range = range(min(grid.keys()) - 1, max(grid.keys()) + 2)
        j_range = range(min(map(min, grid.values())) - 1, max(map(max, grid.values())) + 2)
        for i in i_range:
            for j in j_range:
                new_grid[i][j] = enhance_map[enhance_index(i, j, grid)]

        grid = new_grid

    print(sum(1 for row in grid.values() for v in row.values() if v == '1'))


if __name__ == '__main__':
    map_list = read()
    part1(map_list)
    part2(map_list)
