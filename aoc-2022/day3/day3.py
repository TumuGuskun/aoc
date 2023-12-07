from shared.util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return [line.strip() for line in input_file]


@timed
def part1(inputs):
    total = 0
    for rucksack in inputs:
        first = set(rucksack[: len(rucksack) // 2])
        second = set(rucksack[len(rucksack) // 2 :])
        intersection = first & second
        if (letter := intersection.pop()) in "abcdefghijklmnopqrstuvwxyz":
            total += ord(letter) - 96
        else:
            total += ord(letter) - 64 + 26
    print(total)


@timed
def part2(inputs):
    total = 0
    group_badges = set()
    for i, rucksack in enumerate(inputs):
        if i % 3 == 0:
            group_badges = set(rucksack)
        if i % 3 < 2:
            group_badges &= set(rucksack)
        else:
            group_badges &= set(rucksack)
            if (letter := group_badges.pop()) in "abcdefghijklmnopqrstuvwxyz":
                total += ord(letter) - 96
            else:
                total += ord(letter) - 64 + 26
            group_badges = set()
    print(total)


if __name__ == "__main__":
    input_list = read()
    part1(input_list)
    part2(input_list)
