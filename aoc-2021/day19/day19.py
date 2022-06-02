import numpy as np

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        scanners = {}
        for line in map(lambda x: x.rstrip(), input_file.readlines()):
            if 'scanner' in line:
                index = get_ints(line).pop()
                beacons = []
            elif line == '':
                scanners[index] = Scanner(index, beacons)
            else:
                beacons.append(get_ints(line))
        return scanners


class Scanner:
    def __init__(self, index, beacons):
        self.index = index
        self.coordinates = None
        self.grid = np.zeros((2000, 2000, 2000))
        for beacon in beacons:
            self.grid[tuple(map(lambda x: x + 1000, beacon))] = 1

    def __repr__(self):
        return f'{self.grid}'


@timed
def part1(scans):
    big_grid = np.zeros((1000, 1000, 1000))



@timed
def part2(scans):
    pass


if __name__ == '__main__':
    scan_list = read()
    part1(scan_list)
    part2(scan_list)
