from collections import deque

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        moves = []
        for whole in input_file.read().split(','):
            if whole.startswith('s'):
                moves.append(('s', [int(whole[1:])]))
            elif whole.startswith('x'):
                moves.append(('x', list(map(int, whole[1:].split('/')))))
            elif whole.startswith('p'):
                moves.append(('p',  list(map(ord, whole[1:].split('/')))))
        return moves


@timed
def part1(moves):
    programs = deque(range(ord('a'), ord('p') + 1))
    for move, args in moves:
        programs = do_move(move, args, programs)
    print(''.join(map(chr, programs)))


def do_move(move, args, programs):
    if move == 's':
        a, = args
        programs.rotate(a)
    elif move == 'x':
        a, b = args
        programs[a], programs[b] = programs[b], programs[a]
    else:
        a, b = args
        ai = programs.index(a)
        bi = programs.index(b)
        programs[ai], programs[bi] = programs[bi], programs[ai]
    return programs


@timed
def part2(moves):
    programs = deque(range(ord('a'), ord('p') + 1))
    for _ in range(40):
        for move, args in moves:
            programs = do_move(move, args, programs)
    print(''.join(map(chr, programs)))


if __name__ == '__main__':
    move_list = read()
    part1(move_list)
    part2(move_list)
