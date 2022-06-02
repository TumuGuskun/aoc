from collections import defaultdict

from shared.Util import timed, get_ints


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        ba_sets = []
        op_codes = []
        in_ba = False
        for i, line in enumerate(input_file):
            if line.startswith('Before'):
                b = get_ints(line)
                in_ba = True
            elif line.startswith('After'):
                a = get_ints(line)
                ba_sets.append((b, in_ba_op_code, a))
                in_ba = False
            elif in_ba:
                in_ba_op_code = get_ints(line)
            elif i > 3145:
                op_codes.append(get_ints(line))
        return ba_sets, op_codes


@timed
def part1(opcodes):
    ba_sets, opcodes = opcodes
    ops = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']
    three_or_more = 0
    for b, op_code, a in ba_sets:
        count = 0
        for op in ops:
            bb = b[:]
            if run_code(bb, op, op_code[1:]) == a:
                count += 1
        if count >= 3:
            three_or_more += 1

    print(three_or_more)


def run_code(regs, code, args):
    a, b, c = args
    if code == 'addr':
        regs[c] = regs[a] + regs[b]
    elif code == 'addi':
        regs[c] = regs[a] + b
    elif code == 'mulr':
        regs[c] = regs[a] * regs[b]
    elif code == 'muli':
        regs[c] = regs[a] * b
    elif code == 'banr':
        regs[c] = regs[a] & regs[b]
    elif code == 'bani':
        regs[c] = regs[a] & b
    elif code == 'borr':
        regs[c] = regs[a] | regs[b]
    elif code == 'bori':
        regs[c] = regs[a] | b
    elif code == 'setr':
        regs[c] = regs[a]
    elif code == 'seti':
        regs[c] = a
    elif code == 'gtir':
        regs[c] = 1 if a > regs[b] else 0
    elif code == 'gtri':
        regs[c] = 1 if regs[a] > b else 0
    elif code == 'gtrr':
        regs[c] = 1 if regs[a] > regs[b] else 0
    elif code == 'eqir':
        regs[c] = 1 if a == regs[b] else 0
    elif code == 'eqri':
        regs[c] = 1 if regs[a] == b else 0
    elif code == 'eqrr':
        regs[c] = 1 if regs[a] == regs[b] else 0
    return regs


@timed
def part2(opcodes):
    ba_sets, opcodes = opcodes
    ops = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']
    ops_matches = defaultdict(set)
    for b, op_code, a in ba_sets:
        for op in ops:
            bb = b[:]
            if run_code(bb, op, op_code[1:]) == a:
                ops_matches[op].add(op_code[0])

    int_to_op = {}
    while len(ops_matches) > 0:
        op, match_set = sorted(ops_matches.items(), key=lambda x: len(x[1]))[0]
        ops_matches.pop(op)

        int_op = match_set.pop()
        int_to_op[int_op] = op

        for match_set in ops_matches.values():
            match_set.discard(int_op)

    regs = [0, 0, 0, 0]
    for opcode in opcodes:
        run_code(regs, int_to_op[opcode[0]], opcode[1:])

    print(regs[0])


if __name__ == '__main__':
    opcode_list = read()
    part1(opcode_list)
    part2(opcode_list)
