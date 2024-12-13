from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache

from shared.util import get_ints, get_puzzle, run


@dataclass
class Record:
    potential_location_chunks: list[str]
    broken_spring_lengths: list[int]

    def __hash__(self) -> int:
        return hash(
            (
                tuple(self.potential_location_chunks),
                tuple(self.broken_spring_lengths),
            )
        )

    def copy(self) -> Record:
        return Record(
            potential_location_chunks=self.potential_location_chunks.copy(),
            broken_spring_lengths=self.broken_spring_lengths.copy(),
        )

    def drop_potential_spring(self) -> None:
        self.potential_location_chunks[0] = self.potential_location_chunks[0][1:]

    def use_potential_spring(self) -> None:
        self.potential_location_chunks[0] = "#" + self.potential_location_chunks[0][1:]


def use_all_possible(spring_chunk: str, length: int) -> tuple[bool, str, int]:
    valid = True
    while spring_chunk and length > 0:
        spring_chunk = spring_chunk[1:]
        length -= 1

    if not spring_chunk and length > 0:
        valid = False

    if length == 0:
        if spring_chunk.startswith("#"):
            valid = False

        if spring_chunk.startswith("?"):
            spring_chunk = spring_chunk[1:]

    return valid, spring_chunk, length


@lru_cache()
def get_possible_combinations(record: Record) -> int:
    if not record.potential_location_chunks and record.broken_spring_lengths:
        return 0

    if record.potential_location_chunks and not record.broken_spring_lengths:
        if any("#" in chunk for chunk in record.potential_location_chunks):
            return 0
        return 1

    if not record.potential_location_chunks and not record.broken_spring_lengths:
        return 1

    current_potential_chunk = record.potential_location_chunks[0]
    current_chunk_length = record.broken_spring_lengths[0]

    if len(current_potential_chunk) < current_chunk_length:
        if "#" in current_potential_chunk:
            return 0
        record.potential_location_chunks.pop(0)
        return get_possible_combinations(record)

    if current_potential_chunk.startswith("#"):
        valid, new_chunk, new_length = use_all_possible(
            current_potential_chunk, current_chunk_length
        )
        if not valid:
            return 0

        if new_length == 0:
            record.broken_spring_lengths.pop(0)
        else:
            record.broken_spring_lengths[0] = new_length

        if not new_chunk:
            record.potential_location_chunks.pop(0)
        else:
            record.potential_location_chunks[0] = new_chunk

        return get_possible_combinations(record)

    # lose it
    lost_record = record.copy()
    lost_record.drop_potential_spring()
    lose_it_count = get_possible_combinations(lost_record)

    # use it
    used_record = record.copy()
    used_record.use_potential_spring()
    use_it_count = get_possible_combinations(used_record)

    return lose_it_count + use_it_count


def parse_data(input_data: str) -> list[Record]:
    output = []
    for line in input_data.splitlines():
        locations, springs = line.split(" ")
        output.append(
            Record(
                potential_location_chunks=[
                    chunk for chunk in locations.split(".") if chunk
                ],
                broken_spring_lengths=get_ints(springs),
            )
        )

    return output


def parse_data_2(input_data: str) -> list[Record]:
    output = []
    for line in input_data.splitlines():
        locations, springs = line.split(" ")
        locations = "?".join([locations for _ in range(5)])
        springs = get_ints(springs) * 5
        output.append(
            Record(
                potential_location_chunks=[
                    chunk for chunk in locations.split(".") if chunk
                ],
                broken_spring_lengths=springs,
            )
        )

    return output


def part_1(records: list[Record]) -> int:
    return sum(get_possible_combinations(record) for record in records)


def part_2(records: list[Record]) -> int:
    return sum(get_possible_combinations(record) for record in records)


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(
        puzzle=puzzle,
        part_1=part_1,
        part_2=part_2,
        parser=parse_data,
        part_2_parser=parse_data_2,
    )


if __name__ == "__main__":
    main()
