from dataclasses import dataclass
from itertools import islice
import re
from functools import wraps
from time import perf_counter
from typing import Callable, Iterable, Any, TypeVar

from shared.grid import Grid


T = TypeVar("T")


def timed(func: Callable) -> Callable:
    @wraps(func)
    def timed_wrapper(*args, **kwargs):
        ts = perf_counter()
        result = func(*args, **kwargs)
        te = perf_counter()
        print(f"{func.__name__:<5} finished in {te - ts:>10.6f} seconds")
        return result

    return timed_wrapper


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


def coordinate(grid: Iterable | Grid):
    if isinstance(grid, Grid):
        grid = grid.grid
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            yield (i, j), v


def tail(iterable: Iterable[T]) -> Iterable[T]:
    _, *output = iterable
    return output


def head(iterable: Iterable[Any]) -> Any:
    output, *_ = iterable
    return output


def chomp(iterable: Iterable[T], i: int) -> Iterable[T]:
    output = iterable[:i]
    del iterable[:i]
    return output


def clamp(n: int, smallest: int, largest: int) -> int:
    return max(smallest, min(n, largest))


def chunk(iterable: Iterable, chunk_size: int):
    iterable = iter(iterable)
    return iter(lambda: tuple(islice(iterable, chunk_size)), ())
