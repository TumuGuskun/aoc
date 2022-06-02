from shared.Util import timed, Node


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return int(input_file.read())


@timed
def part1(steps):
    buffer = [0]
    j = 0
    for i in range(1, 2018):
        j = ((j + steps) % i) + 1
        buffer.insert(j, i)
    print(buffer[buffer.index(2017) + 1])


@timed
def part2(steps):
    first = 0
    j = 0
    for i in range(1, 50000000):
        if (j := ((j + steps) % i) + 1) == 1:
            first = i
    print(first)


if __name__ == '__main__':
    step_list = read()
    part1(step_list)
    part2(step_list)
