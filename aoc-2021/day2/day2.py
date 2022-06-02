from shared.Util import timed, Point, get_ints


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        steps = []
        for line in input_file:
            if line.startswith('f'):
                steps.append((Point(1, 0), get_ints(line).pop()))
            elif line.startswith('d'):
                steps.append((Point(0, -1), get_ints(line).pop()))
            elif line.startswith('u'):
                steps.append((Point(0, 1), get_ints(line).pop()))
            else:
                steps.append((Point(-1, 0), get_ints(line).pop()))
        return steps


@timed
def part1(steps):
    sub = Point(0, 0)

    for direction, count in steps:
        for _ in range(count):
            sub += direction

    print(abs(sub.x) * abs(sub.y))


@timed
def part2(steps):
    sub = Point(0, 0)

    aim = 0
    for direction, count in steps:
        if direction == Point(0, -1) or direction == Point(0, 1):
            aim += count * direction.y
        else:
            for _ in range(count):
                sub += direction + Point(0, aim)

    print(abs(sub.x) * abs(sub.y))


if __name__ == '__main__':
    step_list = read()
    part1(step_list)
    part2(step_list)
