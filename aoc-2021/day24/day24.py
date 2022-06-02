from copy import copy
from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        blocks = []
        for _ in range(14):
            lines = []
            for __ in range(18):
                line = input_file.readline().rstrip().split()
                try:
                    line[2] = int(line[2])
                except (ValueError, IndexError):
                    pass
                lines.append(line)
            blocks.append(Block(lines))
        return blocks


class Block:
    def __init__(self, lines):
        cond = int(lines[5][2])
        self.magnitude = cond if cond < 0 else int(lines[15][2])

    def positive(self):
        return self.magnitude > 0

    def __repr__(self):
        return f'{self.magnitude}'

# + 4  9 2
# + 11 2 1
# + 5  9 6
# + 11 1 1
# + 14 5 1
# - 10 9 5
# + 11 7 1
# - 9  9 3
# - 3  9 9
# + 5  9 1
# - 5  9 1
# - 10 4 1
# - 4  9 8
# - 5  8 1


@timed
def part1(instrs):
    stack = []

    value = [0] * 14
    for i, block in enumerate(instrs):
        if block.positive():
            stack.append((i, block))
        else:
            last_i, last_block = stack.pop()
            if (diff := block.magnitude + last_block.magnitude) > 0:
                value[i] = 9
                value[last_i] = 9 - block.magnitude - last_block.magnitude
            else:
                value[i] = 9 + diff
                value[last_i] = value[i] - block.magnitude - last_block.magnitude
    print(''.join(list(map(str, value))))


def run_decompiled(value):
    # 1
    w = next(value)
    z = w + 4

    # 2
    w = next(value)
    z *= 26
    z += w + 11

    # 3
    w = next(value)
    z *= 26
    z += w + 5

    # 4
    w = next(value)
    z *= 26
    z += w + 11

    # 5
    w = next(value)
    z *= 26
    z += w + 14

    # 6
    w = next(value)
    x = z
    z //= 26
    if x % 26 - 10 != w:
        z *= 26
        z += w + 7

    # 7
    w = next(value)
    z *= 26
    z += w + 11

    # 8
    w = next(value)
    x = z
    z //= 26
    if x % 26 - 9 != w:
        z *= 26
        z += w + 4

    # 9
    w = next(value)
    x = z
    z //= 26
    if x % 26 - 3 != w:
        z *= 26
        z += w + 6

    # 10
    w = next(value)
    z *= 26
    z += w + 5

    # 11
    w = next(value)
    x = z
    z //= 26
    if x % 26 - 5 != w:
        z *= 26
        z += w + 9

    # 12
    w = next(value)
    x = z
    z //= 26
    if x % 26 - 10 != w:
        z *= 26
        z += w + 12

    # 13
    w = next(value)
    x = z
    z //= 26
    if x % 26 - 4 != w:
        z *= 26
        z += w + 14

    # 14
    w = next(value)
    x = z
    z //= 26
    if x % 26 - 5 != w:
        z *= 26
        z += w + 14

    return z


def run(instrs, regs, value):
    for instr in instrs:
        if (cmd := instr[0]) == 'inp':
            regs[instr[1]] = next(value)
        else:
            a, b = instr[1:]
            if cmd == 'add':
                regs[a] = regs[a] + (b if isinstance(b, int) else regs[b])
            elif cmd == 'mul':
                regs[a] = regs[a] * (b if isinstance(b, int) else regs[b])
            elif cmd == 'div':
                regs[a] = regs[a] // (b if isinstance(b, int) else regs[b])
            elif cmd == 'mod':
                regs[a] = regs[a] % (b if isinstance(b, int) else regs[b])
            elif cmd == 'eql':
                regs[a] = int(regs[a] == (b if isinstance(b, int) else regs[b]))


@timed
def part2(instrs):
    stack = []

    value = [0] * 14
    for i, block in enumerate(instrs):
        if block.positive():
            stack.append((i, block))
        else:
            last_i, last_block = stack.pop()
            if (diff := block.magnitude + last_block.magnitude) > 0:
                value[last_i] = 1
                value[i] = 1 + block.magnitude + last_block.magnitude
            else:
                value[i] = 1
                value[last_i] = 1 - diff
    print(''.join(list(map(str, value))))


if __name__ == '__main__':
    instr_list = read()
    part1(instr_list)
    part2(instr_list)
