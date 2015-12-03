#!/usr/bin/env python3
"""Solve Day 1/Part 1 of the AdventOfCode

=====================
Day 1: Not Quite Lisp
=====================

Santa is trying to deliver presents in a large apartment building, but
he can't find the right floor - the directions he got are a little
confusing. He starts on the ground floor (floor 0) and then follows
the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a
closing parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he
will never find the top or bottom floors.

For example:

>>> final_floor("(())")
0
>>> final_floor("()()")
0
>>> final_floor("(((")
3
>>> final_floor("(()(()(")
3
>>> final_floor("))(((((")
3
>>> final_floor("())")
-1
>>> final_floor("))(")
-1
>>> final_floor(")))")
-3
>>> final_floor(")())())")
-3

To what floor do the instructions take Santa?

"""

def current_floor(instructions):
    """Yield the current floor based on the instructions

    >>> list(current_floor("((("))
    [1, 2, 3]
    >>> list(current_floor("())(()"))
    [1, 0, -1, 0, 1, 0]
    >>> list(current_floor(""))
    []

    """
    floor = 0
    for instruction in instructions:
        if instruction == '(':
            floor += 1
        if instruction == ')':
            floor -= 1
        yield floor

def final_floor(instructions):
    """Return the final floor based on the instructions

    >>> final_floor("(((")
    3
    >>> final_floor("())(()")
    0
    >>> final_floor("")
    0

    """
    floor = 0
    for floor in current_floor(instructions):
        pass

    return floor

def main(filename):
    """Print the final floor that Santa ends at"""
    with open(filename, 'r') as f:
        instructions = f.read()

    print(final_floor(instructions))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
