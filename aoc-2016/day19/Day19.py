from shared.Util import timed, LinkedList


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        return int(input_file.read())


@timed
def part1_list(elves):
    elf_circle = range(1, elves + 1)
    while len(elf_circle) > 1:
        new_circle = elf_circle[::2]
        if len(elf_circle) % 2 == 0:
            elf_circle = new_circle
        else:
            elf_circle = new_circle[1:]
    print(list(elf_circle).pop())


@timed
def part2_list(elves):
    elf_circle = list(range(1, elves + 1))
    i = len(elf_circle) // 2
    first = False
    out = set()
    while len(elf_circle) - len(out) > 2:
        out.add(elf_circle[i])
        while elf_circle[i] in out:
            i = (i + 1) % len(elf_circle)
        if not first:
            i = (i + 1) % len(elf_circle)
            while elf_circle[i] in out:
                i = (i + 1) % len(elf_circle)
        elif i >= len(elf_circle):
            i %= len(elf_circle)
        first ^= True
    print(next(filter(lambda x: x not in out, elf_circle)))


@timed
def part1(elves):
    linked_list = LinkedList(list(range(1, elves + 1)))
    curr_node = linked_list.head
    while curr_node.next_node != curr_node:
        next_next_node = curr_node.next_node.next_node
        curr_node.next_node = next_next_node
        curr_node = next_next_node

    print(curr_node)


@timed
def part2(elves):
    linked_list = LinkedList(list(range(1, elves + 1)))
    halfway = elves // 2
    prev_node = linked_list.head

    for _ in range(halfway - 1):
        prev_node = prev_node.next_node

    first = False
    curr_node = prev_node.next_node
    while curr_node.next_node != curr_node:
        prev_node.next_node = curr_node.next_node
        if first:
            curr_node = curr_node.next_node
        else:
            prev_node = curr_node.next_node
            curr_node = curr_node.next_node.next_node

        first ^= True
    print(curr_node)


if __name__ == '__main__':
    elf_list = read()
    part1_list(elf_list)
    part2(elf_list)
