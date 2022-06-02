import re
from functools import wraps
from queue import Queue
from time import time
from typing import Callable, Any, Iterable, Tuple, List


def timed(func: Callable) -> Callable:
    @wraps(func)
    def timed_wrapper(*args, **kwargs):
        ts = time()
        result = func(*args, **kwargs)
        te = time()
        print(f'{func.__name__:<5} finished in {te - ts:>10.6f} seconds')
        return result
    return timed_wrapper


def read_op_codes(input_file):
    return [(op, int(arg)) for op, arg in map(lambda line: line.rstrip().split(), input_file.readlines())]


def get_ints(line):
    return list(map(lambda m: int(m.group(0)), re.finditer(r'(-?\d+)', line)))


class Point:
    def __init__(self, x, y, v_x=0, v_y=0):
        self.x = x
        self.y = y

        self.v_x = v_x
        self.v_y = v_y

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

    def is_valid(self, lower_x=0, lower_y=0, upper_x=None, upper_y=None):
        u_x = self.x <= upper_x if upper_x else True
        u_y = self.y <= upper_y if upper_y else True
        lowers = self.x >= lower_x and self.y >= lower_y
        return u_x and u_y and lowers

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

    def __lt__(self, other):
        return max(abs(self.x), abs(self.y)) < max(abs(other.x), abs(other.y))


class LinkedList:
    def __init__(self, elements):
        tail = Node(elements[-1], None)
        next_node = tail
        for e in reversed(elements[:-1]):
            previous_node = Node(e, next_node)
            next_node = previous_node
        tail.set_next(next_node)

        self.head = next_node
        self.tail = tail

    def __repr__(self):
        curr = self.head
        output = []
        while curr != self.tail:
            output.append(curr)
            curr = curr.next_node
        output.append(curr)
        return f"{', '.join(map(str, output))}"


class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next_node = next_node

    def set_next(self, new_next):
        self.next_node = new_next

    def __repr__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other.value


def ints(start=0, step=1):
    while True:
        yield start
        start += step


def bfs(start: Any,
        search_space: Iterable[Any],
        end_condition: Callable[[Any], bool],
        neighbor_function: Callable[[Any, Iterable[Any]], Iterable[Any]]) -> Tuple[Any, List]:
    queue = Queue()
    queue.put((start, []))
    seen = set()
    seen.add(start)

    while not queue.empty():
        curr_node, path = queue.get()
        if end_condition(curr_node):
            return curr_node, path
        else:
            for neighbor in neighbor_function(curr_node, search_space):
                if neighbor not in seen:
                    neighbor_path = path + [curr_node]
                    queue.put((neighbor, neighbor_path))


DIR_MAP = {
    '↑': {
        '→': '→',
        '←': '←',
        'vec': Point(-1, 0)
    },
    '↓': {
        '→': '←',
        '←': '→',
        'vec': Point(1, 0)
    },
    '←': {
        '→': '↑',
        '←': '↓',
        'vec': Point(0, -1)
    },
    '→': {
        '→': '↓',
        '←': '↑',
        'vec': Point(0, 1)
    },
}


class Vector:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction

    def rotate_r(self):
        self.direction = DIR_MAP[self.direction]['→']

    def rotate_l(self):
        self.direction = DIR_MAP[self.direction]['←']

    def flip(self):
        self.rotate_l()
        self.rotate_l()

    def move(self, num=1):
        for _ in range(num):
            self.point += DIR_MAP[self.direction]['vec']

    def __hash__(self):
        return hash(self.point) + hash(self.direction)

    def __eq__(self, other):
        return self.point == other.point and self.direction == other.direction

    def __str__(self):
        return f'{self.point} {self.direction}'

    def __repr__(self):
        return f'{self.point} {self.direction}'
