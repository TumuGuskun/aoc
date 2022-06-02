from collections import defaultdict
from copy import deepcopy

from shared.Util import timed, Point

DIR_MAP = {
    'u': {
        'r': 'r',
        'l': 'l',
        'vec': Point(-1, 0)
    },
    'd': {
        'r': 'l',
        'l': 'r',
        'vec': Point(1, 0)
    },
    'l': {
        'r': 'u',
        'l': 'd',
        'vec': Point(0, -1)
    },
    'r': {
        'r': 'd',
        'l': 'u',
        'vec': Point(0, 1)
    },
}


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        grid = defaultdict(lambda: defaultdict(lambda: '.'))
        for i, row in enumerate(map(lambda li: list(li.rstrip()), input_file.readlines())):
            for j, col in enumerate(row):
                grid[i][j] = col
        return grid


@timed
def part1(nodes):
    nodes = deepcopy(nodes)
    curr = Point(len(nodes) // 2, len(nodes[0]) // 2)
    direction = 'u'
    infected = 0

    for _ in range(10000):
        if nodes[curr.x][curr.y] == '#':
            direction = DIR_MAP[direction]['r']
            nodes[curr.x][curr.y] = '.'
        else:
            direction = DIR_MAP[direction]['l']
            nodes[curr.x][curr.y] = '#'
            infected += 1

        curr += DIR_MAP[direction]['vec']

    print(infected)


@timed
def part2(nodes):
    curr = Point(len(nodes) // 2, len(nodes[0]) // 2)
    direction = 'u'
    infected = 0

    for _ in range(10000000):
        if (node := nodes[curr.x][curr.y]) == '#':
            direction = DIR_MAP[direction]['r']
            nodes[curr.x][curr.y] = 'f'
        elif node == '.':
            direction = DIR_MAP[direction]['l']
            nodes[curr.x][curr.y] = 'w'
        elif node == 'f':
            direction = DIR_MAP[direction]['l']
            direction = DIR_MAP[direction]['l']
            nodes[curr.x][curr.y] = '.'
        elif node == 'w':
            nodes[curr.x][curr.y] = '#'
            infected += 1

        curr += DIR_MAP[direction]['vec']

    print(infected)


if __name__ == '__main__':
    node_list = read()
    part1(node_list)
    part2(node_list)
