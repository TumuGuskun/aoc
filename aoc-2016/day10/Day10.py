import re
from collections import Counter
from queue import Queue

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        start_values = []
        bot_instructions = {}
        for line in input_file.readlines():
            if line.startswith('v'):
                value, bot = map(int, re.findall(r'\d+', line))
                start_values.append((value, bot))
            else:
                start_bot, outputs = line[4:].split(' gives low to ')
                output_1, output_2 = outputs.split(' and high to ')
                output_1 = (output_1.split()[0], int(output_1.split()[1]))
                output_2 = (output_2.split()[0], int(output_2.split()[1]))
                bot_instructions[int(start_bot)] = {'low': output_1, 'high': output_2}

        return start_values, bot_instructions


class Bot:
    def __init__(self, tag, val_1=None, val_2=None):
        self.tag = tag
        if val_2:
            if val_1 > val_2:
                self.upper = val_1
                self.lower = val_2
            else:
                self.lower = val_1
                self.upper = val_2
        elif val_1:
            self.upper = val_1
            self.lower = None

    def add(self, val):
        if self.upper and self.lower:
            raise Exception('tonto')
        else:
            if val > self.upper:
                self.lower = self.upper
                self.upper = val
            else:
                self.lower = val

    def is_full(self):
        return self.upper and self.lower

    def __eq__(self, other):
        return self.tag == other.tag

    def __repr__(self):
        return f'(Bot: {self.tag}, Upper: {self.upper}, Lower: {self.lower})'


@timed
def part1(start_values, instructions):
    queue = Queue()
    seen = set()
    for value, bot_tag in start_values:
        if bot_tag not in seen:
            queue.put(Bot(bot_tag, value))
            seen.add(bot_tag)
        else:
            for bot in queue.queue:
                if bot.tag == bot_tag:
                    bot.add(value)
                    break
    outputs = {}
    while not queue.empty():
        curr_bot = queue.get()
        if curr_bot.is_full():
            if curr_bot.upper == 61 and curr_bot.lower == 17:
                print(curr_bot.tag)

            up_type, up_tag = instructions[curr_bot.tag]['high']
            low_type, low_tag = instructions[curr_bot.tag]['low']

            if up_type == 'output':
                outputs[up_tag] = curr_bot.upper
            else:
                found = False
                for bot in queue.queue:
                    if bot.tag == up_tag:
                        bot.add(curr_bot.upper)
                        found = True
                        break
                if not found:
                    queue.put(Bot(up_tag, curr_bot.upper))

            if low_type == 'output':
                outputs[low_tag] = curr_bot.lower
            else:
                found = False
                for bot in queue.queue:
                    if bot.tag == low_tag:
                        bot.add(curr_bot.lower)
                        found = True
                        break
                if not found:
                    queue.put(Bot(low_tag, curr_bot.lower))
        else:
            queue.put(curr_bot)
    return outputs


@timed
def part2(outputs):
    print(outputs[0] * outputs[1] * outputs[2])


if __name__ == '__main__':
    start_value_list, instruction_list = read()
    output_list = part1(start_value_list, instruction_list)
    part2(output_list)
