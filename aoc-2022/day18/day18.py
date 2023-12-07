from __future__ import annotations
from dataclasses import dataclass
import os
from queue import Queue
from typing import Set
from tqdm import tqdm

from shared.gum import gum_choose
from shared.util import timed, get_ints


@dataclass(frozen=True)
class Cube:
    x: int
    y: int
    z: int

    def __add__(self, other: Cube) -> Cube:
        return Cube(self.x + other.x, self.y + other.y, self.z + other.z)

    @property
    def neighbors(self) -> list[Cube]:
        return [
            self + Cube(1, 0, 0),
            self + Cube(-1, 0, 0),
            self + Cube(0, 1, 0),
            self + Cube(0, -1, 0),
            self + Cube(0, 0, 1),
            self + Cube(0, 0, -1),
        ]

    def can_reach(self, dest_cubes: Set[Cube], cubes: Set[Cube]) -> bool:
        queue = Queue()
        queue.put(self)
        seen = set()
        seen.add(self)
        while not queue.empty():
            curr_cube = queue.get()

            if curr_cube in dest_cubes:
                return True

            for neighbor in curr_cube.neighbors:
                if neighbor not in cubes and neighbor not in seen:
                    seen.add(neighbor)
                    queue.put(neighbor)

        return False


@timed
def read() -> Set[Cube]:
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return {Cube(*get_ints(line)) for line in input_file.readlines()}


@timed
def part1(droplets: Set[Cube]) -> None:
    print(
        sum(
            sum(1 for neighbor in droplet.neighbors if neighbor not in droplets)
            for droplet in droplets
        )
    )


@timed
def part2(droplets: Set[Cube]) -> None:
    outside_cubes = {
        Cube(0, 0, 0),
        Cube(20, 20, 20),
        Cube(0, 20, 0),
        Cube(20, 0, 0),
        Cube(0, 0, 20),
        Cube(20, 20, 0),
        Cube(20, 0, 20),
        Cube(0, 20, 20),
    }
    total = 0
    for droplet in tqdm(droplets):
        for neighbor in droplet.neighbors:
            if neighbor not in droplets and neighbor.can_reach(
                dest_cubes=outside_cubes, cubes=droplets
            ):
                total += 1
    print(total)


if __name__ == "__main__":
    droplet_list = read()
    part1(droplet_list)
    part2(droplet_list)
