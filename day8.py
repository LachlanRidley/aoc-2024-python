from util import in_bounds


with open("day8.txt") as f:
    puzzle = f.read()

grid = [list(row) for row in puzzle.splitlines()]

nodes = set()
for row, line in enumerate(grid):
    for col, char in enumerate(line):
        if char.isalnum():
            nodes.add((char, row, col))

antinodes = set()
for row in range(len(puzzle.splitlines())):
    for col in range(len(puzzle.splitlines()[0])):
        for node in nodes:
            if node[1] == row and node[2] == col:
                # it's the current spot, skip
                continue
            char = node[0]
            dr = node[1] - row
            dc = node[2] - col

            second_node_row = row + dr * 2
            second_node_col = col + dc * 2
            required_node = (char, second_node_row, second_node_col)

            if required_node in nodes:
                antinodes.add((row, col))

print(f"Part 1: {len(antinodes)}")


def vector_between(n1: tuple[int, int], n2: tuple[int, int]) -> tuple[int, int]:
    return (n2[1] - n1[1], n2[2] - n1[2])


resonant_antinodes = set()
for node in nodes:
    matches = [match for match in nodes if node != match and node[0] == match[0]]
    for match in matches:
        vec = vector_between(node, match)
        dirs = [
            (vec[0], vec[1]),
            (-vec[0], -vec[1]),
        ]
        for dir in dirs:
            cursor = (node[1] + dir[0], node[2] + dir[1])
            while in_bounds(grid, cursor):
                resonant_antinodes.add(cursor)
                cursor = (cursor[0] + dir[0], cursor[1] + dir[1])


for row, line in enumerate(grid):
    for col, char in enumerate(line):
        if any([n[0] == row and n[1] == col for n in resonant_antinodes]):
            print("#", end="")
        else:
            print(".", end="")
    print()

print(f"Part 2: {len(resonant_antinodes)}")
