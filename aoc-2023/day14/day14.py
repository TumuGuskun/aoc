from typing import Any

import numpy as np

from shared.grid import NORTH, SOUTH, Grid
from shared.util import coordinate, get_puzzle, run, timed


def parse_data(input_data: str) -> Any:
    return Grid(input_data.splitlines())


def tilt(grid: Grid) -> None:
    for point, element in coordinate(grid):
        if element == "O":
            grid.set_point(point, ".")
            next_point = point + NORTH
            while next_point.is_valid() and grid.get_point(point=next_point) == ".":
                next_point += NORTH

            grid.set_point(point=next_point + SOUTH, value="O")


def calculate_load(grid: Grid) -> int:
    load = 0
    for point, element in coordinate(grid):
        if element == "O":
            load += grid.height - point.i

    return load


@timed
def part_1(grid: Grid) -> int:
    tilt(grid=grid)

    return calculate_load(grid=grid)


def cycle(grid: Grid) -> None:
    for _ in range(4):
        tilt(grid=grid)
        grid.grid = np.rot90(grid.grid, k=-1)


@timed
def part_2(grid: Grid) -> int:
    cycle_count = 0
    seen = {}
    while f"{grid.grid}" not in seen:
        seen[f"{grid.grid}"] = cycle_count
        cycle(grid=grid)
        cycle_count += 1

    cycle_length = cycle_count - seen[f"{grid.grid}"]
    remainder = (1000000000 - cycle_count) % cycle_length

    for _ in range(remainder):
        cycle(grid=grid)

    return calculate_load(grid=grid)


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(
        puzzle=puzzle,
        part_1=part_1,
        part_2=part_2,
        parser=parse_data,
    )


if __name__ == "__main__":
    main()
