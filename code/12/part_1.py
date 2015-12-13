#!/usr/bin/env python3
"""Solve Day 12/Part 1 of the AdventOfCode

"""

import json

def is_number(value):
    try:
        _ = int(value)
        return True
    except TypeError:
        return False
    except ValueError:
        return False

def is_array(value):
    return isinstance(value, list)

def is_dict(value):
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
