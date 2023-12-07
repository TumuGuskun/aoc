import os

from shared.gum import gum_choose
from shared.util import timed, get_ints


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return [get_ints(line.replace("-", " ")) for line in input_file.readlines()]


@timed
def part1(elf_pairs):
    print(
        sum(
            (
                1
                for min1, max1, min2, max2 in elf_pairs
                if (min1 <= min2 <= max2 <= max1) or (min2 <= min1 <= max1 <= max2)
            )
        )
    )


@timed
def part2(elf_pairs):
    print(
        sum(
            (
                1
                for min1, max1, min2, max2 in elf_pairs
                if (min1 <= min2 <= max1) or (min2 <= min1 <= max2)
            )
        )
    )


if __name__ == "__main__":
    elf_pair_list = read()
    part1(elf_pair_list)
    part2(elf_pair_list)
