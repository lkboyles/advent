#!/usr/bin/env python3
"""Solve Day 13/Part 1 of the AdventOfCode

"""

import part_1

def main(filename):
    """Read password and determine next good one"""
    with open(filename, 'r') as f:
        ratings = part_1.read_ratings(f)

    for person in ratings.get_guest_list():
        ratings.add_rating("self", person, 0)
        ratings.add_rating(person, "self", 0)

    optimal_happiness = part_1.find_optimal_arrangement(ratings)
    print(optimal_happiness)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
