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
