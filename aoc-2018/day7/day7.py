import re
from collections import defaultdict

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        edges = defaultdict(list)
        for line in input_file.readlines():
            node_a, node_b = re.search(r'Step (\w) must be finished before step (\w)', line).group(1, 2)
            edges[node_a].append(node_b)
        return edges


@timed
def part1(edges):
    queue = {node for node in edges.keys() if all(node not in d for d in edges.values())}
    output = ''
    finished = set()
    while len(queue) > 0:
        for e in sorted(queue, reverse=True):
            if all(node in finished for node, d in edges.items() if e in d):
                min_node = e
        finished.add(min_node)
        queue.remove(min_node)
        output += min_node
        for neighbor in edges[min_node]:
            if neighbor not in queue and neighbor not in finished:
                queue.add(neighbor)
    print(output)


@timed
def part2(edges):
    queue = {node for node in edges.keys() if all(node not in d for d in edges.values())}
    output = ''
    finished = set()

    workers = [Worker() for _ in range(5)]
    time = 0
    while len(queue) > 0:
        for worker in workers:
            if worker.available:
                for e in sorted(queue, reverse=True):
                    if all(node in finished for node, d in edges.items() if e in d):
                        worker.take_task(e)
                        queue.remove(e)
                        break

        print(workers)
        next_time_step = min(worker.time_left for worker in workers if not worker.available)
        time += next_time_step
        for worker in workers:
            worker.spend_time(next_time_step)

        for worker in workers:
            if worker.time_left == 0 and not worker.available:
                finished_task = worker.finish_task()
                finished.add(finished_task)
                output += finished_task

                for neighbor in edges[finished_task]:
                    if neighbor not in queue and neighbor not in finished:
                        queue.add(neighbor)

    print(time)


class Worker:
    def __init__(self):
        self.task = 'idle'
        self.time_left = 0
        self.available = True

    def take_task(self, task):
        self.task = task
        self.time_left = 60 + ord(task) - 64
        self.available = False

    def spend_time(self, time):
        if self.time_left > 0:
            self.time_left -= time

    def finish_task(self):
        task, self.task = self.task, 'idle'
        self.available = True
        return task

    def __repr__(self):
        return f'{self.task:>6}: {self.time_left:<2}'


if __name__ == '__main__':
    edge_list = read()
    part1(edge_list)
    part2(edge_list)
