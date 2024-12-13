from dataclasses import dataclass, field
from queue import Queue
from typing import Any

from shared.grid import Grid
from shared.point import Point
from shared.util import get_puzzle, run, timed


def parse_data(input_data: str) -> Any:
    return Grid(input_data.splitlines())


@dataclass
class Path:
    current_position: Point
    path: list[str] = field(default_factory=list)
    heat_loss: int = 0


@timed
def part_1(grid: Grid) -> int:
    min_heat_loss = 10000000000000

    seen = set()
    queue = Queue()

    start = Point(0, 0)
    finish = Point(grid.width - 1, grid.height - 1)
    seen.add(start)
    queue.put(Path(current_position=start))

    while not queue.empty():
        current_path = queue.get()

        if current_path.current_position == finish:
            print(current_path)
            min_heat_loss = min(min_heat_loss, current_path.heat_loss)
            continue

        for point, value in grid.get_adjacents(current_path.current_position):
            print(point, value)
            if point not in seen:
                direction = point - current_path.current_position
                if all(direction == point for point in current_path.path[-3:]):
                    continue
                seen.add(point)
                queue.put(
                    Path(
                        current_position=point,
                        path=current_path.path + [direction],
                        heat_loss=current_path.heat_loss + int(value),
                    )
                )

    return min_heat_loss


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
