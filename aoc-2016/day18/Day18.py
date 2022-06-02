from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: x.rstrip(), input_file.readlines()))


@timed
def part1(tiles):
    line, height = tiles
    width = len(line)
    line = '.' + line + '.'
    lines = [line]
    for i in range(int(height) - 1):
        new_line = ''
        old_line = lines[i]
        for j in range(width):
            l, c, r = old_line[j:j + 3]
            if (l == c == '^' and r == '.') or \
               (r == c == '^' and l == '.') or \
               (l == c == '.' and r == '^') or \
               (r == c == '.' and l == '^'):
                new_line += '^'
            else:
                new_line += '.'
        new_line = '.' + new_line + '.'
        lines.append(new_line)

    print(sum(map(lambda x: sum(1 for e in x if e == '.'), lines)) - 2 * int(height))


@timed
def part2(tiles):
    pass


if __name__ == '__main__':
    tile_list = read()
    part1(tile_list)
    part2(tile_list)
