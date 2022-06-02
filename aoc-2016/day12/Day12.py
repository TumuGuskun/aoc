from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        instructions = []
        for line in input_file.readlines():
            instructions.append(list(map(lambda x: int(x) if x.isdigit() or x.startswith('-') else x, line.split())))

    return instructions


def run(registers, pointer, instructions):
    while pointer < len(instructions):
        instr, *args = instructions[pointer]
        if instr == 'cpy':
            a, b = args
            if isinstance(a, str):
                registers[b] = registers[a]
            else:
                registers[b] = a
            pointer += 1
        elif instr == 'inc':
            a, = args
            registers[a] += 1
            pointer += 1
        elif instr == 'dec':
            a, = args
            registers[a] -= 1
            pointer += 1
        elif instr == 'jnz':
            a, b = args
            if isinstance(a, str):
                pointer += b if registers[a] != 0 else 1
            else:
                pointer += b if a != 0 else 1


@timed
def part1(instructions):
    registers = {
        'a': 0,
        'b': 0,
        'c': 0,
        'd': 0
    }
    run(registers, 0, instructions)
    print(registers['a'])


@timed
def part2(instructions):
    registers = {
        'a': 0,
        'b': 0,
        'c': 1,
        'd': 0
    }
    run(registers, 0, instructions)
    print(registers['a'])


if __name__ == '__main__':
    instruction_list = read()
    part1(instruction_list)
    part2(instruction_list)
