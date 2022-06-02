from collections import defaultdict
from functools import reduce, cache
from math import sqrt

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return int(input_file.read())


@cache
def factors(n):
    step = 2 if n % 2 else 1
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(sqrt(n))+1, step) if n % i == 0)))


@timed
def part1(presents):
    i = 2
    while True:
        if sum(factors(i)) * 10 >= presents:
            print(i)
            break
        i += 2


@timed
def part2(presents):
    i = 2
    while True:
        if sum(filter(lambda x: i < x * 50, factors(i))) * 11 >= presents:
            print(i)
            break
        i += 2


if __name__ == '__main__':
    present_list = read()
    part1(present_list)
    part2(present_list)
