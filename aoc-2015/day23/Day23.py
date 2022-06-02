from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        instructions = []
        for line in input_file.readlines():
            line = line.rstrip()
            instr, args = line[:3], line[4:]
            if ',' in args:
                args = args.split(', ')
                reg = 0 if args[0] == 'a' else 1
                instructions.append((instr, reg, int(args[1])))
            elif '+' in args or '-' in args:
                instructions.append((instr, int(args)))
            else:
                instructions.append((instr, 0 if args == 'a' else 1))
    return instructions


def run_program(instructions, registers):
    instr_pointer = 0
    while instr_pointer < len(instructions):
        curr = instructions[instr_pointer]
        instr = curr[0]
        if instr == 'jio' or instr == 'jie':
            reg, inc = curr[1], curr[2]
            if instr == 'jio':
                if registers[reg] == 1:
                    instr_pointer += inc
                else:
                    instr_pointer += 1
            else:
                if registers[reg] % 2 == 0:
                    instr_pointer += inc
                else:
                    instr_pointer += 1
        elif instr == 'hlf':
            registers[curr[1]] //= 2
            instr_pointer += 1
        elif instr == 'tpl':
            registers[curr[1]] *= 3
            instr_pointer += 1
        elif instr == 'inc':
            registers[curr[1]] += 1
            instr_pointer += 1
        elif instr == 'jmp':
            instr_pointer += curr[1]


@timed
def part1(instructions):
    registers = [0, 0]
    run_program(instructions, registers)
    print(registers[1])


@timed
def part2(instructions):
    registers = [1, 0]
    run_program(instructions, registers)
    print(registers[1])


if __name__ == '__main__':
    instruction_list = read()
    part1(instruction_list)
    part2(instruction_list)
