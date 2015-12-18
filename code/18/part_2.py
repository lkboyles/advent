#!/usr/bin/env python3
"""Solve Day 18/Part 2 of the AdventOfCode

"""

import itertools
import numpy as np

import part_1

class ModifiedGrid(part_1.Grid):
    def __init__(self, initial_grid):
        """x

        >>> lines = [".#.#.#", "...##.", "#....#", "..#...", "#.#..#", "####.."]
        >>> grid = ModifiedGrid.from_file(lines)
        >>> grid
        ##.#.#
        ...##.
        #....#
        ..#...
        #.#..#
        ####.#

        """
        part_1.Grid.__init__(self, initial_grid)
        self.turn_on_corners()

    def turn_on_corners(self):
        self.grid[1, 1] = True
        self.grid[-2, 1] = True
        self.grid[-2, -2] = True
        self.grid[1, -2] = True

    def step(self):
        """x

        >>> lines = [".#.#.#", "...##.", "#....#", "..#...", "#.#..#", "####.."]
        >>> grid = ModifiedGrid.from_file(lines)
        >>> grid.step()
        >>> grid
        #.##.#
        ####.#
        ...##.
        ......
        #...#.
        #.####

        """
        self.turn_on_corners()
        part_1.Grid.step(self)
        self.turn_on_corners()

def main(filename):
    with open(filename, 'r') as f:
        grid = ModifiedGrid.from_file(f)

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
