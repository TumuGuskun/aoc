import re
from dataclasses import dataclass
from pprint import pprint

from shared.gum import gum_choose
from shared.util import get_input_files, timed


@dataclass
class Card:
    card_id: int
    winning_numbers: list[int]
    played_numbers: list[int]


@timed
def read():
    files = get_input_files(__file__)
    if len(files) == 1:
        file_name = files[0]
    else:
        _, file_name = gum_choose(files, "Choose input file")

    print(f"Reading from {file_name.split('/')[-1]}")
    with open(file_name) as input_file:
        cards = []
        for line in input_file.readlines():
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
def part1(cards: list[Card]):
    total_score = 0
    for card in cards:
        matches = sum(
            1 for number in card.played_numbers if number in card.winning_numbers
        )
        total_score += 0 if matches == 0 else 2 ** (matches - 1)
    print(total_score)


@timed
def part2(cards: list[Card]):
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

    print(sum(card_dict.values()))


if __name__ == "__main__":
    card_list = read()
    part1(card_list)
    part2(card_list)
