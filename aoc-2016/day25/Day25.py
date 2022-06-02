from shared.Util import timed, ints


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    instructions = []
    with open(file_name) as input_file:
        for line in input_file.readlines():
            instructions.append(list(map(lambda x: int(x) if x.isdigit() or x.startswith('-') else x, line.split())))

    return instructions


def run(registers, pointer, instructions):
    count = 0
    output = [1]
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
            n = b if isinstance(b, int) else registers[b]
            if isinstance(a, str):
                pointer += n if registers[a] != 0 else 1
            else:
                pointer += n if a != 0 else 1
        elif instr == 'out':
            a, = args
            if output[-1] == 0:
                if registers[a] == 1:
                    output.append(1)
                else:
                    return False
            else:
                if registers[a] == 0:
                    output.append(0)
                else:
                    return False
            count += 1
            if count > 100:
                return True
            pointer += 1


@timed
def part1(instructions):
    a = 0
    while True:
        registers = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': a + 2548
        }
        if run(registers, 0, instructions):
            print(a)
            break
        else:
            a += 1


@timed
def part2(instructions):
    print(next(a for a in ints(start=2548) if ((a ^ (a >> 1)) + 1) & (a ^ (a >> 1)) == 0) - 2548)


if __name__ == '__main__':
    instruction_list = read()
    part1(instruction_list)
    part2(instruction_list)
