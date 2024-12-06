import enum


# puzzle = """....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#..."""
with open("day-6.txt") as f:
    puzzle = f.read()


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


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


def in_bounds(grid, row, col):
    return row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])


def print_grid(grid):
    for row in grid:
        print("".join(row))


def walk(grid, pos, dir, start_pos, start_dir, obstruction, steps):
    if steps > 0 and pos == start_pos and dir == start_dir:
        return "in loop"

    next_pos = pos
    if dir == Direction.UP:
        next_pos = (pos[0] - 1, pos[1])
    elif dir == Direction.DOWN:
        next_pos = (pos[0] + 1, pos[1])
    elif dir == Direction.LEFT:
        next_pos = (pos[0], pos[1] - 1)
    elif dir == Direction.RIGHT:
        next_pos = (pos[0], pos[1] + 1)

    if not in_bounds(grid, *next_pos):
        return "escaped"

    if grid[next_pos[0]][next_pos[1]] == "#" or next_pos == obstruction:
        if dir == Direction.UP:
            dir = Direction.RIGHT
        elif dir == Direction.RIGHT:
            dir = Direction.DOWN
        elif dir == Direction.DOWN:
            dir = Direction.LEFT
        elif dir == Direction.LEFT:
            dir = Direction.UP
        return ("turned", dir)

    return ("moved", next_pos)


visited_tiles = set([guard_pos])
steps = 0
while True:
    move = walk(facility, guard_pos, guard_dir, None, None, None, steps)
    steps += 1
    if move == "escaped":
        break
    elif move == "in loop":
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
for i, row in enumerate(facility):
    for j, tile in enumerate(row):
        if tile != ".":
            continue
        obstruction = (i, j)

        if obstruction == original_start_pos:
            # print("skipping start pos", obstruction)
            continue
        # print("checking with obstruction", obstruction)
        guard_pos = original_start_pos
        guard_dir = original_start_dir
        steps = 0
        visited = set()
        while True:
            move = walk(
                facility,
                guard_pos,
                guard_dir,
                original_start_pos,
                original_start_dir,
                obstruction,
                steps,
            )
            steps += 1
            if move == "escaped":
                # print("damn, escaped!")
                break
            elif move == "in loop":
                # print("trapped in loop, success!")
                valid_obstructions += 1
                break
            elif move[0] == "turned":
                guard_dir = move[1]
                continue
            elif move[0] == "moved":
                guard_pos = move[1]
                # visited_tiles.add(guard_pos)
            if steps > 10000:
                print("> 10000 steps, giving up")
                break
            if (guard_pos, guard_dir) in visited:
                # print("trapped in loop, success!")
                valid_obstructions += 1
                break
            visited.add((guard_pos, guard_dir))

print(f"Part 2: {valid_obstructions}")
