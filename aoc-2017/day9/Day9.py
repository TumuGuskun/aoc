import json

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.read()


@timed
def part1(streams):
    in_garbage = False
    escaped = False
    depth = 0
    count = 0
    garbage = 0
    for e in streams:
        if in_garbage:
            if not escaped:
                if e == '!':
                    escaped = True
                elif e == '>':
                    in_garbage = False
                else:
                    garbage += 1
            else:
                escaped = False
        else:
            if e == '{':
                depth += 1
            elif e == '}':
                count += depth
                depth -= 1
            elif e == '<':
                in_garbage = True
    print(count, garbage)


@timed
def part2(streams):
    pass


if __name__ == '__main__':
    stream_list = read()
    part1(stream_list)
    part2(stream_list)
