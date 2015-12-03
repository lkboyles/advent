#!/usr/bin/env python3
"""Solve Day 3/Part 1 of the AdventOfCode

=============================================
Day 3: Perfectly Spherical Houses in a Vacuum
=============================================

Santa is delivering presents to an infinite two-dimensional grid of
houses.

He begins by delivering a present to the house at his starting
location, and then an elf at the North Pole calls him via radio and
tells him where to move next. Moves are always exactly one house to
the north (^), south (v), east (>), or west (<). After each move, he
delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much
eggnog, and so his directions are a little off, and Santa ends up
visiting some houses more than once.

For example:

- ">" delivers presents to 2 houses: one at the starting location, and
  one to the east.

- "^>v<" delivers presents to 4 houses in a square, including twice to
  the house at his starting/ending location.

- "^v^v^v^v^v" delivers a bunch of presents to some very lucky
  children at only 2 houses.

How many houses receive at least one present?

"""

import collections

class Position:
    """Represent a position in two-dimensional space

    >>> Position(1, 2)
    Position(1, 2)
    >>> Position(0, 0).right()
    Position(0, 1)
    >>> Position(0, 0).down()
    Position(1, 0)
    >>> Position(0, 0).left()
    Position(0, -1)
    >>> Position(0, 0).up()
    Position(-1, 0)

    >>> a = Position(0, 0)
    >>> a.copy().up()
    Position(-1, 0)
    >>> a
    Position(0, 0)

    """
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)

    def __le__(self, other):
        return self.row < other.row and self.col < other.col

    def __repr__(self):
        return "Position({}, {})".format(self.row, self.col)

    def right(self):
        self.col += 1
        return self

    def down(self):
        self.row += 1
        return self

    def left(self):
        self.col -= 1
        return self

    def up(self):
        self.row -= 1
        return self

    def copy(self):
        return Position(self.row, self.col)

def get_total_houses_visited(presents_per_house):
    """Determine the total number of houses visited

    If a house has any presents, then it must have been visited at
    least once.

    >>> get_total_houses_visited({})
    0
    >>> get_total_houses_visited({Position(0, 0): 1})
    1
    >>> get_total_houses_visited({Position(0, 0): 2})
    1
    >>> get_total_houses_visited({Position(0, 0): 2, Position(0, 1): 1})
    2

    """
    return len(presents_per_house)

def get_presents_per_house(positions):
    """Return a mapping from positions to number of presents

    Santa will leave a new present at each position he is at. This
    method determines how many presents each house will get, which is
    equivalent to the number of times that Santa is at that position.

    >>> import pprint
    >>> p1 = Position(0, 0)
    >>> p2 = Position(0, 1)

    >>> get_presents_per_house([p1]) == {Position(0, 0): 1}
    True
    >>> get_presents_per_house([p1, p2]) == {Position(0, 0): 1, Position(0, 1): 1}
    True
    >>> get_presents_per_house([p1, p2, p1]) == {Position(0, 0): 2, Position(0, 1): 1}
    True

    """
    presents_per_house = collections.defaultdict(int)

    for position in positions:
        presents_per_house[position] += 1

    return presents_per_house

def decode_instruction(instruction, position):
    """Return a new position based on the instruction

    >>> start = Position(0, 0)
    >>> right = start.copy().right()
    >>> down = start.copy().down()
    >>> left = start.copy().left()
    >>> up = start.copy().up()

    >>> decode_instruction(">", start) == right
    True
    >>> decode_instruction("v", start) == down
    True
    >>> decode_instruction("<", start) == left
    True
    >>> decode_instruction("^", start) == up
    True

    >>> decode_instruction("X", start)
    Traceback (most recent call last):
     ...
    ValueError: Instruction must be one of '>v<^'

    """
    if instruction == ">":
        return position.copy().right()
    elif instruction == "v":
        return position.copy().down()
    elif instruction == "<":
        return position.copy().left()
    elif instruction == "^":
        return position.copy().up()
    else:
        raise ValueError("Instruction must be one of '>v<^'")

def get_positions(instructions):
    """Generate each new position based on the instructions

    >>> list(get_positions(""))
    [Position(0, 0)]
    >>> list(get_positions(">"))
    [Position(0, 0), Position(0, 1)]
    >>> list(get_positions(">v<^"))
    [Position(0, 0), Position(0, 1), Position(1, 1), Position(1, 0), Position(0, 0)]

    """
    position = Position(0, 0)
    yield position

    for instruction in instructions:
        position = decode_instruction(instruction, position)
        yield position

def main(filename):
    """Print the total number of houses visited based on the instructions"""
    with open(filename, 'r') as f:
        instructions = f.read()

    positions = get_positions(instructions)
    presents_per_house = get_presents_per_house(positions)
    total_houses_visited = get_total_houses_visited(presents_per_house)

    print(total_houses_visited)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
