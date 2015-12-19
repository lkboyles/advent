#!/usr/bin/env python3
"""Solve Day 18/Part 1 of the AdventOfCode

"""

import numpy as np

class Grid(object):
    def __init__(self, initial_grid):
        self.grid = initial_grid

    @classmethod
    def from_file(cls, fileobj):
        grid = [
            [
                c == "#"
                for c in line.strip()
            ]
            for line in fileobj
        ]

        np_grid = np.zeros((2+len(grid), 2+len(grid[0])), dtype=bool)
        np_grid[1:-1, 1:-1] = grid

        return cls(np_grid)

    def __repr__(self):
        """x

        >>> lines = [".#.#.#", "...##.", "#....#", "..#...", "#.#..#", "####.."]
        >>> grid = Grid.from_file(lines)
        >>> grid
        .#.#.#
        ...##.
        #....#
        ..#...
        #.#..#
        ####..

        """
        return "\n".join(''.join("#" if val else "." for val in row[1:-1]) for row in self.grid[1:-1])

    def step(self):
        """x

        >>> lines = [".#.#.#", "...##.", "#....#", "..#...", "#.#..#", "####.."]
        >>> grid = Grid.from_file(lines)
        >>> grid.step()
        >>> grid
        ..##..
        ..##.#
        ...##.
        ......
        #.....
        #.##..

        """
        previous = self.grid.copy()

        for row in range(1, previous.shape[0]-1):
            for col in range(1, previous.shape[1]-1):
                current = previous[row, col]
                neighbors = np.sum(previous[row-1:row+2, col-1:col+2]) - current

                if current:
                    self.grid[row, col] = neighbors == 2 or neighbors == 3
                else:
                    self.grid[row, col] = neighbors == 3

    def count_lights(self):
        return np.sum(self.grid)

def main(filename):
    with open(filename, 'r') as f:
        grid = Grid.from_file(f)

    for _ in range(100):
        grid.step()

    lights = grid.count_lights()

    print(lights)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
