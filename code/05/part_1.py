#!/usr/bin/env python3
"""Solve Day 5/Part 1 of the AdventOfCode

=============================================
Day 5: Doesn't He Have Intern-Elves For This?
=============================================

Santa needs help figuring out which strings in his text file are
naughty or nice.

A nice string is one with all of the following properties:

- It contains at least three vowels (aeiou only), like aei, xazegov,
  or aeiouaeiouaeiou.

- It contains at least one letter that appears twice in a row, like
  xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).

- It does not contain the strings ab, cd, pq, or xy, even if they are
  part of one of the other requirements.

For example:

- ugknbfddgicrmopn is nice because it has at least three vowels
  (u...i...o...), a double letter (...dd...), and none of the
  disallowed substrings.

- aaa is nice because it has at least three vowels and a double
  letter, even though the letters used by different rules overlap.

- jchzalrnumimnmhp is naughty because it has no double letter.

- haegwjzuvuyypxyu is naughty because it contains the string xy.

- dvszwmarrgswjxmb is naughty because it contains only one vowel.

How many strings are nice?

"""

import re

def is_string_nice(string):
    """Determine if a string is nice (True) or naughty (False)

    A nice string is defined by three properties:

    - At least 3 vowels

    - At least one pair of doubled letters

    - Lacks any of the naughty sequences

    >>> is_string_nice("ugknbfddgicrmopn")
    True
    >>> is_string_nice("aaa")
    True
    >>> is_string_nice("jchzalrnumimnmhp")
    False
    >>> is_string_nice("haegwjzuvuyypxyu")
    False
    >>> is_string_nice("dvszwmarrgswjxmb")
    False

    """
    has_three_vowels = count_vowels(string) >= 3
    has_double_letters = len(get_repeats(string)) > 0
    lacks_naughty_sequence = len(get_naughty_sequences(string)) == 0

    return has_three_vowels and has_double_letters and lacks_naughty_sequence

def get_naughty_sequences(string):
    """Get the occurrences of the naughty sequences in the string

    The naughty sequences are: "ab", "cd", "pq", and "xy".

    >>> get_naughty_sequences("")
    []
    >>> get_naughty_sequences("xxabxx")
    [(2, 'ab')]
    >>> get_naughty_sequences("-ab-cd-pq-xy-")
    [(1, 'ab'), (4, 'cd'), (7, 'pq'), (10, 'xy')]

    """
    matches = re.finditer(r'(?:ab|cd|pq|xy)', string)
    results = [
        (match.start(), match.group())
        for match in matches
    ]

    return results

def get_repeats(string):
    """Get the different repeated characters in the string

    A character is repeated if it occurs next to itself. For example,
    "aa" is repeated, because the letter A is next to the letter
    A. But "aba" has no repeats because the letter A is next to B.

    This function returns a list of tuples, where the first element is
    the index the repeat occurred at, and the second is the repeat
    that was found.

    Note: Due to the way the `re` module works, a string like "aaa"
    will only give show one repeat. Likewise, the string "aaaa" will
    only show 2 repeats.

    >>> get_repeats("abc")
    []
    >>> get_repeats("")
    []
    >>> get_repeats("aab")
    [(0, 'aa')]
    >>> get_repeats("aaa")
    [(0, 'aa')]

    """
    matches = re.finditer(r'(.)\1', string)
    results = [
        (match.start(), match.group())
        for match in matches
    ]

    return results

def count_vowels(string):
    """Count the number of vowels (aeiou) in the string

    >>> [(c, count_vowels(c)) for c in "aeioubc"]
    [('a', 1), ('e', 1), ('i', 1), ('o', 1), ('u', 1), ('b', 0), ('c', 0)]
    >>> count_vowels("")
    0
    >>> count_vowels("aaa")
    3

    """
    matches = re.findall(r'[aeiou]', string)

    return len(matches)

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
