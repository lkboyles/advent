#!/usr/bin/env python3
"""Solve Day 14/Part 1 of the AdventOfCode

"""

import enum
import re
import itertools

class Reindeer(object):
    def __init__(self, name, top_speed, time_at_top_speed, time_resting):
        self.name = name
        self.top_speed = top_speed
        self.time_at_top_speed = time_at_top_speed
        self.time_resting = time_resting

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def distance_at_time(self, time):
        """x

        >>> r = Reindeer("comet", 14, 10, 127)
        >>> r.distance_at_time(0)
        0
        >>> r.distance_at_time(1)
        14
        >>> r.distance_at_time(2)
        28
        >>> r.distance_at_time(10)
        140
        >>> r.distance_at_time(1000)
        1120

        """
        full_cycle_time = self.time_at_top_speed + self.time_resting
        full_cycles = time // full_cycle_time
        full_cycle_distance = self.top_speed * self.time_at_top_speed * full_cycles

        remaining_time = time % full_cycle_time
        remaining_distance = self.top_speed * min(remaining_time, self.time_at_top_speed)

        total_distance = full_cycle_distance + remaining_distance

        return total_distance

def read_reindeers(lines):
    matcher = re.compile(r'([A-Za-z]+) .* ([0-9]+) .* ([0-9]+) .* ([0-9]+)')
    reindeers = []
    for line in lines:
        match = matcher.match(line)
        (name, top_speed, time_at_top_speed, time_resting) = match.groups()
        reindeer = Reindeer(
            name,
            int(top_speed),
            int(time_at_top_speed),
            int(time_resting),
        )

        reindeers.append(reindeer)

    return reindeers

def winning_reindeer(reindeers, time):
    distances = [
        (reindeer, reindeer.distance_at_time(time))
        for reindeer in reindeers
    ]

    return max(distances, key=lambda x: x[1])

def main(filename):
    """Read reindeer and determine distance of the winning reindeer after
    some time."""
    with open(filename, 'r') as f:
        reindeers = read_reindeers(f)

    _, distance = winning_reindeer(reindeers, 2503)

    print(distance)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
