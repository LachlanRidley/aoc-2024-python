from rich import print
from typing import Dict, List
from util import find_shortest_path, make_empty_grid
from vector import Vector

with open("day18.txt") as f:
    puzzle = f.read()
size = 71
dropped = 1024

bytes = list()
for byte in puzzle.splitlines():
    x, y = byte.split(",")
    bytes.append(Vector(int(x), int(y)))


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

first_x_bytes = bytes[:dropped:]
grid = make_empty_grid(size, size)

for byte in first_x_bytes:
    grid[byte] = "#"

part_1 = find_shortest_path(grid, start_vec, end_vec)
print(f"Part 1: {part_1}")

grid = make_empty_grid(size, size)
part_2 = find_blocking_byte(bytes, grid, start_vec, end_vec)

print(f"Part 2: {part_2}")
