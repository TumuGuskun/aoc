from typing import Any

from shared.util import *


def parse_data(input_data: str) -> Any:
    return [get_ints(line) for line in input_data.splitlines()]


def check_if_equation_works(
    test_value: int,
    input_values: list[int],
    combine_allowed: bool,
) -> bool:
    if len(input_values) == 0:
        return test_value == 0

    if test_value <= 0:
        return False

    last_value = input_values[-1]

    use_multiply = False
    if test_value % last_value == 0:
        use_multiply = check_if_equation_works(
            test_value // last_value, input_values[:-1], combine_allowed=combine_allowed
        )

    use_add = check_if_equation_works(
        test_value - last_value,
        input_values[:-1],
        combine_allowed=combine_allowed,
    )

    use_combine = False
    if combine_allowed:
        test_value_str = str(test_value)
        last_value_str = str(last_value)

        if len(test_value_str) > len(last_value_str) and test_value_str.endswith(
            last_value_str
        ):
            use_combine = check_if_equation_works(
                int(test_value_str[: -len(last_value_str)]),
                input_values[:-1],
                combine_allowed=combine_allowed,
            )

    return use_multiply or use_add or use_combine


def part_1(equations: list[list[int]]) -> int:
    count = 0

    for equation in equations:
        test_value, *inputs = equation
        if check_if_equation_works(test_value, inputs, False):
            count += test_value

    return count


def part_2(equations: list[list[int]]) -> int:
    count = 0

    for equation in equations:
        test_value, *inputs = equation
        if check_if_equation_works(test_value, inputs, True):
            count += test_value

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
