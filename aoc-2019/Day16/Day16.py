def get_input(filename):
    with open(filename, 'r') as input_file:
        return list(map(int, str(input_file.read())))


def part1(filename):
    signal = get_input(filename)

    signal *= 10000

    sig_len = len(signal)

    for phase in range(100):
        new_signal = []
        for i in range(sig_len):
            j = i + 1
            pattern = [0] * j + [1] * j + [0] * j + [-1] * j
            pattern *= sig_len // len(pattern) + 1
            digit = abs(sum([x * y for (x, y) in zip(pattern[1:], signal)])) % 10
            new_signal.append(digit)
        signal = new_signal

    offset = int(''.join(map(str, signal[:7])))

    print(''.join(map(str, signal[offset + 1:offset + 9])))


if __name__ == '__main__':
    part1('input.txt')
