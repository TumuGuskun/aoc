from dataclasses import dataclass
from pprint import pprint
from typing import Any

from shared.util import get_ints, get_puzzle, run, timed


@dataclass
class Map:
    name: str
    destination_start: int
    source_start: int
    range_length: int


def parse_data(input_data: str) -> Any:
    seeds, map_types, typed_map = [], [], []

    for line in input_data.splitlines():
        line = line.strip()
        if line.startswith("seeds:"):
            seeds = get_ints(line)
        elif not line:
            map_types.append(typed_map)
        elif line[0].isalpha():
            map_name = line.split(" ")[0]
            typed_map = []
        else:
            typed_map.append(Map(map_name, *get_ints(line)))

    map_types.append(typed_map)

    return seeds, map_types


@timed
def part_1(input_data: tuple[list[int], list[list[Map]]]) -> Any:
    seeds, maps = input_data

    # Body Logic
    locations = []

    for seed in seeds:
        curr_value = seed
        for map_type in maps:
            for typed_map in map_type:
                if (
                    0
                    <= (offset := curr_value - typed_map.source_start)
                    < typed_map.range_length
                ):
                    curr_value = typed_map.destination_start + offset
                    break

        locations.append(curr_value)

    return min(locations)


@timed
def part_2(input_data: tuple[list[int], list[list[Map]]]) -> Any:
    seeds, maps = input_data

    # Body Logic
    min_location = float("inf")

    seed_iter = iter(seeds)
    for seed_start, seed_range in zip(seed_iter, seed_iter):
        for seed in range(seed_start, seed_start + seed_range):
            curr_value = seed
            for map_type in maps:
                for typed_map in map_type:
                    if (
                        0
                        <= (offset := curr_value - typed_map.source_start)
                        < typed_map.range_length
                    ):
                        curr_value = typed_map.destination_start + offset
                        break

            min_location = min(min_location, curr_value)

    return min_location


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(
        puzzle=puzzle,
        part_1=part_1,
        part_2=part_2,
        parser=parse_data,
        run_examples=True,
        run_part_2=False,
    )


if __name__ == "__main__":
    main()
