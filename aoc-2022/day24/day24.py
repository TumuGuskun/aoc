from dataclasses import dataclass, field
from queue import Queue
from typing import Set
import os


from shared.gum import gum_choose
from shared.grid import Grid
from shared.vector import Vector
from shared.point import Point
from shared.util import timed, coordinate


@dataclass
class Blizzards:
    blizzards: list[Vector]

    def move(self, grid: Grid) -> Set[Point]:
        x_height, y_length = grid.height, grid.width
        points = set()
        for blizzard in self.blizzards:
            blizzard.move()
            if blizzard.position.i == 0:
                blizzard.position.i = x_height - 2
            elif blizzard.position.i == x_height - 1:
                blizzard.position.i = 1
            elif blizzard.position.j == 0:
                blizzard.position.j = y_length - 2
            elif blizzard.position.j == y_length - 1:
                blizzard.position.j = 1
            points.add(blizzard.position)
        return points


@timed
def read() -> tuple[Grid, Blizzards]:
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        grid = Grid(grid=input_file.readlines(), edges=["#"])
    blizzard_positions = []
    for (i, j), v in coordinate(grid):
        if v != "." and v != "#":
            blizzard_positions.append(Vector(position=Point(i, j), direction=v))

    return grid, Blizzards(blizzards=blizzard_positions)


@timed
def part1(grid: Grid, blizzards: Blizzards) -> None:
    queue = Queue()
    start = Point(0, 1)
    dest = Point(36, 100)

    storms = {blizzard.position for blizzard in blizzards.blizzards}
    queue.put((0, [start], start))
    storm_timer = 0
    while not queue.empty():
        curr_storm_timer, curr_path, curr_spot = queue.get()

        if curr_spot == dest:
            print(curr_storm_timer, len(curr_path))
            return

        if curr_storm_timer != storm_timer:
            storm_timer = curr_storm_timer
            print(storm_timer)
            storms = blizzards.move(grid=grid)

        print(grid)
        for neighbor, _ in grid.get_adjacents(curr_spot) + [
            (curr_spot, grid.get_point(curr_spot))
        ]:
            if neighbor not in storms:
                print(neighbor)
                queue.put((curr_storm_timer + 1, curr_path + [neighbor], neighbor))
        input()


@timed
def part2(grid: Grid, blizzards: list[Vector]) -> None:
    pass


if __name__ == "__main__":
    grid, blizzards = read()
    part1(grid, blizzards)
    part2(grid, blizzards)
