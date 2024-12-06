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


grid = [list(r) for r in puzzle.splitlines()]
dir = Direction.UP
for i, row in enumerate(grid):
    for j, tile in enumerate(row):
        if tile == "^":
            guard = (i, j)
            grid[i][j] = "."


def in_bounds(grid, row, col):
    return row >= 0 and col >= 0 and row < len(grid) and col < len(grid[0])


def print_grid(grid):
    for row in grid:
        print("".join(row))


grid[guard[0]][guard[1]] = "X"
while True:
    if dir == Direction.UP:
        next_pos = (guard[0] - 1, guard[1])
    elif dir == Direction.DOWN:
        next_pos = (guard[0] + 1, guard[1])
    elif dir == Direction.LEFT:
        next_pos = (guard[0], guard[1] - 1)
    elif dir == Direction.RIGHT:
        next_pos = (guard[0], guard[1] + 1)

    if not in_bounds(grid, *next_pos):
        break

    next_tile = grid[next_pos[0]][next_pos[1]]

    if next_tile == "#":
        if dir == Direction.UP:
            dir = Direction.RIGHT
        elif dir == Direction.RIGHT:
            dir = Direction.DOWN
        elif dir == Direction.DOWN:
            dir = Direction.LEFT
        elif dir == Direction.LEFT:
            dir = Direction.UP
    else:
        grid[next_pos[0]][next_pos[1]] = "X"
        guard = next_pos

visited = 0
for row in grid:
    for tile in row:
        if tile == "X":
            visited += 1

print(f"Part 1: {visited}")
