import re

from shared.util import get_puzzle, run, timed


def parse_data(input_data: str) -> list[str]:
    return list(map(lambda x: x.strip(), input_data.splitlines()))


@timed
def part_1(parsed_data: list[str]) -> int:
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
def part_2(parsed_data: list[str]) -> int:
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
    puzzle = get_puzzle(__file__)
    run(puzzle=puzzle, part_1=part_1, part_2=part_2, parser=parse_data)


if __name__ == "__main__":
    main()
