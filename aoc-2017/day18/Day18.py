from collections import defaultdict
from queue import Queue

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return [(op, list(map(lambda y: int(y) if y[-1].isdigit() else y, args))) for op, *args in map(lambda line: line.rstrip().split(), input_file.readlines())]


@timed
def part1(instructions):
    registers = defaultdict(int)
    pointer = 0
    while True:
        run_instruction(instructions, pointer, registers)


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

    return pointer


@timed
def part2(instructions):
    reg_1, reg_2 = defaultdict(int), defaultdict(int)
    reg_1['p'], reg_2['p'] = 0, 1
    queue_1, queue_2 = Queue(), Queue()
    pointer_1, pointer_2 = 0, 0

    counter = 0
    rcv_counter = 0
    while True:
        op_1, _ = instructions[pointer_1]
        op_2, _ = instructions[pointer_2]
        if op_2 == 'snd':
            counter += 1
        if op_1 == op_2 == 'rcv':
            rcv_counter += 1
            if rcv_counter == 2:
                print(counter)
                return
        else:
            rcv_counter = 0
        pointer_1 = run_instruction(instructions, pointer_1, reg_1, queue_1, queue_2)
        pointer_2 = run_instruction(instructions, pointer_2, reg_2, queue_2, queue_1)


if __name__ == '__main__':
    instruction_list = read()
    # part1(instruction_list)
    part2(instruction_list)
