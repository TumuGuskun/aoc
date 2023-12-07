import os

from shared.gum import gum_choose
from shared.util import timed


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        return input_file.read().strip()


@timed
def part1(signals):
    for i, char in enumerate(signals):
        if len(set(signals[i : i + 4])) == 4:
            print(i + 4)
            break


@timed
def part2(signals):
    for i, char in enumerate(signals):
        if len(set(signals[i : i + 14])) == 14:
            print(i + 14)
            break


if __name__ == "__main__":
    signal_list = read()
    part1(signal_list)
    part2(signal_list)
