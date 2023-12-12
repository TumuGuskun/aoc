import re
from dataclasses import dataclass

from typing import Any

from shared.util import get_puzzle, run, timed


@dataclass
class Card:
    card_id: int
    winning_numbers: list[int]
    played_numbers: list[int]


def parse_data(input_data: str) -> Any:
    cards = []
    for line in input_data.splitlines():
        card, numbers = line.split(":")
        card_id = re.search(r"(\d+)", card).group(1)
        winning_numbers, played_numbers = numbers.split("|")
        cards.append(
            Card(
                int(card_id),
                list(map(int, winning_numbers.split())),
                list(map(int, played_numbers.split())),
            )
        )

    return cards


@timed
def part_1(input_data: str) -> Any:
    cards = parse_data(input_data=input_data)

    # Body Logic
    total_score = 0
    for card in cards:
        matches = sum(
            1 for number in card.played_numbers if number in card.winning_numbers
        )
        total_score += 0 if matches == 0 else 2 ** (matches - 1)

    return total_score


@timed
def part_2(input_data: str) -> Any:
    cards = parse_data(input_data=input_data)

    # Body Logic
    card_dict = {card.card_id: 1 for card in cards}

    for card in cards:
        matches = sum(
            1 for number in card.played_numbers if number in card.winning_numbers
        )
        if matches == 0:
            continue

        for i in range(matches):
            if (next_id := card.card_id + i + 1) in card_dict:
                card_dict[next_id] += card_dict[card.card_id]

    return sum(card_dict.values())


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(puzzle=puzzle, part_1=part_1, part_2=part_2)


if __name__ == "__main__":
    main()
