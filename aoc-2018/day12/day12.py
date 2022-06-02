from collections import defaultdict

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        initial_state = input_file.readline().rstrip().split('initial state: ').pop()
        input_file.readline()
        rules = {}
        for line in input_file.readlines():
            match, output = line.rstrip().split(' => ')
            rules[match] = output
        return initial_state, rules


@timed
def part1(rules):
    initial_states, rules = rules
    row = defaultdict(lambda: '.', {k: v for k, v in enumerate(initial_states)})

    for _ in range(20):
        new_row = defaultdict(lambda: '.')
        planted = [key for key, value in row.items() if value == '#']
        for i in range(min(planted) - 2, max(planted) + 3):
            match_string = row[i - 2] + row[i - 1] + row[i] + row[i + 1] + row[i + 2]
            new_row[i] = rules[match_string]
        row = new_row

    print(sum(x for x, plant in row.items() if plant == '#'))


@timed
def part2(rules):
    initial_states, rules = rules
    row = defaultdict(lambda: '.', {k: v for k, v in enumerate(initial_states)})

    seen = {}
    diff = 0
    for _ in range(50000000000):
        new_row = defaultdict(lambda: '.')
        planted = [key for key, value in row.items() if value == '#']
        for i in range(min(planted) - 2, max(planted) + 3):
            match_string = row[i - 2] + row[i - 1] + row[i] + row[i + 1] + row[i + 2]
            new_row[i] = rules[match_string]
        row = new_row
        if (curr_row := ''.join(row.values())) in seen:
            diff = 50000000000 - _ - 1
            break
        else:
            seen[curr_row] = _

    print(sum(x + diff for x, plant in row.items() if plant == '#'))


if __name__ == '__main__':
    rule_list = read()
    part1(rule_list)
    part2(rule_list)
