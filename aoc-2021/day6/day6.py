from collections import Counter

from shared.Util import timed, get_ints


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return get_ints(input_file.read())


@timed
def part1(states):
    cache = [0] * 200
    for i in range(100):
        if i < 7:
            cache[i] = 1
        elif i < 14:
            cache[i] = 2
        else:
            cache[i] = cache[i - 7] + cache[i - 9]

    count = 0
    for state in states:
        count += cache[86 - state]

    print(count)


@timed
def part2(states):
    cache = [0] * 300
    for i in range(300):
        if i < 7:
            cache[i] = 1
        elif i < 14:
            cache[i] = 2
        else:
            cache[i] = cache[i - 7] + cache[i - 9]

    count = 0
    for state in states:
        count += cache[262 - state]

    print(count)


if __name__ == '__main__':
    state_list = read()
    part1(state_list)
    part2(state_list)
