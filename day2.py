from typing import Generator, Iterator
from util import between, window, yoink

with open("day2.txt") as f:
    puzzle = f.read()

reports = [list(map(int, r.split(" "))) for r in puzzle.splitlines()]


def check(report: list[int]) -> bool:
    if sorted(report) != report and sorted(report, reverse=True) != report:
        return False

    return all([between(1, 3, abs(a - b)) for [a, b] in window(report, 2)])


valid_reports = [report for report in reports if check(report)]
valid_reports_with_dampener = [
    report
    for report in reports
    if any([check(yoink(report, i)) for i in range(len(report))])
]

print(f"Part 1: {len(valid_reports)}")
print(f"Part 2: {len(valid_reports_with_dampener)}")
