from typing import Any, Literal

from shared.util import *


@dataclass
class Block:
    id: int | Literal["."]
    size: int

    def __repr__(self) -> str:
        return ", ".join([str(self.id)] * self.size)


def parse_data(input_data: str) -> Any:
    return [int(i) for i in input_data.strip()]


def checksum(disk_map: list[int | Literal["."]]) -> int:
    stripped_disk_map = [i for i in disk_map if i != "."]
    return sum(i * value for i, value in enumerate(stripped_disk_map))


def unpack(data: list[int]) -> list[int | Literal["."]]:
    output = []

    block_id = 0
    block = True
    for value in data:
        if block:
            output.extend([block_id] * value)
            block = False
            block_id += 1
        else:
            output.extend(["."] * value)
            block = True

    return output


def unpack_two(data: list[int]) -> list[Block]:
    output = []

    block_id = 0
    block = True
    for value in data:
        if block:
            if value > 0:
                output.append(Block(id=block_id, size=value))
            block = False
            block_id += 1
        else:
            if value > 0:
                output.append(Block(id=".", size=value))
            block = True

    return output


def sort_data_one(data: list[int | Literal["."]]) -> list[int | Literal["."]]:
    output = []

    for value in data:
        if value != ".":
            output.append(value)
            continue

        while data[-1] == ".":
            data.pop()

        output.append(data.pop())

    return output


def sort_data_two(data: list[Block]) -> list[Block]:
    value_blocks = sorted(
        [block for block in data if block.id != "."], key=lambda x: x.id, reverse=True
    )

    for value_block in value_blocks:
        for i, block in enumerate(data):
            if block.id != ".":
                continue

            if block.size < value_block.size:
                continue

            if i >= data.index(value_block):
                break

            new_dot_block = Block(id=".", size=block.size - value_block.size)
            data.pop(i)
            value_block_index = data.index(value_block)
            data[value_block_index] = Block(id=".", size=value_block.size)

            if new_dot_block.size > 0:
                data.insert(i, new_dot_block)

            data.insert(i, value_block)
            break

    return data


def checksum_two(data: list[Block]) -> int:
    index = 0
    checksum = 0

    for block in data:
        if block.id == ".":
            index += block.size
            continue
        for _ in range(block.size):
            checksum += index * block.id
            index += 1

    return checksum


def part_1(disk_map: list[int]) -> int:
    unpacked_data = unpack(disk_map)
    sorted_data = sort_data_one(unpacked_data)
    return checksum(sorted_data)


def part_2(disk_map: list[int]) -> int:
    unpacked_data = unpack_two(disk_map)
    sorted_data = sort_data_two(unpacked_data)
    return checksum_two(sorted_data)


def main() -> None:
    puzzle = get_puzzle(__file__)
    run(
        puzzle=puzzle,
        part_1=part_1,
        part_2=part_2,
        parser=parse_data,
    )


if __name__ == "__main__":
    main()
