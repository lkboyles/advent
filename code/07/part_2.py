#!/usr/bin/env python3
"""Solve Day 7/Part 1 of the AdventOfCode

=============================
Day 7: Some Assembly Required
=============================

Now, take the signal you got on wire a, override wire b to that
signal, and reset the other wires (including wire a).

What new signal is ultimately provided to wire a?

"""

import part_1

def main(filename):
    """Read instructions for circuit and report wire 'a'"""
    circuit = part_1.Circuit()
    with open(filename, 'r') as f:
        for line in f:
            part_1.parse_line_and_update(circuit, line)

    wire_a = circuit.get_wire('a')

    part_1.parse_line_and_update(circuit, '{} -> b'.format(wire_a.get_value()))

    circuit.invalidate()

    print(wire_a.get_value())

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
