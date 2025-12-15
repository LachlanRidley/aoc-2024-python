from typing import Any, Dict, Iterator, List, Self, Type, TypeVar

from direction import Direction
from vector import Vector


class Tree[T]:
    value: T
    children: set[Self]

    def __init__(self, loc):
        self.value = loc
        self.children = set()


T = TypeVar("T")


def flatten(xss: List[List[Type[T]]]) -> List[T]:
    return [x for xs in xss for x in xs]


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


def make_empty_grid(width: int, height: int) -> Dict[Vector, str]:
    grid = {}
    for y in range(height):
        for x in range(width):
            v = Vector(int(x), int(y))
            grid[v] = "."
    return grid


def find_shortest_path(
    grid: Dict[Vector, str], start: Vector, end: Vector
) -> int | None:
    weights = {start: 0}
    unvisited_set = set([start])
    visited_set = set()

    while unvisited_set:
        next = min(unvisited_set, key=lambda x: weights[x])
        unvisited_set.remove(next)
        visited_set.add(next)
        neighbours = filter(
            lambda x: x in grid and grid[x] != "#", next.get_direct_neighbours()
        )
        for neighbour in neighbours:
            new_weight = weights[next] + 1
            if neighbour not in weights or new_weight < weights[neighbour]:
                weights[neighbour] = weights[next] + 1
                unvisited_set.add(neighbour)

    if end in visited_set:
        return weights[end]
    else:
        return None
