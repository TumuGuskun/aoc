import re
from typing import Any

from aocd.models import Puzzle

from shared.util import export_data, run, timed


@timed
def get_puzzle() -> Puzzle:
    year = int(__file__.split("/")[-3].removeprefix("aoc-"))
    day = int(__file__.split("/")[-2].removeprefix("day"))

    puzzle = Puzzle(year=year, day=day)
    export_data(puzzle=puzzle, year=year, day=day)
    return puzzle


def parse_data(input_data: str) -> Any:
    return list(map(lambda x: x.strip(), input_data.splitlines()))


@timed
def part_1(input_data: str) -> Any:
    parsed_data = parse_data(input_data=input_data)

    # Body Logic
    reduced_numbers = []
    for line in parsed_data:
        line_numbers = re.sub(r"[a-z]", "", line)
        reduced_numbers.append(int(line_numbers[0] + line_numbers[-1]))

    return sum(reduced_numbers)


NUMBER_PATTERNS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


@timed
def part_2(input_data: str) -> Any:
    parsed_data = parse_data(input_data=input_data)

    # Body Logic
    reduced_numbers = []
    for line in parsed_data:
        reduced_number = []
        for i in range(len(line)):
            if line[i].isdecimal():
                reduced_number.append(line[i])
            else:
                for pattern, replacement in NUMBER_PATTERNS.items():
                    if line[i : i + len(pattern)] == pattern:
                        reduced_number.append(replacement)

        reduced_numbers.append(reduced_number)

    return sum(map(lambda x: int(x[0] + x[-1]), reduced_numbers))


def main() -> None:
    puzzle, _ = get_puzzle()
    run(puzzle=puzzle, part_1=part_1, part_2=part_2)


if __name__ == "__main__":
    main()
