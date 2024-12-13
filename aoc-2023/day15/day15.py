from dataclasses import dataclass, field
from email.policy import default
from imp import load_compiled
from posixpath import ismount
from pprint import pprint
from typing import Any

from shared.util import get_puzzle, run, timed


def parse_data(input_data: str) -> Any:
    return input_data.split(",")


def hash(string: str) -> int:
    current_value = 0

    for char in string:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256

    return current_value


@timed
def part_1(sequence: list[str]) -> int:
    return sum(hash(step) for step in sequence)


@dataclass
class Lens:
    label: str
    focal_length: int


@dataclass
class Block:
    number: int
    lenses: list[Lens] = field(default_factory=list)

    @property
    def focusing_power(self) -> int:
        return sum(
            lens.focal_length * (self.number + 1) * i
            for i, lens in enumerate(self.lenses, start=1)
        )

    def add_lens(self, new_lens: Lens) -> None:
        for i, old_lens in enumerate(self.lenses):
            if old_lens.label == new_lens.label:
                self.lenses[i] = new_lens
                return

        self.lenses.append(new_lens)

    def remove_lens(self, label: str) -> None:
        for i, lens in enumerate(self.lenses):
            if lens.label == label:
                self.lenses.pop(i)
                return


@timed
def part_2(sequence: list[str]) -> int:
    blocks = [Block(i) for i in range(256)]

    for step in sequence:
        if "=" in step:
            label, lens_number = step.split("=")
            box_number = hash(label)
            blocks[box_number].add_lens(
                new_lens=Lens(label=label, focal_length=int(lens_number))
            )
        else:
            label = step.replace("-", "")
            box_number = hash(label)
            blocks[box_number].remove_lens(label=label)

    return sum(block.focusing_power for block in blocks)


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
