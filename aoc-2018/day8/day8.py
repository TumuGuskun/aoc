from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.read().split()))


@timed
def part1(nodes):
    print(get_metadata(nodes)[1])


def get_metadata(nodes):
    if not nodes:
        return [], 0
    else:
        children, meta_count = nodes[:2]
        nodes = nodes[2:]
        meta_sum = 0
        for _ in range(children):
            nodes, child_sum = get_metadata(nodes)
            meta_sum += child_sum

        for i in range(meta_count):
            meta_sum += nodes[i]

        return nodes[meta_count:], meta_sum


@timed
def part2(nodes):
    print(updated_get_weight(nodes)[1])


def updated_get_weight(nodes):
    if not nodes:
        return [], 0
    else:
        children, meta_count = nodes[:2]
        nodes = nodes[2:]

        if not children:
            return nodes[meta_count:], sum(nodes[:meta_count])
        else:
            child_weights = []
            for _ in range(children):
                nodes, child_sum = updated_get_weight(nodes)
                child_weights.append(child_sum)

            weight = 0
            for i in range(meta_count):
                index = nodes[i]
                if index - 1 < len(child_weights):
                    weight += child_weights[index - 1]

            return nodes[meta_count:], weight


if __name__ == '__main__':
    node_list = read()
    part1(node_list)
    part2(node_list)
