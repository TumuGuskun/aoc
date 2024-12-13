from typing import Any

from shared.util import *
from shared.memory import *


def parse_data(input_data: str) -> Any:
    return Computer(corrupted_memory=input_data)


def part_1(computer: Computer) -> int:
    computer.disable_command(Do)
    computer.disable_command(Dont)
    return computer.run()


def part_2(computer: Computer) -> int:
    return computer.run()


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
