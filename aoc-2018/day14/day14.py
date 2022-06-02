from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return int(input_file.read())


@timed
def part1(rounds):
    recipes = [3, 7]
    elf_1, elf_2 = 0, 1

    while len(recipes) < rounds + 10:
        recipe_1, recipe_2 = recipes[elf_1], recipes[elf_2]
        recipes.extend(list(map(int, str(recipe_1 + recipe_2))))
        elf_1 = (elf_1 + recipe_1 + 1) % len(recipes)
        elf_2 = (elf_2 + recipe_2 + 1) % len(recipes)

    print(''.join(list(map(str, recipes[rounds:rounds + 10]))))


@timed
def part2(rounds):
    recipes = [3, 7]
    elf_1, elf_2 = 0, 1

    rounds = list(map(int, str(rounds)))
    while recipes[-len(rounds):] != rounds and recipes[-len(rounds) - 1:-1] != rounds:
        recipe_1, recipe_2 = recipes[elf_1], recipes[elf_2]
        recipes.extend(list(map(int, str(recipe_1 + recipe_2))))
        elf_1 = (elf_1 + recipe_1 + 1) % len(recipes)
        elf_2 = (elf_2 + recipe_2 + 1) % len(recipes)

    print(len(recipes) - len(rounds))


if __name__ == '__main__':
    round_list = read()
    part1(round_list)
    part2(round_list)
