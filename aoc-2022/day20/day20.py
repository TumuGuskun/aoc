from copy import deepcopy
from dataclasses import dataclass
import os
from tqdm import tqdm

from shared.gum import gum_choose
from shared.util import timed, get_ints


@dataclass(frozen=True)
class Number:
    order: int
    value: int


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return [
            Number(i, get_ints(line).pop())
            for i, line in enumerate(input_file.readlines())
        ]


@timed
def part1(numbers: list[Number]) -> None:
    mixed = deepcopy(numbers)
    ordered = {number.order: number for number in numbers}
    for _, number in sorted(ordered.items(), key=lambda n: n[1].order):
        curr_index = mixed.index(number)
        next_index = (curr_index + number.value) % (len(mixed) - 1)
        del mixed[curr_index]
        mixed.insert(next_index, number)

    total = 0
    zero_element = next(filter(lambda n: n.value == 0, mixed))
    zero_index = mixed.index(zero_element)
    for index_addition in [1000, 2000, 3000]:
        grove_coord = (zero_index + index_addition) % len(mixed)
        total += mixed[grove_coord].value
    print(total)


@timed
def part2(numbers: list[Number]) -> None:
    mult = 811589153
    mixed = [Number(number.order, number.value * mult) for number in numbers]
    ordered = {number.order: number for number in mixed}
    for _ in tqdm(range(10)):
        for _, number in sorted(ordered.items(), key=lambda n: n[1].order):
            curr_index = mixed.index(number)
            next_index = (curr_index + number.value) % (len(mixed) - 1)
            del mixed[curr_index]
            mixed.insert(next_index, number)

    total = 0
    zero_element = next(filter(lambda n: n.value == 0, mixed))
    zero_index = mixed.index(zero_element)
    for index_addition in [1000, 2000, 3000]:
        grove_coord = (zero_index + index_addition) % len(mixed)
        total += mixed[grove_coord].value
    print(total)


if __name__ == "__main__":
    number_list = read()
    part1(number_list)
    part2(number_list)
