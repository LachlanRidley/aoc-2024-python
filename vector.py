from typing import NamedTuple, Self

from util import Direction


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

    def get_direction_between(self, v: Self) -> Direction | None:
        if self.x == v.x and self.y - 1 == v.y:
            return Direction.UP
        if self.x == v.x and self.y + 1 == v.y:
            return Direction.DOWN
        if self.y == v.y and self.x - 1 == v.x:
            return Direction.LEFT
        if self.y == v.y and self.x + 1 == v.x:
            return Direction.RIGHT
        return None

    def __add__(self, other) -> Self:
        from util import Direction, move_pos

        if isinstance(other, Direction):
            return move_pos(self, other)
        raise NotImplementedError()
