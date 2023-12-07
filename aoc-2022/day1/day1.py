from shared.util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        elves = []
        elf = []
        for line in input_file.readlines():
            if line == "\n":
                elves.append(sum(elf))
                elf = []
            else:
                elf.append(int(line))
        return elves


@timed
def part1(inputs):
    print(max(inputs))


@timed
def part2(inputs):
    print(sum(sorted(inputs, reverse=True)[:3]))


if __name__ == "__main__":
    input_list = read()
    part1(input_list)
    part2(input_list)
