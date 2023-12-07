from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from math import prod
import os

from shared.gum import gum_choose
from shared.util import timed, get_ints


@dataclass
class Monkey:
    monkey_id: int
    items: list[int]
    op_op: str
    op_num: int
    test_num: int
    true_monkey: int
    false_monkey: int
    inspected_count: int = 0

    def inspect(self) -> list[tuple[int, int]]:
        item_output = []
        for item in self.items:
            self.inspected_count += 1
            item = self.op(item)
            if self.test(item):
                item_output.append((item, self.true_monkey))
            else:
                item_output.append((item, self.false_monkey))
        self.items = []
        return item_output

    def throw_to(self, item: int, other: Monkey) -> None:
        other.items.append(item)

    def op(self, item: int) -> int:
        match self.op_op:
            case "+":
                return item + self.op_num
            case "^":
                return item**self.op_num
            case "*":
                return item * self.op_num
        return 0

    def test(self, item: int) -> bool:
        return item % self.test_num == 0

    def __copy__(self):
        return Monkey(
            monkey_id=self.monkey_id,
            items=self.items.copy(),
            op_op=self.op_op,
            op_num=self.op_num,
            test_num=self.test_num,
            true_monkey=self.true_monkey,
            false_monkey=self.false_monkey,
        )


@timed
def read():
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    monkeys = []
    with open(file_name) as input_file:
        monkey_id = 0
        items = []
        op_op = ""
        op_num = 0
        test_num = 0
        true_monkey = 0
        false_monkey = 0
        for line in input_file.readlines():
            line = line.strip()
            if not line:
                monkeys.append(
                    Monkey(
                        monkey_id=monkey_id,
                        items=items,
                        op_op=op_op,
                        op_num=op_num,
                        test_num=test_num,
                        true_monkey=true_monkey,
                        false_monkey=false_monkey,
                    )
                )
            elif line.startswith("Monkey"):
                monkey_id = get_ints(line).pop()
            elif line.startswith("Starting"):
                items = get_ints(line)
            elif line.startswith("Operation"):
                ints = get_ints(line)
                if not ints:
                    op_op = "^"
                    op_num = 2
                else:
                    op_num = ints.pop()
                    if "+" in line:
                        op_op = "+"
                    else:
                        op_op = "*"
            elif line.startswith("Test"):
                test_num = get_ints(line).pop()
            elif "true" in line:
                true_monkey = get_ints(line).pop()
            elif "false" in line:
                false_monkey = get_ints(line).pop()
    return monkeys


@timed
def part1(monkeys: list[Monkey]):
    for _ in range(20):
        for monkey in monkeys:
            inspected_items = monkey.inspect()
            for item, next_monkey in inspected_items:
                item //= 3
                monkey.throw_to(item, monkeys[next_monkey])
    monkeys.sort(key=lambda m: m.inspected_count, reverse=True)
    print(monkeys[0].inspected_count * monkeys[1].inspected_count)


@timed
def part2(monkeys: list[Monkey]):
    big_divisor = prod([monkey.test_num for monkey in monkeys])
    for _ in range(10000):
        for monkey in monkeys:
            inspected_items = monkey.inspect()
            for item, next_monkey in inspected_items:
                item %= big_divisor
                monkey.throw_to(item, monkeys[next_monkey])
    monkeys.sort(key=lambda m: m.inspected_count, reverse=True)
    print(monkeys[0].inspected_count * monkeys[1].inspected_count)


if __name__ == "__main__":
    monkey_list = read()
    part1(deepcopy(monkey_list))
    part2(deepcopy(monkey_list))
