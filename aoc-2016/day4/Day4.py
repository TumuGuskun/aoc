from collections import Counter

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        data = []
        for line in map(lambda x: x.rstrip(), input_file.readlines()):
            name = line[:-11]
            sector_id = line[-10:-7]
            checksum = line[-6:-1]
            data.append((name, int(sector_id), checksum))
        return data


@timed
def part1(data):
    count = 0
    for name, sector_id, checksum in data:
        counts = Counter(name.replace('-', ''))
        real = True
        most_common = list(reversed(sorted(counts.most_common(), key=lambda x: (-x[1], x[0]))))
        for check in checksum:
            if not check == most_common.pop()[0]:
                real = False
                break
        if real:
            count += sector_id
    print(count)


@timed
def part2(data):
    for name, sector_id, checksum in data:
        real_name = ''.join(list(map(lambda s: chr((ord(s) + sector_id - 97) % 26 + 97), name)))
        real_name = real_name.replace('f', ' ')
        if real_name.startswith('north'):
            print(sector_id)
            break


if __name__ == '__main__':
    data_list = read()
    part1(data_list)
    part2(data_list)
