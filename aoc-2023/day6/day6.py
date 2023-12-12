from math import prod

from typing import Any

from shared.util import get_puzzle, run, timed, get_ints


def get_winners(time: int, distance: int) -> int:
    midway = time // 2

    if distance > (time - midway) * midway:
        raise Exception()

    # find first winner using binary search
    lowest = 0
    left = 0
    right = midway
    while left <= right:
        mid = (left + right) // 2
        if distance > (time - mid) * mid:
            left = mid + 1
        else:
            lowest = mid
            right = mid - 1

    return time - 2 * lowest + 1


def parse_data(input_data: str) -> Any:
    times, distances = map(get_ints, input_data.splitlines())
    return list(zip(times, distances))


@timed
def part_1(input_data: str) -> Any:
    inputs = parse_data(input_data=input_data)

    # Body Logic
    winners = []
    for time, distance in inputs:
        winners.append(get_winners(time, distance))

    print(winners)

    return prod(winners)


@timed
def part_2(input_data: str) -> Any:
    inputs = parse_data(input_data=input_data)

    # Body Logic
    time = int("".join(map(str, [x[0] for x in inputs])))
    distance = int("".join(map(str, [x[1] for x in inputs])))

    return get_winners(time, distance)


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(puzzle=puzzle, part_1=part_1, part_2=part_2)


if __name__ == "__main__":
    main()
