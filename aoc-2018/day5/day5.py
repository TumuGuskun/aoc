import string
from collections import Counter
from functools import reduce

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.read()


@timed
def part1(polymers):
    new_polymer = []
    for mer in polymers:
        if not new_polymer:
            new_polymer.append(mer)
        else:
            if ord(mer) ^ ord(new_polymer[-1]) == 32:
                new_polymer.pop()
            else:
                new_polymer.append(mer)

    print(len(new_polymer))


@timed
def part2(polymers):
    minimum = float('inf')
    for unit in string.ascii_lowercase:
        polymer_mod = polymers.replace(unit, '').replace(unit.upper(), '')
        new_polymer = []
        for mer in polymer_mod:
            if not new_polymer:
                new_polymer.append(mer)
            else:
                if ord(mer) ^ ord(new_polymer[-1]) == 32:
                    new_polymer.pop()
                else:
                    new_polymer.append(mer)

        minimum = min(minimum, len(new_polymer))
    print(minimum)


if __name__ == '__main__':
    polymer_list = read()
    part1(polymer_list)
    part2(polymer_list)
