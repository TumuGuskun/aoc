from collections import defaultdict
from math import lcm
from typing import Any

from aocd.examples import Example

from shared.util import get_puzzle, run, timed


def parse_data(input_data: str) -> Any:
    nodes = defaultdict(list)
    directions, maze_nodes = input_data.split("\n\n")
    directions = [0 if d == "L" else 1 for d in directions]

    for maze_node in maze_nodes.splitlines():
        node, children = maze_node.split(" = ")
        children = children.replace("(", "").replace(")", "").split(", ")
        nodes[node] = children

    return directions, nodes


@timed
def part_1(input_data: str) -> Any:
    directions, nodes = parse_data(input_data=input_data)
    curr_node = "AAA"
    step_count = 0

    # Body Logic
    while curr_node != "ZZZ":
        curr_direction = directions[step_count % len(directions)]
        curr_node = nodes[curr_node][curr_direction]
        step_count += 1

    return step_count


@timed
def part_2(input_data: str) -> Any:
    directions, nodes = parse_data(input_data=input_data)

    start_nodes = [node for node in nodes if node.endswith("A")]
    step_counts = []

    for start_node in start_nodes:
        curr_node = start_node
        step_count = 0

        while not curr_node.endswith("Z"):
            curr_direction = directions[step_count % len(directions)]
            curr_node = nodes[curr_node][curr_direction]
            step_count += 1

        step_counts.append(step_count)

    return lcm(*step_counts)


def main() -> None:
    puzzle = get_puzzle(__file__)
    examples = [
        Example(
            input_data="RL\n\nAAA = (BBB, CCC)\nBBB = (DDD, EEE)\nCCC = (ZZZ, GGG)\nDDD = (DDD, DDD)\nEEE = (EEE, EEE)\nGGG = (GGG, GGG)\nZZZ = (ZZZ, ZZZ)",
            answer_a="2",
            answer_b="",
        ),
        Example(
            input_data="LLR\n\nAAA = (BBB, BBB)\nBBB = (AAA, ZZZ)\nZZZ = (ZZZ, ZZZ)",
            answer_a="6",
            answer_b="",
        ),
        Example(
            input_data="LR\n\n11A = (11B, XXX)\n11B = (XXX, 11Z)\n11Z = (11B, XXX)\n22A = (22B, XXX)\n22B = (22C, 22C)\n22C = (22Z, 22Z)\n22Z = (22B, 22B)\nXXX = (XXX, XXX)",
            answer_a="",
            answer_b="6",
        ),
    ]
    puzzle._get_examples = lambda parser_name=None: examples
    run(puzzle=puzzle, part_1=part_1, part_2=part_2)


if __name__ == "__main__":
    main()
