from typing import Any

from shared.util import *
from shared.grid import *


def parse_data(input_data: str) -> Any:
    return Grid(input_data.splitlines(), edges=[])


def part_1(grid: Grid) -> int:
    nodes = set()

    unique_chars = np.unique(grid.grid)

    for unique_char in unique_chars:
        if unique_char == ".":
            continue

        all_char_points = grid.find(unique_char)
        for base_char_point in all_char_points:
            for other_char_point in all_char_points:
                if base_char_point == other_char_point:
                    continue

                possible_node = other_char_point * 2 - base_char_point
                if grid.check_point_in_bounds(possible_node):
                    nodes.add(possible_node)
                    if grid.get_point(possible_node) == ".":
                        grid.set_point(possible_node, "#")

    return len(nodes)


def part_2(grid: Grid) -> int:
    nodes = set()

    unique_chars = np.unique(grid.grid)

    for unique_char in unique_chars:
        if unique_char == ".":
            continue

        all_char_points = grid.find(unique_char)
        for base_char_point in all_char_points:
            for other_char_point in all_char_points:
                if base_char_point == other_char_point:
                    continue

                vector = other_char_point - base_char_point
                current_possible = other_char_point
                while grid.check_point_in_bounds(current_possible):
                    nodes.add(current_possible)
                    current_possible += vector

    return len(nodes)


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
