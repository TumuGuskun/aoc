from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Optional


@dataclass
class Point:
    i: int
    j: int

    def __add__(self, other: Point) -> Point:
        return Point(self.i + other.i, self.j + other.j)

    def __hash__(self) -> int:
        return hash((self.i, self.j))

    def __eq__(self, other: Point) -> bool:
        return self.i == other.i and self.j == other.j

    def __str__(self) -> str:
        return f"({self.i}, {self.j})"

    def __repr__(self) -> str:
        return f"({self.i}, {self.j})"

    def is_valid(
        self,
        lower_x: int = 0,
        lower_y: int = 0,
        upper_x: Optional[int] = None,
        upper_y: Optional[int] = None,
    ) -> bool:
        u_x = self.i <= upper_x if upper_x is not None else True
        u_y = self.j <= upper_y if upper_y is not None else True
        lowers = self.i >= lower_x and self.j >= lower_y
        return u_x and u_y and lowers

    def __lt__(self, other: Point) -> bool:
        return max(abs(self.i), abs(self.j)) < max(abs(other.i), abs(other.j))

    def euc_distance(self, other: Point) -> float:
        return sqrt((self.i - other.i) ** 2 + (self.j - other.j) ** 2)

    def man_distance(self, other: Point) -> int:
        return abs(self.i - other.i) + abs(self.j - other.j)

    def is_neighbor(self, other: Point) -> bool:
        return abs(self.i - other.i) <= 1 and abs(self.j - other.j) <= 1
