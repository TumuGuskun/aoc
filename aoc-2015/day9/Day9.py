from collections import defaultdict
from copy import copy

from shared.Util import timed

DISTANCES = defaultdict(dict)


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        for line in input_file.readlines():
            towns, distance = line.split(' = ')
            town_a, town_b = towns.split(' to ')
            DISTANCES[town_a].update({town_b: int(distance)})
            DISTANCES[town_b].update({town_a: int(distance)})


def min_distance(node, seen):
    if len(seen) == len(DISTANCES) - 1:
        return [distance for town, distance in DISTANCES[node].items() if town not in seen][0]
    else:
        minimum = float('inf')
        for town in [t for t in DISTANCES[node] if t not in seen]:
            new_seen = copy(seen)
            new_seen.add(town)
            minimum = min(minimum, min_distance(town, new_seen) + DISTANCES[node][town])
        return minimum


def max_distance(node, seen):
    if len(seen) == len(DISTANCES) - 1:
        return [distance for town, distance in DISTANCES[node].items() if town not in seen][0]
    else:
        maximum = 0
        for town in [t for t in DISTANCES[node] if t not in seen]:
            new_seen = copy(seen)
            new_seen.add(town)
            maximum = max(maximum, max_distance(town, new_seen) + DISTANCES[node][town])
        return maximum


@timed
def part1():
    print(min(min_distance(start_node, {start_node}) for start_node in DISTANCES.keys()))


@timed
def part2():
    print(max(max_distance(start_node, {start_node}) for start_node in DISTANCES.keys()))


if __name__ == '__main__':
    read()
    part1()
    part2()
