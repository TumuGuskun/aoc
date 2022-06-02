import re

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: x.rstrip(), input_file.readlines()))


@timed
def part1(strings):
    delta = 0
    for string in strings:
        paren = re.sub(r'\\\\', r'2', string[1:-1])
        hexed = re.sub(r'\\x[0-9a-f^x]{2}', r'1', paren)
        escaped = re.sub(r'\\', r'', hexed)
    print(delta)


@timed
def part2(strings):
    delta = 0
    for string in strings:
        delta += string.count('"') + string.count('\\') + 2
    print(delta)


if __name__ == '__main__':
    string_list = read()
    part1(string_list)
    part2(string_list)
