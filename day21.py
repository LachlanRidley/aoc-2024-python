import functools
from typing import Dict, List, Set
from util import Direction, window
from vector import Vector
from rich import print


def key_by_value(dic, value):
    for k, v in dic.items():
        if v == value:
            return k
    return None


type Grid = Dict[Vector, str]


def find_shortest_path(grid: Grid, start: str, end: str) -> List[Direction]:
    # TODO rework this, you don't need pathfinding this complicated
    #      to reduce pressing "A", you want to line up one axis then go straight to the button
    #      The only real wrinkle is that when lining up you don't want to go through the void
    #      So some trick will be needed there. Otherwise it's straightforward

    # something along the lines of
    # pick arbitrarily line up horizontal or vertically first
    # check that lines don't go over void
    # if they do, switch to whichever route you didn't pick at first
    # done!

    if start == end:
        return []
    start_vec = key_by_value(grid, start)
    end_vec = key_by_value(grid, end)
    weights = {start_vec: (0, [])}
    unvisited_set = set([start_vec])
    visited_set = set()

    while unvisited_set:
        next = min(unvisited_set, key=lambda x: weights[x][0])
        unvisited_set.remove(next)
        visited_set.add(next)
        neighbours = available_moves(grid, next)
        for neighbour in neighbours:
            new_weight = (
                weights[next][0] + 1,
                [*weights[next][1], next.get_direction_between(neighbour)],
            )
            if neighbour not in weights or new_weight[0] < weights[neighbour][0]:
                weights[neighbour] = new_weight
                unvisited_set.add(neighbour)

    if end_vec in visited_set:
        return weights[end_vec][1]
    else:
        return None


def available_moves(keypad: Grid, position: Vector) -> Set[Vector]:
    possible_moves = position.get_direct_neighbours()
    possible_moves = list(filter(lambda x: x in keypad, possible_moves))
    return possible_moves


def command_all_the_robots(code: str):
    numeric_keypad = {
        Vector(0, 0): "7",
        Vector(1, 0): "8",
        Vector(2, 0): "9",
        Vector(0, 1): "4",
        Vector(1, 1): "5",
        Vector(2, 1): "6",
        Vector(0, 2): "1",
        Vector(1, 2): "2",
        Vector(2, 2): "3",
        Vector(1, 3): "0",
        Vector(2, 3): "A",
    }

    directional_keypad = {
        Vector(1, 0): Direction.UP.to_str(),
        Vector(2, 0): "A",
        Vector(0, 1): Direction.LEFT.to_str(),
        Vector(1, 1): Direction.DOWN.to_str(),
        Vector(2, 1): Direction.RIGHT.to_str(),
    }

    keypads = [numeric_keypad, directional_keypad, directional_keypad]
    target = code
    instructions = ""
    for keypad in keypads:
        instructions = ""
        for current_key, target_key in window("A" + target, 2):
            next_path = find_shortest_path(keypad, current_key, target_key)
            instructions += "".join(map(lambda d: d.to_str(), next_path))
            instructions += "A"
        target = instructions

    return instructions


puzzle = """029A
980A
179A
456A
379A"""
complexity = 0
for code in puzzle.splitlines():
    sequence = command_all_the_robots(code)
    print(f"{code}: {sequence}")
    print(f"{len(sequence)} * {int(code[:-1])}")
    complexity += len(sequence) * int(code[:-1])

print(f"Part 1: {complexity}")
