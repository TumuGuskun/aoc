from collections import defaultdict

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return [(int(x[0]), int(x[1])) for x in map(lambda y: y.split(', '), input_file.readlines())]


@timed
def part1(coordinates):
    sorted_x = sorted(coordinates, key=lambda x: x[0])
    sorted_y = sorted(coordinates, key=lambda x: x[1])

    min_x, max_x = sorted_x[0][0], sorted_x[-1][0]
    min_y, max_y = sorted_y[0][1], sorted_y[-1][1]

    point_counts = defaultdict(float)
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            closest_point = find_closest((i, j), coordinates)
            if i == min_x or i == max_x or j == min_y or j == max_y:
                point_counts[closest_point] += float('inf')
            else:
                point_counts[closest_point] += 1

    print(int(max([value for key, value in point_counts.items() if value != float('inf')])))


def find_closest(point, coordinates):
    minimum = float('inf')
    min_coord = None
    for coord in coordinates:
        if (new_min := abs(point[0] - coord[0]) + abs(point[1] - coord[1])) < minimum:
            minimum = new_min
            min_coord = coord
        elif new_min == minimum:
            min_coord = ('nope')
    return min_coord


@timed
def part2(coordinates):
    sorted_x = sorted(coordinates, key=lambda x: x[0])
    sorted_y = sorted(coordinates, key=lambda x: x[1])

    min_x, max_x = sorted_x[0][0], sorted_x[-1][0]
    min_y, max_y = sorted_y[0][1], sorted_y[-1][1]

    print(sum(1 for i in range(min_x, max_x + 1) for j in range(min_y, max_y + 1) if sum(abs(i - coord[0]) + abs(j - coord[1]) for coord in coordinates) < 10000))


if __name__ == '__main__':
    coordinate_list = read()
    part1(coordinate_list)
    part2(coordinate_list)
