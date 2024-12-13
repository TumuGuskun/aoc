from typing import Any

from shared.grid import Grid
from shared.point import Point
from shared.util import coordinate, get_puzzle, run


def parse_data(input_data: str) -> Any:
    output = []
    for grid in input_data.split("\n\n"):
        output.append(Grid(grid.splitlines()))
    return output


def get_mirrored_rows(grid: Grid, bad_row: int = -1) -> int:
    for i in range(grid.height - 1):
        mirrored = True
        for j in range(min(grid.height - i - 1, i + 1)):
            top = grid.get_row(i - j)
            bottom = grid.get_row(i + j + 1)
            if (top != bottom).any():
                mirrored = False
                break

        if mirrored and i + 1 != bad_row:
            return i + 1

    return 0


def get_mirrored_cols(grid: Grid, bad_col: int = -1) -> int:
    for j in range(grid.width - 1):
        mirrored = True
        for i in range(min(grid.width - j - 1, j + 1)):
            left = grid.get_column(j - i)
            right = grid.get_column(j + i + 1)
            if (left != right).any():
                mirrored = False
                break

        if mirrored and j + 1 != bad_col:
            return j + 1

    return 0


def part_1(grids: list[Grid]) -> Any:
    # Body Logic
    result = 0
    for grid in grids:
        if (row_count := get_mirrored_rows(grid)) > 0:
            result += 100 * row_count
        if (col_count := get_mirrored_cols(grid)) > 0:
            result += col_count

    return result


def reset_grid(element: str, point: Point, grid: Grid) -> None:
    if element == "#":
        grid.set_point(point, "#")
    else:
        grid.set_point(point, ".")


def part_2(grids: list[Grid]) -> Any:
    result = 0
    for grid in grids:
        current_row = get_mirrored_rows(grid)
        current_col = get_mirrored_cols(grid)

        for point, element in coordinate(grid=grid):
            if element == "#":
                grid.set_point(point, ".")
            else:
                grid.set_point(point, "#")

            if row_count := get_mirrored_rows(grid, current_row):
                result += 100 * row_count
                reset_grid(element, point, grid)
                break

            if col_count := get_mirrored_cols(grid, current_col):
                result += col_count
                reset_grid(element, point, grid)
                break

            reset_grid(element, point, grid)

    return result


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
