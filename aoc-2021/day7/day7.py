from shared.Util import timed, get_ints


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return get_ints(input_file.read())


@timed
def part1(crabs):
    print(min(sum(abs(crab - i) for crab in crabs) for i in range(min(crabs), max(crabs) + 1)))


@timed
def part2(crabs):
    print(min(sum(calc_dist(crab, i) for crab in crabs) for i in range(min(crabs), max(crabs) + 1)))


def calc_dist(crab, i):
    n = abs(crab - i) + 1
    return n * (n - 1) // 2


if __name__ == '__main__':
    crab_list = read()
    part1(crab_list)
    part2(crab_list)
