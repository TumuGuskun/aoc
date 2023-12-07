from collections import Counter
from dataclasses import dataclass, field
from typing import Optional
import numpy as np
import os

from shared.gum import gum_choose
from shared.grid import Grid
from shared.point import Point
from shared.util import timed, coordinate


PADDING = 1000


def check_up(elf, neighbors: list[tuple[int, int]]) -> Optional[Point]:
    if len(neighbors) == 8:
        return None
    if (
        (elf.x - 1, elf.y) not in neighbors
        or (elf.x - 1, elf.y - 1) not in neighbors
        or (elf.x - 1, elf.y + 1) not in neighbors
    ):
        return None
    return Point(elf.x - 1, elf.y)


def check_down(elf, neighbors: list[tuple[int, int]]) -> Optional[Point]:
    if len(neighbors) == 8:
        return None
    if (
        (elf.x + 1, elf.y) not in neighbors
        or (elf.x + 1, elf.y - 1) not in neighbors
        or (elf.x + 1, elf.y + 1) not in neighbors
    ):
        return None
    return Point(elf.x + 1, elf.y)


def check_left(elf, neighbors: list[tuple[int, int]]) -> Optional[Point]:
    if len(neighbors) == 8:
        return None
    if (
        (elf.x, elf.y - 1) not in neighbors
        or (elf.x - 1, elf.y - 1) not in neighbors
        or (elf.x + 1, elf.y - 1) not in neighbors
    ):
        return None
    return Point(elf.x, elf.y - 1)


def check_right(elf, neighbors: list[tuple[int, int]]) -> Optional[Point]:
    if len(neighbors) == 8:
        return None
    if (
        (elf.x, elf.y + 1) not in neighbors
        or (elf.x - 1, elf.y + 1) not in neighbors
        or (elf.x + 1, elf.y + 1) not in neighbors
    ):
        return None
    return Point(elf.x, elf.y + 1)


MOVE_CHECKS = [check_up, check_down, check_left, check_right]


@dataclass
class Elf:
    position: Point
    proposed_move: Point = field(default_factory=lambda: Point(0, 0))

    def propose_move(self, grid: Grid, round: int) -> Point:
        neighbors = [n[0] for n in grid.get_neighbors(self.position.i, self.position.j)]
        for i in range(4):
            if (
                move := MOVE_CHECKS[(i + round) % 4](self.position, neighbors)
            ) is not None:
                self.proposed_move = move
                return self.proposed_move
        self.proposed_move = self.position
        return self.proposed_move

    def move(self, grid: Grid) -> None:
        grid.set_point(self.position.i, self.position.j, ".")
        self.position = self.proposed_move
        grid.set_point(self.position.i, self.position.j, "#")


@timed
def read() -> tuple[Grid, list[Elf]]:
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name, "r") as input_file:
        input_lines = input_file.readlines()
        lines = ["." * PADDING + line.strip() + "." * PADDING for line in input_lines]
        top_bot = ["." * len(lines[0])] * PADDING
        lines = top_bot + lines + top_bot
        elves = [Elf(Point(x, y)) for (x, y), char in coordinate(lines) if char == "#"]
        return Grid(grid=lines, edges=["#"]), elves


@timed
def part1(grid: Grid, elves: list[Elf]) -> None:
    for i in range(10):
        proposed_moves = Counter()
        for elf in elves:
            proposed_moves[elf.propose_move(grid=grid, round=i)] += 1

        for elf in elves:
            if proposed_moves[elf.proposed_move] == 1:
                elf.move(grid=grid)

    final_elves = np.argwhere(grid.grid == "#")
    max_x, _ = max(final_elves, key=lambda e: e[0])
    min_x, _ = min(final_elves, key=lambda e: e[0])
    _, max_y = max(final_elves, key=lambda e: e[1])
    _, min_y = min(final_elves, key=lambda e: e[1])

    smol = grid.grid[min_x : max_x + 1, min_y : max_y + 1]
    print((smol == ".").sum())


@timed
def part2(grid: Grid, elves: list[Elf]) -> None:
    counter = 9
    while True:
        counter += 1
        proposed_moves = Counter()
        for elf in elves:
            proposed_moves[elf.propose_move(grid=grid, round=counter)] += 1

        moved = False
        for elf in elves:
            if proposed_moves[elf.proposed_move] == 1:
                if elf.position != elf.proposed_move:
                    elf.move(grid=grid)
                    moved = True

        if not moved:
            print(counter + 1)
            break


if __name__ == "__main__":
    grid, elf_list = read()
    part1(grid, elf_list)
    part2(grid, elf_list)
