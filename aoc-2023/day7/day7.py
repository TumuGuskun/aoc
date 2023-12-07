from dataclasses import dataclass
from enum import Enum
from typing import Any

from aocd.models import Puzzle

from shared.util import export_data, run, timed


class Rank(Enum):
    FIVE_OF_A_KIND = 0
    FOUR_OF_A_KIND = 1
    FULL_HOUSE = 2
    THREE_OF_A_KIND = 3
    TWO_PAIR = 4
    ONE_PAIR = 5
    HIGH_CARD = 6


REGULAR_RANKINGS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

WILD_CARD_RANKINGS = REGULAR_RANKINGS.copy()
WILD_CARD_RANKINGS["J"] = 1


@dataclass
class Hand:
    cards: str
    bid: int
    jokers: bool = False

    @property
    def type(self) -> Rank:
        card_set = set(self.cards)
        if len(card_set) == 1:
            return Rank.FIVE_OF_A_KIND

        if len(card_set) == 2:
            if any(self.cards.count(card) == 4 for card in card_set):
                if self.jokers and "J" in card_set:
                    return Rank.FIVE_OF_A_KIND
                else:
                    return Rank.FOUR_OF_A_KIND

            if self.jokers and "J" in card_set:
                return Rank.FIVE_OF_A_KIND
            else:
                return Rank.FULL_HOUSE

        if len(card_set) == 3:
            if any(self.cards.count(card) == 3 for card in card_set):
                if self.jokers and "J" in card_set:
                    return Rank.FOUR_OF_A_KIND
                else:
                    return Rank.THREE_OF_A_KIND

            if self.jokers and "J" in card_set:
                if self.cards.count("J") == 2:
                    return Rank.FOUR_OF_A_KIND
                else:
                    return Rank.FULL_HOUSE
            else:
                return Rank.TWO_PAIR

        if len(card_set) == 4:
            if self.jokers and "J" in card_set:
                return Rank.THREE_OF_A_KIND
            return Rank.ONE_PAIR

        if self.jokers and "J" in card_set:
            return Rank.ONE_PAIR

        return Rank.HIGH_CARD

    def __gt__(self, other: Any) -> bool:
        if self.type.value < other.type.value:
            return True
        elif self.type.value > other.type.value:
            return False
        else:
            card_ranking = WILD_CARD_RANKINGS if self.jokers else REGULAR_RANKINGS
            for i, card in enumerate(self.cards):
                if card_ranking[card] > card_ranking[other.cards[i]]:
                    return True
                elif card_ranking[card] < card_ranking[other.cards[i]]:
                    return False
        return False

    def __lt__(self, other: Any) -> bool:
        if self.type.value > other.type.value:
            return True
        elif self.type.value < other.type.value:
            return False
        else:
            card_ranking = WILD_CARD_RANKINGS if self.jokers else REGULAR_RANKINGS
            for i, card in enumerate(self.cards):
                if card_ranking[card] < card_ranking[other.cards[i]]:
                    return True
                elif card_ranking[card] > card_ranking[other.cards[i]]:
                    return False
        return False


def get_puzzle() -> Puzzle:
    year = int(__file__.split("/")[-3].removeprefix("aoc-"))
    day = int(__file__.split("/")[-2].removeprefix("day"))

    puzzle = Puzzle(year=year, day=day)
    export_data(puzzle=puzzle, year=year, day=day)
    return puzzle


def parse_data(input_data: str) -> Any:
    output = []
    for line in input_data.splitlines():
        cards, bid = line.split()
        output.append(Hand(cards=cards, bid=int(bid)))

    return output


@timed
def part_1(input_data: str) -> Any:
    parsed_data = parse_data(input_data=input_data)

    # Body Logic
    sorted_data = sorted(parsed_data)

    return sum([hand.bid * i for i, hand in enumerate(sorted_data, start=1)])


@timed
def part_2(input_data: str) -> Any:
    parsed_data = parse_data(input_data=input_data)
    for hand in parsed_data:
        hand.jokers = True

    return sum([hand.bid * i for i, hand in enumerate(sorted(parsed_data), start=1)])


def main() -> None:
    puzzle = get_puzzle()
    run(puzzle=puzzle, part_1=part_1, part_2=part_2)


if __name__ == "__main__":
    main()
