from util import Tree, in_bounds


with open("day10.txt") as f:
    puzzle = f.read()


grid = [list(map(int, list(row))) for row in puzzle.splitlines()]

trailheads = set()
for row, line in enumerate(grid):
    for col, loc in enumerate(line):
        if loc == 0:
            trailheads.add((row, col))


def get_candidate_neighbours(
    loc: tuple[int, int],
    grid: list[list[tuple[int, int]]],
    visited: set[tuple[int, int]],
) -> list[tuple[int, int]]:
    height = grid[loc[0]][loc[1]]
    neighbours = [
        (loc[0] - 1, loc[1]),
        (loc[0] + 1, loc[1]),
        (loc[0], loc[1] - 1),
        (loc[0], loc[1] + 1),
    ]
    neighbours = list(filter(lambda n: in_bounds(grid, n), neighbours))
    neighbours = list(filter(lambda n: n not in visited, neighbours))
    neighbours = list(filter(lambda n: grid[n[0]][n[1]] - height == 1, neighbours))
    return neighbours


scores = list()
for trailhead in trailheads:
    visited = set()
    candidates = set([trailhead])

    while len(candidates) > 0:
        next = candidates.pop()
        candidates.update(get_candidate_neighbours(next, grid, visited))
        visited.add(next)
    peaks = sum([grid[x[0]][x[1]] == 9 for x in visited])
    scores.append(peaks)

print(f"Part 1: {sum(scores)}")


def build_tree(
    loc: tuple[int, int],
    visited: set[tuple[int, int]],
    grid: list[list[tuple[int, int]]],
) -> Tree:
    candidates = get_candidate_neighbours(loc, grid, visited)
    tree = Tree(loc)
    for candidate in candidates:
        sub_tree = build_tree(candidate, visited.union(loc), grid)
        tree.children.add(sub_tree)
    return tree


def count_trails(tree: Tree, depth: int):
    loc = tree.value
    if grid[loc[0]][loc[1]] == 9:
        return 1

    return sum([count_trails(walk, depth + 1) for walk in tree.children])


combined_ratings = 0
for trailhead in trailheads:
    trails = build_tree(trailhead, set(), grid)
    combined_ratings += count_trails(trails, 0)

print(f"Part 2: {combined_ratings}")
