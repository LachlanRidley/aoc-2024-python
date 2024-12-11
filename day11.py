import functools
from typing import Iterable

with open("day11.txt") as f:
    puzzle = f.read()
# puzzle = "125 17"

stones = list(map(int, puzzle.split(" ")))


def flatten(xs):
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


@functools.cache
def evolve(stone: int) -> int | list[int]:
    if stone == 0:
        return 1
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        first, second = s[: len(s) // 2], s[len(s) // 2 :]
        return [int(first), int(second)]
    else:
        return stone * 2024


def chunks(lst: list[int], n: int) -> Iterable[list[int]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def blink(stones: list[int]) -> list[int]:
    stones = map(evolve, stones)
    return [s for s in flatten(stones)]


for i in range(25):
    print(i)
    stones = blink(stones)

print(f"Part 1: {len(stones)}")

for i in range(50):
    print(i)
    stones = blink(stones)

print(f"Part 2: {len(stones)}")
