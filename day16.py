from typing import Dict, Set, Tuple

from networkx import all_shortest_paths, shortest_path_length
from util import Direction, flatten
from vector import Vector
from rich import print
import networkx as nx

with open("day16.txt") as f:
    puzzle = f.read()

grid = {}
reindeer = (Vector(0, 0), Direction.RIGHT)
end = Vector(0, 0)
for y, line in enumerate(puzzle.split("\n")):
    for x, tile in enumerate(line):
        if tile == "S":
            reindeer = (Vector(x, y), Direction.RIGHT)
            grid[Vector(x, y)] = "."
        elif tile == "E":
            end = Vector(x, y)
            grid[Vector(x, y)] = "."
        else:
            grid[Vector(x, y)] = tile


def get_available_moves(
    grid: Dict[Vector, str], location: Vector, facing: Direction
) -> Set[Tuple[Vector, Direction]]:
    moves = set()

    location_after_move = location + facing
    if grid[location_after_move] == ".":
        moves.add((location_after_move, facing))

    moves.add((location, facing.turn_left()))
    moves.add((location, facing.turn_right()))

    return moves


G = nx.DiGraph()
for node in grid.keys():
    for direction in Direction:
        if grid[node] == "#":
            continue
        moves = get_available_moves(grid, node, direction)
        for move in moves:
            cost = 1 if move[0] != node else 1000
            G.add_edge((node, direction), move, weight=cost)

nx_length = min(
    shortest_path_length(
        G,
        source=reindeer,
        target=(end, direction),
        weight="weight",
    )
    for direction in Direction
)

print(f"Part 1: {nx_length}")

all_paths = all_shortest_paths(
    G,
    source=reindeer,
    target=(
        end,
        Direction.UP,
    ),  # UP is arbitrary, we only care about visited nodes rather than the cost so spinning on the end position won't affect the result
    weight="weight",
    method="bellman-ford",
)
unique_nodes_on_shortest_path: Set[Vector] = set(
    [node[0] for node in flatten(all_paths)]
)
print(f"Part 2: {len(unique_nodes_on_shortest_path)}")
