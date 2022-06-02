from collections import defaultdict
from functools import cache
from queue import Queue

from shared.Util import timed

REPLACEMENTS = {}


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    replacements = defaultdict(list)
    with open(file_name) as input_file:
        broke = False
        for line in input_file.readlines():
            line = line.rstrip()
            if not broke:
                if line:
                    start, finish = line.split(' => ')
                    replacements[start].append(finish)
                else:
                    broke = True
            else:
                molecule = line
    return replacements, molecule


@timed
def part1(replacements, molecule):
    unique_moles = set()
    for start, finishes in replacements.items():
        for i in range(len(molecule) - len(start) + 1):
            if molecule[i:].startswith(start):
                for finish in finishes:
                    new_mole = molecule[:i] + finish + molecule[i + len(start):]
                    unique_moles.add(new_mole)
    print(len(unique_moles))


@cache
def replace(molecule):
    if molecule == 'e':
        return 0
    else:
        minimum = float('inf')
        for i in range(len(molecule)):
            for start, finishes in REPLACEMENTS.items():
                for finish in finishes:
                    if molecule[i:].startswith(finish):
                        new_mole = molecule[:i] + start + molecule[i + len(finish):]
                        minimum = min(1 + replace(new_mole), minimum)
        return minimum


@timed
def part2(replacements, molecule):
    total = sum(1 for token in molecule if token.isupper())
    ar_rn = 0
    y = 0
    for i in range(len(molecule)):
        if molecule[i:].startswith('Ar') or molecule[i:].startswith('Rn'):
            ar_rn += 1
        if molecule[i:].startswith('Y'):
            y += 1

    print(total - ar_rn - 2*y - 1)


@timed
def part2_failed(replacements, molecule):
    queue = Queue()
    queue.put((molecule, 0))
    depth_set = set()
    while not queue.empty():
        curr_mole, depth = queue.get()
        if depth not in depth_set:
            print(depth, len(queue.queue))
            depth_set.add(depth)
        if curr_mole == 'e':
            print(depth)
            return
        else:
            for i in range(len(curr_mole)):
                for start, finishes in replacements.items():
                    for finish in finishes:
                        if curr_mole[i:].startswith(finish):
                            new_mole = curr_mole[:i] + start + curr_mole[i + len(finish):]
                            queue.put((new_mole, depth + 1))


if __name__ == '__main__':
    replacement_list, mole = read()
    part1(replacement_list, mole)
    part2(replacement_list, mole)
