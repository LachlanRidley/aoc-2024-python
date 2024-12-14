from dataclasses import dataclass
import math
import re
from vector import Vector

from rich import print


@dataclass
class Robot:
    position: Vector
    velocity: Vector


@dataclass
class Quad:
    x0: int
    x1: int
    y0: int
    y1: int

    def contains_position(self, v: Vector) -> bool:
        return between(v, self.x0, self.x1, self.y0, self.y1)


def load_robots(puzzle: str) -> list[Robot]:
    robots = list()
    for line in puzzle.splitlines():
        coords = re.findall(r"p=([0-9+-]*),([0-9+-]*) v=([0-9+-]*),([0-9+-]*)", line)
        robots.append(
            Robot(
                Vector(int(coords[0][0]), int(coords[0][1])),
                Vector(int(coords[0][2]), int(coords[0][3])),
            )
        )
    return robots


def between(v: Vector, x0: int, x1: int, y0: int, y1: int) -> bool:
    return x0 <= v.x and v.x <= x1 and y0 <= v.y and v.y <= y1


def advance(robots: list[Robot], t: int):
    for robot in robots:
        x = (robot.position.x + t * robot.velocity.x) % width
        y = (robot.position.y + t * robot.velocity.y) % height
        robot.position = Vector(x, y)


def print_grid(
    robots: list[Robot],
    width: int,
    height: int,
    mx: int,
    my: int,
    hide_middle: bool = True,
):
    for y in range(height):
        if hide_middle and y == my:
            print()
            continue
        for x in range(width):
            if hide_middle and x == mx:
                print(" ", end="")
                continue
            robot_count = len(
                [r for r in robots if r.position.x == x and r.position.y == y]
            )
            if robot_count == 0:
                print(".", end="")
            else:
                print(robot_count, end="")
        print()


with open("day14.txt") as f:
    puzzle = f.read()
width = 101
height = 103


robots = load_robots(puzzle)
advance(robots, 100)

mx = width // 2
my = height // 2
quadrant_1 = Quad(0, mx - 1, 0, my - 1)
quadrant_2 = Quad(mx + 1, width, 0, my - 1)
quadrant_3 = Quad(0, mx - 1, my + 1, height)
quadrant_4 = Quad(mx + 1, width, my + 1, height)

q1_count = len(
    [robot for robot in robots if quadrant_1.contains_position(robot.position)]
)
q2_count = len(
    [robot for robot in robots if quadrant_2.contains_position(robot.position)]
)
q3_count = len(
    [robot for robot in robots if quadrant_3.contains_position(robot.position)]
)
q4_count = len(
    [robot for robot in robots if quadrant_4.contains_position(robot.position)]
)

print_grid(robots, width, height, mx, my, hide_middle=True)

print(f"Part 1: {math.prod([q1_count, q2_count, q3_count, q4_count])}")

robots = load_robots(puzzle)
t = 8006
advance(robots, t)
while True:
    interesting = False
    for robot in robots:
        neighbours = robot.position.get_direct_neighbours()
        neighbouring_robots = [r for r in robots if r.position in neighbours]
        if len(neighbouring_robots) >= 4:
            interesting = True
    if interesting:
        print(f"T = {t}")
        print_grid(robots, width, height, mx, my, hide_middle=False)
        ans = input("done?")
        if ans == "y":
            break
    t += 1
    advance(robots, 1)

print(f"Part 2: {t} seconds")
