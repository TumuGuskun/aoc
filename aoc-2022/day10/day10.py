import os
import numpy as np

from shared.gum import gum_choose
from shared.util import timed, read_op_codes, OpCode
from shared.grid import Grid


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return read_op_codes(lines=input_file.readlines())


def add_to_output(cycle_count: int, signal_strength: int) -> int:
    if cycle_count in [20, 60, 100, 140, 180, 220]:
        return signal_strength * cycle_count
    return 0


@timed
def part1(op_codes: list[OpCode]):
    signal_strength = 1
    output = 0
    cycle_count = 0
    for op_code in op_codes:
        match op_code.op:
            case "noop":
                cycle_count += 1
                output += add_to_output(
                    cycle_count=cycle_count, signal_strength=signal_strength
                )
            case "addx":
                for _ in range(2):
                    cycle_count += 1
                    output += add_to_output(
                        cycle_count=cycle_count, signal_strength=signal_strength
                    )
                signal_strength += op_code.first
    print(output)


@timed
def part2(op_codes: list[OpCode]):
    grid = np.chararray((6, 40), unicode=True)
    grid[:] = str(".")
    screen = Grid(grid=grid)
    gen_op_codes = (op_code for op_code in op_codes)

    addx_1 = False
    addx_2 = False
    curr_op_code = OpCode(op="noop", args=[])
    curr_position = 1
    for cycle in range(240):
        if not addx_1 and not addx_2:
            curr_op_code = next(gen_op_codes)
            if curr_op_code.op == "addx":
                addx_1 = True
        if cycle % 40 in range(curr_position - 1, curr_position + 2):
            screen.set_point(value="#", i=(cycle // 40), j=(cycle % 40))
        if addx_2:
            curr_position += curr_op_code.first
            addx_1 = False
            addx_2 = False
        if addx_1:
            addx_2 = True
    print(screen)


if __name__ == "__main__":
    op_code_list = read()
    part1(op_code_list)
    part2(op_code_list)
