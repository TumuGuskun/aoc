from copy import copy
from typing import Any

from shared.grid import Grid
from shared.point import Point
from shared.util import get_puzzle, run, timed
from shared.vector import Vector


def parse_data(input_data: str) -> Any:
    return Grid(input_data.splitlines())


def move_beam(grid: Grid, beam: Vector, seen: set[Vector]) -> None:
    while grid.check_point_in_bounds(beam.position) and beam not in seen:
        seen.add(copy(beam))
        if grid.get_point(beam.position) == "\\":
            if beam.direction == ">":
                beam.direction = "v"
            elif beam.direction == "<":
                beam.direction = "^"
            elif beam.direction == "^":
                beam.direction = "<"
            elif beam.direction == "v":
                beam.direction = ">"
        elif grid.get_point(beam.position) == "/":
            if beam.direction == ">":
                beam.direction = "^"
            elif beam.direction == "<":
                beam.direction = "v"
            elif beam.direction == "^":
                beam.direction = ">"
            elif beam.direction == "v":
                beam.direction = "<"
        elif grid.get_point(beam.position) == "|":
            if beam.direction == ">" or beam.direction == "<":
                beam.direction = "v"
                beam_copy = Vector(beam.position, "^")
                move_beam(grid=grid, beam=beam_copy, seen=seen)
        elif grid.get_point(beam.position) == "-":
            if beam.direction == "^" or beam.direction == "v":
                beam.direction = ">"
                beam_copy = Vector(beam.position, "<")
                move_beam(grid=grid, beam=beam_copy, seen=seen)

        beam.move()


@timed
def part_1(grid: Grid) -> int:
    beam = Vector(Point(0, 0), ">")
    seen = set()
    move_beam(grid=grid, beam=beam, seen=seen)

    return len({vector.position for vector in seen})


@timed
def part_2(grid: Grid) -> int:
    max_energy = 0
    seen = set()
    for i in range(grid.height):
        beam = Vector(Point(i, 0), ">")
        seen.clear()
        move_beam(grid=grid, beam=beam, seen=seen)
        max_energy = max(max_energy, len({vector.position for vector in seen}))

        beam = Vector(Point(i, grid.width - 1), "<")
        seen.clear()
        move_beam(grid=grid, beam=beam, seen=seen)
        max_energy = max(max_energy, len({vector.position for vector in seen}))

    for j in range(grid.width):
        beam = Vector(Point(0, j), "v")
        seen.clear()
        move_beam(grid=grid, beam=beam, seen=seen)
        max_energy = max(max_energy, len({vector.position for vector in seen}))

        beam = Vector(Point(grid.height - 1, j), "^")
        seen.clear()
        move_beam(grid=grid, beam=beam, seen=seen)
        max_energy = max(max_energy, len({vector.position for vector in seen}))

    return max_energy


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
