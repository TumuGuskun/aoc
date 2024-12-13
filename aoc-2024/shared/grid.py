from __future__ import annotations

from typing import Any, Generator, Optional

import numpy as np
from numpy import ndarray

from shared.point import Point

NORTH = Point(-1, 0)
SOUTH = Point(1, 0)
EAST = Point(0, 1)
WEST = Point(0, -1)

NE = Point(-1, 1)
NW = Point(-1, -1)
SE = Point(1, 1)
SW = Point(1, -1)

DIRECTIONS = [NORTH, SOUTH, EAST, WEST, NE, NW, SE, SW]


class Grid:
    def __init__(self, grid: Any, edges: Optional[list[str]] = None) -> None:
        if isinstance(grid[0], str):
            grid = [list(line.rstrip()) for line in grid]
        if grid[0][0].isdigit():
            grid = [[int(e) for e in row] for row in grid]
        self.grid = np.array(grid, dtype=object)
        self.edges = edges
        self.size = self.grid.size
        self.height, self.width = self.grid.shape

    def get_adjacents(self, point: Point) -> list[tuple[Point, Any]]:
        if point.i == 0:
            if point.j == 0:
                directions = [SOUTH, EAST]
            elif point.j == self.width - 1:
                directions = [SOUTH, WEST]
            else:
                directions = [SOUTH, WEST, EAST]
        elif point.i == self.height - 1:
            if point.j == 0:
                directions = [NORTH, EAST]
            elif point.j == self.width - 1:
                directions = [NORTH, WEST]
            else:
                directions = [NORTH, WEST, EAST]
        elif point.j == 0:
            directions = [SOUTH, NORTH, EAST]
        elif point.j == self.width - 1:
            directions = [NORTH, SOUTH, WEST]
        else:
            directions = [SOUTH, NORTH, EAST, WEST]

        neighbors = [point + direction for direction in directions]
        if self.edges:
            return [
                (p, value)
                for p in neighbors
                if (value := self.get_point(point=p)) not in self.edges
            ]
        else:
            return [(p, self.get_point(point=p)) for p in neighbors]

    def set_point(self, point: Point, value: Any) -> None:
        self.grid[point.i, point.j] = value

    def inc_point(self, point: Point) -> None:
        self.grid[point.i, point.j] += 1

    def get_point(self, point: Point) -> Any:
        return self.grid[point.i, point.j]

    def get_columns(self) -> Generator[ndarray, None, None]:
        for j in range(self.grid.shape[1]):
            yield self.grid[:, j]

    def get_rows(self) -> Generator[ndarray, None, None]:
        for i in range(self.grid.shape[0]):
            yield self.grid[i, :]

    def get_row(self, i: int) -> ndarray:
        return self.grid[i, :]

    def get_column(self, j: int) -> ndarray:
        return self.grid[:, j]

    def get_diagonals(self, point: Point) -> list[tuple[Point, Any]]:
        if point.i == 0:
            if point.j == 0:
                directions = [SE]
            elif point.j == self.width - 1:
                directions = [SW]
            else:
                directions = [SE, SW]
        elif point.i == self.height - 1:
            if point.j == 0:
                directions = [NE]
            elif point.j == self.width - 1:
                directions = [NW]
            else:
                directions = [NW, NE]
        elif point.j == 0:
            directions = [SE, NE]
        elif point.j == self.width - 1:
            directions = [NW, SW]
        else:
            directions = [NW, NE, SW, SE]

        diags = [point + direction for direction in directions]
        if self.edges:
            return [
                (p, value)
                for p in diags
                if (value := self.get_point(p)) not in self.edges
            ]
        else:
            return [(p, self.get_point(p)) for p in diags]

    def check_point_valid(self, point: Point) -> bool:
        return (
            self.check_point_in_bounds(point=point)
            and self.get_point(point=point) not in self.edges
        )

    def check_point_in_bounds(self, point: Point) -> bool:
        return (0 <= point.i < self.height) and (0 <= point.j < self.width)

    def __copy__(self) -> Grid:
        return Grid(self.grid, edges=self.edges)

    def get_neighbors(self, point: Point) -> list[tuple[Point, Any]]:
        return self.get_diagonals(point=point) + self.get_adjacents(point=point)

    def __repr__(self) -> str:
        output = ""
        for row in self.grid:
            line = ""
            for e in row:
                line += str(e)
            output += line + "\n"
        return output

    def __hash__(self) -> int:
        return hash(f"{self.grid}")

    def __lt__(self, other: Grid) -> bool:
        return True

    def __eq__(self, other) -> bool:
        return np.array_equal(self.grid, other.grid)

    def find(self, value: Any) -> list[Point]:
        return list(map(lambda p: Point(*p), np.argwhere(self.grid == value)))

    def insert_row(self, i: int, value: Any) -> None:
        self.grid = np.insert(self.grid, i, value, axis=0)
        self.height += 1

    def insert_column(self, j: int, value: Any) -> None:
        self.grid = np.insert(self.grid, j, value, axis=1)
        self.width += 1

    def get_n_in_a_row(
        self,
        point: Point,
        direction: Point,
        n: int,
    ) -> list[tuple[Point, Any]]:
        points = [(point, self.get_point(point=point))]
        for _ in range(n - 1):
            point += direction
            if not self.check_point_in_bounds(point):
                break
            points.append((point, self.get_point(point=point)))

        return points

    def get_point_if_valid(self, point: Point) -> Optional[Any]:
        if self.check_point_in_bounds(point):
            return self.get_point(point)
        return None
