from shared.Util import timed, LinkedList


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.read().split(',')))


@timed
def part1(numbers):
    num_list = list(range(256))
    start = 0
    skip = 0

    for number in numbers:
        if start + number > 256:
            new_end = (start + number) % 256
            new_list = list(reversed(num_list[start:] + num_list[:new_end]))
            num_list[start:] = new_list[:256 - start]
            num_list[:new_end] = new_list[256 - start:]
        else:
            num_list[start:start + number] = reversed(num_list[start:start + number])
        start = (start + number + skip) % 256
        skip += 1

    print(num_list[0] * num_list[1])


@timed
def part2(numbers):
    numbers = list(map(ord, '31,2,85,1,80,109,35,63,98,255,0,13,105,254,128,33'))
    numbers += [17, 31, 73, 47, 23]

    num_list = list(range(256))
    start = 0
    skip = 0

    for _ in range(64):
        for number in numbers:
            if start + number > 256:
                new_end = (start + number) % 256
                new_list = list(reversed(num_list[start:] + num_list[:new_end]))
                num_list[start:] = new_list[:256 - start]
                num_list[:new_end] = new_list[256 - start:]
            else:
                num_list[start:start + number] = reversed(num_list[start:start + number])
            start = (start + number + skip) % 256
            skip += 1

    new_nums = []
    count = 0
    running = 0
    for number in num_list:
        if count < 16:
            running ^= number
            count += 1
        else:
            new_nums.append(running)
            running = number
            count = 1

    new_nums.append(running)
    print(''.join(list(map(lambda x: f'{x:#04x}'[2:], new_nums))))


if __name__ == '__main__':
    number_list = read()
    part1(number_list)
    part2(number_list)
