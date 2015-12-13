#!/usr/bin/env python3
"""Solve Day 13/Part 1 of the AdventOfCode

"""

import collections
import re
import itertools

class HappinessRatings(object):
    def __init__(self):
        self.ratings = collections.defaultdict(lambda: collections.defaultdict(int))

    def add_rating(self, person, next_to, gained):
        self.ratings[person][next_to] = gained

    def get_rating(self, person, next_to):
        return self.ratings[person][next_to]

    def get_guest_list(self):
        return list(self.ratings.keys())

class Table(object):
    def __init__(self, arrangement):
        self.arrangement = arrangement

    def get_total_happiness(self, ratings):
        """x

        >>> ratings = HappinessRatings()
        >>> ratings.add_rating("A", "B", 4)
        >>> ratings.add_rating("A", "C", 3)
        >>> ratings.add_rating("B", "A", -2)
        >>> ratings.add_rating("B", "C", 5)
        >>> ratings.add_rating("C", "A", -1)

        >>> table = Table(["A", "B", "C"])
        >>> table.get_total_happiness(ratings)
        2

        """
        total_happiness = 0
        for i in range(len(self.arrangement)):
            person = self.arrangement[i]
            next_to = self.arrangement[i-1]
            total_happiness += ratings.get_rating(person, next_to)
            total_happiness += ratings.get_rating(next_to, person)

        return total_happiness

def read_ratings(lines):
    expr = r'([a-zA-Z]+) would (gain|lose) ([0-9]+) .* to ([a-zA-Z]+)'
    ratings = HappinessRatings()
    for line in lines:
        match = re.match(expr, line)
        (person, gain_or_lose, rating, next_to) = match.groups()
        rating = int(rating)
        rating *= 1 if gain_or_lose == "gain" else -1

        ratings.add_rating(person, next_to, rating)

    return ratings

def generate_arrangements(guest_list):
    for arrangement in itertools.permutations(guest_list):
        yield Table(arrangement)

def find_optimal_arrangement(ratings):
    guest_list = ratings.get_guest_list()
    best = 0
    for table in generate_arrangements(guest_list):
        happiness = table.get_total_happiness(ratings)
        best = max(best, happiness)

    return best

def main(filename):
    """Read password and determine next good one"""
    with open(filename, 'r') as f:
        ratings = read_ratings(f)

    optimal_happiness = find_optimal_arrangement(ratings)
    print(optimal_happiness)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
