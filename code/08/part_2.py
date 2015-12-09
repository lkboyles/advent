#!/usr/bin/env python3
"""Solve Day 8/Part 2 of the AdventOfCode

"""

# Comments and test code come later.
import part_1

def convert_to_code_representation(string):
    inner = string.replace("\\", "\\\\").replace('"', "\\\"")
    return '"{}"'.format(inner)

def main(filename):
    """Read instructions for circuit and report wire 'a'"""
    total_actual_characters = 0
    total_code_characters = 0
    with open(filename, 'r') as f:
        for line in f:
            code_line = convert_to_code_representation(line)
            (actual, code) = part_1.count_characters(code_line)
            total_actual_characters += actual
            total_code_characters += code

    delta = total_code_characters - total_actual_characters
    print(delta)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
