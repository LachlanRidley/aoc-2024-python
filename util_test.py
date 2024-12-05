import unittest
from util import Grid


class TestGrid(unittest.TestCase):
    def test_new(self):
        grid = Grid.new(2, 3)
        self.assertEqual(grid.__repr__(), "None,None\nNone,None\nNone,None")


if __name__ == "__main__":
    unittest.main()
