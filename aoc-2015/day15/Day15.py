import numpy as np

from itertools import product

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    ingredients = {}
    with open(file_name) as input_file:
        for line in input_file.readlines():
            name, attributes = line.split(': ')
            ingredients[name] = np.array(list(map(lambda x: int(x.split(' ')[1]), attributes.split(', '))))

    ingredients_array = np.column_stack(list(ingredients.values()))
    return ingredients_array


@timed
def part1(ingredients):
    maximum = 0

    combinations = product(*[range(101)] * len(ingredients[0]))
    combinations = (c for c in combinations if sum(c) == 100)

    for combination in combinations:
        result_arr = np.matmul(ingredients, np.array(combination))
        result_non_zero = np.where(result_arr < 0, 0, result_arr)
        maximum = max(maximum, np.prod(result_non_zero[:-1]))
    print(maximum)


@timed
def part2(ingredients):
    maximum = 0

    combinations = product(*[range(101)] * len(ingredients[0]))
    combinations = (c for c in combinations if sum(c) == 100)

    for combination in combinations:
        result_arr = np.matmul(ingredients, np.array(combination))
        result_non_zero = np.where(result_arr < 0, 0, result_arr)
        if result_non_zero[-1] == 500:
            maximum = max(maximum, np.prod(result_non_zero[:-1]))
    print(maximum)


if __name__ == '__main__':
    ingredient_list = read()
    part1(ingredient_list)
    part2(ingredient_list)
