from collections import Counter

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.readlines()


@timed
def part1(ids):
    three_count = 0
    two_count = 0
    for box_id in ids:
        counted = Counter(box_id)
        if 2 in counted.values():
            two_count += 1
        if 3 in counted.values():
            three_count += 1

    print(two_count * three_count)


@timed
def part2(ids):
    for i in range(len(ids[0])):
        if two_value := [key for key, value in Counter(map(lambda box_id: box_id[:i] + box_id[i + 1:-1], ids)).items() if value == 2]:
            print(two_value.pop())
            return


if __name__ == '__main__':
    id_list = read()
    part1(id_list)
    part2(id_list)
