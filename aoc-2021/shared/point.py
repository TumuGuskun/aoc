class Point:
    def __init__(self, x, y, v_x=0, v_y=0):
        self.x = x
        self.y = y

        self.v_x = v_x
        self.v_y = v_y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def is_valid(self, lower_x=0, lower_y=0, upper_x=None, upper_y=None):
        u_x = self.x <= upper_x if upper_x else True
        u_y = self.y <= upper_y if upper_y else True
        lowers = self.x >= lower_x and self.y >= lower_y
        return u_x and u_y and lowers

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

    def __lt__(self, other):
        return max(abs(self.x), abs(self.y)) < max(abs(other.x), abs(other.y))