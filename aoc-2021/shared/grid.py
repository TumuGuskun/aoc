import numpy as np


class Grid:
    def __init__(self, grid, edges=None):
        if isinstance(grid[0], str):
            grid = [list(line.rstrip()) for line in grid]
        self.grid = np.array(grid, dtype=object)
        self.edges = edges
        self.size = self.grid.size

    def adjacents(self, i, j):
        if i == 0:
            if j == 0:
                neighbors = [(i + 1, j), (i, j + 1)]
            elif j == self.grid.shape[1] - 1:
                neighbors = [(i + 1, j), (i, j - 1)]
            else:
                neighbors = [(i + 1, j), (i, j - 1), (i, j + 1)]
        elif i == self.grid.shape[0] - 1:
            if j == 0:
                neighbors = [(i - 1, j), (i, j + 1)]
            elif j == self.grid.shape[1] - 1:
                neighbors = [(i - 1, j), (i, j - 1)]
            else:
                neighbors = [(i - 1, j), (i, j - 1), (i, j + 1)]
        elif j == 0:
            neighbors = [(i + 1, j), (i - 1, j), (i, j + 1)]
        elif j == self.grid.shape[1] - 1:
            neighbors = [(i - 1, j), (i + 1, j), (i, j - 1)]
        else:
            neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]

        if self.edges:
            return [(p, self.grid[p]) for p in neighbors if self.grid[p] not in self.edges]
        else:
            return [(p, self.grid[p]) for p in neighbors]

    def set(self, i, j, v):
        self.grid[i, j] = v

    def inc(self, i, j):
        self.grid[i, j] += 1

    def get(self, i, j):
        return self.grid[i, j]

    def columns(self):
        for j in range(self.grid.shape[1]):
            yield self.grid[:, j]

    def row(self):
        for i in range(self.grid.shape[0]):
            yield self.grid[i, :]

    def diags(self, i, j):
        if i == 0:
            if j == 0:
                diags = [(i + 1, j + 1)]
            elif j == self.grid.shape[1] - 1:
                diags = [(i + 1, j - 1)]
            else:
                diags = [(i + 1, j + 1), (i + 1, j - 1)]
        elif i == self.grid.shape[0] - 1:
            if j == 0:
                diags = [(i - 1, j + 1)]
            elif j == self.grid.shape[1] - 1:
                diags = [(i - 1, j - 1)]
            else:
                diags = [(i - 1, j - 1), (i - 1, j + 1)]
        elif j == 0:
            diags = [(i + 1, j + 1), (i - 1, j + 1)]
        elif j == self.grid.shape[1] - 1:
            diags = [(i - 1, j - 1), (i + 1, j - 1)]
        else:
            diags = [(i + 1, j + 1), (i - 1, j + 1), (i - 1, j - 1), (i + 1, j - 1)]

        if self.edges:
            return [(p, self.grid[p]) for p in diags if self.grid[p] not in self.edges]
        else:
            return [(p, self.grid[p]) for p in diags]

    def __copy__(self):
        return Grid(self.grid, edges=self.edges)

    def neighbors(self, i, j):
        return self.diags(i, j) + self.adjacents(i, j)

    def __repr__(self):
        output = ''
        for row in self.grid:
            line = ''
            for e in row:
                line += str(e)
            output += line + '\n'
        return output

    def __hash__(self):
        return hash(f'{self.grid}')

    def __lt__(self, other):
        return True

    def __eq__(self, other):
        return np.array_equal(self.grid, other.grid)
