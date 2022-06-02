import re

from shared.Util import timed

GEN_A = 16807
GEN_B = 48271
MOD = 2147483647


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, map(lambda line: re.search(r'(\d+)', line).group(1), input_file.readlines())))


@timed
def part1(seeds):
    a, b = seeds
    count = 0
    for _ in range(40000000):
        a = (a * GEN_A) % MOD
        b = (b * GEN_B) % MOD
        if (a & 65535) == (b & 65535):
            count += 1
    print(count)


def gen(seed, a_b):
    if a_b == 'a':
        factor = GEN_A
    else:
        factor = GEN_B

    while True:
        seed = (seed * factor) % MOD
        if a_b == 'a':
            if seed % 4 == 0:
                yield seed
        else:
            if seed % 8 == 0:
                yield seed


@timed
def part2(seeds):
    a, b = seeds
    a_gen = gen(a, 'a')
    b_gen = gen(b, 'b')

    count = 0
    for _ in range(5000000):
        a = next(a_gen)
        b = next(b_gen)

        if (a & 65535) == (b & 65535):
            count += 1
    print(count)


if __name__ == '__main__':
    seed_list = read()
    part1(seed_list)
    part2(seed_list)
