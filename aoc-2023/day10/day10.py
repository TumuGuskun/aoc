from __future__ import annotations

from dataclasses import dataclass

from shared.grid import EAST, NORTH, SOUTH, WEST, Grid
from shared.point import Point
from shared.util import coordinate, get_puzzle, run, timed


def parse_data(input_data: str) -> Grid:
    grid = Grid(input_data.splitlines())
    return grid


@dataclass(frozen=True)
class Pipe:
    pipe_type: str
    coordinates: Point

    def get_adjacent_pipes(self, grid: Grid) -> list[Pipe]:
        if self.pipe_type == "|":
            coordinate_1 = self.coordinates + NORTH
            coordinate_2 = self.coordinates + SOUTH
        elif self.pipe_type == "-":
            coordinate_1 = self.coordinates + EAST
            coordinate_2 = self.coordinates + WEST
        elif self.pipe_type == "7":
            coordinate_1 = self.coordinates + SOUTH
            coordinate_2 = self.coordinates + WEST
        elif self.pipe_type == "J":
            coordinate_1 = self.coordinates + NORTH
            coordinate_2 = self.coordinates + WEST
        elif self.pipe_type == "F":
            coordinate_1 = self.coordinates + SOUTH
            coordinate_2 = self.coordinates + EAST
        elif self.pipe_type == "L":
            coordinate_1 = self.coordinates + NORTH
            coordinate_2 = self.coordinates + EAST
        else:
            raise Exception

        return [
            Pipe(
                pipe_type=grid.get_point(coordinate_1),
                coordinates=coordinate_1,
            ),
            Pipe(
                pipe_type=grid.get_point(coordinate_2),
                coordinates=coordinate_2,
            ),
        ]


NORTH_RECEIVING = ["|", "7", "F"]
SOUTH_RECEIVING = ["|", "J", "L"]
EAST_RECEIVING = ["-", "7", "J"]
WEST_RECEIVING = ["-", "F", "L"]


def infer_start_pipe(point: Point, grid: Grid) -> Pipe:
    if grid.get_point(point + NORTH) in NORTH_RECEIVING:
        if grid.get_point(point + SOUTH) in SOUTH_RECEIVING:
            return Pipe(pipe_type="|", coordinates=point)
        elif grid.get_point(point + EAST) in EAST_RECEIVING:
            return Pipe(pipe_type="L", coordinates=point)
        elif grid.get_point(point + WEST) in WEST_RECEIVING:
            return Pipe(pipe_type="J", coordinates=point)

    elif grid.get_point(point + SOUTH) in SOUTH_RECEIVING:
        if grid.get_point(point + NORTH) in NORTH_RECEIVING:
            return Pipe(pipe_type="|", coordinates=point)
        if grid.get_point(point + EAST) in EAST_RECEIVING:
            return Pipe(pipe_type="F", coordinates=point)
        elif grid.get_point(point + WEST) in WEST_RECEIVING:
            return Pipe(pipe_type="7", coordinates=point)

    elif grid.get_point(point + WEST) in WEST_RECEIVING:
        if grid.get_point(point + EAST) in EAST_RECEIVING:
            return Pipe(pipe_type="-", coordinates=point)
        elif grid.get_point(point + NORTH) in NORTH_RECEIVING:
            return Pipe(pipe_type="J", coordinates=point)
        elif grid.get_point(point + SOUTH) in SOUTH_RECEIVING:
            return Pipe(pipe_type="7", coordinates=point)

    elif grid.get_point(point + EAST) in EAST_RECEIVING:
        if grid.get_point(point + WEST) in WEST_RECEIVING:
            return Pipe(pipe_type="-", coordinates=point)
        elif grid.get_point(point + NORTH) in NORTH_RECEIVING:
            return Pipe(pipe_type="L", coordinates=point)
        elif grid.get_point(point + SOUTH) in SOUTH_RECEIVING:
            return Pipe(pipe_type="F", coordinates=point)

    raise Exception


def get_loop(grid: Grid) -> list[Pipe]:
    start_point = grid.find("S")[0]
    start_pipe = infer_start_pipe(point=start_point, grid=grid)
    grid.set_point(start_point, start_pipe.pipe_type)

    curr_pipe = start_pipe.get_adjacent_pipes(grid=grid)[0]

    seen = {start_pipe, curr_pipe}
    maze = [start_pipe, curr_pipe]
    stack = [curr_pipe]

    while len(stack) > 0:
        curr_pipe = stack.pop()
        adjacent_pipes = curr_pipe.get_adjacent_pipes(grid=grid)
        for adjacent_pipe in adjacent_pipes:
            if adjacent_pipe not in seen:
                seen.add(adjacent_pipe)
                stack.append(adjacent_pipe)
                maze.append(adjacent_pipe)

    return maze


@timed
def part_1(grid: Grid) -> int:
    loop = get_loop(grid=grid)

    return len(loop) // 2


def dot_in_loop(dot: Point, loop: set[Point], grid: Grid) -> bool:
    if dot in loop:
        return False

    edge_count = 0
    for i in range(dot.i):
        point = Point(i, dot.j)
        pipe_type = grid.get_point(Point(i, dot.j))

        if point in loop:
            if pipe_type in ["7", "L"]:
                edge_count += 0.5
            elif pipe_type in ["F", "J"]:
                edge_count += -0.5
            elif pipe_type == "-":
                edge_count += 1

    return int(edge_count) % 2 == 1


@timed
def part_2(grid: Grid) -> int:
    loop = set(pipe.coordinates for pipe in get_loop(grid=grid))

    return len([_ for dot, _ in coordinate(grid) if dot_in_loop(dot, loop, grid)])


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(puzzle=puzzle, part_1=part_1, part_2=part_2, parser=parse_data)


if __name__ == "__main__":
    main()
