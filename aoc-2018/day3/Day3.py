import re
from collections import Counter

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        claims = []
        for claim in input_file.readlines():
            search = re.search(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', claim)
            claims.append((search.group(1), tuple(map(int, search.group(2, 3))), tuple(map(int, search.group(4, 5)))))
        return claims


@timed
def part1(claims):
    counts = Counter()
    for _, (start_x, start_y), (width, height) in claims:
        for i in range(1, width + 1):
            for j in range(1, height + 1):
                counts[(start_x + i, start_y + j)] += 1

    print(len([count for count, value in counts.items() if value >= 2]))


@timed
def part2(claims):
    counts = Counter()
    for _, (start_x, start_y), (width, height) in claims:
        for i in range(1, width + 1):
            for j in range(1, height + 1):
                counts[(start_x + i, start_y + j)] += 1

    for box_id, (start_x, start_y), (width, height) in claims:
        found = True
        for i in range(1, width + 1):
            for j in range(1, height + 1):
                if counts[(start_x + i, start_y + j)] != 1:
                    found = False
                    break
            if not found:
                break
        if found:
            print(box_id)


if __name__ == '__main__':
    claim_list = read()
    part1(claim_list)
    part2(claim_list)
