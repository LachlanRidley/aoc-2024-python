from dataclasses import dataclass
from typing import Any
from util import Direction
from vector import Vector
from rich import print


with open("day12.txt") as f:
    puzzle = f.read()

grid = {}
for y, row in enumerate(puzzle.splitlines()):
    for x, plot in enumerate(row):
        grid[Vector(x, y)] = plot


def print_grid(cells, default_char=" "):
    minx = min(v.x for v in cells.keys())
    miny = min(v.y for v in cells.keys())
    maxx = max(v.x for v in cells.keys())
    maxy = max(v.y for v in cells.keys())

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print(cells.get(Vector(x, y), default_char), end="")
        print()


@dataclass
class Region:
    plots: set[Vector]


def flood_fill(grid: dict[Vector, Any], start: Vector) -> set[Vector]:
    candidates = set([start])
    flooded = set()
    while len(candidates) > 0:
        vec = candidates.pop()
        flooded.add(vec)
        neighbours = get_direct_neighbours(vec)
        neighbours.intersection_update(grid)
        neighbours.difference_update(flooded)
        neighbours = set(filter(lambda p: grid[start] == grid[p], neighbours))
        candidates.update(neighbours)

    return flooded


def measure_perimeter(grid: dict[Vector, Any], region: set[Vector]) -> int:
    perimeter = 0
    for plot in region:
        perimeter += len(
            [
                neighbour
                for neighbour in get_direct_neighbours(plot)
                if neighbour not in grid
                or grid[neighbour]
                != grid[
                    plot
                ]  # don't filter out neighbours not on the grid this time so that regions on the edge of the grid include perimeters at the borders
            ]
        )
    return perimeter


def remove_if_present(s: set[Any], key: Any) -> Any | None:
    try:
        s.remove(key)
    except KeyError:
        return None
    return key


def count_sides(grid: dict[Vector, Any], region: set[Vector]) -> int:
    # for each plot in the region add to a set its borders (Vector, Direction)
    borders = set()
    for plot in region:
        if bordering(grid, plot, Vector(plot.x - 1, plot.y)):
            borders.add((plot, Direction.LEFT))
        if bordering(grid, plot, Vector(plot.x + 1, plot.y)):
            borders.add((plot, Direction.RIGHT))
        if bordering(grid, plot, Vector(plot.x, plot.y - 1)):
            borders.add((plot, Direction.UP))
        if bordering(grid, plot, Vector(plot.x, plot.y + 1)):
            borders.add((plot, Direction.DOWN))

    # group the borders together:
    sides = 0
    while borders:
        #   pick a border
        borders_in_side = {borders.pop()}
        visited = set()
        #   find any borders that touch
        #   add them to unsearched borders
        #   keep going until there are no borders that could be part of that side
        while borders_in_side:
            plot, dir = borders_in_side.pop()
            visited.add((plot, dir))
            if dir in {Direction.LEFT, Direction.RIGHT}:
                if x := remove_if_present(borders, (Vector(plot[0], plot[1] - 1), dir)):
                    borders_in_side.add(x)
                if x := remove_if_present(borders, (Vector(plot[0], plot[1] + 1), dir)):
                    borders_in_side.add(x)
            else:
                if x := remove_if_present(borders, (Vector(plot[0] - 1, plot[1]), dir)):
                    borders_in_side.add(x)
                if x := remove_if_present(borders, (Vector(plot[0] + 1, plot[1]), dir)):
                    borders_in_side.add(x)
        #   We've found a side, increment and chuck all those borders out
        sides += 1
    #   keep going until we've chucked out every border
    return sides


def bordering(grid: dict[Vector, Any], a: Vector, b: Vector) -> bool:
    if b not in grid:
        return True

    return grid[a] != grid[b]


def get_direct_neighbours(v: Vector) -> set[Vector]:
    return {
        Vector(v.x - 1, v.y),
        Vector(v.x + 1, v.y),
        Vector(v.x, v.y - 1),
        Vector(v.x, v.y + 1),
    }


def find_regions(grid: dict[Vector, any]):
    unvisited_plots = set(grid.keys())
    regions = list()
    while len(unvisited_plots) > 0:
        plot = unvisited_plots.pop()
        region = flood_fill(grid, plot)
        unvisited_plots.difference_update(region)
        regions.append(region)
    return regions


regions = find_regions(grid)
part_1 = sum([measure_perimeter(grid, region) * len(region) for region in regions])
print(f"Part 1: {part_1}")

part_2 = 0
for i, region in enumerate(regions):
    part_2 += count_sides(grid, region) * len(region)
print(f"Part 2: {part_2}")
