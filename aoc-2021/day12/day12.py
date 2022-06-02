import sys
from collections import defaultdict

from shared.Util import *
from shared.bfs import BFS


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        edges = defaultdict(list)
        for line in input_file:
            a, b = line.rstrip().split('-')
            edges[a].append(b)
            edges[b].append(a)
        for value in edges.values():
            if 'start' in value:
                value.remove('start')
        edges.pop('end')
        return edges


@timed
def part1(edges):
    def count(curr, space):
        return curr == 'end'

    def neighbor(curr, path, space):
        return filter(lambda n: n.isupper() or n not in path, space[curr])

    print(BFS('start', edges, neighbor, count_condition=count).run().count)


@timed
def part2(edges):

    def count(curr, space):
        return curr == 'end'

    paths = set()
    for edge in edges.keys():
        if edge.islower() and edge != 'start':

            def neighbor(curr, path, space):
                neighbors = []
                for n in space[curr]:
                    if n.islower():
                        if n == edge and path.count(n) < 2:
                            neighbors.append(n)
                        elif n not in path:
                            neighbors.append(n)
                    else:
                        neighbors.append(n)
                return neighbors

            paths |= BFS('start', edges, neighbor, count_condition=count).run().paths

    print(len(paths))


if __name__ == '__main__':
    edge_list = read()
    part1(edge_list)
    part2(edge_list)
