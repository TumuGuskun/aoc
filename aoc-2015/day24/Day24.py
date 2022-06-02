from collections import defaultdict
from functools import cache
from math import prod

from shared.Util import timed

ALL = defaultdict(lambda: 100000)


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.readlines()))


@cache
def use_or_lose(sizes, capacity):
    if capacity == 0:
        return []
    elif not sizes:
        return list(range(100))
    elif sizes[0] > capacity:
        return use_or_lose(sizes[1:], capacity)
    else:
        use = use_or_lose(sizes[1:], capacity - sizes[0]) + [sizes[0]]
        lose = use_or_lose(sizes[1:], capacity)
        return min(use, lose, key=lambda x: len(x))


@timed
def part1(packages):
    group_size = sum(packages) // 3
    print(prod(use_or_lose(tuple(packages), group_size)))


@timed
def part2(packages):
    group_size = sum(packages) // 4
    print(prod(use_or_lose(tuple(packages), group_size)))


if __name__ == '__main__':
    package_list = read()
    part1(package_list)
    part2(package_list)
