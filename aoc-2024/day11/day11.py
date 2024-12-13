from functools import cache
from typing import Any

from shared.util import *


def parse_data(input_data: str) -> Any:
    return get_ints(input_data)


@cache
def blink_stone_n_times(stone: int, n: int) -> int:
    if n == 0:
        return 1

    if stone == 0:
        return blink_stone_n_times(1, n - 1)

    str_stone = str(stone)
    if len(str_stone) % 2 == 0:
        half = len(str_stone) // 2
        left = int(str_stone[:half])
        right = int(str_stone[half:])
        return blink_stone_n_times(left, n - 1) + blink_stone_n_times(right, n - 1)

    return blink_stone_n_times(stone * 2024, n - 1)


def part_1(state: list[int]) -> int:
    return sum(blink_stone_n_times(stone, 25) for stone in state)


def part_2(state: list[int]) -> int:
    return sum(blink_stone_n_times(stone, 75) for stone in state)


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(
        puzzle=puzzle,
        part_1=part_1,
        part_2=part_2,
        parser=parse_data,
        force_run_2=True,
    )


if __name__ == "__main__":
    main()
