from __future__ import annotations
import os
import operator

from shared.gum import gum_choose
from shared.util import timed


ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,  # use operator.div for Python 2
    "%": operator.mod,
    "^": operator.xor,
    "==": operator.eq,
}


class Expr:
    def __init__(self, name: str, expr: str) -> None:
        self.name = name
        if expr.isnumeric():
            self.expr = int(expr)
        else:
            self.expr = None
            self.left, self.op, self.right = expr.split()

    def evaluate(self, expressions: dict[str, Expr]) -> int | bool:
        if self.expr is not None:
            return self.expr
        else:
            return ops[self.op](
                expressions[self.left].evaluate(expressions=expressions),
                expressions[self.right].evaluate(expressions=expressions),
            )


@timed
def read() -> dict[str, str]:
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        jobs = {}
        for line in input_file.readlines():
            name, expr = line.strip().split(": ")
            jobs[name] = Expr(name=name, expr=expr)
    return jobs


@timed
def part1(jobs: dict[str, Expr]) -> None:
    print(jobs["root"].evaluate(expressions=jobs))


@timed
def part2(jobs: dict[str, Expr]) -> None:
    jobs["root"].op = "=="
    target = jobs[jobs["root"].right].evaluate(jobs)
    current = 0
    jobs["humn"].expr = 1
    curr_streak = 0
    while current != target:
        if current < target:
            if curr_streak > 0:
                curr_streak = -1
            elif curr_streak < -100:
                curr_streak *= 2
            else:
                curr_streak -= 1
        else:
            if curr_streak < 0:
                curr_streak = 1
            elif curr_streak > 100:
                curr_streak *= 2
            else:
                curr_streak += 1
        jobs["humn"].expr += curr_streak
        current = jobs[jobs["root"].left].evaluate(expressions=jobs)
    print(jobs["humn"].expr)


if __name__ == "__main__":
    job_list = read()
    part1(job_list)
    part2(job_list)
