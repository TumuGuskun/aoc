from __future__ import annotations
from itertools import zip_longest
import os

from shared.gum import gum_choose
from shared.util import timed


class Snafu:
    MAP = {"=": -2, "-": -1, -1: "-", -2: "="}

    def __init__(self, number: str) -> None:
        self.number = []
        for digit in reversed(number):
            if digit.isnumeric():
                self.number.append(int(digit))
            else:
                self.number.append(self.MAP[digit])

    def __add__(self, other: Snafu) -> Snafu:
        new_number = []
        carry = 0
        for self_value, other_value in zip_longest(
            self.number, other.number, fillvalue=0
        ):
            new_value = self_value + other_value + carry
            if new_value >= 3:
                carry = 1
                new_value -= 5
            elif new_value <= -3:
                carry = -1
                new_value += 5
            else:
                carry = 0

            new_number.append(new_value)

        new_number.append(carry)

        new_snafu = Snafu("")
        new_snafu.number = new_number
        return new_snafu

    def to_decimal(self) -> int:
        return sum(5**i * value for i, value in enumerate(self.number))

    def __repr__(self) -> str:
        return "".join(
            list(
                map(
                    lambda d: self.MAP[d] if d in self.MAP else str(d),
                    reversed(self.number),
                )
            )
        ).lstrip("0")


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return [Snafu(line.strip()) for line in input_file.readlines()]


@timed
def part1(numbers: list[Snafu]):
    print(sum(numbers, start=Snafu("0")))


@timed
def part2(numbers):
    pass


if __name__ == "__main__":
    number_list = read()
    part1(number_list)
    part2(number_list)
