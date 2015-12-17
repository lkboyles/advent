#!/usr/bin/env python3
"""Solve Day 17/Part 1 of the AdventOfCode

=================================
Day 17: No Such Thing as Too Much
=================================

The elves bought too much eggnog again - 150 liters this time. To fit
it all into your refrigerator, you'll need to move it into smaller
containers. You take an inventory of the capacities of the available
containers.

For example, suppose you have containers of size 20, 15, 10, 5, and 5
liters. If you need to store 25 liters, there are four ways to do it:

- 15 and 10

- 20 and 5 (the first 5)

- 20 and 5 (the second 5)

- 15, 5, and 5

Filling all containers entirely, how many different combinations of
containers can exactly fit all 150 liters of eggnog?

"""

import itertools

def get_combinations(container_sizes, target_amount):
    """Yield each combination of containers that holds the given amount

    >>> list(get_combinations([20, 15, 10, 5, 5], 25))
    [(20, 5), (20, 5), (15, 10), (15, 5, 5)]

    """
    for i in range(len(container_sizes)):
        for combination in itertools.combinations(container_sizes, i):
            if sum(combination) == target_amount:
                yield combination

def main(filename):
    """Read container sizes and find number of combinations that can hold
    150 liters"""
    with open(filename, 'r') as f:
        container_sizes = [int(line) for line in f]

    combinations = get_combinations(container_sizes, 150)

    num_combinations = sum(1 for _ in combinations)

    print(num_combinations)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
