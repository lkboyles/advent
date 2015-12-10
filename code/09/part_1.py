#!/usr/bin/env python3
"""Solve Day 9/Part 1 of the AdventOfCode

============================
Day 9: All in a Single Night
============================

Every year, Santa manages to deliver all of his presents in a single
night.

This year, however, he has some new locations to visit; his elves have
provided him the distances between every pair of locations. He can
start and end at any two (different) locations he wants, but he must
visit each location exactly once. What is the shortest distance he can
travel to achieve this?

For example, given the following distances:

- London to Dublin = 464

- London to Belfast = 518

- Dublin to Belfast = 141

The possible routes are therefore:

- Dublin -> London -> Belfast = 982

- London -> Dublin -> Belfast = 605

- London -> Belfast -> Dublin = 659

- Dublin -> Belfast -> London = 659

- Belfast -> Dublin -> London = 605

- Belfast -> London -> Dublin = 982

The shortest of these is "London -> Dublin -> Belfast = 605", and so
the answer is 605 in this example.

What is the distance of the shortest route?

"""

import collections
import re

import numpy as np

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

    def get_locations(self):
        return set(self.distances.keys())

    def get_adjacent_locations(self, start):
        if start is None:
            return set(self.distances.keys())

        return set(self.distances[start].keys())

    def get_distance(self, start, end):
        """x

        >>> w = standard_test_world()
        >>> w.get_distance("A", "B")
        1.0
        >>> w.get_distance("D", "A")
        4.0
        >>> w.get_distance(None, "A")
        0
        >>> w.get_distance("A", None)
        0

        """
        if start is None or end is None:
            return 0

        return self.distances[start][end]

    def get_distances(self):
        """Get a list of location names and a matrix of distances

        >>> w = World()
        >>> w.read_line("A to B = 1")
        >>> w.read_line("B to C = 2")
        >>> w.read_line("C to D = 3")
        >>> w.read_line("D to A = 4")

        >>> locations, distances = w.get_distances()
        >>> locations
        ['A', 'B', 'C', 'D']
        >>> distances
        array([[ inf,   1.,  inf,   4.],
               [  1.,  inf,   2.,  inf],
               [ inf,   2.,  inf,   3.],
               [  4.,  inf,   3.,  inf]])

        """
        locations = sorted(self.distances.keys())
        location_mapping = { v: i for i, v in enumerate(locations) }

        distances = float('inf') * np.ones((len(locations), len(locations)))
        for i, start in enumerate(locations):
            for end, distance in self.distances[start].items():
                j = location_mapping[end]
                distances[i, j] = distance

        return (locations, distances)

def standard_test_world():
    world = World()
    world.read_line("A to B = 1")
    world.read_line("B to C = 2")
    world.read_line("C to D = 3")
    world.read_line("D to A = 4")

    return world

def get_candidates(world, start, visited):
    """Get a set of adjacent locations to start that haven't been visited

    >>> world = standard_test_world()
    >>> start = None
    >>> visited = set()
    >>> sorted(get_candidates(world, start, visited))
    ['A', 'B', 'C', 'D']

    >>> world = standard_test_world()
    >>> start = 'A'
    >>> visited = set()
    >>> sorted(get_candidates(world, start, visited))
    ['B', 'D']

    >>> world = standard_test_world()
    >>> start = 'A'
    >>> visited = {'B'}
    >>> sorted(get_candidates(world, start, visited))
    ['D']

    """
    adjacent = world.get_adjacent_locations(start)
    candidates = adjacent - visited

    return candidates

def find_extreme_distance_from_location(world, start, visited, minimum=True):
    """x

    >>> world = standard_test_world()
    >>> start = None
    >>> visited = set()
    >>> find_extreme_distance_from_location(world, start, visited, minimum=True)
    6.0
    >>> find_extreme_distance_from_location(world, start, visited, minimum=False)
    9.0

    """
    # Add the current location to the set of visited locations unless
    # we are choosing the first location to start with.
    if start is not None:
        visited = visited | {start}

    # Get locations that are adjacent and not visited
    candidates = get_candidates(world, start, visited)

    # If there are no candidates, then we are done
    if len(candidates) == 0:
        # If we haven't visited everyone, then return a value which
        # means "this distance should be discarded"
        if len(visited) != len(world.get_locations()):
            return float('inf') if minimum else -float('inf')

        # Otherwise, we've reached every node, so the distance from
        # the current node to all remaining nodes is 0.
        return 0

    # Start the extreme at a value which will always be discarded when
    # a distance is calculated.
    extreme_distance = float('inf') if minimum else -float('inf')

    # Test every candidate
    for candidate in candidates:
        # Get the distance from the current node to the candidate
        # node, and then determine the extreme path length from the
        # candidate node
        distance = world.get_distance(start, candidate)
        distance += find_extreme_distance_from_location(
            world,
            candidate,
            visited,
            minimum,
        )

        # Update the extreme distance according to whether we want to
        # find the minimum or maximum distances.
        if minimum:
            extreme_distance = min(distance, extreme_distance)
        else:
            extreme_distance = max(distance, extreme_distance)

    return extreme_distance

def find_extreme_distance(world, minimum=True):
    """Find the extreme (minimum or maximum) distance for a given world"""
    start = None
    visited = set()
    distance = find_extreme_distance_from_location(
        world,
        start,
        visited,
        minimum,
    )

    return distance

def main(filename):
    """Read instructions for circuit and report wire 'a'"""
    world = World()
    with open(filename, 'r') as f:
        world.read_file(f)

    shortest_distance = find_extreme_distance(world, minimum=True)
    print(shortest_distance)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
