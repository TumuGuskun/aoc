from queue import Queue
from shared.OpCoder import OpCoder
from collections import defaultdict
from subprocess import call
from time import sleep


class Area:
    def __init__(self):
        self.area = defaultdict(lambda: defaultdict(lambda: ' '))

    def update_board(self, x, y, status, direction):
        if (x, y) == (0, 0):
            self.area[y][x] = 'Ⓧ'
        elif status == 1:
            self.area[y][x] = '.'
        elif status == 0:
            if direction == 0:
                y += 1
            elif direction == 1:
                x += 1
            elif direction == 2:
                y -= 1
            elif direction == 3:
                x -= 1
            self.area[y][x] = '█'
        elif status == 2:
            self.area[y][x] = 'O'

    def print_ship(self):
        min_x, max_x = 0, 0
        for y in self.area:
            key_list = [min_x, max_x]
            key_list.extend(self.area[y].keys())
            min_x = min(key_list)
            max_x = max(key_list)
        call('clear')
        for i in range(max(self.area.keys()), min(self.area.keys()) - 1, -1):
            line = []
            for j in range(min_x, max_x + 1):
                line.append(self.area[i][j])
            print(''.join(line))

    def get_neighbors(self, x, y):
        neighbor_list = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [(n_x, n_y) for n_x, n_y in neighbor_list if self.area[n_y][n_x] in ['.', 'O']]

    def set(self, x, y, symbol):
        self.area[y][x] = symbol


class Bot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = 0
        self.found = False
        self.mapping = [1, 4, 2, 3]
        self.count = 0

    def next_move(self, status):
        if status == 0:
            self.dir -= 1
        elif status == 1:
            self.dir += 1
        elif status == 2:
            self.dir += 1
            if self.count == 1:
                self.found = True
            else:
                self.count += 1
        else:
            raise Exception('Wat')

        self.dir %= 4
        return self.mapping[self.dir]

    def move(self, status):
        if status == 1 or status == 2:
            if self.dir == 0:
                self.y += 1
            elif self.dir == 1:
                self.x += 1
            elif self.dir == 2:
                self.y -= 1
            elif self.dir == 3:
                self.x -= 1
            else:
                raise Exception('Derp')


def get_input(filename):
    with open(filename, 'r') as input_file:
        op_codes = list(map(int, input_file.read().split(',')))
    return op_codes


def part1(filename):
    op_codes = get_input(filename)

    queue = Queue()
    op_coder = OpCoder(op_codes, queue)

    area = Area()
    area.update_board(0, 0, 3, 0)

    bot = Bot()

    queue.put(1)

    while not bot.found:
        status = op_coder.run()
        bot.move(status)
        area.update_board(bot.x, bot.y, status, bot.dir)
        queue.put(bot.next_move(status))

    area.print_ship()

    bfs_queue = Queue()
    bfs_queue.put(((0, 0), 0))

    seen = dict()
    seen[(0, 0)] = None
    while not bfs_queue.empty():
        (x, y), depth = bfs_queue.get()
        if area.area[y][x] == 'O':
            print(depth)
            break
        for neighbor in area.get_neighbors(x, y):
            if neighbor not in seen:
                seen[neighbor] = (x, y)
                bfs_queue.put((neighbor, depth + 1))

    bfs_queue = Queue()
    bfs_queue.put(((x, y), 0))
    see_depth = 0
    seen = dict()
    seen[(0, 0)] = None
    while not bfs_queue.empty():
        sleep(0.08)
        (x, y), depth = bfs_queue.get()
        area.set(x, y, 'O')
        for neighbor in area.get_neighbors(x, y):
            if neighbor not in seen:
                seen[neighbor] = (x, y)
                bfs_queue.put((neighbor, depth + 1))
        if see_depth < depth:
            see_depth += 1
            area.print_ship()

    print(depth)


if __name__ == '__main__':
    part1('input.txt')
