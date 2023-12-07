from __future__ import annotations
from functools import cache
import os
from dataclasses import dataclass, field
from pprint import pprint
from typing import Optional

from shared.gum import gum_choose
from shared.util import timed


@dataclass(eq=True)
class File:
    name: str
    size: int


@dataclass(unsafe_hash=True)
class Directory:
    name: str
    parent: Directory = field(default=None)
    sub_dirs: list[Directory] = field(default_factory=list, hash=False)
    files: list[File] = field(default_factory=list, hash=False)
    size: int = 0

    def __repr__(self) -> str:
        return str(
            {
                "name": self.name,
                "parent": self.parent.name if self.parent else None,
                "sub_dirs": [sub_dir.name for sub_dir in self.sub_dirs],
                "files": [f for f in self.files],
                "size": self.size,
            }
        )


@timed
def read() -> Directory:
    files = os.listdir(os.getcwd())
    _, file_name = gum_choose([f for f in files if f.endswith(".txt")])
    with open(file_name) as input_file:
        outputs = [line.strip() for line in input_file.readlines()]
        start_dir = Directory(name="/")
        curr_dir = start_dir
        for output in outputs:
            if output.startswith("$"):
                if "cd" in output:
                    _, _, dir_name = output.split()
                    if dir_name == "..":
                        curr_dir = curr_dir.parent
                    else:
                        curr_dir = next(
                            sub_dir
                            for sub_dir in curr_dir.sub_dirs
                            if sub_dir.name == dir_name
                        )
            elif output.startswith("dir"):
                _, dir_name = output.split()
                curr_dir.sub_dirs.append(Directory(name=dir_name, parent=curr_dir))
            else:
                size, file_name = output.split()
                curr_dir.files.append(File(name=file_name, size=int(size)))

        start_dir.size = calculate_dir_size(directory=start_dir)
    return start_dir


@timed
def part1(start_dir: Directory):
    print(find_sizes_under_100k(directory=start_dir))


def find_sizes_under_100k(directory: Directory) -> int:
    sizes_under_100k = 0
    if directory.size < 100000:
        sizes_under_100k += directory.size
    sizes_under_100k += sum(
        find_sizes_under_100k(sub_dir) for sub_dir in directory.sub_dirs
    )
    return sizes_under_100k


def calculate_dir_size(directory: Directory) -> int:
    for sub_dir in directory.sub_dirs:
        sub_dir.size = calculate_dir_size(directory=sub_dir)
    return sum(f.size for f in directory.files) + sum(
        sub_dir.size for sub_dir in directory.sub_dirs
    )


@timed
def part2(start_dir: Directory):
    total_disk_space = 70000000
    needed_disk_space = 30000000
    available_disk_space = total_disk_space - start_dir.size
    disk_space_to_free = needed_disk_space - available_disk_space
    print(
        find_minimum_dir(
            directory=start_dir,
            needed_disk_space=disk_space_to_free,
            curr_minimum=float("inf"),
        )
    )


def find_minimum_dir(
    directory: Directory, needed_disk_space: int, curr_minimum: int
) -> int:
    if needed_disk_space < directory.size < curr_minimum:
        curr_minimum = directory.size

    if minimum_sub_dir := [
        find_minimum_dir(sub_dir, needed_disk_space, curr_minimum)
        for sub_dir in directory.sub_dirs
    ]:
        curr_minimum = min(curr_minimum, *minimum_sub_dir)
    return curr_minimum


if __name__ == "__main__":
    output_list = read()
    part1(output_list)
    part2(output_list)
