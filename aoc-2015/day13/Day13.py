from collections import defaultdict
from itertools import permutations

from shared.Util import timed

HAPPINESS = defaultdict(dict)


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        for line in input_file.readlines():
            line = line.rstrip()[:-1]
            first, target = line.split(' happiness units by sitting next to ')
            source, net_gain = first.split(' would ')
            plus_minus, change = net_gain.split(' ')
            effect = int(change) * (1 if plus_minus == 'gain' else -1)
            HAPPINESS[source].update({target: effect})


def get_seating_score(seating):
    score = 0
    for i in range(len(seating)):
        score += HAPPINESS[seating[i - 1]][seating[i]]
        score += HAPPINESS[seating[i]][seating[i - 1]]
    return score


@timed
def part1():
    best = 0
    for perm in permutations(HAPPINESS.keys()):
        best = max(best, get_seating_score(perm))
    print(best)


@timed
def part2():
    for value in HAPPINESS.values():
        value.update({'Me': 0})
    HAPPINESS.update({'Me': {name: 0 for name in HAPPINESS.keys()}})
    best = 0
    for perm in permutations(HAPPINESS.keys()):
        best = max(best, get_seating_score(perm))
    print(best)


if __name__ == '__main__':
    read()
    part1()
    part2()
