from typing import Any

from shared.util import get_puzzle, run, timed


def parse_data(input_data: str) -> Any:
    output = []
    for line in input_data.splitlines():
        pass

    return output


@timed
def part_1(input_data: str) -> int:
    return None


@timed
def part_2(input_data: str) -> int:
    return None


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
