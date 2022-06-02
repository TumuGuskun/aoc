from collections import defaultdict

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.readlines()


@timed
def part1(instructions):
    state = 'a'
    pointer = 0
    tape = defaultdict(int)

    for _ in range(12459852):
        curr_value = tape[pointer]
        if state == 'a':
            if curr_value == 0:
                tape[pointer] = 1
                pointer += 1
                state = 'b'
            else:
                tape[pointer] = 1
                pointer -= 1
                state = 'e'
        elif state == 'b':
            if curr_value == 0:
                tape[pointer] = 1
                pointer += 1
                state = 'c'
            else:
                tape[pointer] = 1
                pointer += 1
                state = 'f'
        elif state == 'c':
            if curr_value == 0:
                tape[pointer] = 1
                pointer -= 1
                state = 'd'
            else:
                tape[pointer] = 0
                pointer += 1
                state = 'b'
        elif state == 'd':
            if curr_value == 0:
                tape[pointer] = 1
                pointer += 1
                state = 'e'
            else:
                tape[pointer] = 0
                pointer -= 1
                state = 'c'
        elif state == 'e':
            if curr_value == 0:
                tape[pointer] = 1
                pointer -= 1
                state = 'a'
            else:
                tape[pointer] = 0
                pointer += 1
                state = 'd'
        else:
            if curr_value == 0:
                tape[pointer] = 1
                pointer += 1
                state = 'a'
            else:
                tape[pointer] = 1
                pointer += 1
                state = 'c'
    print(sum(tape.values()))


@timed
def part2(instructions):
    pass


if __name__ == '__main__':
    instruction_list = read()
    part1(instruction_list)
    part2(instruction_list)
