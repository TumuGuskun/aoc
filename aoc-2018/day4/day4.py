import re
from collections import Counter, defaultdict
from datetime import datetime

from shared.Util import timed


@timed
def read():
    file_name = f'input{input("Input file #: ")}.txt'
    with open(file_name) as input_file:
        time_stamps = []
        for line in input_file.readlines():
            search = re.search(r'\[1518-(\d+)-(\d+) (\d+):(\d+)] (.*)', line)
            time = datetime(year=1518, month=int(search.group(1)), day=int(search.group(2)), hour=int(search.group(3)), minute=int(search.group(4)))
            time_stamps.append((time, search.group(5)))
        return time_stamps


@timed
def part1(times):
    counter = defaultdict(lambda: Counter())
    for time, action in sorted(times):
        if action.startswith('G'):
            guard = int(re.search(r'Guard #(\d+)', action).group(1))
        elif action.startswith('f'):
            sleep_start = time.minute
        else:
            for i in range(sleep_start, time.minute):
                counter[guard][i] += 1

    maximum = 0
    for guard, sleep_sched in counter.items():
        if (new_max := sum(sleep_sched.values())) > maximum:
            slep_guard = guard
            maximum = new_max

    print(slep_guard * counter[slep_guard].most_common(1).pop()[0])


@timed
def part2(times):
    counter = defaultdict(lambda: Counter())
    for time, action in sorted(times):
        if action.startswith('G'):
            guard = int(re.search(r'Guard #(\d+)', action).group(1))
        elif action.startswith('f'):
            sleep_start = time.minute
        else:
            for i in range(sleep_start, time.minute):
                counter[guard][i] += 1

    maximum = 0
    for guard, sleep_sched in counter.items():
        if (new_max := max(sleep_sched.values())) > maximum:
            slep_guard = guard
            maximum = new_max

    print(slep_guard * counter[slep_guard].most_common(1).pop()[0])


if __name__ == '__main__':
    time_list = read()
    part1(time_list)
    part2(time_list)
