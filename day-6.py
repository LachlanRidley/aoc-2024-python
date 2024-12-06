from typing import Literal

from util import Direction, at_position, in_bounds, move_pos


with open("day-6.txt") as f:
    puzzle = f.read()


facility = [list(r) for r in puzzle.splitlines()]
guard_dir = Direction.UP
original_start_dir = Direction.UP
for i, row in enumerate(facility):
    for j, tile in enumerate(row):
        if tile == "^":
            guard_pos = (i, j)
            original_start_pos = guard_pos
            facility[i][j] = "."
            break


def walk(
    grid: list[list[str]],
    pos: tuple[int, int],
    dir: Direction,
    obstruction: tuple[int, int] | None = None,
) -> (
    tuple[Literal["escaped"]]
    | tuple[Literal["turned"], Direction]
    | tuple[Literal["moved"], tuple[int, int]]
):
    next_pos = move_pos(pos, dir)

    if not in_bounds(grid, next_pos):
        return ("escaped",)

    if at_position(grid, next_pos) == "#" or next_pos == obstruction:
        dir = dir.turn_right()
        return ("turned", dir)

    return ("moved", next_pos)


visited_tiles = set([guard_pos])
while True:
    move = walk(facility, guard_pos, guard_dir)
    if move[0] == "escaped":
        break
    elif move[0] == "turned":
        guard_dir = move[1]
        continue
    elif move[0] == "moved":
        guard_pos = move[1]
        visited_tiles.add(guard_pos)
visited = len(visited_tiles)

print(f"Part 1: {visited}")

valid_obstructions = 0
for obstruction in visited_tiles:
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

print(f"Part 2: {valid_obstructions}")
