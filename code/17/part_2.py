#!/usr/bin/env python3
"""Solve Day 17/Part 2 of the AdventOfCode

=================================
Day 17: No Such Thing as Too Much
=================================

While playing with all the containers in the kitchen, another load of
eggnog arrives! The shipping and receiving department is requesting as
many containers as you can spare.

Find the minimum number of containers that can exactly fit all 150
liters of eggnog. How many different ways can you fill that number of
containers and still hold exactly 150 litres?

In the example above, the minimum number of containers was two. There
were three ways to use that many containers, and so the answer there
would be 3.

"""

import part_1

def main(filename):
    """Read container sizes and count the number of combinations that use
    the minimum number of containers"""
    with open(filename, 'r') as f:
        container_sizes = [int(line) for line in f]

    combinations = list(part_1.get_combinations(container_sizes, 150))

    min_containers = min(len(x) for x in combinations)

    num_combinations = sum(1 for x in combinations if len(x) == min_containers)

    print(num_combinations)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
