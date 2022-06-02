from math import prod

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        binary = f'{bin(int(input_file.read(), 16))[2:]}'
        binary = '0' * (4 - len(binary) % 4) + binary
        return binary


@timed
def part1(binary):
    version, _, _ = parse(binary)
    print(version)


@timed
def part2(binary):
    _, value, _ = parse(binary)
    print(value)


def parse(binary):
    version = int(binary, 2)
    pid = int(binary[3:6], 2)
    binary = binary[6:]

    if pid == 4:
        literals = ''
        while binary[0] == '1':
            literals += binary[1:5]
            binary = binary[5:]

        literals += binary[1:5]
        binary = binary[5:]
        value = int(literals, 2)
    else:
        sub_values, sub_versions = [], []
        if binary[0] == '0':
            len_bits = 15
            binary = binary[1:]

            len_sub_packs = int(binary[:len_bits], 2)
            binary = binary[len_bits:]
            sub_binary = binary[:len_sub_packs]
            binary = binary[len_sub_packs:]
            while sub_binary:
                sub_version, sub_value, sub_binary = parse(sub_binary)
                sub_values.append(sub_value)
                sub_versions.append(sub_version)
        else:
            len_bits = 11
            binary = binary[1:]

            sub_packs = int(binary[:len_bits], 2)
            binary = binary[len_bits:]
            sub_values = []
            for _ in range(sub_packs):
                sub_version, sub_value, binary = parse(binary)
                sub_values.append(sub_value)
                sub_versions.append(sub_version)

        if pid == 0:
            value = sum(sub_values)
        elif pid == 1:
            value = prod(sub_values)
        elif pid == 2:
            value = min(sub_values)
        elif pid == 3:
            value = max(sub_values)
        elif pid == 5:
            value = int(sub_values[0] > sub_values[1])
        elif pid == 6:
            value = int(sub_values[0] < sub_values[1])
        elif pid == 7:
            value = int(sub_values[0] == sub_values[1])
        else:
            raise Exception('Fuck you')

        version += sum(sub_versions)

    return version, value, binary


if __name__ == '__main__':
    transmission_list = read()
    part1(transmission_list)
    part2(transmission_list)
