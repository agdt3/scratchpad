#! /bin/python

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Grid:
    def __init__(self, size, start, end, obstacles):
        self._size = size
        self._start = start
        self._end = end
        self._obstacles = obstacles

    def is_blocked(self, point):
        return point in self._obstacles

class Path:
    def __init__(self, grid):
        self._grid = grid

if __name__ == "__main__":
    g = Grid()
