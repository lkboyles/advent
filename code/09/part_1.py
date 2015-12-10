#!/usr/bin/env python3
"""Solve Day 9/Part 1 of the AdventOfCode

"""

import collections
import re

class World(object):
    """Represent a collection of distances between places"""
    def __init__(self):
        """Initialize the distance mapping

        >>> w = World()
        >>> w.distances['a']['b']
        inf
        >>> w.distances['a']['b'] = 13.0
        >>> w.distances['a']['b']
        13.0

        """
        def end_to_distance():
            return collections.defaultdict(lambda: float('inf'))

        def start_to_end():
            return collections.defaultdict(end_to_distance)

        self.distances = start_to_end()

    def read_file(self, fileobj):
        for line in fileobj:
            self.read_line(line)

    def read_line(self, line):
        """Reads a line from a file and adds to collection of distances

        >>> w = World()
        >>> w.read_line("foo to bar = 13")
        >>> w.distances["foo"]["bar"]
        13.0
        >>> w.distances["bar"]["foo"]
        13.0

        """
        expr = r'([a-zA-Z]+) to ([a-zA-Z]+) = ([0-9]+(?:\.[0-0]+)?)'
        match = re.match(expr, line)
        if not match:
            raise ValueError("Unrecognized line: '{}'".format(line))

        (start, end, distance_string) = match.groups()
        distance = float(distance_string)

        self.add_distance(start, end, distance)

    def add_distance(self, start, end, distance):
        """Adds a particular distance between a start an end

        >>> w = World()
        >>> w.add_distance("foo", "bar", 13)
        >>> w.distances["foo"]["bar"]
        13.0
        >>> w.distances["bar"]["foo"]
        13.0

        """
        self.distances[start][end] = float(distance)
        self.distances[end][start] = float(distance)

    def get_distances(self):
        locations = sorted(self.distances.keys())
        location_mapping = { v: i for i, v in enumerate(locations) }

        distances = np.zeros((len(locations), len(locations)))
        for i, start in enumerate(locations):
            for end, distance in self.distances[start].items():
                j = location_mapping[end]
                distances[i, j] = distance

        return (locations, distances)

def main(filename):
    """Read instructions for circuit and report wire 'a'"""
    total_actual_characters = 0
    total_code_characters = 0
    with open(filename, 'r') as f:
        for line in f:
            (actual, code) = count_characters(line)
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
