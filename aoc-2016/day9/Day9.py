from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.read().rstrip()


def parse_marker(i, sequences):
    marker = ''
    for j, char in enumerate(sequences[i + 1:]):
        if char == ')':
            return map(int, marker.split('x')), j
        else:
            marker += char


@timed
def part1(sequences):
    i = 0
    decompressed = ''
    while i < len(sequences):
        if sequences[i] == '(':
            (length, reps), j = parse_marker(i, sequences)
            decompressed += sequences[i + j + 2:i + j + length + 2] * reps
            i = i + j + length + 2
        else:
            decompressed += sequences[i]
            i += 1
    print(len(decompressed))


def count_chars(sequence):
    if not sequence:
        return 0
    elif sequence.startswith('('):
        (length, reps), j = parse_marker(0, sequence)
        return count_chars(sequence[j + 2:j + length + 2]) * reps + count_chars(sequence[j + length + 2:])
    else:
        total = sequence.split('(', maxsplit=1)
        if len(total) > 1:
            chars, rest = total
            return len(chars) + count_chars('(' + rest)
        else:
            return len(total[0])


@timed
def part2(sequences):
    print(count_chars(sequences))


if __name__ == '__main__':
    sequence_list = read()
    part1(sequence_list)
    part2(sequence_list)
