from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    instructions = []
    with open(file_name) as input_file:
        for line in input_file.readlines():
            instructions.append(list(map(lambda x: int(x) if x.isdigit() or x.startswith('-') else x, line.split())))

    return instructions


def run(registers, pointer, instructions):
    while pointer < len(instructions):
        try:
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
                n = b if isinstance(b, int) else registers[b]
                if isinstance(a, str):
                    pointer += n if registers[a] != 0 else 1
                else:
                    pointer += n if a != 0 else 1
            elif instr == 'tgl':
                a, = args
                n = a if isinstance(a, int) else registers[a]
                update_pointer = pointer + n
                if 0 <= update_pointer < len(instructions):
                    old_instr, *old_args = instructions[update_pointer]
                    if old_instr == 'inc':
                        instructions[update_pointer] = ['dec', *old_args]
                    elif len(old_args) == 1:
                        instructions[update_pointer] = ['inc', *old_args]
                    elif old_instr == 'jnz':
                        instructions[update_pointer] = ['cpy', *old_args]
                    elif len(old_args) == 2:
                        instructions[update_pointer] = ['jnz', *old_args]
                pointer += 1
        except TypeError:
            print(instr, *args)
            pointer += 1


@timed
def part1(instructions):
    registers = {
        'a': 7,
        'b': 0,
        'c': 0,
        'd': 0
    }
    run(registers, 0, instructions)
    print(registers['a'])


@timed
def part2(instructions):
    registers = {
        'a': 12,
        'b': 0,
        'c': 0,
        'd': 0
    }
    run(registers, 0, instructions)
    print(registers)


if __name__ == '__main__':
    instruction_list = read()
    part1(instruction_list)
    part2(instruction_list)
