from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(ord, input_file.read()))


def increment(password):
    if not password:
        return []
    elif password[-1] == 122:
        return increment(password[:-1]) + [97]
    else:
        password[-1] += 1
        return password


def test_straight(password):
    for i in range(6):
        if password[i + 2] - password[i + 1] == 1 and password[i + 1] - password[i] == 1:
            return True
    return False


def test_pairs(password):
    seen = set()
    for i in range(7):
        if password[i + 1] == password[i] and password[i] not in seen:
            seen.add(password[i])
    return len(seen) >= 2


@timed
def part1(password):
    while not test_straight(password) or not test_pairs(password):
        password = increment(password)
    print(''.join(list(map(chr, password))))
    return password


@timed
def part2(password):
    password = increment(password)
    part1(password)


if __name__ == '__main__':
    password_list = read()
    new_password = part1(password_list)
    part2(new_password)
