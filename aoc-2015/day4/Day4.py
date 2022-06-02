from shared.Util import timed
from hashlib import md5


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.read().rstrip()


@timed
def part1(hash_prefix):
    start = '00000'
    i = 1
    while True:
        hashed = md5(f'{hash_prefix}{i}'.encode())
        if hashed.hexdigest().startswith(start):
            print(i)
            break
        i += 1


@timed
def part2(hash_prefix):
    start = '000000'
    i = 1
    while True:
        hashed = md5(f'{hash_prefix}{i}'.encode())
        if hashed.hexdigest().startswith(start):
            print(i)
            break
        i += 1


if __name__ == '__main__':
    hash_list = read()
    part1(hash_list)
    part2(hash_list)
