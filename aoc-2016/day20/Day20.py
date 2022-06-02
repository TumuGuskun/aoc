from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        ip_ranges = []
        for line in input_file.readlines():
            ip_ranges.append(tuple(map(int, line.split('-'))))
    return ip_ranges


@timed
def part1(ips):
    candidate = 0
    for lower, upper in sorted(ips, key=lambda x: x[0]):
        if candidate <= upper:
            if candidate < lower:
                print(candidate)
                break
            candidate = upper + 1


@timed
def part2(ips):
    count = 0
    candidate = 0
    for lower, upper in sorted(ips, key=lambda x: x[0]):
        if candidate <= upper:
            if candidate < lower:
                count += lower - candidate
            candidate = upper + 1
    print(count)


if __name__ == '__main__':
    ip_list = read()
    part1(ip_list)
    part2(ip_list)
