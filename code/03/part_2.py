#!/usr/bin/env python3
"""Solve Day 3/Part 2 of the AdventOfCode

=============================================
Day 3: Perfectly Spherical Houses in a Vacuum
=============================================

Last year, Santa delivered presents to an infinite two-dimensional
grid of houses.

He began by delivering a present to the house at his starting
location, and then an elf at the North Pole called him via radio and
told him where to move next. Moves are always exactly one house to the
north (^), south (v), east (>), or west (<). After each move, he
delivered another present to the house at his new location.

However, the elf back at the north pole has had a little too much
eggnog, and so his directions are a little off, and Santa ends up
visiting some houses more than once.

This year, to speed up the process, Santa creates a robot version of
himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two
presents to the same starting house), then take turns moving based on
instructions from the elf, who is eggnoggedly reading from the same
script as the previous year.

For example:

- "^v" delivers presents to 3 houses, because Santa goes north, and
  then Robo-Santa goes south.

- "^>v<" now delivers presents to 3 houses, and Santa and Robo-Santa
  end up back where they started.

- "^v^v^v^v^v" now delivers presents to 11 houses, with Santa going
  one direction and Robo-Santa going the other.

This year, how many houses receive at least one present?

"""
import collections

import part_1

def merge_presents_per_house(santa_presents, robot_presents):
    """Combine the presents Santa and Robot Santa delivered

    >>> from part_1 import Position
    >>> santa_presents = {Position(0, 0): 1, Position(0, 1): 1}
    >>> robot_presents = {Position(0, 0): 1, Position(1, 0): 1}
    >>> expected = {Position(0, 0): 2, Position(0, 1): 1, Position(1, 0): 1}

    >>> merge_presents_per_house(santa_presents, robot_presents) == expected
    True

    """

    total_presents_per_house = collections.defaultdict(int)

    for key, value in santa_presents.items():
        total_presents_per_house[key] += value

    for key, value in robot_presents.items():
        total_presents_per_house[key] += value

    return total_presents_per_house

def split_up_instructions(instructions):
    """Divide instructions between Santa and Robot Santa

    Santa gets the 0th, 2nd, 4th, etc., while Robot Santa gets the
    1st, 3rd, 5th, etc. instructions.

    >>> split_up_instructions('')
    ('', '')
    >>> split_up_instructions('><')
    ('>', '<')
    >>> split_up_instructions('><^')
    ('>^', '<')
    >>> split_up_instructions('><^v')
    ('>^', '<v')

    """
    santa_instructions = instructions[0::2]
    robot_instructions = instructions[1::2]

    return (santa_instructions, robot_instructions)

def main(filename):
    """Print the total number of houses visited based on the instructions"""
    with open(filename, 'r') as f:
        instructions = f.read()

    santa_instructions, robot_instructions = split_up_instructions(instructions)

    santa_positions = part_1.get_positions(santa_instructions)
    robot_positions = part_1.get_positions(robot_instructions)

    santa_presents_per_house = part_1.get_presents_per_house(santa_positions)
    robot_presents_per_house = part_1.get_presents_per_house(robot_positions)

    presents_per_house = merge_presents_per_house(
        santa_presents_per_house,
        robot_presents_per_house,
    )

    total_houses_visited = part_1.get_total_houses_visited(presents_per_house)

    print(total_houses_visited)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
