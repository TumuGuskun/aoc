import numpy as np

from shared.Util import timed, Point


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        grid_id = int(input_file.read())
        array = np.zeros(shape=(300,300))
        for i in range(1, 301):
            for j in range(1, 301):
                rack_id = i + 10
                array[i - 1, j - 1] = (((((j * rack_id) + grid_id) * rack_id) // 100) % 10) - 5
        return array


@timed
def part1(array):
    print(max([max([(np.sum(array[i:i+3, j:j+3]), Point(i + 1, j + 1)) for j in range(297)]) for i in range(297)]))


@timed
def part2(array):
    print(max([max([max([(np.sum(array[i:i+size, j:j+size]), Point(i + 1, j + 1), size) for j in range(300 - size)]) for i in range(300 - size)]) for size in range(1, 4)]))
    # max_power = 0
    # max_size = 0
    # max_power_point = Point(0, 0)
    # for size in range(1, 301):
    #     for i in range(300 - size):
    #         for j in range(300 - size):
    #             if (power := np.sum(array[i:i+size, j:j+size])) > max_power:
    #                 max_power = power
    #                 max_size = size
    #                 max_power_point = Point(i + 1, j + 1)

    # print(max_power, max_power_point, max_size)


if __name__ == '__main__':
    id_list = read()
    part1(id_list)
    part2(id_list)
