#!/usr/bin/env python3
"""Solve Day 9/Part 2 of the AdventOfCode

============================
Day 9: All in a Single Night
============================

The next year, just to show off, Santa decides to take the route with
the longest distance instead.

He can still start and end at any two (different) locations he wants,
and he still must visit each location exactly once.

For example, given the distances above, the longest route would be 982
via (for example) Dublin -> London -> Belfast.

What is the distance of the longest route?

"""

import part_1

def main(filename):
    """Read instructions for circuit and report wire 'a'"""
    world = part_1.World()
    with open(filename, 'r') as f:
        world.read_file(f)

    longest_distance = part_1.find_extreme_distance(world, minimum=False)
    print(longest_distance)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
