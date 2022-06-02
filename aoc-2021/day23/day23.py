from copy import copy, deepcopy
from queue import PriorityQueue

from pipe import where, select

import numpy as np

from shared.Util import *
from shared.bfs import BFS


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return Grid(input_file.readlines(), edges='#ABCD')


@timed
def part1(grid):
    bfs(grid, Amphipod)


def bfs(grid):
    queue = PriorityQueue()
    seen = {}
    queue.put((0, grid))
    seen[grid] = 0

    while not queue.empty():
        curr_cost, curr_grid = queue.get()
        pods = [Amphipod2(p, v) for p, v in coordinate(curr_grid.grid) if v in 'ABCD']

        if all(pod.is_done(curr_grid) for pod in pods):
            print(curr_cost)
            print(curr_grid)
            return
        else:
            for i, pod in enumerate(pods):
                for move, move_cost in pod.find_moves(curr_grid):
                    new_g = copy(curr_grid)
                    new_g.set(*move, pod.species)
                    new_g.set(*pod.pos, '.')
                    if new_g not in seen or curr_cost + move_cost < seen[new_g]:
                        queue.put((curr_cost + move_cost, new_g))
                        seen[new_g] = curr_cost + move_cost

    print(curr_grid)


class Amphipod:
    def __init__(self, pos, species):
        self.pos = pos
        self.species = species
        self.goal_x = [2, 3]

        if self.species == 'A':
            self.cost = 1
            self.goal_y = 3
        elif self.species == 'B':
            self.cost = 10
            self.goal_y = 5
        elif self.species == 'C':
            self.cost = 100
            self.goal_y = 7
        elif self.species == 'D':
            self.cost = 1000
            self.goal_y = 9

    def is_done(self, grid):
        if self.pos[0] == 3 and self.pos[1] == self.goal_y:
            return True
        elif self.pos[0] == 2 and self.pos[1] == self.goal_y and grid.get(3, self.goal_y) == self.species:
            return True
        else:
            return False

    def find_moves(self, grid):
        if self.pos[0] == 1:
            if grid.get(3, self.goal_y) == '.':
                desired_moves = [(3, self.goal_y)]
            elif grid.get(3, self.goal_y) == self.species and grid.get(2, self.goal_y) == '.':
                desired_moves = [(2, self.goal_y)]
            else:
                desired_moves = []
        else:
            doors = [(1, 3), (1, 5), (1, 7), (1, 9)]
            if self.is_done(grid):
                desired_moves = []
            elif grid.get(3, self.goal_y) == '.':
                desired_moves = [(3, self.goal_y)]
            elif grid.get(3, self.goal_y) == self.species and grid.get(2, self.goal_y) == '.':
                desired_moves = [(2, self.goal_y)]
            else:
                desired_moves = list(
                    list(np.argwhere(grid.grid == '.')) | where(lambda x: tuple(x) not in doors)
                                                        | where(lambda x: x[0] == 1)

                )
                if self.species == 'D':
                    desired_moves = desired_moves | where(lambda x: tuple(x) not in [(1, 1), (1, 2), (1, 10), (1, 11)])

        return list(
            desired_moves | select(lambda p: (p, BFS(start=self.pos,
                                                     search_space=grid,
                                                     neighbor_function=lambda c, _, seen, ___: filter(lambda n2: n2[0] not in seen, zip(map(first, grid.adjacents(*c)), [0] * 4)),
                                                     end_condition=lambda c, __: c[0] == p[0] and c[1] == p[1]).run().paths))
                          | where(lambda p: p[1])
                          | select(lambda p: (p[0], (len(min(p[1], key=len)) - 1) * self.cost))
        )

    def __eq__(self, other):
        return self.species == other.species

    def __repr__(self):
        return f'{self.species}: {self.pos}'

    def __copy__(self):
        return Amphipod(self.pos, self.species)

    def __hash__(self):
        return 0

    def __lt__(self, other):
        return self.cost < other.cost


@timed
def part2(_):
    with open('input1.txt') as input_file:
        grid = Grid(input_file.readlines(), edges='#ABCD')

    bfs(grid)


class Amphipod2:
    def __init__(self, pos, species):
        self.pos = pos
        self.species = species
        self.goal_x = [2, 3, 4, 5]

        if self.species == 'A':
            self.cost = 1
            self.goal_y = 3
        elif self.species == 'B':
            self.cost = 10
            self.goal_y = 5
        elif self.species == 'C':
            self.cost = 100
            self.goal_y = 7
        elif self.species == 'D':
            self.cost = 1000
            self.goal_y = 9

    def is_done(self, grid):
        if self.pos[0] == 5 and self.pos[1] == self.goal_y:
            return True
        elif grid.get(5, self.goal_y) == self.species:
            if self.pos[0] == 4 and self.pos[1] == self.goal_y:
                return True
            elif grid.get(4, self.goal_y) == self.species:
                if self.pos[0] == 3 and self.pos[1] == self.goal_y:
                    return True
                elif grid.get(3, self.goal_y) == self.species:
                    if self.pos[0] == 2 and self.pos[1] == self.goal_y:
                        return True
        return False

    def find_moves(self, grid):
        if self.pos[0] == 1:
            desired_moves = []
            if grid.get(5, self.goal_y) == '.':
                desired_moves = [(5, self.goal_y)]
            elif grid.get(5, self.goal_y) == self.species:
                if grid.get(4, self.goal_y) == '.':
                    desired_moves = [(4, self.goal_y)]
                elif grid.get(4, self.goal_y) == self.species:
                    if grid.get(3, self.goal_y) == '.':
                        desired_moves = [(3, self.goal_y)]
                    elif grid.get(3, self.goal_y) == self.species:
                        if grid.get(2, self.goal_y) == '.':
                            desired_moves = [(2, self.goal_y)]
        else:
            doors = [(1, 3), (1, 5), (1, 7), (1, 9)]
            if self.is_done(grid):
                desired_moves = []
            else:
                if grid.get(5, self.goal_y) == '.':
                    desired_moves = [(5, self.goal_y)]
                elif grid.get(5, self.goal_y) == self.species:
                    if grid.get(4, self.goal_y) == '.':
                        desired_moves = [(4, self.goal_y)]
                    elif grid.get(4, self.goal_y) == self.species:
                        if grid.get(3, self.goal_y) == '.':
                            desired_moves = [(3, self.goal_y)]
                        elif grid.get(3, self.goal_y) == self.species:
                            if grid.get(2, self.goal_y) == '.':
                                desired_moves = [(2, self.goal_y)]
                else:
                    desired_moves = list(list(np.argwhere(grid.grid == '.')) | where(lambda x: tuple(x) not in doors)
                                                                             | where(lambda x: x[0] == 1))

        return list(
            desired_moves | select(lambda p: (p, BFS(start=self.pos,
                                                     search_space=grid,
                                                     neighbor_function=lambda c, _, seen, ___: filter(lambda n2: n2[0] not in seen, zip(map(first, grid.adjacents(*c)), [0] * 4)),
                                                     end_condition=lambda c, __: c[0] == p[0] and c[1] == p[1]).run().paths))
            | where(lambda p: p[1])
            | select(lambda p: (p[0], (len(min(p[1], key=len)) - 1) * self.cost))
        )

    def __eq__(self, other):
        return self.species == other.species

    def __repr__(self):
        return f'{self.species}: {self.pos}'

    def __copy__(self):
        return Amphipod2(self.pos, self.species)

    def __hash__(self):
        return 0

    def __lt__(self, other):
        return self.cost < other.cost


if __name__ == '__main__':
    maze_list = read()
    # part1(maze_list)
    part2(maze_list)
