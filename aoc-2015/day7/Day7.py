from functools import cache

from shared.Util import timed

OPERATIONS = {}

@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    operations = {}
    with open(file_name) as input_file:
        for line in map(lambda x: x.rstrip(), input_file.readlines()):
            expression, out_gate = line.split(' -> ')
            operands = expression.split(' ')
            if len(operands) == 1:
                a = int(operands[0]) if operands[0].isdigit() else operands[0]
                operations[out_gate] = {'inputs': a, 'op': 'eq'}
            elif len(operands) == 2:
                operations[out_gate] = {'inputs': operands[1], 'op': operands[0]}
            else:
                a = int(operands[0]) if operands[0].isdigit() else operands[0]
                b = int(operands[2]) if operands[2].isdigit() else operands[2]
                operations[out_gate] = {'inputs': [a, b], 'op': operands[1]}
    return operations


@cache
def evaluate(node):
    if type(node) is int:
        return node
    else:
        next_node = OPERATIONS[node]
        if next_node['op'] == 'eq':
            return evaluate(next_node['inputs'])
        elif next_node['op'] == 'NOT':
            return ~ evaluate(next_node['inputs'])
        elif next_node['op'] == 'AND':
            return evaluate(next_node['inputs'][0]) & evaluate(next_node['inputs'][1])
        elif next_node['op'] == 'OR':
            return evaluate(next_node['inputs'][0]) | evaluate(next_node['inputs'][1])
        elif next_node['op'] == 'RSHIFT':
            return evaluate(next_node['inputs'][0]) >> evaluate(next_node['inputs'][1])
        elif next_node['op'] == 'LSHIFT':
            return evaluate(next_node['inputs'][0]) << evaluate(next_node['inputs'][1])
        else:
            raise Exception(f'Unexpected op: {next_node}')


@timed
def part1(operations):
    print(evaluate('a') % 65536)


@timed
def part2(operations):
    evaluate.cache_clear()
    global OPERATIONS
    OPERATIONS['b']['inputs'] = 16076
    print(evaluate('a') % 65536)


if __name__ == '__main__':
    operation_list = read()
    OPERATIONS.update(operation_list)
    part1(operation_list)
    part2(operation_list)
