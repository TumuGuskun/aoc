from functools import cache
from typing import Any

from shared.util import *


def parse_data(input_data: str) -> Any:
    return Grid(input_data.splitlines(), edges=[])


@cache
def get_reachable_nines(grid: Grid, trailhead: Point) -> set[Point]:
    value = grid.get_point(trailhead)

    if value == 9:
        return {trailhead}

    reachable_nines = set()
    for neighbor_point, neighbor_value in grid.get_adjacents(trailhead):
        if neighbor_value == value + 1:
            reachable_nines.update(get_reachable_nines(grid, neighbor_point))

    return reachable_nines


@cache
def get_trail_ratings(grid: Grid, trailhead: Point) -> int:
    value = grid.get_point(trailhead)

    if value == 9:
        return 1

    trail_ratings = 0
    for neighbor_point, neighbor_value in grid.get_adjacents(trailhead):
        if neighbor_value == value + 1:
            trail_ratings += get_trail_ratings(grid, neighbor_point)

    return trail_ratings


def part_1(grid: Grid) -> int:
    count = 0

    for trailhead in grid.find(0):
        reachable_nines = get_reachable_nines(grid, trailhead)
        count += len(reachable_nines)

    return count


def part_2(grid: Grid) -> int:
    count = 0

    for trailhead in grid.find(0):
        trail_ratings = get_trail_ratings(grid, trailhead)
        count += trail_ratings

    return count


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
