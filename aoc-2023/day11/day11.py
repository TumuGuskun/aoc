from copy import copy
from typing import Any

import numpy as np

from shared.grid import Grid
from shared.point import Point
from shared.util import get_puzzle, run, timed


def parse_data(input_data: str) -> Any:
    return Grid(input_data.splitlines())


def get_empty_rows_columns(grid: Grid) -> tuple[list[int], list[int]]:
    rows = []
    for i in range(grid.height):
        if np.count_nonzero(grid.get_row(i) == "#") == 0:
            rows.append(i)

    columns = []
    for j in range(grid.width):
        if np.count_nonzero(grid.get_column(j) == "#") == 0:
            columns.append(j)

    return rows, columns


def get_updated_man_distance(
    point_a: Point,
    point_b: Point,
    extra_distance: int,
    empty_rows: list[int],
    empty_columns: list[int],
) -> int:
    regular_man_distance = point_a.man_distance(point_b)
    empty_rows_between = len(
        [
            1
            for row in empty_rows
            if point_a.i < row < point_b.i or point_b.i < row < point_a.i
        ]
    )
    empty_columns_between = len(
        [
            1
            for column in empty_columns
            if point_a.j < column < point_b.j or point_b.j < column < point_a.j
        ]
    )
    return regular_man_distance + extra_distance * (
        empty_rows_between + empty_columns_between
    )


@timed
def part_1(grid: Grid) -> Any:
    # Body Logic
    empty_rows, empty_columns = get_empty_rows_columns(grid=grid)
    total = 0
    galaxies = grid.find("#")

    for i, galaxy in enumerate(galaxies):
        for j in range(i + 1, len(galaxies)):
            man_distance = get_updated_man_distance(
                galaxy, galaxies[j], 1, empty_rows, empty_columns
            )
            total += man_distance

    return total


@timed
def part_2(grid: Grid) -> Any:
    # Body Logic
    empty_rows, empty_columns = get_empty_rows_columns(grid=grid)
    total = 0
    galaxies = grid.find("#")

    for i, galaxy in enumerate(galaxies):
        for j in range(i + 1, len(galaxies)):
            man_distance = get_updated_man_distance(
                galaxy, galaxies[j], 999999, empty_rows, empty_columns
            )
            total += man_distance

    return total


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(
        puzzle=puzzle,
        part_1=part_1,
        part_2=part_2,
        parser=parse_data,
        force_run_2=True,
    )


if __name__ == "__main__":
    main()
