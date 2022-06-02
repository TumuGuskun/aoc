from functools import wraps
from time import time
from typing import Callable


def timed(func: Callable) -> Callable:
    @wraps(func)
    def timed_wrapper(*args, **kwargs):
        ts = time()
        result = func(*args, **kwargs)
        te = time()
        print(f'{func.__name__:<5} finished in {te - ts:>10.6f} seconds')
        return result
    return timed_wrapper


def read_op_codes():
    with open('input.txt') as input_file:
        return [(op, int(arg)) for op, arg in map(lambda line: line.rstrip().split(), input_file.readlines())]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'