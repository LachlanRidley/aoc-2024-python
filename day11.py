import functools


with open("day11.txt") as f:
    puzzle = f.read()

stones = list(map(int, puzzle.split(" ")))


@functools.cache
def build_tree(stone: int, depth: int) -> int:
    if depth == 0:
        return 1

    if stone == 0:
        child_count = build_tree(1, depth - 1)
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        first, second = s[: len(s) // 2], s[len(s) // 2 :]
        child_count = build_tree(int(first), depth - 1) + build_tree(
            int(second), depth - 1
        )
    else:
        child_count = build_tree(stone * 2024, depth - 1)

    return child_count


def blink(stones: list[int], depth: int) -> list[int]:
    return sum([build_tree(stone, depth) for stone in stones])


part_1 = blink(stones, 25)
print(f"Part 1: {part_1} | expected 186424")

part_2 = blink(stones, 75)
print(f"Part 2: {part_2} | expected 219838428124832")
