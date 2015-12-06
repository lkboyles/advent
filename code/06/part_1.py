#!/usr/bin/env python3
"""Solve Day 6/Part 1 of the AdventOfCode

=============================
Day 6: Probably a Fire Hazard
=============================

Because your neighbors keep defeating you in the holiday house
decorating contest year after year, you've decided to deploy one
million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has
mailed you instructions on how to display the ideal lighting
configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the
lights at each corner are at 0,0, 0,999, 999,999, and 999,0. The
instructions include whether to turn on, turn off, or toggle various
inclusive ranges given as coordinate pairs. Each coordinate pair
represents opposite corners of a rectangle, inclusive; a coordinate
pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3
square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your
lights by doing the instructions Santa sent you in order.

For example:

- "turn on 0,0 through 999,999" would turn on (or leave on) every
  light.

- "toggle 0,0 through 999,0" would toggle the first line of 1000
  lights, turning off the ones that were on, and turning on the ones
  that were off.

- "turn off 499,499 through 500,500" would turn off (or leave off) the
  middle four lights.

After following the instructions, how many lights are lit?

"""

import enum
import re

import numpy as np

class ChristmasLightState(enum.IntEnum):
    OFF = 0
    ON = 1

class ChristmasLights(object):
    """Wrapper for manipulating Christmas lights

    The wrapper is constructed with the size of the (square) grid,
    with all lights initially off. It then supports several operations
    on slices of the lights, where a slice is defined as a range from
    the top left to the bottom right (in a 4-tuple (top, left, bottom,
    right)). The bottom-right range is inclusive, meaning the range
    (0, 0, 2, 2) represents a 3x3 grid of 9 lights.

    The operations supported are:

    - func:`turn_on` set all of the lights in the slice to on

    - func:`turn_off` set all of the lights in the slice to off

    - func:`toggle` set all of the lights that were on to off, and all
      the ones that were off to on.

    """
    def __init__(self, size=1000):
        """Create the grid and set every light to off"""
        self.size = size
        self.lights = ChristmasLightState.OFF * np.ones((self.size, self.size))

    def __eq__(self, other):
        return np.all(self.lights == other.lights)

    def copy(self):
        """Create a copy of the current state of the lights"""
        lights = ChristmasLights(self.size)
        lights.lights[:] = self.lights

        return lights

    def count_lit(self):
        """Return the number of lights that are on

        >>> l = ChristmasLights(4)
        >>> l.turn_on(0, 0, 2, 2)
        >>> l.count_lit()
        9

        """
        return int(np.sum(self.lights))

    def toggle(self, top, left, bottom, right):
        """Toggle lights in the given range

        >>> l = ChristmasLights(4)
        >>> l.toggle(0, 1, 3, 2)
        >>> expected = np.array([[0, 1, 1, 0]] * 4)
        >>> np.all(l.lights == expected)
        True

        >>> l.toggle(1, 0, 2, 3)
        >>> expected = np.array([
        ... [ 0,  1,  1,  0],
        ... [ 1,  0,  0,  1],
        ... [ 1,  0,  0,  1],
        ... [ 0,  1,  1,  0],
        ... ])
        >>> np.all(l.lights == expected)
        True

        """
        self._multiply_add_and_clamp(top, left, bottom, right, -1, 1)

    def turn_on(self, top, left, bottom, right):
        """Turn on lights in the given range

        >>> l = ChristmasLights(4)
        >>> l.turn_on(0, 0, 1, 1)
        >>> l.turn_on(2, 2, 3, 3)
        >>> expected = np.array([
        ... [  1,  1,  0,  0 ],
        ... [  1,  1,  0,  0 ],
        ... [  0,  0,  1,  1 ],
        ... [  0,  0,  1,  1 ],
        ... ])
        >>> np.all(l.lights == expected)
        True

        """
        self._multiply_add_and_clamp(top, left, bottom, right, 0, 1)

    def turn_off(self, top, left, bottom, right):
        """Turn off lights in the given range

        >>> l = ChristmasLights(4)
        >>> l.turn_on(0, 0, 3, 3)
        >>> l.turn_off(0, 0, 1, 1)
        >>> l.turn_off(2, 2, 3, 3)
        >>> expected = np.array([
        ... [  0,  0,  1,  1 ],
        ... [  0,  0,  1,  1 ],
        ... [  1,  1,  0,  0 ],
        ... [  1,  1,  0,  0 ],
        ... ])
        >>> np.all(l.lights == expected)
        True

        """
        self._multiply_add_and_clamp(top, left, bottom, right, 0, 0)

    def _multiply_add_and_clamp(self, top, left, bottom, right, mult, addend):
        """Perform operations on the given range and clamp values"""
        self.lights[top:bottom+1, left:right+1] *= mult
        self.lights[top:bottom+1, left:right+1] += addend

        mask = self.lights < ChristmasLightState.OFF
        self.lights[mask] = ChristmasLightState.OFF

def parse_and_update(lights, string):
    """Parse the given string and update the lights accordingly

    >>> base = ChristmasLights(4)
    >>> l = base.copy()
    >>> parse_and_update(l, "turn on 0,1 through 2,3")
    >>> l.count_lit()
    9
    >>> expected = base.copy()
    >>> expected.turn_on(0, 1, 2, 3)
    >>> l == expected
    True

    >>> base = ChristmasLights(4)
    >>> base.turn_on(0, 0, 3, 3)
    >>> l = base.copy()
    >>> parse_and_update(l, "turn off 0,1 through 2,3")
    >>> l.count_lit()
    7
    >>> expected = base.copy()
    >>> expected.turn_off(0, 1, 2, 3)
    >>> l == expected
    True

    >>> base = ChristmasLights(4)
    >>> base.turn_on(1, 0, 2, 3)
    >>> l = base.copy()
    >>> parse_and_update(l, "toggle 0,1 through 2,3")
    >>> l.count_lit()
    5
    >>> expected = base.copy()
    >>> expected.toggle(0, 1, 2, 3)
    >>> l == expected
    True

    >>> l = ChristmasLights(4)
    >>> parse_and_update(l, 'hello world')
    Traceback (most recent call last):
     ...
    ValueError: Unrecognized command

    """
    positions = try_parse_turn_on(string)
    if positions:
        lights.turn_on(*positions)
        return

    positions = try_parse_turn_off(string)
    if positions:
        lights.turn_off(*positions)
        return

    positions = try_parse_toggle(string)
    if positions:
        lights.toggle(*positions)
        return

    raise ValueError("Unrecognized command")

def try_parse_positions(string):
    """Try to parse the range or return None

    >>> try_parse_positions("0,0 through 999,999")
    (0, 0, 999, 999)
    >>> try_parse_positions("0,10 through 50,999")
    (0, 10, 50, 999)
    >>> try_parse_positions("0,10 through 50,999 ")
    (0, 10, 50, 999)
    >>> try_parse_positions("0,10 through ,999") is None
    True
    >>> try_parse_positions(" 0,10 through 10,999") is None
    True
    >>> try_parse_positions("000000") is None
    True

    """
    match = re.match(r'(\d+),(\d+) through (\d+),(\d+)', string)
    if not match:
        return None

    (top, left, bottom, right) = map(int, match.groups())

    return (top, left, bottom, right)

def try_parse_turn_on(string):
    """Try to parse the turn on command or return None

    >>> try_parse_turn_on("turn on 0,0 through 999,999")
    (0, 0, 999, 999)
    >>> try_parse_turn_on("turn off 0,0 through 999,999") is None
    True
    >>> try_parse_turn_on("turn on 0,0 through 999,") is None
    True

    """
    turn_on = re.match(r'turn on ', string)
    if not turn_on:
        return None

    positions = try_parse_positions(string[turn_on.end():])

    return positions

def try_parse_turn_off(string):
    """Try to parse the turn off command or return None

    >>> try_parse_turn_off("turn off 0,0 through 999,999")
    (0, 0, 999, 999)
    >>> try_parse_turn_off("turn on 0,0 through 999,999") is None
    True
    >>> try_parse_turn_off("turn off 0,0 through 999,") is None
    True

    """
    turn_off = re.match(r'turn off ', string)
    if not turn_off:
        return None

    positions = try_parse_positions(string[turn_off.end():])

    return positions

def try_parse_toggle(string):
    """Try to parse the toggle command or return None

    >>> try_parse_toggle("toggle 0,0 through 999,999")
    (0, 0, 999, 999)
    >>> try_parse_toggle("turn off 0,0 through 999,999") is None
    True
    >>> try_parse_toggle("toggle 0,0 through 999,") is None
    True

    """
    toggle = re.match(r'toggle ', string)
    if not toggle:
        return None

    positions = try_parse_positions(string[toggle.end():])

    return positions

def main(filename):
    """Read instructions for lights and count lit ones"""
    lights = ChristmasLights(1000)
    with open(filename, 'r') as f:
        for line in f:
            parse_and_update(lights, line)

    count = lights.count_lit()
    print(count)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
