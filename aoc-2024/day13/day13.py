from typing import Any

from shared.util import *


@dataclass
class Button:
    id: str
    x: int
    y: int


def parse_data(input_data: str) -> Any:
    output = []
    system = np.zeros((2, 2))
    solution = np.zeros(2)
    for line in input_data.splitlines():
        if "A" in line:
            system[:, 0] = get_ints(line)
        elif "B" in line:
            system[:, 1] = get_ints(line)
        elif "Prize" in line:
            solution = get_ints(line)
            output.append((system.copy(), solution.copy()))

    return output


def part_1(machines: list[tuple[ndarray, ndarray]]) -> int:
    total = 0
    for system, solution in machines:
        answer = np.linalg.solve(system, solution)
        answer = [round(i, 4) for i in answer]

        if any(i % 1 != 0 for i in answer):
            continue

        total += sum(answer * np.array([3, 1]))

    return int(total)


def part_2(machines: list[tuple[ndarray, ndarray]]) -> int:
    total = 0
    for system, solution in machines:
        solution += np.array([10000000000000, 10000000000000])
        answer = np.linalg.solve(system, solution)
        answer = [round(i, 4) for i in answer]

        if any(i % 1 != 0 for i in answer):
            continue

        total += sum(answer * np.array([3, 1]))

    return int(total)


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(
        puzzle=puzzle,
        part_1=part_1,
        part_2=part_2,
        parser=parse_data,
        force_run_2=True,
    )


if __name__ == "__main__":
    main()
