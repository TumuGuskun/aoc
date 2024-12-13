import os
import re
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from itertools import islice
from time import perf_counter
from typing import Any, Callable, Iterable, Optional, TypeVar

from aocd.examples import Example
from aocd.models import Puzzle
from yaspin import yaspin

from shared.grid import Grid
from shared.point import Point

T = TypeVar("T")


def timed(func: Callable) -> Callable:
    @wraps(func)
    def timed_wrapper(*args, **kwargs):
        ts = perf_counter()
        result = func(*args, **kwargs)
        te = perf_counter()
        return result, te - ts

    return timed_wrapper


class Color(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7


def colored(txt: str, color: Color):
    if color is None:
        return txt
    code = color.value
    reset = "\x1b[0m"
    return f"\x1b[{code + 30}m{txt}{reset}"


@dataclass
class OpCode:
    op: str
    args: list[int]

    @property
    def first(self) -> int:
        return self.args[0]


def read_op_codes(lines: list[str]) -> list[OpCode]:
    op_codes = []
    for line in lines:
        op, *args = line.rstrip().split()
        op_codes.append(OpCode(op=op, args=list(map(int, args))))
    return op_codes


def get_ints(line: str) -> list[int]:
    return list(map(lambda m: int(m.group(0)), re.finditer(r"(-?\d+)", line)))


def get_caps(line: str) -> list[str]:
    return list(map(lambda m: m.group(0), re.finditer(r"(-?[A-Z]+)", line)))


def ints(start=0, step=1):
    while True:
        yield start
        start += step


def coordinate(grid: Iterable | Grid) -> Iterable[tuple[Point, Any]]:
    if isinstance(grid, Grid):
        grid = grid.grid
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            yield Point(i, j), v


def tail(iterable: Iterable[T]) -> Iterable[T]:
    _, *output = iterable
    return output


def head(iterable: Iterable[Any]) -> Any:
    output, *_ = iterable
    return output


def chomp(iterable: list[T], i: int) -> list[T]:
    output = iterable[:i]
    del iterable[:i]
    return output


def clamp(n: int, smallest: int, largest: int) -> int:
    return max(smallest, min(n, largest))


def chunk(iterable: Iterable, chunk_size: int):
    iterable = iter(iterable)
    return iter(lambda: tuple(islice(iterable, chunk_size)), ())


def get_input_files(script_file: str) -> list[str]:
    input_files = []
    for dirpath, _, filenames in os.walk(os.path.dirname(os.path.abspath(script_file))):
        for f in filenames:
            if f.endswith(".txt"):
                input_files.append(os.path.abspath(os.path.join(dirpath, f)))

    return input_files


def get_time_color(time: float) -> Color:
    if time < 0.5:
        return Color.GREEN
    elif time < 5:
        return Color.YELLOW
    else:
        return Color.RED


def print_run_output(output: list[str]) -> None:
    print("{: <30} {: <40} {: >20}".format(*output))


def print_example_output(
    example_number: int,
    my_answer: Any,
    their_answer: str,
    time: float,
) -> None:
    time_color = get_time_color(time)
    if str(my_answer) != their_answer:
        output = [
            colored(f"❌ Example {example_number} failed", Color.RED),
            colored(f"expected {their_answer}, got {my_answer}", Color.MAGENTA),
            colored(f"{time:>8.6f}s", time_color),
        ]
    else:
        output = [
            colored(f"✅ Example {example_number} passed", Color.GREEN),
            colored(f"Answer: {my_answer}", Color.MAGENTA),
            colored(f"{time:>8.6f}s", time_color),
        ]

    print_run_output(output=output)


def check_examples(
    examples: list[Example],
    solve_function: Callable,
    parser: Callable,
) -> bool:
    print(
        colored(
            f"\n{solve_function.__name__.replace('_', ' ').upper()}\n------\n",
            Color.YELLOW,
        )
    )

    passed_all_examples = True
    ran_any = False
    for i, example in enumerate(examples, start=1):
        if solve_function.__name__ == "part_1":
            their_answer = example.answer_a
        else:
            their_answer = example.answer_b

        if not their_answer:
            continue

        ran_any = True
        with yaspin(text=f"Running example {i}", color="yellow"):
            ts = perf_counter()
            my_answer = solve_function(parser(example.input_data))
            te = perf_counter()
            passed_all_examples = str(my_answer) == their_answer and passed_all_examples
        print_example_output(i, my_answer, their_answer, te - ts)

    if not ran_any:
        print_run_output(
            [
                colored("⚠️ No examples found", Color.CYAN),
                colored(" ", Color.MAGENTA),
                colored(" ", Color.RED),
            ]
        )
        return False

    return passed_all_examples


def submit(puzzle: Puzzle, solve_function: Callable, parser: Callable) -> None:
    part_name = solve_function.__name__.replace("_", " ").capitalize()

    with yaspin(
        text=f"Running {part_name}",
        color="yellow",
    ):
        ts = perf_counter()
        answer = solve_function(parser(puzzle.input_data))
        te = perf_counter()

    time = te - ts
    time_color = get_time_color(time)
    if part_name == "Part 1":
        puzzle.answer_a = answer
        passed = puzzle.answered_a
    else:
        puzzle.answer_b = answer
        passed = puzzle.answered_b

    if passed:
        output = [
            colored(f"✅ {part_name} passed", Color.GREEN),
            colored(f"Answer: {answer}", Color.MAGENTA),
            colored(f"{time:>8.6f}s", time_color),
        ]
    else:
        output = [
            colored(f"❌ {part_name} failed", Color.RED),
            colored(f"Guessed: {answer}", Color.MAGENTA),
            colored(f"{time:>8.6f}s", time_color),
        ]

    print_run_output(output=output)


def run(
    puzzle: Puzzle,
    part_1: Callable,
    part_2: Callable,
    parser: Callable,
    part_2_parser: Optional[Callable] = None,
    run_part_1: bool = True,
    run_part_2: bool = True,
    run_examples: bool = True,
    force_run_2: bool = False,
) -> None:
    if run_part_1:
        if run_examples:
            run_part_1 = check_examples(puzzle.examples, part_1, parser)

        if run_part_1:
            submit(puzzle, part_1, parser)

    if run_part_2 and puzzle.answered_a:
        parser = parser if part_2_parser is None else part_2_parser
        if run_examples:
            run_part_2 = check_examples(puzzle.examples, part_2, parser)

        if run_part_2 or force_run_2:
            submit(puzzle, part_2, parser)


def import_export_data(puzzle: Puzzle, year: int, day: int) -> None:
    if not os.path.exists(
        f"/Users/timgaskin/workspace/aoc/aoc-{year}/day{day}/input.txt"
    ):
        with open(
            f"/Users/timgaskin/workspace/aoc/aoc-{year}/day{day}/input.txt", "w"
        ) as f:
            f.write(puzzle.input_data)

    if os.path.exists(
        f"/Users/timgaskin/workspace/aoc/aoc-{year}/day{day}/examples.txt"
    ):
        with open(
            f"/Users/timgaskin/workspace/aoc/aoc-{year}/day{day}/examples.txt"
        ) as f:
            examples = []
            for example in f.read().split("\n\n-----------------------------\n\n"):
                if not example:
                    continue

                example = example.split("\n---\n")
                raw_answer_a, raw_answer_b = example[2].strip().split("\n")
                answer_a = "" if "None" in raw_answer_a else raw_answer_a.split(": ")[1]
                answer_b = "" if "None" in raw_answer_b else raw_answer_b.split(": ")[1]
                examples.append(
                    Example(
                        input_data=example[1],
                        answer_a=answer_a,
                        answer_b=answer_b,
                    )
                )

            puzzle._get_examples = lambda parser_name=None: examples
    else:
        with open(
            f"/Users/timgaskin/workspace/aoc/aoc-{year}/day{day}/examples.txt", "w"
        ) as f:
            f.write(
                "\n\n-----------------------------\n\n".join(
                    [
                        "\n".join(
                            [
                                f"### Example {i}",
                                "---",
                                example.input_data,
                                "---",
                                f"Answer 1: {example.answer_a}",
                                f"Answer 2: {example.answer_b}",
                            ]
                        )
                        for i, example in enumerate(puzzle.examples, start=1)
                    ]
                )
            )


def get_puzzle(file_path: str) -> Puzzle:
    year = int(file_path.split("/")[-3].removeprefix("aoc-"))
    day = int(file_path.split("/")[-2].removeprefix("day"))

    puzzle = Puzzle(year=year, day=day)
    import_export_data(puzzle=puzzle, year=year, day=day)
    return puzzle
