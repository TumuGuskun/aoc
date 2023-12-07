from __future__ import annotations

import re
from dataclasses import dataclass

from shared.gum import gum_choose
from shared.util import get_input_files, timed


@dataclass
class Pull:
    red: int = 0
    blue: int = 0
    green: int = 0

    @staticmethod
    def from_description(description: str) -> Pull:
        pull = Pull()
        for color in ["red", "blue", "green"]:
            if (match := re.search(rf"(\d+) {color}", description)) is not None:
                setattr(pull, color, int(match.group(1)))
        return pull

    @property
    def power(self) -> int:
        return self.red * self.blue * self.green

    def is_valid(self) -> bool:
        return self.red <= 12 and self.blue <= 14 and self.green <= 13


@dataclass
class Game:
    game_id: int
    pulls: list[Pull]

    def is_valid(self) -> bool:
        return all(pull.is_valid() for pull in self.pulls)

    def get_miminal_set(self) -> Pull:
        max_red = max(pull.red for pull in self.pulls)
        max_blue = max(pull.blue for pull in self.pulls)
        max_green = max(pull.green for pull in self.pulls)
        return Pull(max_red, max_blue, max_green)


@timed
def read() -> list[Game]:
    files = get_input_files(__file__)
    if len(files) == 1:
        file_name = files[0]
    else:
        _, file_name = gum_choose(files, "Choose input file")

    print(f"Reading from {file_name.split('/')[-1]}")
    with open(file_name) as input_file:
        games = []
        for game_line in input_file.readlines():
            game_id = int(re.search(r"Game (\d+):", game_line).group(1))
            pulls = [
                Pull.from_description(raw_pull)
                for raw_pull in game_line.split(":")[1].split(";")
            ]
            games.append(Game(game_id, pulls))

        return games


@timed
def part1(games: list[Game]) -> None:
    print(sum([game.game_id for game in games if game.is_valid()]))


@timed
def part2(games: list[Game]) -> None:
    print(sum([game.get_miminal_set().power for game in games]))


if __name__ == "__main__":
    game_list = read()
    part1(game_list)
    part2(game_list)
