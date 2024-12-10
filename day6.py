from typing import Literal

from util import Direction
from vector import Vector


with open("day6.txt") as f:
    puzzle = f.read()

facility = {}
guard_dir = Direction.UP
original_start_dir = Direction.UP
for y, row in enumerate(puzzle.splitlines()):
    for x, tile in enumerate(row):
        pos = Vector(x, y)
        if tile == "^":
            guard_pos = pos
            original_start_pos = guard_pos
            facility[pos] = "."
        else:
            facility[pos] = tile


def move_pos(v: Vector, dir: Direction) -> Vector:
    match dir:
        case Direction.UP:
            return Vector(v.x, v.y - 1)
        case Direction.DOWN:
            return Vector(v.x, v.y + 1)
        case Direction.LEFT:
            return Vector(v.x - 1, v.y)
        case Direction.RIGHT:
            return Vector(v.x + 1, v.y)


def walk(
    grid: dict[Vector, str],
    pos: Vector,
    dir: Direction,
    obstruction: Vector | None = None,
) -> (
    tuple[Literal["escaped"]]
    | tuple[Literal["turned"], Direction]
    | tuple[Literal["moved"], Vector]
):
    next_pos = move_pos(pos, dir)

    if next_pos not in grid:
        return ("escaped",)

    if grid[next_pos] == "#" or next_pos == obstruction:
        dir = dir.turn_right()
        return ("turned", dir)

    return ("moved", next_pos)


visited_locations = set([guard_pos])
while True:
    move = walk(facility, guard_pos, guard_dir)
    if move[0] == "escaped":
        break
    elif move[0] == "turned":
        guard_dir = move[1]
        continue
    elif move[0] == "moved":
        guard_pos = move[1]
        visited_locations.add(guard_pos)

print(f"Part 1: {len(visited_locations)} | expected 5086")

valid_obstructions = 0
for obstruction in visited_locations:
    if obstruction == original_start_pos:
        continue

    guard_pos = original_start_pos
    guard_dir = original_start_dir
    visited = set()
    while True:
        move = walk(facility, guard_pos, guard_dir, obstruction)
        match move[0]:
            case "escaped":
                break
            case "turned":
                guard_dir = move[1]
            case "moved":
                guard_pos = move[1]

        if (guard_pos, guard_dir) in visited:
            valid_obstructions += 1
            break
        visited.add((guard_pos, guard_dir))

print(f"Part 2: {valid_obstructions} | expected 1770")
