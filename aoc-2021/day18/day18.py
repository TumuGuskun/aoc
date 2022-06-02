from itertools import combinations

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        snambers = []
        for line in map(lambda x: x.rstrip(), input_file.readlines()):
            snambers.append(list(map(lambda x: int(x) if x.isdigit() else x, line)))
        return snambers


@timed
def part1(snambers):
    result = snambers[0]
    for snamber in snambers[1:]:
        result = add(result, snamber)
        result = reduce(result)

    print(magnitude(result))


def add(snamber1, snamber2):
    output = ['[']
    output.extend(snamber1)
    output.append(',')
    output.extend(snamber2)
    output.append(']')
    return output


def magnitude(snamber):
    if len(snamber) == 1:
        return snamber[0]
    else:
        depth = 0
        first_snamber = []
        for i, e in enumerate(snamber[1:]):
            first_snamber.append(e)
            depth += 1 if e == '[' else -1 if e == ']' else 0
            if depth == 0:
                break

        second_snamber = snamber[i + 3:-1]
        return 3 * magnitude(first_snamber) + 2 * magnitude(second_snamber)


def explode(snamber, i):
    l_snamber = snamber[i + 1]
    r_snamber = snamber[i + 3]

    for j, e in enumerate(snamber[i::-1]):
        if isinstance(e, int):
            snamber[i - j] = e + l_snamber
            break

    for j, e in enumerate(snamber[i + 5:]):
        if isinstance(e, int):
            snamber[i + 5 + j] = e + r_snamber
            break

    del snamber[i + 1:i + 5]
    snamber[i] = 0
    return snamber


def split(snamber, i):
    return snamber[:i] + add([snamber[i] // 2], [-(snamber[i] // -2)]) + snamber[i + 1:]


def reduce(snamber):
    while True:
        changed = False
        depth = 0
        for i, e in enumerate(snamber):
            depth += 1 if e == '[' else -1 if e == ']' else 0
            if depth == 5:
                snamber = explode(snamber, i)
                changed = True
                break

        if changed:
            continue

        for i, e in enumerate(snamber):
            if isinstance(e, int) and e > 9:
                snamber = split(snamber, i)
                changed = True
                break

        if changed:
            continue

        return snamber


@timed
def part2(snambers):
    max_mag = 0
    for a, b in combinations(snambers, 2):
        max_mag = max(max_mag, magnitude(reduce(add(a, b))), magnitude(reduce(add(b, a))))

    print(max_mag)


if __name__ == '__main__':
    snamber_list = read()
    part1(snamber_list)
    part2(snamber_list)
