from collections import defaultdict
from itertools import islice, count
from math import sqrt
from queue import Queue

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return [(op, list(map(lambda y: int(y) if y[-1].isdigit() else y, args))) for op, *args in map(lambda line: line.rstrip().split(), input_file.readlines())]


def run_instruction(instructions, pointer, registers, send_queue: Queue, receive_queue: Queue):
    op, args = instructions[pointer]
    if op == 'snd':
        a, = args
        send_queue.put(registers[a])
        pointer += 1
    elif op == 'set':
        a, b = args
        registers[a] = b if isinstance(b, int) else registers[b]
        pointer += 1
    elif op == 'add':
        a, b = args
        registers[a] += b if isinstance(b, int) else registers[b]
        pointer += 1
    elif op == 'sub':
        a, b = args
        registers[a] -= b if isinstance(b, int) else registers[b]
        pointer += 1
    elif op == 'mul':
        a, b = args
        registers[a] *= b if isinstance(b, int) else registers[b]
        pointer += 1
    elif op == 'mod':
        a, b = args
        registers[a] %= b if isinstance(b, int) else registers[b]
        pointer += 1
    elif op == 'rcv':
        a, = args
        if not receive_queue.empty():
            registers[a] = receive_queue.get()
            pointer += 1
    elif op == 'jgz':
        a, b = args
        c = a if isinstance(a, int) else registers[a]
        pointer += (b if isinstance(b, int) else registers[b]) if c > 0 else 1
    elif op == 'jnz':
        a, b = args
        c = a if isinstance(a, int) else registers[a]
        pointer += (b if isinstance(b, int) else registers[b]) if c != 0 else 1

    return pointer


@timed
def part1(instructions):
    registers = defaultdict(int)
    pointer = 0
    counter = 0
    while 0 <= pointer < len(instructions):
        op, _ = instructions[pointer]
        if op == 'mul':
            counter += 1
        pointer = run_instruction(instructions, pointer, registers, None, None)

    print(counter)


def is_prime(n):
    return all(n % i for i in islice(count(2), int(sqrt(n) - 1)))


@timed
def part2(instructions):
    print(len(list(filter(lambda num: not is_prime(num), range(106700, 123701, 17)))))
    print(sum(1 for num in range(106700, 123701, 17) if not is_prime(num)))


if __name__ == '__main__':
    instruction_list = read()
    part1(instruction_list)
    part2(instruction_list)
