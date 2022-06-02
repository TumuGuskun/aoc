from collections import Counter
from copy import copy

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: x.rstrip(), input_file))


@timed
def part1(numbers):
    counters = [Counter() for _ in numbers[0]]

    for number in numbers:
        for i, e in enumerate(number):
            counters[i][e] += 1

    gamma = [counter.most_common()[0][0] for counter in counters]
    epsilon = [counter.most_common()[1][0] for counter in counters]

    print(int(''.join(gamma), 2) * int(''.join(epsilon), 2))


@timed
def part2(numbers):
    og_numbers = copy(numbers)
    co2_numbers = copy(numbers)

    i = 0
    while len(og_numbers) > 1:
        counter = Counter([number[i] for number in og_numbers])
        top_num = '1' if counter['1'] == counter['0'] else counter.most_common()[0][0]
        og_numbers = [number for number in og_numbers if number[i] == top_num]
        i += 1

    i = 0
    while len(co2_numbers) > 1:
        counter = Counter([number[i] for number in co2_numbers])
        top_num = '0' if counter['1'] == counter['0'] else counter.most_common()[1][0]
        co2_numbers = [number for number in co2_numbers if number[i] == top_num]
        i += 1

    print(int(og_numbers.pop(), 2) * int(co2_numbers.pop(), 2))


if __name__ == '__main__':
    number_list = read()
    part1(number_list)
    part2(number_list)
