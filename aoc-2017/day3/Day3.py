from collections import defaultdict

from shared.Util import timed, Point


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(int, input_file.readlines()))


def board_inc():
    grid = defaultdict(int)
    grid[Point(0, 0)] = 1
    grid[Point(1, 0)] = 1
    direction = 'r'
    current = Point(1, 0)
    count = 3
    while True:
        if direction == 'r':
            if grid[Point(current.x, current.y + 1)] == 0:
                current = Point(current.x, current.y + 1)
                grid[current] = count
                direction = 'u'
            else:
                current = Point(current.x + 1, current.y)
                grid[current] = count
        elif direction == 'u':
            if grid[Point(current.x - 1, current.y)] == 0:
                current = Point(current.x - 1, current.y)
                grid[current] = count
                direction = 'l'
            else:
                current = Point(current.x, current.y + 1)
                grid[current] = count
        elif direction == 'l':
            if grid[Point(current.x, current.y - 1)] == 0:
                current = Point(current.x, current.y - 1)
                grid[current] = count
                direction = 'd'
            else:
                current = Point(current.x - 1, current.y)
                grid[current] = count
        else:
            if grid[Point(current.x + 1, current.y)] == 0:
                current = Point(current.x + 1, current.y)
                grid[current] = count
                direction = 'r'
            else:
                current = Point(current.x, current.y - 1)
                grid[current] = count
        yield current, count
        count += 1


@timed
def part1(squares):
    squares = list(reversed(squares))
    current = squares.pop()
    for position, value in board_inc():
        if value == current:
            print(abs(position.x) + abs(position.y))
            if squares:
                current = squares.pop()
                continue
            else:
                break


def get_neighbor_sum(grid, point):
    return sum(grid[Point(x, y)] for x, y in [(point.x - 1, point.y - 1),
                                              (point.x + 1, point.y - 1),
                                              (point.x, point.y - 1),
                                              (point.x - 1, point.y),
                                              (point.x + 1, point.y),
                                              (point.x - 1, point.y + 1),
                                              (point.x + 1, point.y + 1),
                                              (point.x, point.y + 1)])


def board_sum():
    grid = defaultdict(int)
    grid[Point(0, 0)] = 1
    grid[Point(1, 0)] = 1
    direction = 'r'
    current = Point(1, 0)
    while True:
        if direction == 'r':
            if grid[Point(current.x, current.y + 1)] == 0:
                current = Point(current.x, current.y + 1)
                grid[current] = get_neighbor_sum(grid, current)
                direction = 'u'
            else:
                current = Point(current.x + 1, current.y)
                grid[current] = get_neighbor_sum(grid, current)
        elif direction == 'u':
            if grid[Point(current.x - 1, current.y)] == 0:
                current = Point(current.x - 1, current.y)
                grid[current] = get_neighbor_sum(grid, current)
                direction = 'l'
            else:
                current = Point(current.x, current.y + 1)
                grid[current] = get_neighbor_sum(grid, current)
        elif direction == 'l':
            if grid[Point(current.x, current.y - 1)] == 0:
                current = Point(current.x, current.y - 1)
                grid[current] = get_neighbor_sum(grid, current)
                direction = 'd'
            else:
                current = Point(current.x - 1, current.y)
                grid[current] = get_neighbor_sum(grid, current)
        else:
            if grid[Point(current.x + 1, current.y)] == 0:
                current = Point(current.x + 1, current.y)
                grid[current] = get_neighbor_sum(grid, current)
                direction = 'r'
            else:
                current = Point(current.x, current.y - 1)
                grid[current] = get_neighbor_sum(grid, current)
        yield current, grid[current]


@timed
def part2(squares):
    end = squares.pop()
    for _, value in board_sum():
        if value > end:
            print(value)
            break


if __name__ == '__main__':
    square_list = read()
    part1(square_list)
    part2(square_list)
