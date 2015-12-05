#!/usr/bin/env python3
"""Solve Day 5/Part 2 of the AdventOfCode

=============================================
Day 5: Doesn't He Have Intern-Elves For This?
=============================================

Realizing the error of his ways, Santa has switched to a better model
of determining whether a string is naughty or nice. None of the old
rules apply, as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

- It contains a pair of any two letters that appears at least twice in
  the string without overlapping, like xyxy (xy) or aabcdefgaa (aa),
  but not like aaa (aa, but it overlaps).

- It contains at least one letter which repeats with exactly one
  letter between them, like xyx, abcdefeghi (efe), or even aaa.

For example:

- qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice
  (qj) and a letter that repeats with exactly one letter between them
  (zxz).

- xxyxx is nice because it has a pair that appears twice and a letter
  that repeats with one between, even though the letters used by each
  rule overlap.

- uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat
  with a single letter between them.

- ieodomkazucvgmuy is naughty because it has a repeating letter with
  one between (odo), but no pair that appears twice.

How many strings are nice under these new rules?

"""

import re

def is_string_nice(string):
    """Determine if a string is nice (True) or naughty (False)

    >>> is_string_nice("qjhvhtzxzqqjkmpb")
    True
    >>> is_string_nice("xxyxx")
    True
    >>> is_string_nice("uurcxstgmygtbstg")
    False
    >>> is_string_nice("ieodomkazucvgmuy")
    False

    """
    return has_separated_repeats(string) and has_paired_characters(string)

def has_separated_repeats(string):
    """Check if string has repeated characters separated by another

    >>> has_separated_repeats("xyx")
    True
    >>> has_separated_repeats("abcdefeghi")
    True
    >>> has_separated_repeats("aaa")
    True
    >>> has_separated_repeats("")
    False
    >>> has_separated_repeats("abc")
    False
    >>> has_separated_repeats("aa")
    False

    """
    return bool(re.search(r'(.).\1', string))

def has_paired_characters(string):
    """Check if the string has a pair of characters that appears twice

    >>> has_paired_characters("xyxy")
    True
    >>> has_paired_characters("aabcdefgaa")
    True
    >>> has_paired_characters("aaa")
    False

    """
    return bool(re.search(r'(..).*\1', string))

def main(filename):
    """Count the number of nice lines in a file"""
    with open(filename, 'r') as f:
        count = sum(is_string_nice(line) for line in f)

        print(count)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
