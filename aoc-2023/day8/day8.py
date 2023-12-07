from typing import Any

from shared.util import get_puzzle, run, timed


def parse_data(input_data: str) -> Any:
    output = []
    for line in input_data.splitlines():
        pass

    return output


@timed
def part_1(input_data: str) -> Any:
    parsed_data = parse_data(input_data=input_data)

    # Body Logic
    return None


@timed
def part_2(input_data: str) -> Any:
    parsed_data = parse_data(input_data=input_data)

    # Body Logic
    return None


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(puzzle=puzzle, part_1=part_1, part_2=part_2)


if __name__ == "__main__":
    main()
