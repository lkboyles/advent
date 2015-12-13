#!/usr/bin/env python3
"""Solve Day 12/Part 1 of the AdventOfCode

============================
Day 12: JSAbacusFramework.io
============================

Santa's Accounting-Elves need help balancing the books after a recent
order. Unfortunately, their accounting software uses a peculiar
storage format. That's where you come in.

They have a JSON document which contains a variety of things: arrays
([1,2,3]), objects ({"a":1, "b":2}), numbers, and strings. Your first
job is to simply find all of the numbers throughout the document and
add them together.

For example:

- [1,2,3] and {"a":2,"b":4} both have a sum of 6.

- [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.

- {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.

- [] and {} both have a sum of 0.

You will not encounter any strings containing numbers.

What is the sum of all numbers in the document?

"""

import json

def is_number(value):
    """Determine whether the value is an integer number

    >>> is_number(123)
    True
    >>> is_number("123")
    True
    >>> is_number("abc")
    False
    >>> is_number({"a": 1})
    False
    >>> is_number([1, 2, 3])
    False

    """
    try:
        _ = int(value)
        return True
    except TypeError:
        return False
    except ValueError:
        return False

def is_array(value):
    """Determine whether the value is an array (list)

    >>> is_array([1, 2, 3])
    True
    >>> is_array("abc")
    False
    >>> is_array("123")
    False
    >>> is_array({"a": 1})
    False

    """
    return isinstance(value, list)

def is_dict(value):
    """Determine whether the value is a dictionary

    >>> is_dict({"a": 1})
    True
    >>> is_dict("abc")
    False
    >>> is_dict("123")
    False
    >>> is_dict([1, 2, 3])
    False

    """
    return isinstance(value, dict)

def recursively_find_numbers(obj):
    if is_number(obj):
        return int(obj)

    if is_array(obj):
        return sum(recursively_find_numbers(x) for x in obj)

    if is_dict(obj):
        return sum(recursively_find_numbers(x) for x in obj.values())

    return 0

def main(filename):
    """Read password and determine next good one"""
    with open(filename, 'r') as f:
        data = json.load(f)

    sum_of_numbers = recursively_find_numbers(data)
    print(sum_of_numbers)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
