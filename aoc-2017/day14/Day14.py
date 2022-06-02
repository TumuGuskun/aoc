from queue import Queue

from shared.Util import timed, Point

import numpy as np


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.read().rstrip()


def knot_hash(numbers):
    numbers = list(map(ord, numbers))
    numbers += [17, 31, 73, 47, 23]
    num_list = list(range(256))
    start = 0
    skip = 0

    for _ in range(64):
        for number in numbers:
            if start + number > 256:
                new_end = (start + number) % 256
                new_list = list(reversed(num_list[start:] + num_list[:new_end]))
                num_list[start:] = new_list[:256 - start]
                num_list[:new_end] = new_list[256 - start:]
            else:
                num_list[start:start + number] = reversed(num_list[start:start + number])
            start = (start + number + skip) % 256
            skip += 1

    new_nums = []
    count = 0
    running = 0
    for number in num_list:
        if count < 16:
            running ^= number
            count += 1
        else:
            new_nums.append(running)
            running = number
            count = 1

    new_nums.append(running)
    return ''.join(list(map(lambda x: f'{x:#04x}'[2:], new_nums)))


@timed
def part1(hashes):
    count = 0
    for i in range(128):
        hashed = ''.join([f'{int(e, 16):04b}' for e in knot_hash(f'{hashes}-{i}')])
        count += sum(1 for e in hashed if e == '1')
    print(count)


def get_neighbors(point, board):
    possible = [point + Point(0, -1), point + Point(0, 1), point + Point(-1, 0), point + Point(1, 0)]
    valid = filter(lambda x: x.is_valid(upper_x=127, upper_y=127), possible)
    ones = filter(lambda p: board[p.x, p.y] == 1, valid)
    return ones


@timed
def part2(hashes):
    board = []
    for i in range(128):
        board.append(list(map(int, ''.join([f'{int(e, 16):04b}' for e in knot_hash(f'{hashes}-{i}')]))))
    board = np.array(board)

    queue = Queue()
    seen = set()
    counter = 0

    for x, row in enumerate(board):
        for y, square in enumerate(row):
            if (point := Point(x, y)) not in seen and square == 1:
                counter += 1
                queue.put(point)
                seen.add(point)

                while not queue.empty():
                    curr_point = queue.get()
                    for next_point in get_neighbors(curr_point, board):
                        if next_point not in seen:
                            seen.add(next_point)
                            queue.put(next_point)
    print(counter)


if __name__ == '__main__':
    hash_list = read()
    part1(hash_list)
    part2(hash_list)
