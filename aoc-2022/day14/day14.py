import os
import numpy as np

from shared.gum import gum_choose
from shared.grid import Grid
from shared.point import Point
from shared.util import timed, chunk, get_ints


START_COL_MOD = 325
END_COL_MOD = 325


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        grid = Grid(
            grid=np.chararray((174, 1000 - START_COL_MOD - END_COL_MOD), unicode=True)
        )
        grid.grid[:] = "."
        for line in input_file.readlines():
            walls = list(chunk(get_ints(line), 2))
            for next_index, (j1, i1) in enumerate(walls[:-1], start=1):
                j2, i2 = walls[next_index]
                if i1 == i2:
                    for j in range(min(j1, j2), max(j1, j2) + 1):
                        grid.set_point(i1, j - START_COL_MOD, "#")
                else:
                    for i in range(min(i1, i2), max(i1, i2) + 1):
                        grid.set_point(i, j1 - START_COL_MOD, "#")
    return grid


def move_sand(sand: Point, grid: Grid) -> Point:
    if grid.get_point(i=sand.i + 1, j=sand.j) == ".":
        return Point(sand.i + 1, sand.j)
    if grid.get_point(i=sand.i + 1, j=sand.j - 1) == ".":
        return Point(sand.i + 1, sand.j - 1)
    if grid.get_point(i=sand.i + 1, j=sand.j + 1) == ".":
        return Point(sand.i + 1, sand.j + 1)
    return sand


@timed
def part1(grid: Grid):
    count = 0
    try:
        while True:
            sand = Point(i=0, j=500 - START_COL_MOD)
            while True:
                new_sand = move_sand(sand=sand, grid=grid)
                if new_sand == sand:
                    count += 1
                    grid.set_point(i=sand.i, j=sand.j, value="o")
                    break
                sand = new_sand
    except:
        print(count)


@timed
def part2(grid: Grid):
    grid.grid[173] = "#"
    count = 0
    sand_start = Point(i=0, j=500 - START_COL_MOD)
    while True:
        sand = sand_start
        while True:
            new_sand = move_sand(sand=sand, grid=grid)
            if new_sand == sand:
                count += 1
                grid.set_point(i=sand.i, j=sand.j, value="o")
                break
            sand = new_sand
        if sand == sand_start:
            break
    print(count + 1068)


if __name__ == "__main__":
    wall_list = read()
    part1(wall_list)
    part2(wall_list)
