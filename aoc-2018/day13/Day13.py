from collections import defaultdict

from shared.Util import timed


MAZE = defaultdict(lambda: defaultdict(str))


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        carts = []
        for i, line in enumerate(input_file):
            for j, val in enumerate(line):
                if val in ['/', '\\', '+']:
                    MAZE[i][j] = val
                elif val in ['<', '>', '^', 'v']:
                    carts.append(Cart(j, i, val))
        return carts


@timed
def part1(mazes):
    carts = mazes
    while True:
        seen = set()
        for cart in sorted(carts, key=lambda c: (c.y, c.x)):
            cart.move()
            if (cart.x, cart.y) in seen:
                print(cart)
                return
            else:
                seen.add((cart.x, cart.y))


@timed
def part2(mazes):
    carts = mazes
    while len(carts) > 1:
        seen = set()
        new_carts = []
        for cart in sorted(carts, key=lambda c: (c.y, c.x)):
            if cart in seen:
                while cart in new_carts:
                    new_carts.remove(cart)
            else:
                seen.add(cart)
                cart.move()
                if cart not in seen:
                    new_carts.append(cart)
                    seen.add(cart)
                else:
                    while cart in new_carts:
                        new_carts.remove(cart)

        carts = new_carts

    print(carts)


class Cart:
    map_dir = {
        '<': {
            'r': '^',
            'l': 'v',
            's': '<',
            '/': 'v',
            '\\': '^'
        },
        '>': {
            'r': 'v',
            'l': '^',
            's': '>',
            '/': '^',
            '\\': 'v'
        },
        'v': {
            'r': '<',
            'l': '>',
            's': 'v',
            '/': '<',
            '\\': '>'
        },
        '^': {
            'r': '>',
            'l': '<',
            's': '^',
            '/': '>',
            '\\': '<'
        },
        'turn': {
            'l': 's',
            's': 'r',
            'r': 'l'
        }
    }

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turn = 'l'

    def move(self):
        if self.direction == '<':
            self.x -= 1
        elif self.direction == '>':
            self.x += 1
        elif self.direction == 'v':
            self.y += 1
        elif self.direction == '^':
            self.y -= 1

        if (spot := MAZE[self.y][self.x]) == '+':
            self.direction = self.map_dir[self.direction][self.turn]
            self.turn = self.map_dir['turn'][self.turn]
        elif spot in ['/', '\\']:
            self.direction = self.map_dir[self.direction][spot]

    def __repr__(self):
        return f'({self.x}, {self.y}): {self.direction}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


if __name__ == '__main__':
    maze_list = read()
    # part1(maze_list)
    part2(maze_list)
