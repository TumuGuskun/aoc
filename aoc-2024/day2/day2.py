from typing import Any

from shared.util import *


def parse_data(input_data: str) -> Any:
    return [get_ints(line) for line in input_data.splitlines()]


def is_within_threshold(a, b):
    return 0 < abs(a - b) < 4


def part_1(input_data: list[list[int]]) -> int:
    count = 0
    for line in input_data:
        if is_ascending(line) or is_descending(line):
            if all(is_within_threshold(a, b) for a, b in zip(line, line[1:])):
                count += 1
    return count


def part_2(input_data: list[list[int]]) -> int:
    count = 0
    for line in input_data:
        for variant in get_variants_without_one(line):
            if is_ascending(variant) or is_descending(variant):
                if all(is_within_threshold(a, b) for a, b in zip(variant, variant[1:])):
                    count += 1
                    break
    return count


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
