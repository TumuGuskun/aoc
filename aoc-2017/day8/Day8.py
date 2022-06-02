import re
from collections import defaultdict

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        instructions = []
        for line in map(lambda x: x.rstrip(), input_file.readlines()):
            to_do, condition = line.split(' if ')
            reg, op, n = to_do.split()
            instructions.append((reg, op, int(n), condition))
        return instructions


@timed
def part1(instructions):
    registers = defaultdict(int)
    maximum = 0
    for reg, op, n, condition in instructions:
        condition = re.sub(r'([a-z]+)', r"registers['\1']", condition)
        if eval(condition):
            if op == 'inc':
                registers[reg] += n
            else:
                registers[reg] -= n
            maximum = max(maximum, registers[reg])
    print(max(registers.values()), maximum)


@timed
def part2(instructions):
    pass


if __name__ == '__main__':
    instruction_list = read()
    part1(instruction_list)
    part2(instruction_list)
