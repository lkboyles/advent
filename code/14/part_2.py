#!/usr/bin/env python3
"""Solve Day 14/Part 2 of the AdventOfCode

"""

import collections

import part_1

def winning_reindeer_by_score(reindeers, time):
    scores = collections.defaultdict(int)
    for current_time in range(1, time):
        reindeer, _ = part_1.winning_reindeer(reindeers, current_time)
        scores[reindeer] += 1

    return max(scores.items(), key=lambda x: x[1])

def main(filename):
    """Read password and determine next good one"""
    with open(filename, 'r') as f:
        reindeers = part_1.read_reindeers(f)

    _, score = winning_reindeer_by_score(reindeers, 2503)

    print(score)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
