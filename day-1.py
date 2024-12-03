with open("day-1.txt") as f:
    puzzle = f.read()

elems = [line.split() for line in puzzle.split("\n")]

list_1 = [int(x[0]) for x in elems]
list_1.sort()

list_2 = [int(x[1]) for x in elems]
list_2.sort()

part_1 = sum([abs(list_1[i] - list_2[i]) for i in range(len(list_1))])
part_2 = sum([x * len([e for e in list_2 if e == x]) for x in list_1])

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
