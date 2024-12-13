from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Optional

from shared.util import get_ints, get_puzzle, run, timed


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def sum(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclass
class Test:
    result: str
    subpart: str = ""
    comparator: str = ""
    value: int = 0

    def evaluate(self, part: Part) -> Optional[str]:
        if self.subpart:
            part_value = getattr(part, self.subpart)
            if self.comparator == ">" and part_value > self.value:
                return self.result
            elif self.comparator == "<" and part_value < self.value:
                return self.result
        else:
            return self.result


def parse_data(input_data: str) -> tuple[dict, list[Part]]:
    workflows = defaultdict(list)
    parts: list[Part] = []
    for line in input_data.splitlines():
        if line.startswith("{"):
            parts.append(Part(*get_ints(line)))
        elif line:
            workflow, tests = line.split("{")
            for test in tests.strip("}").split(","):
                if ":" in test:
                    test, result = test.split(":")
                    subpart = test[0]
                    comparator = test[1]
                    value = int(test[2:])
                    workflows[workflow].append(
                        Test(
                            result=result,
                            subpart=subpart,
                            comparator=comparator,
                            value=value,
                        )
                    )
                else:
                    workflows[workflow].append(Test(result=test))

    return workflows, parts


@timed
def part_1(input_data: tuple[dict, list[Part]]) -> int:
    workflows, parts = input_data

    total = 0
    for part in parts:
        workflow = workflows["in"]
        while True:
            done = False
            for test in workflow:
                if result := test.evaluate(part):
                    if result == "A":
                        total += part.sum()
                        done = True
                        break
                    elif result == "R":
                        done = True
                        break
                    workflow = workflows[result]
                    break

            if done:
                break

    return total


@timed
def part_2(input_data: str) -> Any:
    return None


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(
        puzzle=puzzle,
        part_1=part_1,
        part_2=part_2,
        parser=parse_data,
    )


if __name__ == "__main__":
    main()
