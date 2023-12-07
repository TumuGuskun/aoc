import os

from shared.gum import gum_choose
from shared.util import timed, coordinate
from shared.grid import Grid


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return Grid(
            grid=[list(map(int, list(line.strip()))) for line in input_file.readlines()]
        )


def visible_from_outside(value: int, i: int, j: int, grid: Grid) -> bool:
    curr_row = grid.get_row(i)
    curr_column = grid.get_column(j)
    return (
        all(value > tree for tree in curr_row[:j])
        or all(value > tree for tree in curr_row[j + 1 :])
        or all(value > tree for tree in curr_column[:i])
        or all(value > tree for tree in curr_column[i + 1 :])
    )


@timed
def part1(inputs: Grid):
    visible = 0
    for (i, j), value in coordinate(grid=inputs.grid):
        if (
            i == 0
            or j == 0
            or i == len(inputs.get_column(0)) - 1
            or j == len(inputs.get_row(0)) - 1
        ):
            visible += 1
        elif visible_from_outside(value, i, j, inputs):
            visible += 1
    print(visible)


def score_tree(tree: int, i: int, j: int, grid: Grid) -> int:
    curr_row = grid.get_row(i)
    curr_column = grid.get_column(j)

    up = 0
    curr_i = i - 1
    while 0 <= curr_i and curr_column[curr_i] < tree:
        up += 1
        curr_i -= 1
    if 0 <= curr_i:
        up += 1

    down = 0
    curr_i = i + 1
    while curr_i < len(curr_column) and curr_column[curr_i] < tree:
        down += 1
        curr_i += 1
    if curr_i < len(curr_column):
        down += 1

    right = 0
    curr_j = j + 1
    while curr_j < len(curr_row) and curr_row[curr_j] < tree:
        right += 1
        curr_j += 1
    if curr_j < len(curr_row):
        right += 1

    left = 0
    curr_j = j - 1
    while 0 <= curr_j and curr_row[curr_j] < tree:
        left += 1
        curr_j -= 1
    if 0 <= curr_j:
        left += 1

    return up * down * left * right


@timed
def part2(inputs):
    highest_score = 0
    for (i, j), tree in coordinate(grid=inputs):
        highest_score = max(highest_score, score_tree(tree, i, j, inputs))
    print(highest_score)


if __name__ == "__main__":
    input_list = read()
    part1(input_list)
    part2(input_list)
