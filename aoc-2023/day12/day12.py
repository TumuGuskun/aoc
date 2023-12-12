from copy import copy
from dataclasses import dataclass
import re
from typing import Any

from aocd.examples import Example

from shared.util import get_ints, get_puzzle, run, timed


@dataclass
class Record:
    potential_locations: str
    springs: list[int]

    def is_valid(self, locations: str) -> bool:
        broken_springs = re.findall(r"(#+)", locations)

        if len(broken_springs) != len(self.springs):
            return False

        for i, chunk_length in enumerate(self.springs):
            if chunk_length != len(broken_springs[i]):
                return False

        return True


def parse_data(input_data: str) -> Any:
    output = []
    for line in input_data.splitlines():
        locations, springs = line.split(" ")
        output.append(Record(potential_locations=locations, springs=get_ints(springs)))

    return output


def get_potential_orders(record: Record) -> list[str]:
    current_location = record.potential_locations[0]
    if len(record.potential_locations) == 1:
        return (
            [current_location] if record.potential_locations[0] != "?" else ["#", "."]
        )

    record.potential_locations = record.potential_locations[1:]
    new_orders = []
    for potential_order in get_potential_orders(record):
        if current_location == "?":
            new_orders.extend([f".{potential_order}", f"#{potential_order}"])
        else:
            new_orders.append(f"{current_location}{potential_order}")

    return new_orders


@timed
def part_1(input_data: str) -> Any:
    records: list[Record] = parse_data(input_data=input_data)

    # Body Logic
    total = 0
    for record in records:
        for potential_order in get_potential_orders(copy(record)):
            if record.is_valid(potential_order):
                total += 1

    return total


@timed
def part_2(input_data: str) -> Any:
    parsed_data = parse_data(input_data=input_data)

    # Body Logic
    return None


def main() -> None:
    puzzle = get_puzzle(__file__)
    puzzle._get_examples = lambda parser_name=None: [
        Example(
            input_data="""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""",
            answer_a="21",
            answer_b="",
        )
    ]
    run(puzzle=puzzle, part_1=part_1, part_2=part_2)


if __name__ == "__main__":
    main()
