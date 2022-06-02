from copy import copy

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.readlines()))


@timed
def part1(jumps):
    instructions = copy(jumps)
    pointer = 0
    steps = 0
    while 0 <= pointer < len(instructions):
        new_pointer = pointer + instructions[pointer]
        instructions[pointer] += 1
        pointer = new_pointer
        steps += 1
    print(steps)


@timed
def part2(jumps):
    instructions = jumps
    pointer = 0
    steps = 0
    while 0 <= pointer < len(instructions):
        new_pointer = pointer + instructions[pointer]
        instructions[pointer] += -1 if instructions[pointer] >= 3 else 1
        pointer = new_pointer
        steps += 1
    print(steps)


if __name__ == '__main__':
    jump_list = read()
    part1(jump_list)
    part2(jump_list)
