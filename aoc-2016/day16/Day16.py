from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(lambda x: x.rstrip(), input_file.readlines()))


@timed
def part1(sequences):
    sequence, length = sequences
    length = int(length)

    while len(sequence) < length:
        sequence = sequence + '0' + ''.join(reversed(sequence)).replace('0', '2').replace('1', '0').replace('2', '1')

    sequence = list(map(int, sequence[:length]))
    while len(sequence) % 2 == 0:
        new_sequence = []
        for i, e in enumerate(sequence[:-1]):
            if i % 2 == 0:
                if e == sequence[i + 1]:
                    new_sequence.append(1)
                else:
                    new_sequence.append(0)
        sequence = new_sequence

    print(''.join(map(str, sequence)))


@timed
def part2(sequences):
    sequence, length = sequences
    length = 35651584

    while len(sequence) < length:
        sequence = sequence + '0' + ''.join(reversed(sequence)).replace('0', '2').replace('1', '0').replace('2', '1')

    sequence = list(map(int, sequence[:length]))
    while len(sequence) % 2 == 0:
        new_sequence = []
        for i, e in enumerate(sequence[:-1]):
            if i % 2 == 0:
                if e == sequence[i + 1]:
                    new_sequence.append(1)
                else:
                    new_sequence.append(0)
        sequence = new_sequence

    print(''.join(map(str, sequence)))


if __name__ == '__main__':
    sequence_list = read()
    part1(sequence_list)
    part2(sequence_list)
