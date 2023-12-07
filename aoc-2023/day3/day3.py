import numbers
import re
from dataclasses import dataclass
from pprint import pprint

from shared.gum import gum_choose
from shared.point import Point
from shared.util import coordinate, get_input_files, timed


@dataclass
class Number:
    value: int
    coordinates: list[Point]


@dataclass(frozen=True)
class Symbol:
    value: str
    coordinate: Point


@timed
def read() -> tuple[list[Number], set[Symbol]]:
    files = get_input_files(__file__)
    if len(files) == 1:
        file_name = files[0]
    else:
        _, file_name = gum_choose(files, "Choose input file")

    print(f"Reading from {file_name.split('/')[-1]}")
    with open(file_name) as input_file:
        numbers = []
        symbol_points = set()
        in_number = False
        curr_value = ""
        curr_coordinates = []
        for (i, j), value in coordinate(input_file.readlines()):
            if value.isalnum():
                if in_number:
                    curr_value += value
                    curr_coordinates.append(Point(i, j))
                else:
                    in_number = True
                    curr_value = value
                    curr_coordinates = [Point(i, j)]
            else:
                if in_number:
                    numbers.append(Number(int(curr_value), curr_coordinates))
                    in_number = False

            if re.match(r"[^\s\w\.]", value):
                symbol_points.add(Symbol(value, Point(i, j)))

    return numbers, symbol_points


@timed
def part1(inputs: tuple[list[Number], set[Symbol]]) -> None:
    numbers, symbols = inputs
    valid_numbers = []
    for number in numbers:
        for symbol in symbols:
            if any(
                symbol.coordinate.is_neighbor(coord) for coord in number.coordinates
            ):
                valid_numbers.append(number)
                break
    print(sum(number.value for number in valid_numbers))


@timed
def part2(inputs: tuple[list[Number], set[Symbol]]) -> None:
    numbers, symbols = inputs
    gears = []
    for symbol in symbols:
        if symbol.value == "*":
            neighbors = []
            for number in numbers:
                if any(
                    symbol.coordinate.is_neighbor(coord) for coord in number.coordinates
                ):
                    neighbors.append(number)

            if len(neighbors) == 2:
                gears.append(neighbors)

    print(sum(gear[0].value * gear[1].value for gear in gears))


if __name__ == "__main__":
    number_list = read()
    part1(number_list)
    part2(number_list)
