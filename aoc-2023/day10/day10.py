from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from shared.grid import Grid, NORTH, SOUTH, EAST, WEST
from aocd.examples import Example

from shared.point import Point
from shared.util import coordinate, get_puzzle, run, timed


def parse_data(input_data: str) -> Any:
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
def part_1(input_data: str) -> Any:
    grid: Grid = parse_data(input_data=input_data)

    # Body Logic
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
def part_2(input_data: str) -> Any:
    grid: Grid = parse_data(input_data=input_data)

    # Body Logic
    loop = set(pipe.coordinates for pipe in get_loop(grid=grid))

    return len(
        [_ for dot, _ in coordinate(grid) if dot_in_loop(Point(*dot), loop, grid)]
    )


def main() -> None:
    puzzle = get_puzzle(__file__)
    puzzle._get_examples = lambda parser_name=None: [
        Example(
            input_data="-L|F7\n7S-7|\nL|7||\n-L-J|\nL|-JF",
            answer_a="4",
            answer_b="",
        ),
        Example(
            input_data="..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ...",
            answer_a="8",
            answer_b="",
        ),
        Example(
            input_data="""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""",
            answer_a="",
            answer_b="4",
        ),
        Example(
            input_data="""..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........""",
            answer_a="",
            answer_b="4",
        ),
        Example(
            input_data=""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""",
            answer_a="",
            answer_b="8",
        ),
        Example(
            input_data="""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""",
            answer_a="",
            answer_b="10",
        ),
    ]
    run(puzzle=puzzle, part_1=part_1, part_2=part_2)


if __name__ == "__main__":
    main()
