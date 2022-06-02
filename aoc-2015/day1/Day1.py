from shared.Util import timed


@timed
def read():
    file_name = f'input.txt'
    with open(file_name) as input_file:
        return list(input_file.read())


@timed
def part1(parens):
    print(sum(map(lambda x: 1 if x == '(' else -1, parens)))


@timed
def part2(parens):
    floor = 0
    for i, paren in enumerate(parens):
        floor += 1 if paren == '(' else -1
        if floor == -1:
            print(i + 1)
            break


if __name__ == '__main__':
    paren_list = read()
    part1(paren_list)
    part2(paren_list)
