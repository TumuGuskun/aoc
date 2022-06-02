from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.readlines()


@timed
def part1(mazes):
    pass


@timed
def part2(mazes):
    pass


class Piece:
    def __init__(self):
        pass


class Board:
    def __init(self, file):
        self.board = []


if __name__ == '__main__':
    maze_list = read()
    part1(maze_list)
    part2(maze_list)
