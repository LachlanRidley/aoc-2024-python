import enum
from typing import Self


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

    def turn_left(self):
        match self:
            case Direction.UP:
                return Direction.LEFT
            case Direction.RIGHT:
                return Direction.UP
            case Direction.DOWN:
                return Direction.RIGHT
            case Direction.LEFT:
                return Direction.DOWN

    def turn_right(self):
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP

    @classmethod
    def from_str(cls, s: str) -> Self:
        match s:
            case "^":
                return Direction.UP
            case "v":
                return Direction.DOWN
            case ">":
                return Direction.RIGHT
            case "<":
                return Direction.LEFT
        raise RuntimeError(f"invalid direction string = {s}")

    def to_str(self) -> str:
        match self:
            case Direction.UP:
                return "^"
            case Direction.DOWN:
                return "v"
            case Direction.RIGHT:
                return ">"
            case Direction.LEFT:
                return "<"
