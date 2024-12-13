from typing import Any


from shared.util import get_ints, get_puzzle, run


def parse_data(input_data: str) -> Any:
    left_list = []
    right_list = []
    for line in input_data.splitlines():
        left, right = get_ints(line)
        left_list.append(left)
        right_list.append(right)
    return (left_list, right_list)


def part_1(input_data: tuple[list[int], list[int]]) -> int:
    left_list, right_list = input_data
    return sum(
        abs(left - right) for left, right in zip(sorted(left_list), sorted(right_list))
    )


def part_2(input_data: tuple[list[int], list[int]]) -> int:
    left_list, right_list = input_data

    return sum(v * right_list.count(v) for v in left_list)


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
