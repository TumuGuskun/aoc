from typing import Any

from shared.util import *


def parse_data(input_data: str) -> Any:
    return Grid(input_data.splitlines(), edges=[])


@dataclass
class Region:
    value: str
    points: set[Point]

    @property
    def area(self) -> int:
        return len(self.points)

    @property
    def perimeter(self) -> int:
        perimeter = 0
        for point in self.points:
            perimeter += 4 - sum(
                1 for other_point in self.points if point.man_distance(other_point) == 1
            )

        return perimeter

    @property
    def price(self) -> int:
        return self.area * self.perimeter

    def get_discount_price(self, grid: Grid) -> int:
        return self.area * self.get_sides(grid)

    def get_sides(self, grid: Grid) -> int:
        sides = 0
        for point in self.points:
            point_sides = 0
            # check east and west
            north_point = point + NORTH
            north_value = grid.get_point_if_valid(north_point)
            if north_value != self.value:
                if (
                    grid.get_point_if_valid(point + EAST) != self.value
                    or grid.get_point_if_valid(north_point + EAST) == self.value
                ):
                    point_sides += 1
                    sides += 1

            south_point = point + SOUTH
            south_value = grid.get_point_if_valid(south_point)
            if south_value != self.value:
                if (
                    grid.get_point_if_valid(point + EAST) != self.value
                    or grid.get_point_if_valid(south_point + EAST) == self.value
                ):
                    point_sides += 1
                    sides += 1

            east_point = point + EAST
            east_value = grid.get_point_if_valid(east_point)
            if east_value != self.value:
                if (
                    north_value != self.value
                    or grid.get_point_if_valid(east_point + NORTH) == self.value
                ):
                    point_sides += 1
                    sides += 1

            west_point = point + WEST
            west_value = grid.get_point_if_valid(west_point)
            if west_value != self.value:
                if (
                    north_value != self.value
                    or grid.get_point_if_valid(west_point + NORTH) == self.value
                ):
                    point_sides += 1
                    sides += 1

        return sides


def get_regions(grid: Grid) -> list[Region]:
    regions = []
    big_seen = set()

    for point, value in coordinate(grid):
        if point in big_seen:
            continue

        queue = [point]
        region_points = {point}

        while queue:
            current_point = queue.pop()
            for neighbor_point, neighbor_value in grid.get_adjacents(current_point):
                if neighbor_value == value and neighbor_point not in region_points:
                    region_points.add(neighbor_point)
                    big_seen.add(neighbor_point)
                    queue.append(neighbor_point)

        regions.append(Region(value, region_points))

    return regions


def part_1(grid: Grid) -> int:
    return sum(region.price for region in get_regions(grid))


def part_2(grid: Grid) -> int:
    return sum(region.get_discount_price(grid) for region in get_regions(grid))


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
