#!/usr/bin/env python3
"""Solve Day 19/Part 2 of the AdventOfCode

"""

import itertools
import re

def number_of_steps(molecule):
    """x

    >>> number_of_steps("ABCDE")
    4
    >>> number_of_steps("ARnBRnCRnDRnEArArArAr")
    4
    >>> number_of_steps("ARnBRnCYDArYERnFYGArAr")
    3

    """
    # Thanks https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/cy4etju
    elements = [el.group() for el in re.finditer(r'[A-Z][a-z]?', molecule)]
    rn_or_ar = [el for el in elements if el == 'Rn' or el == 'Ar']
    y_elements = [el for el in elements if el == 'Y']

    steps = len(elements) - len(rn_or_ar) - 2*len(y_elements) - 1

    return steps

def main(filename):
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "":
                break

            pass

        molecule = f.readline()

    steps = number_of_steps(molecule)
    print(steps)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
