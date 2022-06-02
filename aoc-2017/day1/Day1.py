from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.read()))


@timed
def part1(digits):
    print(sum(map(lambda y: y[1], filter(lambda x: x[1] == digits[(x[0] + 1) % len(digits)], enumerate(digits)))))


@timed
def part2(digits):
    halfway = len(digits) // 2
    print(sum(map(lambda y: y[1], filter(lambda x: x[1] == digits[(x[0] + halfway) % len(digits)], enumerate(digits)))))


if __name__ == '__main__':
    digit_list = read()
    part1(digit_list)
    part2(digit_list)
