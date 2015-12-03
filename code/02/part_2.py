#!/usr/bin/env python3
"""Solve Day 2/Part 2 of the AdventOfCode

========================================
Day 2: I Was Told There Would Be No Math
========================================

The elves are also running low on ribbon. Ribbon is all the same
width, so they only have to worry about the length they need to order,
which they would again like to be exact.

They have a list of the dimensions (length l, width w, and height h)
of each present, and only want to order exactly as much as they
need. Fortunately, every present is a box (a perfect right rectangular
prism).

The ribbon required to wrap a present is the shortest distance around
its sides, or the smallest perimeter of any one face. Each present
also requires a bow made out of ribbon as well; the feet of ribbon
required for the perfect bow is equal to the cubic feet of volume of
the present. Don't ask how they tie the bow, though; they'll never
tell.

For example:

- A present with dimensions 2x3x4 requires 2+2+3+3 = 10 feet of ribbon
  to wrap the present plus 2*3*4 = 24 feet of ribbon for the bow, for
  a total of 34 feet.

- A present with dimensions 1x1x10 requires 1+1+1+1 = 4 feet of ribbon
  to wrap the present plus 1*1*10 = 10 feet of ribbon for the bow, for
  a total of 14 feet.

How many total feet of ribbon should they order?

"""

import part_1

def get_total_ribbon(dimensions):
    """Return the total ribbon needed for all presents


    >>> get_total_ribbon([])
    0
    >>> get_total_ribbon([(1, 1, 1)])
    5
    >>> get_total_ribbon([(1, 1, 1), (2, 3, 4)])
    39

    """
    total_length = 0
    for (length, width, height) in dimensions:
        total_length += get_total_ribbon_for_present(length, width, height)

    return total_length

def get_total_ribbon_for_present(length, width, height):
    """Return the total ribbon needed for one present

    The total is just the amount needed for wrapping the present plus
    the amount for the bow.

    >>> get_total_ribbon_for_present(2, 3, 4)
    34
    >>> get_total_ribbon_for_present(1, 1, 10)
    14
    >>> get_total_ribbon_for_present(1, 1, 1)
    5

    """
    ribbon_length = get_ribbon_for_wrapping_present(length, width, height)
    ribbon_length += get_ribbon_for_bow(length, width, height)

    return ribbon_length

def get_ribbon_for_wrapping_present(length, width, height):
    """Return the amount of ribbon needed to wrap the present

    This is the amount of ribbon needed to go around the smallest
    perimeter of any face.

    >>> get_ribbon_for_wrapping_present(2, 3, 4)
    10
    >>> get_ribbon_for_wrapping_present(1, 1, 10)
    4
    >>> get_ribbon_for_wrapping_present(1, 1, 1)
    4

    """
    # To find the smallest face, we can sort the dimensions, so that
    # the smallest two dimensions are at the beginning of the list,
    # and then summing them up will give us half the total length, so
    # we have to double it to get the final length.
    dimensions = sorted([length, width, height])

    ribbon_length = 2 * sum(dimensions[:2])

    return ribbon_length

def get_ribbon_for_bow(length, width, height):
    """Return the amount of ribbon needed to make the bow

    The bow, for some magical reason, is simply the volume of the
    present.

    >>> get_ribbon_for_bow(2, 3, 4)
    24
    >>> get_ribbon_for_bow(1, 1, 10)
    10
    >>> get_ribbon_for_bow(1, 1, 1)
    1

    """
    ribbon_length = length * width * height

    return ribbon_length

def main(filename):
    """Read dimensions from file and print the total ribbon needed"""
    with open(filename, 'r') as f:
        iterator = part_1.dimension_reader(f)
        total_ribbon = get_total_ribbon(iterator)

        print(total_ribbon)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
