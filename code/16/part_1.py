#!/usr/bin/env python3
"""Solve Day 16/Part 1 of the AdventOfCode

"""

import collections
import re

class Sue(object):
    def __init__(self, number, traits):
        self.number = number
        self.traits = traits

    @classmethod
    def from_line(cls, line):
        (number, rest) = re.match(r'Sue (\d+): (.*)', line).groups()
        traits = {}
        for (name, value) in re.findall(r'(\w+): (\d+)', rest):
            traits[name] = int(value)

        return cls(int(number), traits)

def compatible(master_sue, sue):
    assert len(master_sue.traits) >= len(sue.traits)

    for trait in sue.traits.keys():
        if master_sue.traits[trait] != sue.traits[trait]:
            return False

    return True

def main(filename):
    """Read ingredients and print score of the best combination"""
    with open(filename, 'r') as f:
        sues = [Sue.from_line(line) for line in f]

    master_traits = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    master_sue = Sue(-1, master_traits)

    for compatible_sue in filter(lambda x: compatible(master_sue, x), sues):
        print(compatible_sue.number)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
