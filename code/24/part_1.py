#!/usr/bin/env python3
"""Solve Day 24/Part 1 of the AdventOfCode

"""

import itertools

# Heavily based on
# https://www.reddit.com/r/adventofcode/comments/3y1s7f/day_24_solutions/cy9srkh
def generate_partitions(weights, num_partitions, first_call=True,
                        expected_sum=None):
    if expected_sum is None:
        expected_sum = sum(weights) / num_partitions

    if num_partitions == 1:
        return sum(weights) == expected_sum

    for length in range(1, len(weights)):
        for first_partition in itertools.combinations(weights, length):
            if sum(first_partition) != expected_sum:
                continue

            remaining = list(set(weights) - set(first_partition))

            if not generate_partitions(remaining, num_partitions - 1, False, expected_sum):
                continue

            product = 1
            for weight in first_partition:
                product *= weight

            return product

    return False

def main(filename):
    with open(filename, 'r') as f:
        weights = sorted([int(line) for line in f])

    minimum_qe = generate_partitions(weights, 3)

    print(minimum_qe)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
