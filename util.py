import enum
from typing import Iterator


def window(l: list, size: int) -> Iterator[list[int]]:
    """Iterate through all sublists of a list"""
    for i in range(len(l) - size + 1):
        yield l[i : i + 2]


def between(lower: int, upper: int, number: int) -> bool:
    return lower <= number and number <= upper


def yoink(l: list, index: int) -> list:
    """Remove element at index and return the list (like pop but functional)"""
    return l[:index] + l[index + 1 :]


def in_bounds(grid: list[list], position: tuple[int, int]):
    row, col = position
    return row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])


def at_position(grid: list[list[str]], position: tuple[int, int]) -> str:
    row, col = position
    return grid[row][col]


def print_grid(grid):
    for row in grid:
        print("".join(row))


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


def move_pos(position: tuple[int, int], dir: Direction) -> tuple[int, int]:
    match dir:
        case Direction.UP:
            return (position[0] - 1, position[1])
        case Direction.DOWN:
            return (position[0] + 1, position[1])
        case Direction.LEFT:
            return (position[0], position[1] - 1)
        case Direction.RIGHT:
            return (position[0], position[1] + 1)
