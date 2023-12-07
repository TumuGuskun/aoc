from dataclasses import dataclass
from pprint import pprint

from shared.gum import gum_choose
from shared.util import get_input_files, get_ints, timed


@dataclass
class Map:
    destination_start: int
    source_start: int
    range_length: int


@timed
def read() -> tuple[list[int], list[list[Map]]]:
    files = get_input_files(__file__)
    if len(files) == 1:
        file_name = files[0]
    else:
        _, file_name = gum_choose(files, "Choose input file")

    print(f"Reading from {file_name.split('/')[-1]}")
    with open(file_name) as input_file:
        seeds, map_types = [], []

        typed_map = []
        for line in input_file.readlines():
            line = line.strip()
            if line.startswith("seeds:"):
                seeds = get_ints(line)
            elif not line:
                map_types.append(typed_map)
            elif line[0].isalpha():
                typed_map = []
            else:
                typed_map.append(Map(*get_ints(line)))

        return seeds, map_types


@timed
def part1(inputs: tuple[list[int], list[list[Map]]]):
    seeds, maps = inputs
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

    print(min(locations))


@timed
def part2(inputs: tuple[list[int], list[list[Map]]]):
    seeds, maps = inputs
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

    print(min_location)


if __name__ == "__main__":
    map_list = read()
    part1(map_list)
    part2(map_list)
