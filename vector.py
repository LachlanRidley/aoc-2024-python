from typing import NamedTuple, Self


class Vector(NamedTuple):
    x: int
    y: int

    def get_direct_neighbours(self) -> set[Self]:
        return {
            Vector(self.x - 1, self.y),
            Vector(self.x + 1, self.y),
            Vector(self.x, self.y - 1),
            Vector(self.x, self.y + 1),
        }

    def __add__(self, other) -> Self:
        from util import Direction, move_pos

        if isinstance(other, Direction):
            return move_pos(self, other)
        raise NotImplementedError()
