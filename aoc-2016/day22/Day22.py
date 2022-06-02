import re

from shared.Util import timed, Point


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        input_file.readline()
        input_file.readline()
        nodes = []
        for line in map(lambda f: f.rstrip(), input_file.readlines()):
            node, size, used, avail, percent = line.split()
            x, y = map(int, re.search(r'x(\d+)-y(\d+)', node).groups())
            size = int(size[:-1])
            used = int(used[:-1])
            avail = int(avail[:-1])
            use_p = int(percent[:-1])
            nodes.append((Point(x, y), size, used, avail, use_p))
        return nodes


@timed
def part1(nodes):
    count = 0
    for coord, size, used, avail, use_p in nodes:
        if used != 0:
            count += sum(1 for o in nodes if o[0] != coord and used <= o[3])
    print(count)


@timed
def part2(nodes):
    curr_y = 0
    curr_line = ''
    for coord, size, used, avail, use_p in sorted(nodes, key=lambda x: (x[0].y, x[0].x)):
        if curr_y == coord.y:
            if use_p == 0:
                curr_line += '_'
            elif used > 100:
                curr_line += '|'
            else:
                curr_line += '.'
        else:
            print(curr_line)
            if use_p == 0:
                curr_line = '_'
            elif used > 100:
                curr_line = '|'
            else:
                curr_line = '.'
            curr_y = coord.y
    print(curr_line)


if __name__ == '__main__':
    node_list = read()
    part1(node_list)
    part2(node_list)
