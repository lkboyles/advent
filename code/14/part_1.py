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

class ReindeerState(enum.IntEnum):
    FLYING = 0
    RESTING = 1

def calculate_distance(reindeer):
    """x

    >>> r = Reindeer("test", 1, 5, 2)
    >>> list(itertools.islice(calculate_distance(r), 10))
    [0, 1, 2, 3, 4, 5, 5, 5, 6, 7]

    """
    distance = 0
    (state, last_changed) = (ReindeerState.FLYING, 0)
    for current_time in itertools.count():
        yield distance

        if state == ReindeerState.FLYING:
            if current_time - last_changed == reindeer.time_at_top_speed - 1:
                (state, last_changed) = (ReindeerState.RESTING, current_time)

            distance += reindeer.top_speed
        elif state == ReindeerState.RESTING:
            if current_time - last_changed == reindeer.time_resting:
                (state, last_changed) = (ReindeerState.FLYING, current_time)

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

def distance_at_time(reindeer, max_time):
    """x

    >>> r = Reindeer("test", 1, 5, 2)
    >>> distance_at_time(r, 10)
    7

    >>> r = Reindeer("comet", 14, 10, 127)
    >>> distance_at_time(r, 1)
    14
    >>> distance_at_time(r, 10)
    140
    >>> distance_at_time(r, 11)
    140
    >>> distance_at_time(r, 1000)
    1120

    """
    for time, distance in enumerate(calculate_distance(reindeer)):
        if time == max_time:
            return distance

def distance_of_fastest_reindeer(reindeers, max_time):
    return max(distance_at_time(reindeer, max_time) for reindeer in reindeers)

def main(filename):
    """Read password and determine next good one"""
    with open(filename, 'r') as f:
        reindeers = read_reindeers(f)

        distance = distance_of_fastest_reindeer(reindeers, 2503)
        print(distance)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
