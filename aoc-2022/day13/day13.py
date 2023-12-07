from dataclasses import dataclass
from functools import cmp_to_key
import os

from shared.gum import gum_choose
from shared.util import timed


@dataclass
class Pair:
    left: list[list | int]
    right: list[list | int]


def compare_lists(left: list[list | int], right: list[list | int]) -> int:
    if not right and not left:
        return 0
    if right and not left:
        return -1
    if left and not right:
        return 1

    first_left = left[0]
    first_right = right[0]

    if first_left == first_right:
        return compare_lists(left=left[1:], right=right[1:])

    left_is_int = isinstance(first_left, int)
    right_is_int = isinstance(first_right, int)
    if left_is_int and right_is_int:
        return -1 if first_left < first_right else 1

    if left_is_int and not right_is_int:
        return compare_lists(left=[[first_left]] + left[1:], right=right)

    if not left_is_int and right_is_int:
        return compare_lists(left=left, right=[[first_right]] + right[1:])

    return compare_lists(left=first_left, right=first_right)


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    pairs = []
    with open(file_name) as input_file:
        curr_pair = []
        for line in map(lambda l: l.strip(), input_file.readlines()):
            if not line:
                pairs.append(Pair(left=curr_pair[0], right=curr_pair[1]))
                curr_pair = []
            else:
                curr_pair.append(eval(line))
    return pairs


@timed
def part1(pairs: list[Pair]):
    print(
        sum(
            i
            for i, pair in enumerate(pairs, start=1)
            if compare_lists(pair.left, pair.right) == -1
        )
    )


@timed
def part2(pairs: list[Pair]):
    signals = []
    for pair in pairs:
        signals.append(pair.left)
        signals.append(pair.right)

    signals.append([[2]])
    signals.append([[6]])

    sorted_signals = sorted(signals, key=cmp_to_key(compare_lists), reverse=False)
    print((sorted_signals.index([[2]]) + 1) * (sorted_signals.index([[6]]) + 1))


if __name__ == "__main__":
    pair_list = read()
    part1(pair_list)
    part2(pair_list)
