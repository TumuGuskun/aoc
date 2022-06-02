from collections import Counter

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        passphrases = []
        for line in map(lambda x: x.rstrip(), input_file.readlines()):
            passphrases.append(line.split())
        return passphrases


@timed
def part1(passphrases):
    print(sum(1 for pp in passphrases if Counter(pp).most_common(1).pop()[1] == 1))


@timed
def part2(passphrases):
    print(len(list(filter(lambda pp: Counter(pp).most_common(1).pop()[1] == 1, [map(lambda x: ''.join(sorted(x)), p) for p in passphrases]))))


if __name__ == '__main__':
    passphrase_list = read()
    part1(passphrase_list)
    part2(passphrase_list)
