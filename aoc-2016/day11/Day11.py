from itertools import combinations

from shared.Util import timed


class Building:
    def __init__(self, floors):
        self.elevator = 1
        self.floors = {floor.floor: floor for floor in sorted(floors, key=lambda x: x.floor, reverse=True)}

    def __repr__(self):
        output = ''
        for floor in self.floors.values():
            output += ' E ' if floor.floor == self.elevator else '   '
            output += str(floor) + '\n'
        return output

    def get_floor(self, i):
        return self.floors[i]


class Floor:
    def __init__(self, floor, generators, chips):
        self.floor = floor
        self.generators = generators
        self.chips = chips

    def is_valid(self):
        return all(chip.is_safe(self.generators) for chip in self.chips)

    def get_moves(self):
        valid_moves = []
        for move in self.generators + self.chips:
            if self.new_minus(move).is_valid():
                for floor in self.valid_floors():
                    print('derp')

        for comb in list(combinations(self.generators + self.chips, 2)):
            pass
        print(list(combinations(self.generators + self.chips, 2)))

    def valid_floors(self):
        if self.floor == 1:
            return [2]
        elif self.floor == 4:
            return [3]
        else:
            return [self.floor - 1, self.floor + 1]

    def new_minus(self, o):
        if isinstance(o, Chip):
            new_chips = self.chips.copy()
            new_chips.remove(o)
            return Floor(self.floor, self.generators.copy(), new_chips)
        elif isinstance(o, Generator):
            new_generators = self.generators.copy()
            new_generators.remove(o)
            return Floor(self.floor, new_generators, self.chips.copy())

    def __repr__(self):
        return f'F{self.floor}: {" ".join(map(str, self.generators + self.chips))}'


class Chip:
    def __init__(self, element):
        self.element = element

    def is_safe(self, generators):
        return any(generator.element == self.element for generator in generators) or not generators

    def __copy__(self):
        return Chip(self.element)

    def __repr__(self):
        return f'{self.element.upper()}M'


class Generator:
    def __init__(self, element):
        self.element = element

    def __copy__(self):
        return Generator(self.element)

    def __repr__(self):
        return f'{self.element.upper()}G'


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    floors = []
    with open(file_name) as input_file:
        for line in input_file.readlines():
            floor, contents = line.split(maxsplit=1)
            floors.append(Floor(int(floor),
                                list(map(lambda g: Generator(g[0]), filter(lambda x: 'g' in x, contents.split()))),
                                list(map(lambda m: Chip(m[0]), filter(lambda x: 'm' in x, contents.split())))))
    floors.append(Floor(4, [], []))
    return Building(floors)


@timed
def part1(building):
    print(building)
    for floor in building.floors:
        print(floor.floor)
        floor.get_moves()


@timed
def part2(floors):
    pass


if __name__ == '__main__':
    floor_list = read()
    part1(floor_list)
    part2(floor_list)
