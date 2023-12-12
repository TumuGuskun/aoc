from typing import Any

from aocd.examples import Example

from shared.util import get_ints, get_puzzle, run, timed


def parse_data(input_data: str) -> Any:
    output = []
    for line in input_data.splitlines():
        output.append(get_ints(line))

    return output


@timed
def part_1(input_data: str) -> Any:
    histories = parse_data(input_data=input_data)

    # Body Logic
    prediction_sum = 0
    for history in histories:
        sub_histories = []

        sub_history = []
        for value_1, value_2 in zip(history, history[1:]):
            sub_history.append(value_2 - value_1)

        sub_histories.append(sub_history)
        while len(set(sub_histories[-1])) > 1:
            sub_history = []
            for value_1, value_2 in zip(sub_histories[-1], sub_histories[-1][1:]):
                sub_history.append(value_2 - value_1)
            sub_histories.append(sub_history)

        sub_prediction = 0
        for sub_history in sub_histories[::-1]:
            sub_prediction += sub_history[-1]

        prediction_sum += sub_prediction + history[-1]

    return prediction_sum


@timed
def part_2(input_data: str) -> Any:
    histories = parse_data(input_data=input_data)

    # Body Logic
    prediction_sum = 0
    for history in histories:
        sub_histories = []

        sub_history = []
        for value_1, value_2 in zip(history, history[1:]):
            sub_history.append(value_2 - value_1)

        sub_histories.append(sub_history)
        while len(set(sub_histories[-1])) > 1:
            sub_history = []
            for value_1, value_2 in zip(sub_histories[-1], sub_histories[-1][1:]):
                sub_history.append(value_2 - value_1)
            sub_histories.append(sub_history)

        sub_prediction = 0
        for sub_history in sub_histories[::-1]:
            sub_prediction = sub_history[0] - sub_prediction

        prediction_sum += history[0] - sub_prediction

    return prediction_sum


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(puzzle=puzzle, part_1=part_1, part_2=part_2)


if __name__ == "__main__":
    main()
