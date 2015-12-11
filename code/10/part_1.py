#!/usr/bin/env python3
"""Solve Day 10/Part 1 of the AdventOfCode

"""

import re

def look_and_say_step(string):
    """x

    >>> look_and_say_step("1")
    '11'
    >>> look_and_say_step("11")
    '21'
    >>> look_and_say_step("21")
    '1211'

    """
    new_string = ""
    for (count, character) in look_and_say_values(string):
        new_string += "{}{}".format(count, character)

    return new_string

def look_and_say_values(string):
    """x

    >>> list(look_and_say_values("1"))
    [(1, '1')]
    >>> list(look_and_say_values("11"))
    [(2, '1')]
    >>> list(look_and_say_values("21"))
    [(1, '2'), (1, '1')]

    """
    regex = re.compile(r'(.)\1*')
    for match in regex.finditer(string):
        substring = match.group(0)
        yield (len(substring), substring[0])

def main(filename):
    """Read instructions for circuit and report wire 'a'"""
    with open(filename, 'r') as f:
        string = f.read().strip()

    for _ in range(40):
        string = look_and_say_step(string)

    length = len(string)
    print(length)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
