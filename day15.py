from typing import Dict, Set
from util import Direction, move_pos, print_grid
from vector import Vector
from rich import print


with open("day15.txt") as f:
    puzzle = f.read()

room, program = puzzle.split("\n\n")

grid = {}
robot = Vector(0, 0)
for y, line in enumerate(room.split("\n")):
    for x, tile in enumerate(line):
        if tile == "@":
            robot = Vector(x, y)
            grid[Vector(x, y)] = "."
        else:
            grid[Vector(x, y)] = tile

directions = list(map(Direction.from_str, list(program.replace("\n", ""))))


def find_boxes_to_shift(
    grid: Dict[Vector, str], start_pos: Vector, direction: Direction
) -> list[Vector] | None:
    boxes_to_shift = list()
    push_path = start_pos
    while push_path in grid:
        if grid[push_path] in ("O", "[", "]"):
            boxes_to_shift.append(push_path)
        elif grid[push_path] == ".":
            break
        elif grid[push_path] == "#":
            return None
        push_path = move_pos(push_path, direction)

    return boxes_to_shift


def find_double_boxes_to_shift(
    grid: Dict[Vector, str], start_pos: Vector, direction: Direction
) -> Set[Vector] | None:
    if direction in (Direction.LEFT, Direction.RIGHT):
        # when going horizontal, then we can follow the same logic as before
        return find_boxes_to_shift(grid, start_pos, direction)
    boxes_to_shift = set()
    push_paths = set([start_pos])
    while push_paths:
        push_path = push_paths.pop()

        if push_path not in grid or grid[push_path] == ".":
            continue

        locations_to_shift = set()
        if grid[push_path] == "[":
            locations_to_shift.add(push_path)
            locations_to_shift.add(move_pos(push_path, Direction.RIGHT))
        elif grid[push_path] == "]":
            locations_to_shift.add(move_pos(push_path, Direction.LEFT))
            locations_to_shift.add(push_path)
        elif grid[push_path] == "#":
            # there's a wall in the way, this isn't a valid push
            return None

        boxes_to_shift = boxes_to_shift.union(locations_to_shift)

        for location in locations_to_shift:
            if grid[location] == ".":
                # the block can shift into this location and won't push anything
                continue
            elif grid[location] in ("[", "]"):
                # there's a block where we're moving so we need to check that it can shift on the next layer
                push_paths.add(move_pos(location, direction))
            elif grid[location] == "#":
                # if it's a wall, then we can't shift the boxes
                return None

    return boxes_to_shift


def shift_boxes(
    grid: Dict[Vector, str], boxes_to_shift: list[Vector], direction: Direction
):
    updated_locs = {}
    for box_to_shift in boxes_to_shift:
        updated_locs[move_pos(box_to_shift, direction)] = grid[box_to_shift]
        grid[box_to_shift] = "."
    for new_location, tile in updated_locs.items():
        grid[new_location] = tile


def sum_gps_coordinates(grid: Dict[Vector, str]) -> int:
    coords = 0
    for pos, tile in grid.items():
        if tile in ("O", "["):
            coords += pos.y * 100 + pos.x
    return coords


for direction in directions:
    new_robot_pos = move_pos(robot, direction)
    if new_robot_pos not in grid or grid[new_robot_pos] == "#":
        continue
    if grid[new_robot_pos] == "O":
        boxes_to_shift = find_boxes_to_shift(grid, new_robot_pos, direction)
        if boxes_to_shift:
            shift_boxes(grid, boxes_to_shift, direction)
            robot = new_robot_pos
    if grid[new_robot_pos] == ".":
        robot = new_robot_pos


part_1 = sum_gps_coordinates(grid)
print_grid({**grid, robot: "@"})
print(f"Part 1: {part_1} (which is{"" if part_1 == 1559280 else " not"} 1559280)")

double_grid = {}
robot = Vector(0, 0)
for y, line in enumerate(room.split("\n")):
    for x, tile in enumerate(line):
        v = Vector(x * 2, y)
        v1 = Vector(x * 2 + 1, y)
        if tile == "@":
            robot = v
            double_grid[v] = "."
            double_grid[v1] = "."
        elif tile == "O":
            double_grid[v] = "["
            double_grid[v1] = "]"
        else:
            double_grid[v] = tile
            double_grid[v1] = tile


for direction in directions:
    new_robot_pos = move_pos(robot, direction)

    if new_robot_pos not in double_grid or double_grid[new_robot_pos] == "#":
        continue
    elif double_grid[new_robot_pos] in ("[", "]"):
        boxes_to_shift = find_double_boxes_to_shift(
            double_grid, new_robot_pos, direction
        )
        if boxes_to_shift:
            shift_boxes(double_grid, boxes_to_shift, direction)
            robot = new_robot_pos
    else:
        robot = new_robot_pos


part_2 = sum_gps_coordinates(double_grid)
print_grid({**double_grid, robot: "@"})
print(f"Part 2: {part_2}")
