#!/usr/bin/env python3
"""Solve Day 20/Part 1 of the AdventOfCode

"""

import math
import itertools

import part_1

class ModifiedHouses(part_1.Houses):
    def __init__(self):
        pass

    def elves_delivering_to(self, house_number):
        for divisor in part_1.divisors_for(house_number):
            if house_number > 50 * divisor:
                continue

            yield divisor

    def presents_per_elf(self, elf):
        return 11 * elf

def main(filename):
    with open(filename, 'r') as f:
        present_threshold = int(f.readline())

    houses = ModifiedHouses()

    for house_number in itertools.count():
        if houses.get_number_of_presents(house_number) >= present_threshold:
            break

    print(house_number)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
