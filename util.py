import enum
from typing import Any, Iterator, Self

from vector import Vector


class Tree[T]:
    value: T
    children: set[Self]

    def __init__(self, loc):
        self.value = loc
        self.children = set()


def window(li: list, size: int) -> Iterator[list[int]]:
    """Iterate through all sublists of a list"""
    for i in range(len(li) - size + 1):
        yield li[i : i + 2]


def between(lower: int, upper: int, number: int) -> bool:
    return lower <= number and number <= upper


def yoink(li: list, index: int) -> list:
    """Remove element at index and return the list (like pop but functional)"""
    return li[:index] + li[index + 1 :]


def in_bounds(grid: list[list], position: tuple[int, int]):
    row, col = position
    return row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])


def at_position(grid: list[list[str]], position: tuple[int, int]) -> str:
    row, col = position
    return grid[row][col]


def get_height(grid: dict[Vector, any]) -> int:
    return max([v.y for v in grid])


def get_width(grid: dict[Vector, any]) -> int:
    return max([v.x for v in grid])


def print_grid(grid: dict[Vector, Any]) -> None:
    for y in range(get_height(grid) + 1):
        for x in range(get_width(grid) + 1):
            print(grid[Vector(x, y)], end="")
        print()


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()

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


def move_pos(v: Vector, dir: Direction) -> Vector:
    match dir:
        case Direction.UP:
            return Vector(v[0], v[1] - 1)
        case Direction.DOWN:
            return Vector(v[0], v[1] + 1)
        case Direction.LEFT:
            return Vector(v[0] - 1, v[1])
        case Direction.RIGHT:
            return Vector(v[0] + 1, v[1])
