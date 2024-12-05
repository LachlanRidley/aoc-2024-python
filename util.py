from typing import Self


class Grid[T]:
    _grid: list[list[T | None]]

    @classmethod
    def new(cls, width: int, height: int) -> Self:
        grid = [([None] * height)] * width
        return cls(grid)

    def __init__(self, grid):
        self._grid = grid

    def __repr__(self):
        cols = []
        for y in range(len(self._grid[0])):
            row = []
            for x in range(len(self._grid)):
                row.append(self._grid[x][y])

            cols.append(",".join([str(x) for x in row]))

        return "\n".join(cols)
