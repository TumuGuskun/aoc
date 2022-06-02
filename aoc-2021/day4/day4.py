from copy import copy

from shared.Util import timed, get_ints


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        numbers = get_ints(input_file.readline())
        input_file.readline()

        boards = []
        board = []
        for line in input_file:
            if line == '\n':
                boards.append(Board(board))
                board = []
            else:
                board.append(get_ints(line))
        return numbers, boards


@timed
def part1(bingos):
    numbers, boards = bingos
    boards = copy(boards)

    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.check_win():
                print(board.score(number))
                return


class Board:
    def __init__(self, board):
        self.board = board

    def mark(self, number):
        for i, row in enumerate(self.board):
            for j, e in enumerate(row):
                if e == number:
                    self.board[i][j] = 'x'

    def check_win(self):
        if any(board == ['x'] * 5 for board in self.board):
            return True
        elif any([board[i] for board in self.board] == ['x'] * 5 for i, _ in enumerate(self.board[0])):
            return True
        else:
            return False

    def score(self, number):
        count = 0
        for row in self.board:
            for e in row:
                if e != 'x':
                    count += e
        return count * number

    def __repr__(self):
        output = '\n'
        for row in self.board:
            output += ' '.join(map(str, row)) + '\n'

        return output + '\n'

    def __copy__(self):
        new_board = []
        for row in self.board:
            new_board.append(copy(row))

        return new_board


@timed
def part2(bingos):
    numbers, boards = bingos

    for i, number in enumerate(numbers):
        if len(boards) > 1:
            to_remove = []
            for board in boards:
                board.mark(number)
                if board.check_win():
                    to_remove.append(board)

            for board in to_remove:
                boards.remove(board)

        elif len(boards) == 1:
            last_board = boards[0]
            last_board.mark(number)
            if last_board.check_win():
                print(last_board.score(number))
                return
        else:
            print(to_remove.pop().score(numbers[i - 1]))
            return


if __name__ == '__main__':
    bingo_list = read()
    part1(bingo_list)
    part2(bingo_list)
