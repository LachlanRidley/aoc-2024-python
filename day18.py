from rich import print
from typing import Dict, List
from vector import Vector

with open("day18.txt") as f:
    puzzle = f.read()
size = 71
dropped = 1024

bytes = list()
for byte in puzzle.splitlines():
    x, y = byte.split(",")
    bytes.append(Vector(int(x), int(y)))

grid = {}
first_x_bytes = bytes[:dropped:]
for y in range(size):
    for x in range(size):
        v = Vector(int(x), int(y))
        if v in first_x_bytes:
            grid[v] = "#"
        else:
            grid[v] = "."


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


def find_blocking_byte(
    bytes: List[Vector], grid: Dict[Vector, str], start: Vector, end: Vector
) -> Vector | None:
    for byte in bytes:
        grid[byte] = "#"
        path = find_shortest_path(grid, start, end)
        if path is None:
            return byte
    return None


start_vec = Vector(0, 0)
end_vec = Vector(size - 1, size - 1)

part_1 = find_shortest_path(grid, start_vec, end_vec)
print(f"Part 1: {part_1}")

grid = make_empty_grid(size, size)
part_2 = find_blocking_byte(bytes, grid, start_vec, end_vec)

print(f"Part 2: {part_2}")
