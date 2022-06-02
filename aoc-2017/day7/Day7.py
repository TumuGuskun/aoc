import re

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        programs = []
        for line in input_file.readlines():
            line = line.rstrip()
            if '->' in line:
                start, nodes = line.split(' -> ')
                nodes = nodes.split(', ')
            else:
                start = line
                nodes = []

            name, weight = re.search(r'(\w+) \((\d+)\)', start).groups()
            programs.append((name, weight, nodes))
        return programs


@timed
def part1(programs):
    adjacency = {}
    for program, weight, nodes in programs:
        for node in nodes:
            adjacency[node] = program

    print(next(p for p, _, _ in programs if p not in adjacency))


class Node:
    def __init__(self, name, weight, nodes, programs):
        self.name = name
        self.weight = int(weight)
        self.nodes = []
        for node in nodes:
            name, weight, sub_nodes = next(p for p in programs if p[0] == node)
            self.nodes.append(Node(name, weight, sub_nodes, programs))

    def get_sub_weights(self):
        return [node.get_weight() for node in self.nodes]

    def get_weight(self):
        return self.weight + sum(self.get_sub_weights())

    def is_balanced(self):
        sub_weights = len(set(self.get_sub_weights()))
        return sub_weights == 1 or sub_weights == 0


def balance(node):
    if node.is_balanced():
        return
    else:
        print([(n.weight, n.get_weight()) for n in node.nodes])
        for node in node.nodes:
            balance(node)


@timed
def part2(programs):
    name, weight, nodes = next(p for p in programs if p[0] == 'vmpywg')
    head = Node(name, weight, nodes, programs)

    balance(head)


if __name__ == '__main__':
    program_list = read()
    part1(program_list)
    part2(program_list)
