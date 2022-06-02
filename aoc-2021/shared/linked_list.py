class LinkedList:
    def __init__(self, elements):
        tail = Node(elements[-1], None)
        next_node = tail
        for e in reversed(elements[:-1]):
            previous_node = Node(e, next_node)
            next_node = previous_node
        tail.set_next(next_node)

        self.head = next_node
        self.tail = tail

    def __repr__(self):
        curr = self.head
        output = []
        while curr != self.tail:
            output.append(curr)
            curr = curr.next_node
        output.append(curr)
        return f"{', '.join(map(str, output))}"


class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next_node = next_node

    def set_next(self, new_next):
        self.next_node = new_next

    def __repr__(self):
        return f'{self.value}'

    def __eq__(self, other):
        return self.value == other.value