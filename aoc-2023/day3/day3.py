import re
from dataclasses import dataclass
from typing import Any

from shared.point import Point
from shared.util import coordinate, get_puzzle, run, timed


@dataclass
class Number:
    value: int
    coordinates: list[Point]


@dataclass(frozen=True)
class Symbol:
    value: str
    coordinate: Point


def parse_data(input_data: str) -> tuple[list[Number], set[Symbol]]:
    numbers = []
    symbol_points = set()
    in_number = False
    curr_value = ""
    curr_coordinates = []
    for point, value in coordinate(input_data.splitlines()):
        if value.isalnum():
            if in_number:
                curr_value += value
                curr_coordinates.append(point)
            else:
                in_number = True
                curr_value = value
                curr_coordinates = [point]
        else:
            if in_number:
                numbers.append(Number(int(curr_value), curr_coordinates))
                in_number = False

        if re.match(r"[^\s\w\.]", value):
            symbol_points.add(Symbol(value, point))

    return numbers, symbol_points


@timed
def part_1(input_data: tuple[list[Number], set[Symbol]]) -> int:
    numbers, symbols = input_data
    valid_numbers = []
    for number in numbers:
        for symbol in symbols:
            if any(
                symbol.coordinate.is_neighbor(coord) for coord in number.coordinates
            ):
                valid_numbers.append(number)
                break
    return sum(number.value for number in valid_numbers)


@timed
def part_2(input_data: tuple[list[Number], set[Symbol]]) -> int:
    numbers, symbols = input_data
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

    return sum(gear[0].value * gear[1].value for gear in gears)


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(
        puzzle=puzzle,
        part_1=part_1,
        part_2=part_2,
        parser=parse_data,
    )


if __name__ == "__main__":
    main()
