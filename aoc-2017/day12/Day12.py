from collections import defaultdict
from queue import Queue

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        programs = defaultdict(list)
        for line in input_file.readlines():
            program, rest = line.split(' <-> ')
            programs[int(program)].extend(list(map(int, rest.split(', '))))
        return programs


@timed
def part1(programs):
    queue = Queue()
    seen = set()
    queue.put(0)
    seen.add(0)

    while not queue.empty():
        curr_program = queue.get()
        for program in programs[curr_program]:
            if program not in seen:
                seen.add(program)
                queue.put(program)
    print(len(seen))


@timed
def part2(programs):
    queue = Queue()
    seen = set()
    counter = 0

    for program in programs:
        if program not in seen:
            counter += 1
            queue.put(program)
            seen.add(program)

            while not queue.empty():
                curr_program = queue.get()
                for next_program in programs[curr_program]:
                    if next_program not in seen:
                        seen.add(next_program)
                        queue.put(next_program)
    print(counter)


if __name__ == '__main__':
    program_list = read()
    part1(program_list)
    part2(program_list)
