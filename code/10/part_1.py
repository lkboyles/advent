#!/usr/bin/env python3
"""Solve Day 10/Part 1 of the AdventOfCode

=============================
Day 10: Elves Look, Elves Say
=============================

Today, the Elves are playing a game called look-and-say. They take
turns making sequences by reading aloud the previous sequence and
using that reading as the next sequence. For example, 211 is read as
"one two, two ones", which becomes 1221 (1 2, 2 1s).

Look-and-say sequences are generated iteratively, using the previous
value as input for the next step. For each step, take the previous
value, and replace each run of digits (like 111) with the number of
digits (3) followed by the digit itself (1).

For example:

- 1 becomes 11 (1 copy of digit 1).

- 11 becomes 21 (2 copies of digit 1).

- 21 becomes 1211 (one 2 followed by one 1).

- 1211 becomes 111221 (one 1, one 2, and two 1s).

- 111221 becomes 312211 (three 1s, two 2s, and one 1).

Starting with the digits in your puzzle input, apply this process 40
times. What is the length of the result?

"""

def look_and_say_step(look_and_say_iterator):
    """x

    >>> ''.join(look_and_say_step("1"))
    '11'
    >>> ''.join(look_and_say_step("11"))
    '21'
    >>> ''.join(look_and_say_step("21"))
    '1211'
    >>> ''.join(look_and_say_step("1211"))
    '111221'

    """
    prev = None
    count = 0
    for character in look_and_say_iterator:
        assert (len(character) == 1)
        if prev is None:
            prev = character
            count = 1
        elif character != prev:
            yield str(count)
            yield prev

            prev = character
            count = 1
        else:
            count += 1

    yield str(count)
    yield prev

def main(filename):
    """Read string and apply look-and-say algorithm 40 times"""
    with open(filename, 'r') as f:
        string = f.read().strip()

    for _ in range(40):
        string = look_and_say_step(string)

    length = sum(1 for _ in string)
    print(length)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
