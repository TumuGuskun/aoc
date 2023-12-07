from math import prod

from shared.gum import gum_choose
from shared.util import get_input_files, get_ints, timed


@timed
def read():
    files = get_input_files(__file__)
    if len(files) == 1:
        file_name = files[0]
    else:
        _, file_name = gum_choose(files, "Choose input file")

    print(f"Reading from {file_name.split('/')[-1]}")
    with open(file_name) as input_file:
        times = get_ints(input_file.readline())
        distances = get_ints(input_file.readline())

    return list(zip(times, distances))


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


@timed
def part1(inputs: list[tuple[int, int]]):
    winners = []
    for time, distance in inputs:
        winners.append(get_winners(time, distance))

    print(prod(winners))


@timed
def part2(inputs: list[tuple[int, int]]):
    time = int("".join(map(str, [x[0] for x in inputs])))
    distance = int("".join(map(str, [x[1] for x in inputs])))

    print(get_winners(time, distance))


if __name__ == "__main__":
    input_list = read()
    part1(input_list)
    part2(input_list)
