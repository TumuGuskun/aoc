from shared.Util import timed


@timed
def read():
    file_name = f'input.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: tuple(map(int, x.split('x'))), input_file.readlines()))


@timed
def part1(boxes):
    print(sum(map(lambda b: 2 * (b[0] * b[1] + b[0] * b[2] + b[1] * b[2]) + min(b[0] * b[1], b[0] * b[2], b[1] * b[2]), boxes)))


@timed
def part2(boxes):
    print(sum(map(lambda b: b[0] * b[1] * b[2] + 2 * min(b[0] + b[1], b[0] + b[2], b[1] + b[2]), boxes)))


if __name__ == '__main__':
    box_list = read()
    part1(box_list)
    part2(box_list)
