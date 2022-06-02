from functools import cache
from itertools import count

from shared.Util import timed, ints

@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        scanners = {}
        for line in input_file.readlines():
            scanner, depth = map(int, line.split(': '))
            scanners[scanner] = depth
        return scanners


@timed
def part1(scanners):
    scan_table = {}
    for scanner in scanners:
        scan_table[scanner] = (0, False)

    severity = 0
    position = -1
    for _ in range(max(scanners) + 1):
        position += 1
        if position in scan_table:
            if scan_table[position][0] == 0:
                severity += position * scanners[position]
        for scanner, (scan_pos, up) in scan_table.items():
            if up:
                if scan_pos == 0:
                    scan_table[scanner] = (1, False)
                else:
                    scan_table[scanner] = (scan_pos - 1, True)
            else:
                if scan_pos == scanners[scanner] - 1:
                    scan_table[scanner] = (scan_pos - 1, True)
                else:
                    scan_table[scanner] = (scan_pos + 1, False)
    print(severity)


@cache
def get_scan_pos(time, depth):
    if time == 0:
        return 0, False
    else:
        scan_pos, up = get_scan_pos(time - 1, depth)
        if up:
            if scan_pos == 0:
                return scan_pos + 1, False
            else:
                return scan_pos - 1, True
        else:
            if scan_pos == depth - 1:
                return scan_pos - 1, True
            else:
                return scan_pos + 1, False


@timed
def part2(scanners):
    print(next(i for i in ints() if all((s + i) % (2 * d - 2) != 0 for s, d in scanners.items())))


if __name__ == '__main__':
    scanner_list = read()
    part1(scanner_list)
    part2(scanner_list)
