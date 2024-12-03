import re


with open("day-3.txt") as f:
    puzzle = f.read()

part_1 = sum(
    int(a) * int(b) for (a, b) in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", puzzle)
)

program = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))", puzzle)

part_2 = 0
enabled = True
for statement in program:
    if statement[2] == "do()":
        enabled = True
    elif statement[3] == "don't()":
        enabled = False
    elif enabled:
        part_2 = part_2 + (int(statement[0]) * int(statement[1]))

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
