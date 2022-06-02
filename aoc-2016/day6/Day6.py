from collections import Counter

import numpy as np

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: list(x.rstrip()), input_file.readlines()))


def column(matrix, i):
    return [row[i] for row in matrix]


@timed
def part1(messages):
    correct = ''
    for i in range(len(messages[0])):
        counted = Counter(column(messages, i))
        top = counted.most_common(1)[0][0]
        correct += top
    print(correct)


@timed
def part2(messages):
    correct = ''
    for i in range(len(messages[0])):
        counted = Counter(column(messages, i))
        top = counted.most_common()[-1][0]
        correct += top
    print(correct)


if __name__ == '__main__':
    message_list = read()
    part1(message_list)
    part2(message_list)
