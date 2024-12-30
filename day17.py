from typing import List
from rich import print


def parse(puzzle: str):
    lines = puzzle.splitlines()
    program = list(map(int, lines[4].split(" ")[1].split(",")))
    r_a = int(lines[0].split(" ")[2])
    r_b = int(lines[1].split(" ")[2])
    r_c = int(lines[2].split(" ")[2])

    return (program, r_a, r_b, r_c)


def combo(operand: int):
    if operand == 4:
        return r_a
    if operand == 5:
        return r_b
    if operand == 6:
        return r_c

    return operand


def run(program: List[int]) -> List[int]:
    global r_a, r_b, r_c

    output: List[int] = []

    instruction_pointer = 0

    while instruction_pointer < len(program):
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]

        match opcode:
            case 0:
                r_a = r_a // (2 ** combo(operand))
            case 1:
                r_b = r_b ^ operand
            case 2:
                r_b = combo(operand) % 8
            case 3:
                if r_a != 0:
                    instruction_pointer = operand
                    continue  # don't increment pointer by 2 when jumping
            case 4:
                r_b = r_b ^ r_c
            case 5:
                output.append(combo(operand) % 8)
            case 6:
                r_b = r_a // (2 ** combo(operand))
            case 7:
                r_c = r_a // (2 ** combo(operand))

        instruction_pointer += 2

    return output


# example 1
program, r_a, r_b, r_c = [2, 6], 0, 0, 9
run(program)
assert r_b == 1

# example 2
program, r_a, r_b, r_c = [5, 0, 5, 1, 5, 4], 10, 0, 0
output = run(program)
assert output == [0, 1, 2]

# example 3
program, r_a, r_b, r_c = [0, 1, 5, 4, 3, 0], 2024, 0, 0
output = run(program)
assert output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
assert r_a == 0

# example 4
program, r_a, r_b, r_c = [1, 7], 0, 29, 0
run(program)
assert r_b == 26

# example 5
program, r_a, r_b, r_c = [4, 0], 0, 2024, 43690
run(program)
assert r_b == 44354

with open("day17.txt") as f:
    puzzle = f.read()

# Part 1
program, r_a, r_b, r_c = parse(puzzle)
output = run(program)
print(f"Part 1: {",".join(map(str, output))}")

# Part 2
part_2 = 0
expected_len = 6
increment = 8**3
i = expected_len - 1
while True:
    program, r_a, r_b, r_c = parse(puzzle)
    r_a = part_2
    output = run(program)
    if len(output) == len(program):
        print(f"{part_2} {output}")
        if output[i] == program[i]:
            i -= 1
            increment = 8 ** (i + 1)
        else:
            part_2 += increment
    if output == program:
        break

print(f"Part 2: {part_2}")
