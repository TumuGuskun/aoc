from itertools import permutations

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda l: l.rstrip(), input_file.readlines()))


def swap_position(p, i, j):
    i = int(i)
    j = int(j)
    p[i], p[j] = p[j], p[i]
    return p


def swap_letter(p, a, b):
    i = p.index(a)
    j = p.index(b)
    return swap_position(p, i, j)


def rotate(p, direction, n):
    n = int(n)
    if direction == 'right':
        return p[len(p) - n:] + p[:len(p) - n]
    else:
        return p[n:] + p[:n]


def rotate_position(p, a):
    i = p.index(a)
    n = i + 1 if i < 4 else i + 2
    return rotate(p, 'right', n)


def reverse(p, i, j):
    i = int(i)
    j = int(j)
    p[i:j + 1] = reversed(p[i:j + 1])
    return p


def move(p, i, j):
    i = int(i)
    j = int(j)
    a = p.pop(i)
    p.insert(j, a)
    return p


def scramble(moves, password):
    for line in moves:
        command, rest = line.split(maxsplit=1)
        if command == 'swap':
            t, a, _, _, b = rest.split()
            if t == 'position':
                password = swap_position(password, a, b)
            else:
                password = swap_letter(password, a, b)
        elif command == 'rotate':
            t, rest = rest.split(maxsplit=1)
            if t == 'based':
                password = rotate_position(password, rest[-1])
            else:
                password = rotate(password, t, rest[0])
        elif command == 'reverse':
            _, i, _, j = rest.split()
            password = reverse(password, i, j)
        elif command == 'move':
            _, i, _, _, j = rest.split()
            password = move(password, i, j)
        else:
            raise Exception('command not recognized')
    return password


@timed
def part1(moves):
    print(''.join(scramble(moves, list('abcdefgh'))))


@timed
def part2(moves):
    password = list('fbgdceah')
    for permutation in permutations(list('abcdefgh')):
        if scramble(moves, list(permutation)) == password:
            print(''.join(permutation))
            return


if __name__ == '__main__':
    move_list = read()
    part1(move_list)
    part2(move_list)
