import re
from collections import defaultdict, deque

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return tuple(map(int, re.search(r'(\d+) players; last marble is worth (\d+)', input_file.read()).group(1, 2)))


@timed
def part1(players):
    num_players, num_marbles = players
    scores = defaultdict(int)
    circle = deque([0])

    player = 1
    for marble in range(1, num_marbles + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[player] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

        player = (player + 1) % num_players

    print(max(scores.values()))


@timed
def part2(players):
    num_players, num_marbles = players
    num_marbles *= 100
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(1, num_marbles + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % num_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    print(max(scores.values()))


if __name__ == '__main__':
    player_list = read()
    part1(player_list)
    part2(player_list)
