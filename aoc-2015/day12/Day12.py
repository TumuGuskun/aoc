import json

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return json.load(input_file)


def sum_up(thing):
    if type(thing) is int:
        return thing
    elif type(thing) is str:
        return 0
    elif type(thing) is list:
        return sum(map(sum_up, thing))
    elif type(thing) is dict:
        return sum(map(sum_up, thing.values()))


@timed
def part1(documents):
    print(sum_up(documents))


def sum_up_red(thing):
    if type(thing) is int:
        return thing
    elif type(thing) is str:
        return 0
    elif type(thing) is list:
        return sum(map(sum_up_red, thing))
    elif type(thing) is dict:
        if 'red' in thing.values():
            return 0
        else:
            return sum(map(sum_up_red, thing.values()))


@timed
def part2(documents):
    print(sum_up_red(documents))


if __name__ == '__main__':
    document_list = read()
    part1(document_list)
    part2(document_list)
