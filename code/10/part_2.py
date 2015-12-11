#!/usr/bin/env python3
"""Solve Day 10/Part 2 of the AdventOfCode

=============================
Day 10: Elves Look, Elves Say
=============================

Now, starting again with the digits in your puzzle input, apply this
process 50 times. What is the length of the new result?

"""

import part_1

def main(filename):
    """Read string and apply look-and-say algorithm 50 times"""
    with open(filename, 'r') as f:
        string = f.read().strip()

    for _ in range(50):
        string = part_1.look_and_say_step(string)

    length = sum(1 for _ in string)
    print(length)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
