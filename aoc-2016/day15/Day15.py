from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        discs = []
        for line in map(lambda l: l.rstrip(), input_file.readlines()):
            position, rest = line[6:-1].split(' has ')
            rotations, start = rest.split(' positions; at time=0, it is at position ')
            discs.append((int(position), int(rotations), int(start)))
        return discs


@timed
def part1(discs):
    current = 0
    increment = 1
    for position, rotations, start in discs[:-1]:
        while (current + position + start) % rotations != 0:
            current += increment
        increment *= rotations

    print(current)


@timed
def part2(discs):
    current = 0
    increment = 1
    for position, rotations, start in discs:
        while (current + position + start) % rotations != 0:
            current += increment
        increment *= rotations

    print(current)


if __name__ == '__main__':
    disc_list = read()
    part1(disc_list)
    part2(disc_list)
