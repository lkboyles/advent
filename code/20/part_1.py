#!/usr/bin/env python3
"""Solve Day 20/Part 1 of the AdventOfCode

"""

import math
import itertools

class Houses(object):
    def __init__(self):
        pass

    def get_number_of_presents(self, house_number):
        """x

        >>> h = Houses()
        >>> h.get_number_of_presents(1)
        10
        >>> h.get_number_of_presents(2)
        30
        >>> h.get_number_of_presents(3)
        40
        >>> h.get_number_of_presents(4)
        70

        """
        result = 0
        for elf in self.elves_delivering_to(house_number):
            result += self.presents_per_elf(elf)

        return result

    def elves_delivering_to(self, house_number):
        for divisor in divisors_for(house_number):
            yield divisor

    def presents_per_elf(self, elf):
        return 10 * elf

def divisors_for(number):
    """x

    >>> sorted(list(divisors_for(6)))
    [1, 2, 3, 6]

    """
    yield 1

    if number != 1:
        yield number

    for divisor in range(2, 1+math.floor(math.sqrt(number))):
        if number % divisor == 0:
            quotient = number // divisor
            yield divisor

            if quotient != divisor:
                yield number // divisor

def main(filename):
    with open(filename, 'r') as f:
        present_threshold = int(f.readline())

    houses = Houses()

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
