phrase = "XMAS"

with open("day-4.txt") as f:
    puzzle = f.read()


def check(lines, row, col, row_dir, col_dir):
    for n in range(len(phrase)):
        if row < 0 or row >= len(lines) or col < 0 or col >= len(lines[0]):
            return 0
        if lines[row][col] != phrase[n]:
            return 0
        row += row_dir
        col += col_dir
    return 1


def check_cross(lines, row, col):
    if lines[row][col] != "A":
        return 0

    tl = lines[row - 1][col - 1]
    tr = lines[row - 1][col + 1]
    bl = lines[row + 1][col - 1]
    br = lines[row + 1][col + 1]
    if not ((tl == "M" and br == "S") or (tl == "S" and br == "M")):
        return 0
    if not ((bl == "M" and tr == "S") or (bl == "S" and tr == "M")):
        return 0

    return 1


lines = puzzle.split("\n")
part_1 = 0

for row in range(len(lines)):
    for col in range(len(lines[row])):
        if lines[row][col] == phrase[0]:
            part_1 += check(lines, row, col, 0, 1)
            part_1 += check(lines, row, col, 1, 1)
            part_1 += check(lines, row, col, 1, 0)
            part_1 += check(lines, row, col, 1, -1)
            part_1 += check(lines, row, col, 0, -1)
            part_1 += check(lines, row, col, -1, -1)
            part_1 += check(lines, row, col, -1, 0)
            part_1 += check(lines, row, col, -1, 1)

part_2 = 0
for row in range(1, len(lines) - 1):
    for col in range(1, len(lines[0]) - 1):
        part_2 += check_cross(lines, row, col)

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
