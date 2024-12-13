from collections import defaultdict
from itertools import permutations
from typing import Any

from shared.util import *


def parse_data(input_data: str) -> Any:
    rules = defaultdict(list)
    updates = []
    for line in input_data.splitlines():
        if "|" in line:
            left, right = get_ints(line)
            rules[right].append(left)
        elif "," in line:
            updates.append(get_ints(line))

    return rules, updates


def update_follows_rules(rules: dict[int, list[int]], update: list[int]) -> bool:
    for i, page in enumerate(update):
        if page not in rules:
            continue

        for before_page in rules[page]:
            if before_page not in update:
                continue

            if update.index(before_page) > i:
                return False

    return True


def part_1(input_data) -> int:
    rules, updates = input_data

    total = 0
    for update in updates:
        if update_follows_rules(rules, update):
            total += update[len(update) // 2]

    return total


def part_2(input_data) -> int:
    rules, updates = input_data

    total = 0
    for update in updates:
        if update_follows_rules(rules, update):
            continue

        while not update_follows_rules(rules, update):
            for i, page in enumerate(update):
                if page in rules:
                    for before_page in rules[page]:
                        if (
                            before_page in update
                            and (before_page_index := update.index(before_page)) > i
                        ):
                            update[before_page_index], update[i] = (
                                update[i],
                                update[before_page_index],
                            )
                            break

        total += update[len(update) // 2]

    return total


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
