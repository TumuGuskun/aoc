from functools import reduce

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: x.rstrip(), input_file.readlines()))


PAIRS = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>'
}

POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


AUTO_POINTS = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


@timed
def part1(phrases):
    count = 0
    for phrase in phrases:
        last = []
        for e in phrase:
            if e in PAIRS:
                last.append(PAIRS[e])
            else:
                if last.pop() != e:
                    count += POINTS[e]
    print(count)


@timed
def part2(phrases):
    scores = []
    for phrase in phrases:
        last = []
        corrupt = False
        for e in phrase:
            if e in PAIRS:
                last.append(PAIRS[e])
            else:
                if last.pop() != e:
                    corrupt = True
                    break
        if not corrupt:
            scores.append(reduce(lambda a, n: a*5 + n, map(lambda x: AUTO_POINTS[x], reversed(last)), 0))

    print(sorted(scores)[len(scores) // 2])


if __name__ == '__main__':
    phrase_list = read()
    part1(phrase_list)
    part2(phrase_list)
