from dataclasses import dataclass
import re
from rich import print
from itertools import zip_longest

from sympy import Eq, solve, symbols

from vector import Vector

with open("day13.txt") as f:
    puzzle = f.read()


def grouper(n, iterable):
    args = [iter(iterable)] * n
    return zip_longest(*args)


@dataclass
class Game:
    button_a: Vector
    button_b: Vector

    prize: Vector


button_a_cost = 3
button_b_cost = 1


games = list()
for line1, line2, line3, _ in grouper(4, puzzle.splitlines()):
    results = re.search(r"Button A: X\+(\d*), Y\+(\d*)", line1)
    button_a = Vector(int(results.group(1)), int(results.group(2)))

    results = re.search(r"Button B: X\+(\d*), Y\+(\d*)", line2)
    button_b = Vector(int(results.group(1)), int(results.group(2)))

    results = re.search(r"Prize: X=(\d*), Y=(\d*)", line3)
    prize = Vector(int(results.group(1)), int(results.group(2)))

    games.append(Game(button_a, button_b, prize))


def solve_with_urgh_mathematics(
    game: Game, big_prizes: bool = False
) -> tuple[int, int] | None:
    prize_x = game.prize.x
    prize_y = game.prize.y
    if big_prizes:
        prize_x += 10000000000000
        prize_y += 10000000000000
    (
        a,
        b,
    ) = symbols("a b")

    solution = solve(
        [
            Eq(a * game.button_a.x + b * game.button_b.x, prize_x),
            Eq(a * game.button_a.y + b * game.button_b.y, prize_y),
        ],
        syms=(a, b),
    )
    if solution[a].is_integer and solution[b].is_integer:
        return (solution[a], solution[b])
    return None


def token_cost_of_button_combo(combo: tuple[int, int]) -> int:
    return combo[0] * button_a_cost + combo[1] * button_b_cost


tokens_spent = 0
for game in games:
    winning_combo = solve_with_urgh_mathematics(game)
    if winning_combo:
        tokens_spent += token_cost_of_button_combo(winning_combo)


print(f"Part 1: {tokens_spent}")

tokens_spent = 0
for game in games:
    winning_combo = solve_with_urgh_mathematics(game, True)
    if winning_combo:
        tokens_spent += token_cost_of_button_combo(winning_combo)


print(f"Part 2: {tokens_spent}")
