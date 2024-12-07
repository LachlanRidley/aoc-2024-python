with open("day7.txt") as f:
    puzzle = f.read()

lines = [p.split(": ") for p in puzzle.splitlines()]
equations = [(int(line[0]), list(map(int, line[1].split(" ")))) for line in lines]


def evaluate(total, operators, target, part_2):
    if total > target:
        return False
    if len(operators) == 0:
        return total == target

    remaining = operators[1:]
    with_add = evaluate(total + operators[0], remaining, target, part_2)
    if with_add:
        return True
    with_mul = evaluate(total * operators[0], remaining, target, part_2)
    if with_mul:
        return True
    if part_2:
        with_cat = evaluate(
            int(str(total) + str(operators[0])), remaining, target, part_2
        )
        if with_cat:
            return True
    return False


part_1 = sum(
    [
        target
        for target, operators in equations
        if evaluate(operators[0], operators[1:], target, False)
    ]
)
print(f"Part 1: {part_1}")

part_2 = sum(
    [
        target
        for target, operators in equations
        if evaluate(operators[0], operators[1:], target, True)
    ]
)
print(f"Part 2: {part_2}")
