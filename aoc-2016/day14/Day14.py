from hashlib import md5

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.read()


def find_n_length(string, n, element=None):
    if element:
        return element * n in string
    else:
        for i, e in enumerate(string):
            if e * n in string[i:i+n]:
                return e


@timed
def part1(salt):
    i = 0
    potentials = {}
    keys = []
    while len(keys) < 80:
        md5_hash = md5(f'{salt}{i}'.encode()).hexdigest()
        if e := find_n_length(md5_hash, 3):
            potentials[i] = (e, md5_hash)
        if find_n_length(md5_hash, 5):
            for index, (e, old_md5) in filter(lambda x: 0 < i - x[0] <= 1000, list(potentials.items())):
                if find_n_length(md5_hash, 5, e):
                    keys.append((index, old_md5))
                    potentials.pop(index)
        i += 1
    print(sorted(keys, key=lambda x: x[0])[63][0])


@timed
def part2(salt):
    i = 0
    potentials = {}
    keys = []
    while len(keys) < 64:
        md5_hash = md5(f'{salt}{i}'.encode()).hexdigest()
        for _ in range(2016):
            md5_hash = md5(md5_hash.encode()).hexdigest()
        if e := find_n_length(md5_hash, 3):
            potentials[i] = (e, md5_hash)
        if find_n_length(md5_hash, 5):
            for index, (e, old_md5) in filter(lambda x: 0 < i - x[0] <= 1000, list(potentials.items())):
                if find_n_length(md5_hash, 5, e):
                    keys.append((index, old_md5))
                    potentials.pop(index)
        i += 1
    print(sorted(keys, key=lambda x: x[0])[63][0])


if __name__ == '__main__':
    salt_list = read()
    part1(salt_list)
    part2(salt_list)
