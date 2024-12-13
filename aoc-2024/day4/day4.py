from typing import Any

from shared.util import *
from shared.grid import *


def parse_data(input_data: str) -> Any:
    return Grid(input_data.splitlines())


def part_1(grid: Grid) -> int:
    count = 0
    for point, value in coordinate(grid):
        if value == "X":
            for direction in DIRECTIONS:
                four_letters = grid.get_n_in_a_row(point, direction, 4)
                if [letter for _, letter in four_letters] == ["X", "M", "A", "S"]:
                    count += 1

    return count


def part_2(grid: Grid) -> int:
    count = 0
    for point, value in coordinate(grid):
        if value != "M":
            continue

        for direction in [NE, SE, NW, SW]:
            three_letters = grid.get_n_in_a_row(point, direction, 3)
            if [letter for _, letter in three_letters] != ["M", "A", "S"]:
                continue

            if direction == NE:
                card_directions = [NORTH, EAST]
            elif direction == SE:
                card_directions = [SOUTH, EAST]
            elif direction == NW:
                card_directions = [NORTH, WEST]
            else:
                card_directions = [SOUTH, WEST]

            found_m = False
            found_s = False
            for card_direction in card_directions:
                match grid.get_point_if_valid(point + card_direction + card_direction):
                    case "M":
                        found_m = True
                    case "S":
                        found_s = True

            if found_m and found_s:
                count += 1

    return count // 2


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
