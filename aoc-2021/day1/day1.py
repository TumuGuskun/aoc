from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file))


@timed
def part1(depths):
    print(sum(1 for i, d in enumerate(depths[1:]) if d > depths[i]))


@timed
def part2(depths):
    print(sum(1 for i, d in enumerate(depths[3:]) if d > depths[i]))


if __name__ == '__main__':
    depth_list = read()
    part1(depth_list)
    part2(depth_list)
