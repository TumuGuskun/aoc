from __future__ import annotations
from dataclasses import dataclass, field

from shared.util import timed, get_ints


@dataclass
class Box:
    name: str

    def __repr__(self) -> str:
        return self.name

    def copy(self) -> Box:
        return Box(name=self.name)


@dataclass
class Board:
    board: list[list[Box]] = field(default_factory=lambda: [[] for _ in range(10)])

    def take_boxes(self, num_boxes: int, col_from: int) -> list[Box]:
        boxes = self.board[col_from][-num_boxes:]
        self.board[col_from] = self.board[col_from][:-num_boxes]
        return boxes

    def put_boxes(self, boxes: list[Box], col_to: int) -> None:
        self.board[col_to].extend(boxes)

    def get_top_boxes(self) -> str:
        return "".join([str(col[-1]) for col in self.board if col])

    def flip_boxes(self) -> None:
        for i, col in enumerate(self.board):
            self.board[i] = list(reversed(col))

    def __repr__(self) -> str:
        return str(self.board)

    def copy(self) -> Board:
        return Board(board=[[box.copy() for box in col] for col in self.board])


@dataclass
class Move:
    num_boxes: int
    col_from: int
    col_to: int


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    board = Board()
    moves = []
    with open(file_name) as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if line.startswith("move"):
                moves.append(Move(*get_ints(line)))
            elif line.startswith("["):
                for i, char in enumerate(line):
                    if char not in "[] ":
                        box_index = int(i / 4 + 3 / 4)
                        box = Box(name=char)
                        board.put_boxes(boxes=[box], col_to=box_index)
    board.flip_boxes()
    return board, moves


@timed
def part1(inputs: tuple[Board, list[Move]]) -> None:
    board, moves = inputs
    board = board.copy()
    for move in moves:
        for _ in range(move.num_boxes):
            boxes = board.take_boxes(num_boxes=1, col_from=move.col_from)
            board.put_boxes(boxes=boxes, col_to=move.col_to)
    print(board.get_top_boxes())


@timed
def part2(inputs: tuple[Board, list[Move]]) -> None:
    board, moves = inputs
    for move in moves:
        boxes = board.take_boxes(num_boxes=move.num_boxes, col_from=move.col_from)
        board.put_boxes(boxes=boxes, col_to=move.col_to)
    print(board.get_top_boxes())


if __name__ == "__main__":
    input_list = read()
    part1(input_list)
    part2(input_list)
