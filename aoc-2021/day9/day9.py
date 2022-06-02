from math import prod

from shared.Util import *
from shared.bfs import BFS


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        grid = [list(map(int, line.rstrip())) for line in input_file]
        return Grid(grid)


@timed
def part1(grid):
    print(sum(1 + e for (i, j), e in coordinate(grid) if min(grid.neighbors(i, j), key=second)[1] > e))


@timed
def part2(grid):
    print(prod(sorted([BFS(start, grid, lambda _, __: False, lambda p, g: map(first, filter(lambda n: n[1] != 9, g.neighbors(*p)))).run().count for start in [(i, j) for (i, j), e in coordinate(grid) if min(grid.neighbors(i, j), key=second)[1] > e]], reverse=True)[:3]))


if __name__ == '__main__':
    grid_list = read()
    part1(grid_list)
    part2(grid_list)
