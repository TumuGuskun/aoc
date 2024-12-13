from copy import copy
from typing import Any

from shared.util import *
from shared.grid import *
from shared.vector import *


def parse_data(input_data: str) -> Any:
    return Grid(input_data.splitlines(), edges=[])


def run_guard(grid: Grid, guard: Vector) -> tuple[set[Vector], bool]:
    visited = set()
    while grid.check_point_valid(guard.position):
        if guard in visited:
            return visited, True
        visited.add(copy(guard))
        guard.move()
        if grid.get_point_if_valid(guard.position) == "#":
            guard.move_back()
            guard.rotate_r()
    return visited, False


def part_1(grid: Grid) -> int:
    guard = Vector(grid.find("^")[0], "^")
    visited, _ = run_guard(grid, guard)

    return len(set(vector.position for vector in visited))


def part_2(grid: Grid) -> int:
    count = 0

    guard = Vector(grid.find("^")[0], "^")
    visited, _ = run_guard(grid, guard)

    for point in set(vector.position for vector in visited):
        value = grid.get_point(point)

        if value != ".":
            continue

        guard = Vector(grid.find("^")[0], "^")
        grid.set_point(point, "#")

        _, loop = run_guard(grid, guard)
        if loop:
            count += 1

        grid.set_point(point, ".")

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
