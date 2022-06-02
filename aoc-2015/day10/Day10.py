from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.read()))


def run_sequence(sequences, iterations):
    for _ in range(iterations):
        current = sequences[0]
        count = 1
        next_sequence = []
        for number in sequences[1:]:
            if number == current:
                count += 1
            else:
                next_sequence.append(count)
                next_sequence.append(current)
                current = number
                count = 1
        next_sequence.append(count)
        next_sequence.append(current)
        sequences = next_sequence
    print(len(sequences))


@timed
def part1(sequences):
    run_sequence(sequences, 40)


@timed
def part2(sequences):
    run_sequence(sequences, 50)


if __name__ == '__main__':
    sequence_list = read()
    part1(sequence_list)
    part2(sequence_list)
