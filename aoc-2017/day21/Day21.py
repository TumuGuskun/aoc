from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.readlines()


@timed
def part1(rules):
    pass


@timed
def part2(rules):
    pass


if __name__ == '__main__':
    rule_list = read()
    part1(rule_list)
    part2(rule_list)
