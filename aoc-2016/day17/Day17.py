from functools import cache
from hashlib import md5
from queue import Queue

from shared.Util import timed, Point


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.read().rstrip()


@cache
def get_neighbors(seed):
    possible = [('U', Point(0, -1)), ('D', Point(0, 1)), ('L', Point(-1, 0)), ('R', Point(1, 0))]
    first_four = md5(seed.encode()).hexdigest()[:4]
    valid = [p[1] for p in enumerate(possible) if first_four[p[0]] in 'bcdef']
    return valid


@timed
def part1(seeds):  # RLDUDRDDRR
    queue = Queue()
    queue.put((seeds, Point(0, 0)))
    finish = Point(3, 3)
    while not queue.empty():
        seed, spot = queue.get()
        if spot == finish:
            print(seed[len(seeds):])
            return

        for direction, point in get_neighbors(seed):
            new_spot = spot + point
            if new_spot.is_valid():
                queue.put((seed + direction, new_spot))


@timed
def part2(seeds):  # 590
    queue = Queue()
    queue.put((seeds, Point(0, 0)))
    finish = Point(3, 3)
    maximum = 0
    while not queue.empty():
        seed, spot = queue.get()
        if spot == finish:
            maximum = max(len(seed) - len(seeds), maximum)
        else:
            for direction, point in get_neighbors(seed):
                new_spot = spot + point
                if new_spot.is_valid(upper_x=3, upper_y=3):
                    queue.put((seed + direction, new_spot))
    print(maximum)


if __name__ == '__main__':
    seed_list = read()
    part1(seed_list)
    part2(seed_list)
