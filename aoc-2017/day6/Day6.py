from shared.Util import timed, ints


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.read().split()))


@timed
def part1(banks):
    seen = {tuple(banks): 0}
    for count in ints():
        to_dis = max(banks)
        i = banks.index(to_dis)
        banks[i] = 0
        for j in range(1, to_dis + 1):
            banks[(i + j) % len(banks)] += 1
        if (bank_tuple := tuple(banks)) in seen:
            print(count)
            print(count - seen[bank_tuple])
            return
        else:
            seen[bank_tuple] = count


@timed
def part2(banks):
    pass


if __name__ == '__main__':
    bank_list = read()
    part1(bank_list)
