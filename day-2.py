from itertools import islice

with open("day-2.txt") as f:
    puzzle = f.read()

reports = [list(map(int, r.split(" "))) for r in puzzle.splitlines()]


def between(x: int, y: int, n: int) -> bool:
    return x <= n and n <= y


def check(report: list[int]) -> bool:
    s = report[:]
    s.sort()
    s2 = report[:]
    s2.sort()
    s2.reverse()

    if s != report and s2 != report:
        return False

    for i in range(len(report) - 1):
        a, b = report[i : i + 2]
        if not between(1, 3, abs(a - b)):
            return False

    return True


valid_reports = [report for report in reports if check(report)]

print(f"Part 1: {len(valid_reports)}")

valid_reports_with_dampener = list()
for report in reports:
    safe = False
    for i in range(len(report)):
        doctored_report = report[:]
        doctored_report.pop(i)
        safe = safe or check(doctored_report)
    if safe:
        valid_reports_with_dampener.append(report)

print(f"Part 2: {len(valid_reports_with_dampener)}")
