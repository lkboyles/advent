#!/usr/bin/env python3
"""Solve Day 24/Part 2 of the AdventOfCode

"""

import part_1

def main(filename):
    with open(filename, 'r') as f:
        weights = sorted([int(line) for line in f])

    minimum_qe = part_1.generate_partitions(weights, 4)

    print(minimum_qe)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
