#!/usr/bin/env python3
"""Solve Day 19/Part 1 of the AdventOfCode

"""

class Replacements(object):
    def __init__(self):
        self.replacements = list()

    def add(self, line):
        """x

        >>> r = Replacements()
        >>> r.add('H => OH')
        >>> r.replacements
        [('H', 'OH')]

        """
        (before, after) = line.split(' => ')
        self.replacements.append((before, after))

    def possiblities_for(self, molecule):
        """x

        >>> r = Replacements()
        >>> r.add('H => HO')
        >>> r.add('H => OH')
        >>> r.add('O => HH')
        >>> list(r.replacements_for('HOH'))


        """
        for (before, after) in self.replacements:
            indices = [i.start() for i in re.finditer(before, molecule)]
            yield molecule.replace(before, after)

def all_combinations(p):
    n = len(p)
    for i in range(n):
        yield from itertools.combinations(p, i)

def main(filename):
    with open(filename, 'r') as f:
        replacements = Replacements()
        for line in f:
            line = line.strip()
            if line == "":
                break

            replacements.add(line)

        molecule = f.readline()

    possiblities = replacements.possiblities_for(molecule)

    unique_count = len(set(possiblities))

    print(unique_count)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
