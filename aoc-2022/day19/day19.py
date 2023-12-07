from __future__ import annotations
from collections import Counter
from dataclasses import dataclass, replace
from enum import Enum, auto
import os
from queue import Queue
from tqdm import tqdm

from shared.gum import gum_choose
from shared.util import timed, get_ints


class Bot(Enum):
    ORE = auto()
    CLAY = auto()
    OBSIDIAN = auto()
    GEODE = auto()
    NULL = auto()


@dataclass
class Blueprint:
    id: int
    ore_bot_ore: int
    clay_bot_ore: int
    obsidian_bot_ore: int
    obsidian_bot_clay: int
    geode_bot_ore: int
    geode_bot_obsidian: int


@dataclass(unsafe_hash=True)
class Stockpile:
    ore_bot: int = 1
    clay_bot: int = 0
    obsidian_bot: int = 0
    geode_bot: int = 0
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    def collect(self) -> Stockpile:
        return Stockpile(
            ore_bot=self.ore_bot,
            clay_bot=self.clay_bot,
            obsidian_bot=self.obsidian_bot,
            geode_bot=self.geode_bot,
            ore=self.ore + self.ore_bot,
            clay=self.clay + self.clay_bot,
            obsidian=self.obsidian + self.obsidian_bot,
            geode=self.geode + self.geode_bot,
        )

    def can_create_bot(self, bot_type: Bot, blueprint: Blueprint) -> bool:
        match bot_type:
            case Bot.ORE:
                return self.ore >= blueprint.ore_bot_ore
            case Bot.CLAY:
                return self.ore >= blueprint.clay_bot_ore
            case Bot.OBSIDIAN:
                return (
                    self.ore >= blueprint.obsidian_bot_ore
                    and self.clay >= blueprint.obsidian_bot_clay
                )
            case Bot.GEODE:
                return (
                    self.ore >= blueprint.geode_bot_ore
                    and self.obsidian >= blueprint.geode_bot_obsidian
                )
            case _:
                return False

    def add_bot(self, bot_type: Bot, blueprint: Blueprint) -> Stockpile:
        fields = self.__dict__.copy()
        match bot_type:
            case Bot.ORE:
                fields["ore_bot"] += 1
                fields["ore"] -= blueprint.ore_bot_ore
            case Bot.CLAY:
                fields["clay_bot"] += 1
                fields["ore"] -= blueprint.clay_bot_ore
            case Bot.OBSIDIAN:
                fields["obsidian_bot"] += 1
                fields["ore"] -= blueprint.obsidian_bot_ore
                fields["clay"] -= blueprint.obsidian_bot_clay
            case Bot.GEODE:
                fields["geode_bot"] += 1
                fields["ore"] -= blueprint.geode_bot_ore
                fields["obsidian"] -= blueprint.geode_bot_obsidian
        return Stockpile(**fields)


def get_bot_plans(stockpile: Stockpile, blueprint: Blueprint) -> list[Counter[Bot]]:
    possible_plans = []
    queue = Queue()
    for bot_type in Bot:
        if stockpile.can_create_bot(bot_type=bot_type, blueprint=blueprint):
            queue.put(
                (
                    stockpile.add_bot(bot_type=bot_type, blueprint=blueprint),
                    Counter([bot_type]),
                )
            )

    while not queue.empty():
        curr_stockpile, curr_bots = queue.get()
        if curr_bots not in possible_plans:
            possible_plans.append(curr_bots)

        for bot_type in Bot:
            if curr_stockpile.can_create_bot(bot_type=bot_type, blueprint=blueprint):
                next_bots = curr_bots.copy()
                next_bots[bot_type] += 1
                queue.put(
                    (
                        curr_stockpile.add_bot(bot_type=bot_type, blueprint=blueprint),
                        next_bots,
                    )
                )

    return possible_plans


@timed
def read() -> list[Blueprint]:
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return [Blueprint(*get_ints(line)) for line in input_file.readlines()]


def simulate(blueprint: Blueprint) -> int:
    stockpile = Stockpile()
    queue = Queue()
    queue.put((1, stockpile))
    seen = set()

    max_geodes = 0
    minute_tracker = 0
    while not queue.empty():
        minute, curr_stockpile = queue.get()
        possible_bot_plans = get_bot_plans(
            stockpile=curr_stockpile, blueprint=blueprint
        )

        if minute_tracker != minute:
            print(minute)
            minute_tracker = minute

        curr_stockpile = curr_stockpile.collect()
        if minute == 24:
            max_geodes = max(curr_stockpile.geode, max_geodes)
            continue
        for possible_bot_plan in possible_bot_plans:
            next_stockpile = replace(curr_stockpile)
            for bot in possible_bot_plan:
                next_stockpile = next_stockpile.add_bot(
                    bot_type=bot, blueprint=blueprint
                )
            if next_stockpile not in seen:
                seen.add(next_stockpile)
                queue.put((minute + 1, next_stockpile))
        queue.put((minute + 1, curr_stockpile))

    return stockpile.geode


@timed
def part1(blueprints: list[Blueprint]):
    print(sum([simulate(blueprint) * blueprint.id for blueprint in tqdm(blueprints)]))


@timed
def part2(blueprints: list[Blueprint]):
    pass


if __name__ == "__main__":
    blueprint_list = read()
    part1(blueprint_list)
    part2(blueprint_list)
