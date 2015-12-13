#!/usr/bin/env python3
"""Solve Day 12/Part 2 of the AdventOfCode

"""

import json

import part_1

def recursively_find_numbers(obj):
    if part_1.is_number(obj):
        return int(obj)

    if part_1.is_array(obj):
        return sum(recursively_find_numbers(x) for x in obj)

    if part_1.is_dict(obj):
        if "red" in obj.values():
            return 0

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
