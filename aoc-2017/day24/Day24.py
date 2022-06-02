from queue import Queue

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        components = []
        for line in input_file.readlines():
            port_1, port_2 = map(int, line.split('/'))
            components.append(Component(port_1, port_2))
        return components


class Component:
    def __init__(self, port_1, port_2):
        if port_1 < port_2:
            self.port_1 = port_1
            self.port_2 = port_2
        else:
            self.port_1 = port_2
            self.port_2 = port_1

        self.available = 2

    def get_available(self):
        if self.available == 0:
            return self.port_1
        elif self.available == 1:
            return self.port_2
        else:
            return self.port_1, self.port_2

    def can_connect(self, port):
        return self.port_1 == port or self.port_2 == port

    def __repr__(self):
        return f'({self.port_1}, {self.port_2})'

    def value(self):
        return self.port_1 + self.port_2

    def __eq__(self, other):
        return self.port_1 == other.port_1 and self.port_2 == other.port_2

    def __copy__(self):
        return Component(self.port_1, self.port_2)

    def __hash__(self):
        return hash(self.port_1) + hash(self.port_2)


def use_or_lose(components, curr):
    if not components:
        return 0
    else:
        top_score = 0
        for component in components:
            new_components = components.copy()
            new_components.remove(component)
            if component.port_1 == curr:
                use = component.value() + use_or_lose(new_components, component.port_2)
                lose = use_or_lose(new_components, curr)
                top_score = max(use, lose)
            elif component.port_2 == curr:
                use = component.value() + use_or_lose(new_components, component.port_1)
                lose = use_or_lose(new_components, curr)
                top_score = max(use, lose)
            else:
                top_score = max(top_score, use_or_lose(new_components, curr))

        return top_score


@timed
def part1(bridges):
    queue = []
    seen = []
    queue.append((Component(0, 0), 0, 0, 0))

    top_score = 0

    while len(queue) > 0:
        curr, used, score, depth = queue.pop()
        out_port = curr.port_1 if used == curr.port_2 else curr.port_2
        top_score = max(top_score, score)
        seen = [e for e in seen if e[1] <= depth]

        for next_component in filter(lambda c: c.can_connect(out_port), bridges):
            if not any(next_component == c[0] for c in seen):
                seen.append((next_component, depth))
                queue.append((next_component, out_port, next_component.value() + score, depth + 1))

    print(top_score)


@timed
def part2(bridges):
    pass


if __name__ == '__main__':
    bridge_list = read()
    part1(bridge_list)
    part2(bridge_list)
