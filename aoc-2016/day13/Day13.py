from collections import Counter
from functools import cache
from queue import Queue

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return int(input_file.read())


@cache
def is_open(x, y, num):
    total = x * x + 3 * x + 2 * x * y + y + y * y + num
    binary = f'{total:b}'
    return Counter(binary).get('1') % 2 == 0


@cache
def get_neighbors(x, y, num):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    negative = filter(lambda n: n[0] >= 0 and n[1] >= 0, neighbors)
    return list(filter(lambda n: is_open(n[0], n[1], num), negative))


@timed
def part1(numbers):
    queue = Queue()
    seen = set()
    seen.add((1, 1))
    queue.put((1, 1, 0))

    while not queue.empty():
        x, y, depth = queue.get()
        if x == 31 and y == 39:
            print(depth)
            return

        for new_x, new_y in get_neighbors(x, y, numbers):
            if (new_x, new_y) not in seen:
                queue.put((new_x, new_y, depth + 1))
                seen.add((new_x, new_y))


@timed
def part2(numbers):
    queue = Queue()
    seen = set()
    seen.add((1, 1))
    queue.put((1, 1, 0))

    while not queue.empty():
        x, y, depth = queue.get()
        if depth == 50:
            print(len(seen))
            return

        for new_x, new_y in get_neighbors(x, y, numbers):
            if (new_x, new_y) not in seen:
                queue.put((new_x, new_y, depth + 1))
                seen.add((new_x, new_y))


if __name__ == '__main__':
    number_list = read()
    part1(number_list)
    part2(number_list)
