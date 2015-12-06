#!/usr/bin/env python3
"""Solve Day 6/Part 2 of the AdventOfCode

=============================
Day 6: Probably a Fire Hazard
=============================

You just finish implementing your winning light pattern when you
realize you mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls;
each light can have a brightness of zero or more. The lights all start
at zero.

- The phrase "turn on" actually means that you should increase the
  brightness of those lights by 1.

- The phrase "turn off" actually means that you should decrease the
  brightness of those lights by 1, to a minimum of zero.

- The phrase "toggle" actually means that you should increase the
  brightness of those lights by 2.

For example:

- "turn on 0,0 through 0,0" would increase the total brightness by 1.

- "toggle 0,0 through 999,999" would increase the total brightness by
  2000000.

What is the total brightness of all lights combined after following
Santa's instructions?

"""

import numpy as np

import part_1

class RevisedChristmasLights(part_1.ChristmasLights):
    """Revised wrapper for manipulating Christmas lights

    The wrapper is constructed with the size of the (square) grid,
    with all lights initially off. It then supports several operations
    on slices of the lights, where a slice is defined as a range from
    the top left to the bottom right (in a 4-tuple (top, left, bottom,
    right)). The bottom-right range is inclusive, meaning the range
    (0, 0, 2, 2) represents a 3x3 grid of 9 lights.

    The operations supported are:

    - func:`turn_on` increase the brightness of all lights in the
      slice by 1.

    - func:`turn_off` decrease the brightness of all lights in the
      slice by 1, to a minimum of 0.

    - func:`toggle` increase the brightness of all lights in the slice
      by 2.

    """
    def __init__(self, size=1000):
        """Create the grid and set every light to off"""
        part_1.ChristmasLights.__init__(self, size)

    def brightness(self):
        """Return the total brightness of the lights

        >>> l = RevisedChristmasLights(4)
        >>> l.turn_on(0, 0, 2, 2)
        >>> l.turn_on(0, 0, 0, 0)
        >>> l.brightness()
        10

        """
        return int(np.sum(self.lights))

    def toggle(self, top, left, bottom, right):
        """Increment brightness of given lights by 2

        >>> l = RevisedChristmasLights(4)
        >>> l.toggle(0, 1, 3, 2)
        >>> expected = np.array([[0, 2, 2, 0]] * 4)
        >>> np.all(l.lights == expected)
        True

        >>> l.toggle(1, 0, 2, 3)
        >>> expected = np.array([
        ... [ 0,  2,  2,  0],
        ... [ 2,  4,  4,  2],
        ... [ 2,  4,  4,  2],
        ... [ 0,  2,  2,  0],
        ... ])
        >>> np.all(l.lights == expected)
        True

        """
        self._multiply_add_and_clamp(top, left, bottom, right, 1, 2)

    def turn_on(self, top, left, bottom, right):
        """Increment brightness of given lights by 1

        >>> l = RevisedChristmasLights(4)
        >>> l.turn_on(0, 0, 2, 2)
        >>> l.turn_on(1, 1, 3, 3)
        >>> expected = np.array([
        ... [  1,  1,  1,  0 ],
        ... [  1,  2,  2,  1 ],
        ... [  1,  2,  2,  1 ],
        ... [  0,  1,  1,  1 ],
        ... ])
        >>> np.all(l.lights == expected)
        True

        """
        self._multiply_add_and_clamp(top, left, bottom, right, 1, 1)

    def turn_off(self, top, left, bottom, right):
        """Decrease brightness of given lights by 1, to a minimum of 0

        >>> l = RevisedChristmasLights(4)
        >>> l.turn_on(0, 0, 3, 3)
        >>> l.turn_on(0, 0, 3, 3)
        >>> l.turn_off(0, 0, 2, 2)
        >>> l.turn_off(1, 1, 3, 3)
        >>> expected = np.array([
        ... [  1,  1,  1,  2 ],
        ... [  1,  0,  0,  1 ],
        ... [  1,  0,  0,  1 ],
        ... [  2,  1,  1,  1 ],
        ... ])
        >>> np.all(l.lights == expected)
        True

        """
        self._multiply_add_and_clamp(top, left, bottom, right, 1, -1)

def main(filename):
    """Read instructions for lights and count lit ones"""
    lights = RevisedChristmasLights(1000)
    with open(filename, 'r') as f:
        for line in f:
            part_1.parse_and_update(lights, line)

    brightness = lights.brightness()
    print(brightness)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
