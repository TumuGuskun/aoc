import re

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        ips = []
        for line in input_file.readlines():
            line = line.rstrip().replace('[', ' ').replace(']', ' ').split()
            outsides = line[::2]
            insides = line[1::2]
            ips.append({'outsides': outsides, 'insides': insides})
    return ips


def find_abba(string):
    for i in range(len(string) - 3):
        if string[i] == string[i + 3] and string[i + 1] == string[i + 2] and string[i] != string[i + 1]:
            return True
    return False


@timed
def part1(ips):
    count = 0
    for ip in ips:
        in_outsides = any(find_abba(string) for string in ip['outsides'])
        in_insides = any(find_abba(string) for string in ip['insides'])
        if in_outsides and not in_insides:
            count += 1
    print(count)


@timed
def part2(ips):
    count = 0
    for ip in ips:
        abas = []
        for outside in ip['outsides']:
            for i in range(len(outside) - 2):
                if outside[i] == outside[i + 2] and outside[i] != outside[i + 1]:
                    abas.append(outside[i:i+2])
        for aba in abas:
            bab = aba[1] + aba[0] + aba[1]
            if any(bab in inside for inside in ip['insides']):
                count += 1
                break
    print(count)


if __name__ == '__main__':
    ip_list = read()
    part1(ip_list)
    part2(ip_list)
