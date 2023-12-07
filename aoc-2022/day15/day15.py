from dataclasses import dataclass
from functools import reduce
import os
from typing import Generator

from shared.gum import gum_choose
from shared.util import timed, get_ints
from shared.point import Point


BEACON_ROW = 2_000_000
# BEACON_ROW = 10


@dataclass
class Sensor:
    position: Point
    closest_beacon: Point
    range: int

    @property
    def edges_plus(self):
        for i in range(self.range + 2):
            yield Point(self.position.i + self.range + 1 - i, self.position.j + i)
            yield Point(self.position.i - self.range - 1 + i, self.position.j + i)

            yield Point(self.position.i + self.range + 1 - i, self.position.j - i)
            yield Point(self.position.i - self.range - 1 + i, self.position.j - i)


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        sensors = []
        for line in input_file.readlines():
            sx, sy, bx, by = get_ints(line)
            position = Point(sx, sy)
            beacon = Point(bx, by)
            sensors.append(
                Sensor(
                    position=position,
                    closest_beacon=beacon,
                    range=manhattan_distance(position, beacon),
                )
            )
    return sensors


def manhattan_distance(point1: Point, point2: Point) -> int:
    return abs(point1.i - point2.i) + abs(point1.j - point2.j)


def overspill(sensor: Sensor, the_line: int) -> int:
    return sensor.range - abs(sensor.position.j - the_line)


def overlaps(ranges) -> Generator:
    ranges = sorted(ranges)
    it = iter(ranges)
    try:
        curr_start, curr_stop = next(it)
    except StopIteration:
        return
    for start, stop in it:
        if curr_start <= start <= curr_stop:
            curr_stop = max(curr_stop, stop)
        else:
            yield curr_start, curr_stop
            curr_start, curr_stop = start, stop
    yield curr_start, curr_stop


@timed
def part1(sensors: list[Sensor]):
    ranges = []
    for sensor in sensors:
        if (overage := overspill(sensor=sensor, the_line=BEACON_ROW)) >= 0:
            ranges.append((sensor.position.i - overage, sensor.position.i + overage))

    range_on_line = next(overlaps(ranges))
    print(range_on_line[1] - range_on_line[0])


@timed
def part2(sensors: list[Sensor]):
    for y in range(4_000_000):
        ranges = []
        for sensor in sensors:
            if (overage := overspill(sensor=sensor, the_line=y)) >= 0:
                ranges.append(
                    (sensor.position.i - overage, sensor.position.i + overage)
                )

        joined_ranges = list(overlaps(ranges))
        if len(joined_ranges) > 1:
            print(y + 4_000_000 * (joined_ranges[0][1] + 1))
            break


if __name__ == "__main__":
    sensor_list = read()
    part1(sensor_list)
    part2(sensor_list)
