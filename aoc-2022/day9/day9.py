import os

from shared.gum import gum_choose
from shared.util import timed, clamp
from shared.point import Point


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return [
            (direction, int(distance))
            for direction, distance in map(
                lambda line: line.split(), input_file.readlines()
            )
        ]


DIR_MAP: dict[str, Point] = {
    "U": Point(0, 1),
    "D": Point(0, -1),
    "R": Point(1, 0),
    "L": Point(-1, 0),
}


def point_catch_up(point1: Point, point2: Point) -> Point:
    if abs(point1.i - point2.i) <= 1 and abs(point1.j - point2.j) <= 1:
        return Point(0, 0)
    return Point(clamp(point1.i - point2.i, -1, 1), clamp(point1.j - point2.j, -1, 1))


@timed
def part1(moves):
    tail_seen = set()
    curr_head = Point(0, 0)
    curr_tail = Point(0, 0)

    for direction, distance in moves:
        for _ in range(distance):
            curr_head += DIR_MAP[direction]
            curr_tail += point_catch_up(point1=curr_head, point2=curr_tail)
            tail_seen.add(curr_tail)
    print(len(tail_seen))


@timed
def part2(moves):
    tail_seen = set()
    snek = [Point(0, 0) for _ in range(10)]

    for direction, distance in moves:
        for _ in range(distance):
            snek[0] += DIR_MAP[direction]
            for i, segment in enumerate(snek[1:], start=1):
                snek[i] += point_catch_up(point1=snek[i - 1], point2=segment)
            tail_seen.add(snek[-1])
    print(len(tail_seen))


if __name__ == "__main__":
    move_list = read()
    part1(move_list)
    part2(move_list)
