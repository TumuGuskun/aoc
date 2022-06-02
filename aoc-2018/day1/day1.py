from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.readlines()))


@timed
def part1(frequencies):
    print(sum(frequencies))


@timed
def part2(frequencies):
    seen = set()
    running = 0
    pointer = 0
    while running not in seen:
        running += frequencies[pointer % len(frequencies)]
        seen.add(running)
        print(seen)
        pointer += 1

    print(running)


if __name__ == '__main__':
    frequency_list = read()
    part1(frequency_list)
    part2(frequency_list)
