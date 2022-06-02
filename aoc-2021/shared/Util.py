import re
from functools import wraps
from time import perf_counter
from typing import Callable, Iterable, Any

from shared.grid import Grid


def timed(func: Callable) -> Callable:
    @wraps(func)
    def timed_wrapper(*args, **kwargs):
        ts = perf_counter()
        result = func(*args, **kwargs)
        te = perf_counter()
        print(f'{func.__name__:<5} finished in {te - ts:>10.6f} seconds')
        return result
    return timed_wrapper


def read_op_codes(input_file):
    return [(op, int(arg)) for op, arg in map(lambda line: line.rstrip().split(), input_file.readlines())]


def get_ints(line):
    return list(map(lambda m: int(m.group(0)), re.finditer(r'(-?\d+)', line)))


def ints(start=0, step=1):
    while True:
        yield start
        start += step


def coordinate(grid: Iterable):
    if isinstance(grid, Grid):
        grid = grid.grid
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            yield (i, j), v


def second(tup):
    return tup[1]


def first(tup):
    return tup[0]


def chomp(iterable: Iterable[Any], i: int) -> Iterable[Any]:
    output = iterable[:i]
    del iterable[:i]
    return output
