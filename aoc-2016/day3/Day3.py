from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    triangles = []
    with open(file_name) as input_file:
        for line in input_file.readlines():
            triangle = tuple(map(int, line.split()))
            triangles.append(triangle)
    return triangles


@timed
def part1(triangles):
    print(sum(map(test_triangle, triangles)))


def test_triangle(triangle):
    a, b, c = triangle
    return (a + b > c) and (b + c > a) and (a + c > b)


@timed
def part2(triangles):
    i = 0
    triangle_1 = []
    triangle_2 = []
    triangle_3 = []
    new_triangles = []
    for a, b, c in triangles:
        if i == 3:
            new_triangles.append(triangle_1.copy())
            new_triangles.append(triangle_2.copy())
            new_triangles.append(triangle_3.copy())
            triangle_1 = [a]
            triangle_2 = [b]
            triangle_3 = [c]
            i = 1
        else:
            triangle_1.append(a)
            triangle_2.append(b)
            triangle_3.append(c)
            i += 1
    new_triangles.append(triangle_1.copy())
    new_triangles.append(triangle_2.copy())
    new_triangles.append(triangle_3.copy())
    print(sum(map(test_triangle, new_triangles)))


if __name__ == '__main__':
    triangle_list = read()
    part1(triangle_list)
    part2(triangle_list)
