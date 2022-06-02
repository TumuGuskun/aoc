from dataclasses import dataclass, replace
from functools import cache
from itertools import cycle

from shared.Util import *


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return list(map(get_ints, input_file))


@timed
def part1(players):
    (_, p1_start), (_, p2_start) = players

    i = 0
    die = cycle(range(1, 101))
    players = [Player(score=0, position=p2_start), Player(0, p1_start)]
    while all(p.score < 1000 for p in players):
        i += 1
        turn = i % 2
        p_roll = sum(next(die) for _ in range(3))

        curr_pos = players[turn].position
        curr_score = players[turn].score
        curr_pos += p_roll
        if curr_pos % 10 == 0:
            curr_pos = 10
        else:
            curr_pos = curr_pos % 10
        curr_score += curr_pos
        players[turn] = replace(players[turn], score=curr_score, position=curr_pos)

    print(min(players, key=lambda p: p.score).score * i * 3)


@dataclass(eq=True, frozen=True)
class Player:
    score: int
    position: int


@timed
def part2(players):
    (_, p1_start), (_, p2_start) = players

    print(max(play((Player(score=0, position=p1_start), Player(score=0, position=p2_start)), 0)))


@cache
def play(players, turn):
    if players[0].score > 20:
        return 1, 0
    elif players[1].score > 20:
        return 0, 1
    else:
        scores = []
        for i in range(1, 4):
            for j in range(1, 4):
                for k in range(1, 4):
                    new_players = [None, None]
                    pos = (players[turn].position + i + j + k - 1) % 10 + 1
                    new_players[turn] = replace(players[turn], score=players[turn].score + pos, position=pos)
                    new_players[turn ^ 1] = replace(players[turn ^ 1])

                    scores.append(play(tuple(new_players), turn ^ 1))

        return tuple(sum(i) for i in zip(*scores))


if __name__ == '__main__':
    player_list = read()
    part1(player_list)
    part2(player_list)
