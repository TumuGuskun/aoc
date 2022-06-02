from collections import Counter
from shared.Util import timed

BAD_STRINGS = ['ab', 'cd', 'pq', 'xy']
VOWELS = 'aeiou'


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return input_file.readlines()


def vowel_count(string):
    counted = Counter(string)
    return sum(counted[vowel] for vowel in VOWELS) > 2


def double_letter(string):
    previous = None
    doubled = False
    for letter in string:
        if letter == previous:
            return True
        else:
            previous = letter
    return False


def no_bad_string(string):
    return all(substring not in string for substring in BAD_STRINGS)


@timed
def part1(strings):
    print(sum(vowel_count(string) and double_letter(string) and no_bad_string(string) for string in strings))


def two_letter_pair(string):
    for i in range(len(string) - 2):
        if string[i:i+2] in string[i+2:]:
            return True
    return False


def sandwich(string):
    for i in range(len(string) - 2):
        if string[i] == string[i+2]:
            return True
    return False


@timed
def part2(strings):
    print(sum(two_letter_pair(string) and sandwich(string) for string in strings))


if __name__ == '__main__':
    string_list = read()
    part1(string_list)
    part2(string_list)
