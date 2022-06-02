import numpy as np

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    instructions = []
    with open(file_name) as input_file:
        for line in input_file.readlines():
            line = line.replace('turn ', '')
            first, end = line.split(' through ')
            instruction, start = first.split(' ')
            instructions.append((instruction, tuple(map(int, start.split(','))), tuple(map(int, end.split(',')))))
    return instructions


@timed
def part1(instructions):
    grid = np.zeros(shape=(1000, 1000), dtype=np.int8)
    for instruction, start, end in instructions:
        x = end[0] - start[0] + 1
        y = end[1] - start[1] + 1
        if instruction == 'on':
            grid[start[0]:end[0]+1, start[1]:end[1]+1] |= np.ones(shape=(x, y), dtype=np.int8)
        elif instruction == 'off':
            grid[start[0]:end[0]+1, start[1]:end[1]+1] &= np.zeros(shape=(x, y), dtype=np.int8)
        else:
            grid[start[0]:end[0]+1, start[1]:end[1]+1] ^= np.ones(shape=(x, y), dtype=np.int8)
    print(np.sum(grid))


@timed
def part2(instructions):
    grid = np.zeros(shape=(1000, 1000), dtype=np.int8)
    for instruction, start, end in instructions:
        x = end[0] - start[0] + 1
        y = end[1] - start[1] + 1
        if instruction == 'on':
            grid[start[0]:end[0]+1, start[1]:end[1]+1] += np.ones(shape=(x, y), dtype=np.int8)
        elif instruction == 'off':
            temp = grid[start[0]:end[0]+1, start[1]:end[1]+1] - np.ones(shape=(x, y), dtype=np.int8)
            grid[start[0]:end[0]+1, start[1]:end[1]+1] = np.maximum(temp, np.zeros(shape=(x, y), dtype=np.int8))
        else:
            grid[start[0]:end[0]+1, start[1]:end[1]+1] += np.full(shape=(x, y), dtype=np.int8, fill_value=2)
    print(np.sum(grid))


if __name__ == '__main__':
    instruction_list = read()
    part1(instruction_list)
    part2(instruction_list)
