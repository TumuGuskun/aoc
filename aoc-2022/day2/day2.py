from shared.util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return [line.strip().split() for line in input_file]


# A for Rock, B for Paper, and C for Scissors
# X for Rock, Y for Paper, and Z for Scissors
RPS_MAP = {
    "A": "r",
    "B": "p",
    "C": "s",
    "X": "r",
    "Y": "p",
    "Z": "s",
}

RPS_WINNER = {
    "r": "s",
    "s": "p",
    "p": "r",
}

POINTS = {
    "r": 1,
    "p": 2,
    "s": 3,
}


@timed
def part1(inputs):
    points = 0
    for opponent, me in inputs:
        opp_move = RPS_MAP[opponent]
        me_move = RPS_MAP[me]
        if opp_move == me_move:
            points += 3
        elif RPS_WINNER[me_move] == opp_move:
            points += 6
        points += POINTS[me_move]
    print(points)


@timed
def part2(inputs):
    points = 0
    for opp, me in inputs:
        opp_move = RPS_MAP[opp]
        if me == "X":
            points += POINTS[RPS_WINNER[opp_move]]
        elif me == "Y":
            points += 3 + POINTS[opp_move]
        else:
            points += 6 + POINTS[RPS_WINNER[RPS_WINNER[opp_move]]]
    print(points)


if __name__ == "__main__":
    input_list = read()
    part1(input_list)
    part2(input_list)
