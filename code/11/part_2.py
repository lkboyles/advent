#!/usr/bin/env python3
"""Solve Day 11/Part 2 of the AdventOfCode

========================
Day 11: Corporate Policy
========================

Santa's password expired again. What's the next one?

"""

import part_1

def main(filename):
    """Read password and determine next good ones"""
    with open(filename, 'r') as f:
        password = f.read().strip()

    # Apply two rounds of the algorithm
    password = part_1.find_good_password(password)
    password = part_1.find_good_password(password)
    print(password)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
