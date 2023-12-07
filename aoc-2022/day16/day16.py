from dataclasses import dataclass, field
import os
from queue import Queue
from typing import Set
from more_itertools import set_partitions
from multiprocessing import Pool

from shared.gum import gum_choose
from shared.util import timed, get_ints, get_caps


@dataclass(frozen=True, eq=True)
class Valve:
    name: str = field(hash=True, compare=True)
    flow_rate: int = field(hash=False, compare=False)
    neighbors: list[str] = field(hash=False, compare=False)


@timed
def read() -> dict[str, Valve]:
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    valves = {}
    with open(file_name) as input_file:
        for line in input_file.readlines():
            line = line[1:]
            flow_rate = get_ints(line).pop()
            curr_valve, *leads_to = get_caps(line)
            valves[curr_valve] = Valve(
                name=curr_valve,
                flow_rate=flow_rate,
                neighbors=leads_to,
            )
    return valves


@timed
def part1(valves: dict[str, Valve]) -> None:
    print(
        get_max_flow(
            valves=valves,
            valid_valves={valve for valve in valves.values()},
            end_time=30,
        )
    )


def get_max_flow(
    valves: dict[str, Valve], valid_valves: Set[Valve], end_time: int
) -> int:
    queue = Queue()

    valve_states = set()
    start_valve = valves["AA"]
    queue.put((set(), start_valve, 0, 0))
    max_flow = 0
    while not queue.empty():
        open_valves, curr_valve, time, total_flow = queue.get()

        if time == end_time:
            max_flow = max(total_flow, max_flow)
            continue

        total_flow += sum([valve.flow_rate for valve in open_valves])

        neighbors = [valves[neighbor] for neighbor in curr_valve.neighbors]
        if (
            curr_valve.flow_rate != 0
            and curr_valve in valid_valves
            and curr_valve not in open_valves
        ):
            new_open_valves = open_valves.copy()
            new_open_valves.add(curr_valve)
            valve_state = (
                curr_valve,
                "".join(
                    [
                        valve.name
                        for valve in sorted(new_open_valves, key=lambda v: v.name)
                    ]
                ),
            )
            valve_states.add(valve_state)
            queue.put((new_open_valves, curr_valve, time + 1, total_flow))
        for neighbor in neighbors:
            valve_state = (
                neighbor,
                "".join(
                    [valve.name for valve in sorted(open_valves, key=lambda v: v.name)]
                ),
            )
            if valve_state not in valve_states:
                queue.put((open_valves, neighbor, time + 1, total_flow))
                valve_states.add(valve_state)
    return max_flow


def run(
    valves: dict[str, Valve], my_valves: list[Valve], elephant_valves: list[Valve]
) -> int:
    my_flow = get_max_flow(valves=valves, valid_valves=set(my_valves), end_time=26)
    elephant_flow = get_max_flow(
        valves=valves, valid_valves=set(elephant_valves), end_time=26
    )
    return my_flow + elephant_flow


@timed
def part2(valves: dict[str, Valve]) -> None:
    partitions = set_partitions(
        [valve for valve in valves.values() if valve.flow_rate > 0], 2
    )
    pool = Pool(processes=32)
    results = [
        pool.apply_async(
            run,
            args=(
                valves,
                my_valves,
                elephant_valves,
            ),
        )
        for my_valves, elephant_valves in partitions
    ]
    pool.close()
    pool.join()
    print(max(result.get() for result in results))


if __name__ == "__main__":
    valve_list = read()
    part1(valve_list)
    part2(valve_list)
