from collections import defaultdict
from pprint import pprint

from shared.Util import timed

SUE = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    sues = defaultdict(dict)
    with open(file_name) as input_file:
        for line in input_file.readlines():
            sue, attrs = line.split(': ', 1)
            _, num = sue.split(' ')
            for attr in attrs.split(', '):
                thing, quan = attr.split(': ')
                sues[int(num)].update({thing: int(quan)})
    return sues


@timed
def part1(sues):
    for i, sue in sues.items():
        found = True
        for attr, value in sue.items():
            if value != SUE[attr]:
                found = False
                break
        if found:
            print(i)
            break


@timed
def part2(sues):
    for i, sue in sues.items():
        found = True
        for attr, value in sue.items():
            if attr in ['cats', 'trees']:
                if value <= SUE[attr]:
                    found = False
                    break
            elif attr in ['pomeranians', 'goldfish']:
                if value >= SUE[attr]:
                    found = False
                    break
            else:
                if value != SUE[attr]:
                    found = False
                    break
        if found:
            print(i)
            break


if __name__ == '__main__':
    sue_list = read()
    part1(sue_list)
    part2(sue_list)
