from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os
import re
import numpy as np

from shared.grid import Grid
from shared.gum import gum_choose
from shared.util import timed
from shared.point import Point
from shared.vector import Vector


@timed
def read() -> tuple[Grid, list]:
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    empty_grid = np.chararray((200, 150), unicode=True)
    grid = Grid(grid=empty_grid, edges=["#"])
    with open(file_name) as input_file:
        read_instructions = False
        instructions = []
        for i, line in enumerate(input_file.readlines()):
            if read_instructions:
                instructions = re.split(r"(\d+)", line.strip())
                instructions = [
                    int(e) if e.isnumeric() else ">" if e == "R" else "<"
                    for e in instructions
                    if e
                ]
            elif line == "\n":
                read_instructions = True
            else:
                line = line.rstrip()
                for j, char in enumerate(line.ljust(150, " ")):
                    grid.set_point(Point(i, j), char)

    return grid, instructions


@timed
def part1(grid: Grid, instructions: list[str | int]) -> None:
    j = next(j for j, char in enumerate(grid.get_row(i=0)) if char == ".")
    player = Vector(position=Point(i=0, j=j), direction=">")
    while instructions:
        grid.set_point(point=player.position, value=player.direction)
        print(grid)
        input()
        grid.set_point(point=player.position, value=".")
        curr_instr, *instructions = instructions
        if isinstance(curr_instr, int):
            for _ in range(curr_instr):
                player.move()
                point = player.position
                new_i, new_j = point.i, point.j
                if (
                    not grid.check_point_in_bounds(point=point)
                    or grid.get_point(point=point) == " "
                ):
                    if point.i < 0:
                        new_i = grid.height - next(
                            i
                            for i, char in enumerate(
                                reversed(grid.get_column(j=point.j)), start=1
                            )
                            if char != " "
                        )
                    if point.i > grid.height - 1:
                        new_i = next(
                            i
                            for i, char in enumerate(grid.get_column(j=point.j))
                            if char != " "
                        )
                    if point.j < 0:
                        new_j = grid.width - next(
                            j
                            for j, char in enumerate(
                                reversed(grid.get_row(i=point.i)), start=1
                            )
                            if char != " "
                        )
                    if point.j > grid.height - 1:
                        new_j = next(
                            j
                            for j, char in enumerate(grid.get_row(i=point.i))
                            if char != " "
                        )
                new_position = Point(i=new_i, j=new_j)
                if grid.get_point(point=new_position) == "#":
                    player.move_back()
                else:
                    player.position = new_position

        else:
            player.rotate(curr_instr)
    print(player)


@timed
def part2(grid: Grid, instructions: list[str | int]) -> None:
    pass


if __name__ == "__main__":
    grid, instruction_list = read()
    part1(grid, instruction_list)
    part2(grid, instruction_list)
