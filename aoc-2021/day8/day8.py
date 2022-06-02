from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        values = []
        for line in input_file:
            patterns, output = line.split(' | ')
            values.append((patterns.split(), output.split()))
        return values


@timed
def part1(values):
    print(sum(1 for _, outputs in values for output in outputs if len(output) in [2, 3, 4, 7]))


@timed
def part2(values):
    count = 0
    for patterns, output in values:
        p2n = map_patterns(list(map(lambda p: ''.join(sorted(p)), patterns)))
        count += int(''.join(map(str, map(lambda o: p2n[o], map(lambda e: ''.join(sorted(e)), output)))))
    print(count)


def map_patterns(patterns):
    n2p = {}
    for pattern in filter(lambda p: len(p) in [2, 3, 4, 7], patterns):
        if (length := len(pattern)) == 2:
            n2p[1] = pattern
        elif length == 3:
            n2p[7] = pattern
        elif length == 4:
            n2p[4] = pattern
        elif length == 7:
            n2p[8] = pattern

    for pattern in filter(lambda p: len(p) == 5, patterns):
        if all(e in pattern for e in n2p[1]):
            n2p[3] = pattern
        elif sum(1 for e in pattern if e in n2p[4]) == 3:
            n2p[5] = pattern
        else:
            n2p[2] = pattern

    for pattern in filter(lambda p: len(p) == 6, patterns):
        if sum(1 for e in pattern if e in n2p[4]) == 4:
            n2p[9] = pattern
        elif sum(1 for e in pattern if e in n2p[1]) == 1:
            n2p[6] = pattern
        else:
            n2p[0] = pattern

    return {value: key for key, value in n2p.items()}


if __name__ == '__main__':
    value_list = read()
    part1(value_list)
    part2(value_list)
