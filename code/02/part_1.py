#!/usr/bin/env python3
"""Solve Day 2/Part 1 of the AdventOfCode

========================================
Day 2: I Was Told There Would Be No Math
========================================

The elves are running low on wrapping paper, and so they need to
submit an order for more. They have a list of the dimensions (length
l, width w, and height h) of each present, and only want to order
exactly as much as they need.

Fortunately, every present is a box (a perfect right rectangular
prism), which makes calculating the required wrapping paper for each
gift a little easier: find the surface area of the box, which is 2*l*w
+ 2*w*h + 2*h*l. The elves also need a little extra paper for each
present: the area of the smallest side.

For example:

- A present with dimensions 2x3x4 requires 2*6 + 2*12 + 2*8 = 52
  square feet of wrapping paper plus 6 square feet of slack, for a
  total of 58 square feet.

- A present with dimensions 1x1x10 requires 2*1 + 2*10 + 2*10 = 42
  square feet of wrapping paper plus 1 square foot of slack, for a
  total of 43 square feet.

All numbers in the elves' list are in feet. How many total square feet
of wrapping paper should they order?

"""

def get_total_wrapping_paper_area(dimensions):
    """Return the total area needed for all boxes

    This function accepts an iterator which returns length, width,
    height tuples and determines the total area needed for all of the
    boxes.

    >>> get_total_wrapping_paper_area([(1, 1, 1)])
    7
    >>> get_total_wrapping_paper_area([(1, 1, 1), (1, 1, 10)])
    50
    >>> get_total_wrapping_paper_area([])
    0

    """
    total_area = 0
    for (length, width, height) in dimensions:
        total_area += get_wrapping_paper_area(length, width, height)

    return total_area

def get_wrapping_paper_area(length, width, height):
    """Return the area of paper needed to cover the box

    The area is found by taking the surface area of the box (which is
    the sum of the areas of each side) and then adding a little bit
    extra slack for the elves to wrap with.

    The slack is defined as the area of the smallest side.

    >>> get_wrapping_paper_area(1, 1, 1)
    7
    >>> get_wrapping_paper_area(1, 1, 10)
    43
    >>> get_wrapping_paper_area(2, 3, 4)
    58

    """
    sides = (
        length * width,
        width * height,
        length * height,
    )

    return 2 * sum(sides) + min(sides)

def dimensions_from_line(line):
    """Get dimensions from a single line of text

    Dimensions in a file are expected to be in the form:
    "LxWxH". Where L, W, and H are integers. For example, 2x4x8
    represents the dimensions of a box with length 2, width 4, and
    height 8.

    >>> dimensions_from_line("1x2x3")
    (1, 2, 3)
    >>> dimensions_from_line("2x4x8")
    (2, 4, 8)
    >>> dimensions_from_line("")
    Traceback (most recent call last):
     ...
    ValueError: invalid literal for int() with base 10: ''

    """
    (length, width, height) = map(int, line.split('x'))

    return (length, width, height)

def dimension_reader(fileobj):
    """Return iterator for each set of dimensions in file

    Dimensions are in the form specified by
    :func:`dimensions_from_line`.

    >>> list(dimension_reader(["2x4x8", "1x2x3"]))
    [(2, 4, 8), (1, 2, 3)]
    >>> list(dimension_reader([]))
    []

    """
    for line in fileobj:
        (length, width, height) = dimensions_from_line(line)
        yield (length, width, height)

def main(filename):
    """Read dimensions from file and print the total wrapping paper area"""
    with open(filename, 'r') as f:
        iterator = dimension_reader(f)
        total_area = get_total_wrapping_paper_area(iterator)

        print(total_area)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
