from shared.point import Point

DIR_MAP = {
    '↑': {
        '→': '→',
        '←': '←',
        'vec': Point(-1, 0)
    },
    '↓': {
        '→': '←',
        '←': '→',
        'vec': Point(1, 0)
    },
    '←': {
        '→': '↑',
        '←': '↓',
        'vec': Point(0, -1)
    },
    '→': {
        '→': '↓',
        '←': '↑',
        'vec': Point(0, 1)
    },
}


class Vector:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction

    def rotate_r(self):
        self.direction = DIR_MAP[self.direction]['→']

    def rotate_l(self):
        self.direction = DIR_MAP[self.direction]['←']

    def flip(self):
        self.rotate_l()
        self.rotate_l()

    def move(self, num=1):
        for _ in range(num):
            self.point += DIR_MAP[self.direction]['vec']

    def __hash__(self):
        return hash(self.point) + hash(self.direction)

    def __eq__(self, other):
        return self.point == other.point and self.direction == other.direction

    def __str__(self):
        return f'{self.point} {self.direction}'

    def __repr__(self):
        return f'{self.point} {self.direction}'
