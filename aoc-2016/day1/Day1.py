from shared.Util import timed

DIRS = {
    'N': {
        'R': 'E',
        'L': 'W',
        'vec': (0, 1)
    },
    'E': {
        'R': 'S',
        'L': 'N',
        'vec': (1, 0)
    },
    'S': {
        'R': 'W',
        'L': 'E',
        'vec': (0, -1)
    },
    'W': {
        'R': 'N',
        'L': 'S',
        'vec': (-1, 0)
    }
}


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: (x[0], int(x[1:])), input_file.read().split(', ')))


@timed
def part1(directions):
    curr_dir = 'N'
    pos_x, pos_y = 0, 0
    for turn, distance in directions:
        next_dir = DIRS[curr_dir][turn]
        next_x, next_y = DIRS[next_dir]['vec']
        pos_x += next_x * distance
        pos_y += next_y * distance
        curr_dir = next_dir

    print(abs(pos_x) + abs(pos_y))


@timed
def part2(directions):
    curr_dir = 'N'
    pos_x, pos_y = 0, 0
    poses = set()
    poses.add((0, 0))
    for turn, distance in directions:
        next_dir = DIRS[curr_dir][turn]
        next_x, next_y = DIRS[next_dir]['vec']
        for _ in range(distance):
            pos_x += next_x
            pos_y += next_y
            if (pos_x, pos_y) in poses:
                print(abs(pos_x) + abs(pos_y))
                return
            else:
                poses.add((pos_x, pos_y))
        curr_dir = next_dir


if __name__ == '__main__':
    direction_list = read()
    part1(direction_list)
    part2(direction_list)
