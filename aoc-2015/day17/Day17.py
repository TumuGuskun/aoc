from collections import defaultdict

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.readlines()))


def use_or_lose(sizes, capacity):
    if capacity == 0:
        return 1
    elif not sizes:
        return 0
    elif sizes[0] > capacity:
        return use_or_lose(sizes[1:], capacity)
    else:
        return use_or_lose(sizes[1:], capacity - sizes[0]) + use_or_lose(sizes[1:], capacity)


@timed
def part1(sizes):
    print(use_or_lose(sorted(sizes, reverse=True), 150))


CONTAINERS = defaultdict(int)


def use_or_lose_count(sizes, capacity, depth):
    if capacity == 0:
        CONTAINERS[depth] += 1
        return 1
    elif not sizes:
        return 0
    elif sizes[0] > capacity:
        return use_or_lose_count(sizes[1:], capacity, depth)
    else:
        return use_or_lose_count(sizes[1:], capacity - sizes[0], depth + 1) + \
               use_or_lose_count(sizes[1:], capacity, depth)


@timed
def part2(sizes):
    use_or_lose_count(sorted(sizes, reverse=True), 150, 0)
    print(min(CONTAINERS.items(), key=lambda x: x[0])[1])


if __name__ == '__main__':
    size_list = read()
    part1(size_list)
    part2(size_list)
