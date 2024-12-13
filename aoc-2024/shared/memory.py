from __future__ import annotations
import re
from typing import Any, Callable, Optional, Protocol

from shared.util import get_ints


class Command(Protocol):
    regex: str
    arg_parser: Optional[Callable] = None

    def execute(self, computer: Optional[Computer] = None) -> Any: ...


class Mul:
    regex: str = r"mul\(\d+,\d+\)"
    arg_parser: Callable = get_ints

    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def execute(self) -> int:
        return self.a * self.b


class Do:
    regex: str = r"do\(\)"
    arg_parser: None = None

    def execute(self, computer: Computer) -> None:
        computer.active = True


class Dont:
    regex: str = r"don\'t\(\)"
    arg_parser: None = None

    def execute(self, computer: Computer) -> None:
        computer.active = False


ALL_COMMANDS = [Mul, Do, Dont]


class Computer:
    commands: list[Command]
    env: dict[str, Any]
    active: bool
    disabled_commands: list[type]

    def __init__(
        self,
        corrupted_memory: str,
    ) -> None:
        self.env = {}
        self.active = True
        self.disabled_commands = []
        self.commands = []
        self.load(corrupted_memory)

    def load(self, memory: str) -> None:

        str_commands = re.findall(r"|".join([c.regex for c in ALL_COMMANDS]), memory)

        for str_command in str_commands:
            for command in ALL_COMMANDS:
                if re.match(command.regex, str_command):
                    if command.arg_parser:
                        args = command.arg_parser(str_command)
                        self.commands.append(command(*args))
                    else:
                        self.commands.append(command())

    def run(self) -> Any:
        count = 0
        for command in self.commands:
            if isinstance(command, tuple(self.disabled_commands)):
                continue

            if isinstance(command, (Do, Dont)):
                command.execute(computer=self)
                continue

            if self.active:
                if isinstance(command, Mul):
                    count += command.execute()

        return count

    def disable_command(self, command: type) -> None:
        self.disabled_commands.append(command)

    def __repr__(self) -> str:
        return f"""Computer(
    commands            ={self.commands[:3]}...,
    env                 ={self.env}
    active              ={self.active},
    disabled_commands   ={self.disabled_commands}
)"""
