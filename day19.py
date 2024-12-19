from typing import Set
from rich import print

with open("day19.txt") as f:
    puzzle = f.read()

towels_str, patterns_str = puzzle.split("\n\n")
towels = set(towels_str.split(", "))
patterns = patterns_str.splitlines()


def can_make_pattern(pattern: str, towels: Set[str], depth: int) -> bool:
    if pattern in towels:
        return True

    for towel in towels:
        if pattern.startswith(towel) and can_make_pattern(
            pattern.removeprefix(towel), towels, depth + 1
        ):
            return True

    return False


def ways_to_make_pattern(pattern: str, towels: Set[str]) -> int:
    ways = [0] * (len(pattern) + 1)
    ways[0] = 1

    for i in range(len(pattern)):
        if ways[i] > 0:
            remaining_pattern = pattern[i:]
            for towel in filter(lambda t: remaining_pattern.startswith(t), towels):
                ways[i + len(towel)] += ways[i]

    return ways[len(pattern)]


possible_patterns = set()
for pattern in patterns:
    if can_make_pattern(pattern, towels, 0):
        possible_patterns.add(pattern)

print(f"Part 1: {len(possible_patterns)}")

total_combos = 0
for pattern in possible_patterns:
    combos = ways_to_make_pattern(pattern, towels)
    total_combos += combos

print(f"Part 2: {total_combos}")
