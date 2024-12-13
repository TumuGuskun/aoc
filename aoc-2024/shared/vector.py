from __future__ import annotations

from dataclasses import dataclass

from shared.point import Point

DIR_MAP = {
    "^": {">": ">", "<": "<", "vec": Point(-1, 0)},
    "v": {">": "<", "<": ">", "vec": Point(1, 0)},
    "<": {">": "^", "<": "v", "vec": Point(0, -1)},
    ">": {">": "v", "<": "^", "vec": Point(0, 1)},
}


@dataclass
class Vector:
    position: Point
    direction: str

    def rotate(self, direction: str) -> None:
        self.direction = DIR_MAP[self.direction][direction]

    def rotate_r(self) -> None:
        self.direction = DIR_MAP[self.direction][">"]

    def rotate_l(self) -> None:
        self.direction = DIR_MAP[self.direction]["<"]

    def flip(self) -> None:
        self.rotate_l()
        self.rotate_l()

    def move(self, num: int = 1) -> None:
        for _ in range(num):
            self.position += DIR_MAP[self.direction]["vec"]

    def move_back(self, num: int = 1) -> None:
        self.flip()
        for _ in range(num):
            self.position += DIR_MAP[self.direction]["vec"]
        self.flip()

    def __hash__(self) -> int:
        return hash(self.position) + hash(self.direction)

    def __eq__(self, other: Vector) -> bool:
        return self.position == other.position and self.direction == other.direction

    def __str__(self) -> str:
        return f"{self.position} {self.direction}"

    def __repr__(self) -> str:
        return f"{self.position} {self.direction}"

    def __copy__(self) -> Vector:
        return Vector(self.position, self.direction)
