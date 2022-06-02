from hashlib import md5

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.read()


@timed
def part1(ids):
    index = 0
    password = ''
    while len(password) < 8:
        md5_hash = md5(f'{ids}{index}'.encode()).hexdigest()
        if md5_hash.startswith('00000'):
            password += md5_hash[5]
        index += 1
    print(password)


@timed
def part2(ids):
    i = 0
    password = ['*'] * 8
    while any(spot == '*' for spot in password):
        md5_hash = md5(f'{ids}{i}'.encode()).hexdigest()
        if md5_hash.startswith('00000'):
            index = md5_hash[5]
            char = md5_hash[6]
            if index.isdigit() and int(index) < len(password) and password[int(index)] == '*':
                password[int(index)] = char
        i += 1
    print(''.join(password))


if __name__ == '__main__':
    id_list = read()
    part1(id_list)
    part2(id_list)
