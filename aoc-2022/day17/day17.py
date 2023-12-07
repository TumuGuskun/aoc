from dataclasses import dataclass
import os
from typing import Optional, Set
from copy import copy

from shared.gum import gum_choose
from shared.util import timed
from shared.point import Point


CHAMBER_WIDTH = 7


@dataclass
class Rock:
    points: list[Point]
    last_move: Optional[str] = None

    @property
    def lowest_point(self) -> int:
        return min(point.i for point in self.points)

    @property
    def highest_point(self) -> int:
        return max(point.i for point in self.points)

    def move_up(self, n: int = 1) -> None:
        self.points = [point + Point(1 * n, 0) for point in self.points]
        self.last_move = "^"

    def move_down(self, n: int = 1) -> None:
        self.points = [point + Point(-1 * n, 0) for point in self.points]
        self.last_move = "v"

    def move_sideways(self, wind: str) -> None:
        if wind == ">":
            self.points = [point + Point(0, 1) for point in self.points]
            self.last_move = ">"
        else:
            self.points = [point + Point(0, -1) for point in self.points]
            self.last_move = "<"

    def revert(self) -> None:
        match self.last_move:
            case "<":
                self.move_sideways(">")
            case ">":
                self.move_sideways("<")
            case "v":
                self.move_up()
            case "^":
                self.move_down()

    def is_valid(self, occupied_points: Set[Point]) -> bool:
        return (
            all(point not in occupied_points for point in self.points)
            and min(point.j for point in self.points) >= 0
            and max(point.j for point in self.points) < CHAMBER_WIDTH
        )


ROCKS = [
    Rock(points=[Point(0, 2), Point(0, 3), Point(0, 4), Point(0, 5)]),
    Rock(points=[Point(0, 3), Point(1, 2), Point(1, 3), Point(1, 4), Point(2, 3)]),
    Rock(points=[Point(0, 2), Point(0, 3), Point(0, 4), Point(1, 4), Point(2, 4)]),
    Rock(points=[Point(0, 2), Point(1, 2), Point(2, 2), Point(3, 2)]),
    Rock(points=[Point(0, 2), Point(0, 3), Point(1, 2), Point(1, 3)]),
]


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return list(input_file.read().strip())


@timed
def part1(winds: list[str]) -> None:
    occupied_points = {Point(0, j) for j in range(10)}
    curr_top = 0
    j = 0
    for i in range(2022):
        curr_rock = copy(ROCKS[i % len(ROCKS)])
        curr_rock.move_up(n=curr_top + 4)

        while True:
            # do wind stuff
            curr_wind = winds[j % len(winds)]
            j += 1
            curr_rock.move_sideways(wind=curr_wind)
            if not curr_rock.is_valid(occupied_points=occupied_points):
                curr_rock.revert()

            # fall
            curr_rock.move_down()
            if not curr_rock.is_valid(occupied_points=occupied_points):
                curr_rock.revert()
                for point in curr_rock.points:
                    occupied_points.add(point)

                curr_top = max(curr_top, curr_rock.highest_point)
                break

    print(curr_top)


def find_subarray(big_array: list[int], little_array: list[int]) -> Optional[int]:
    first_ptr = 0
    second_ptr = 0

    first_arr_len = len(big_array)
    second_arr_len = len(little_array)

    start = 0
    while first_ptr < first_arr_len and second_ptr < second_arr_len:
        if big_array[first_ptr] == little_array[second_ptr]:
            first_ptr += 1
            second_ptr += 1

            if second_ptr == second_arr_len:
                return start

        else:
            first_ptr = first_ptr - second_ptr + 1
            second_ptr = 0
            start = first_ptr

    return None


@timed
def part2(winds: list[str]) -> None:
    height_change_list = []
    occupied_points = {Point(0, j) for j in range(7)}
    curr_top = 0
    i = 0
    j = 0
    while True:
        curr_rock = copy(ROCKS[i % len(ROCKS)])
        i += 1
        curr_rock.move_up(n=curr_top + 4)

        while True:
            # do wind stuff
            curr_wind = winds[j % len(winds)]
            j += 1
            curr_rock.move_sideways(wind=curr_wind)
            if not curr_rock.is_valid(occupied_points=occupied_points):
                curr_rock.revert()

            # fall
            curr_rock.move_down()
            if not curr_rock.is_valid(occupied_points=occupied_points):
                curr_rock.revert()
                for point in curr_rock.points:
                    occupied_points.add(point)

                next_top = max(curr_top, curr_rock.highest_point)
                height_change_list.append(max(0, next_top - curr_top))
                curr_top = next_top
                break

        if i > 2000 and (
            cycle_start := find_subarray(
                height_change_list[:-200], height_change_list[-200:]
            )
        ):
            cycle_end = i - 200
            break

    cycle_length = cycle_end - cycle_start
    cycle_height_change = sum(height_change_list[cycle_start:cycle_end])
    height = cycle_height_change * (
        (1_000_000_000_000 - cycle_start) // cycle_length
    ) + sum(height_change_list[:cycle_start])
    i = cycle_length * ((1_000_000_000_000 - cycle_start) // cycle_length) + cycle_start

    j = 0
    while i < 1_000_000_000_000:
        height += height_change_list[j]
        i += 1
        j += 1

    print(height)


if __name__ == "__main__":
    wind_list = read()
    part1(wind_list)
    part2(wind_list)
