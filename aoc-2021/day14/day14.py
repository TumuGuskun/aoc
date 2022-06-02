from collections import Counter, defaultdict

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        start = input_file.readline().rstrip()
        input_file.readline()
        reactions = {}
        for line in input_file.readlines():
            reactants, finish = line.rstrip().split(' -> ')
            reactions[reactants] = finish
        return start, reactions


@timed
def part1(reactions):
    start, reactions = reactions

    start = list(start)

    for _ in range(10):
        new_start = []
        while start:
            new_start.append(start[0])
            if (first_two := ''.join(start[:2])) in reactions:
                new_start.append(reactions[first_two])
            start = start[1:]

        start = new_start

    count = Counter(start)
    print(count.most_common(1).pop()[1] - count.most_common()[-1][1])


@timed
def part2(reactions):
    start, reactions = reactions

    pairs = Counter([start[i:i+2] for i, _ in enumerate(start[:-1])])
    doubled = Counter(start[1:-1])

    for _ in range(40):
        new_pairs = Counter()
        for pair, count in list(pairs.items()):
            new = reactions[pair]
            react1, react2 = pair
            new_pairs += {react1 + new: count, new + react2: count}
            doubled[new] += count
        pairs = new_pairs

    total = Counter()
    for pair, count in pairs.items():
        for e in pair:
            total[e] += count

    total -= doubled
    print(total.most_common(1).pop()[1] - total.most_common()[-1][1])


if __name__ == '__main__':
    reaction_list = read()
    part1(reaction_list)
    part2(reaction_list)
