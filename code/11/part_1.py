#!/usr/bin/env python3
"""Solve Day 11/Part 1 of the AdventOfCode

========================
Day 11: Corporate Policy
========================

Santa's previous password expired, and he needs help choosing a new
one.

To help him remember his new password after the old one expires, Santa
has devised a method of coming up with a password based on the
previous one. Corporate policy dictates that passwords must be exactly
eight lowercase letters (for security reasons), so he finds his new
password by incrementing his old password string repeatedly until it
is valid.

Incrementing is just like counting with numbers: xx, xy, xz, ya, yb,
and so on. Increase the rightmost letter one step; if it was z, it
wraps around to a, and repeat with the next letter to the left until
one doesn't wrap around.

Unfortunately for Santa, a new Security-Elf recently started, and he
has imposed some additional password requirements:

- Passwords must include one increasing straight of at least three
  letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip
  letters; abd doesn't count.

- Passwords may not contain the letters i, o, or l, as these letters
  can be mistaken for other characters and are therefore confusing.

- Passwords must contain at least two different, non-overlapping pairs
  of letters, like aa, bb, or zz.

For example:

- hijklmmn meets the first requirement (because it contains the
  straight hij) but fails the second requirement requirement (because
  it contains i and l).

- abbceffg meets the third requirement (because it repeats bb and ff)
  but fails the first requirement.

- abbcegjk fails the third requirement, because it only has one double
  letter (bb).

- The next password after abcdefgh is abcdffaa.

- The next password after ghijklmn is ghjaabcc, because you eventually
  skip all the passwords that start with ghi..., since i is not
  allowed.

Given Santa's current password, what should his next password be?

"""

def increment_password(password_values, length=None):
    """x

    >>> def runner(string, length=None):
    ...   values = [ord(c) for c in string]
    ...   increment_password(values, length)
    ...   return ''.join(chr(value) for value in values)

    >>> runner('abc')
    'abd'
    >>> runner('xyz')
    'xza'
    >>> runner('xzz')
    'yaa'
    >>> runner('xzz', length=len('xz'))
    'yaz'

    """
    if length is None:
        length = len(password_values)

    for i in range(length):
        password_values[length-i-1] += 1
        if password_values[length-i-1] <= ord('z'):
            break

        password_values[length-i-1] = ord('a')

def get_past_confusing_letters(password_values):
    """x

    >>> def runner(string):
    ...   values = [ord(c) for c in string]
    ...   get_past_confusing_letters(values)
    ...   return ''.join(chr(v) for v in values)

    >>> runner('hixyz')
    'hjaaa'

    """
    confusing = [ord('i'), ord('o'), ord('l')]
    for i in range(len(password_values)):
        if password_values[i] in confusing:
            increment_password(password_values, length=i+1)

            for j in range(i+1, len(password_values)):
                password_values[j] = ord('a')


def find_good_password(password):
    """x

    >>> find_good_password('abcdefgh')
    'abcdffaa'
    >>> find_good_password('ghijklmn')
    'ghjaabcc'

    """
    password_values = [ord(c) for c in password]
    while True:
        increment_password(password_values)

        if meets_requirements(password_values):
            break

        if not lacks_confusing_letters(password_values):
            get_past_confusing_letters(password_values)

    return ''.join(chr(value) for value in password_values)

def meets_requirements(password_values):
    """x

    >>> meets_requirements([ord(c) for c in 'hijklmmn'])
    False
    >>> meets_requirements([ord(c) for c in 'abbceffg'])
    False
    >>> meets_requirements([ord(c) for c in 'abcdffaa'])
    True

    """

    if not has_ascending_sequence(password_values):
        return False

    if not lacks_confusing_letters(password_values):
        return False

    if not contains_two_pairs_of_letters(password_values):
        return False

    return True

def has_ascending_sequence(password_values):
    count = 1
    for i in range(1, len(password_values)):
        prev = password_values[i - 1]
        cur = password_values[i]

        if cur == prev + 1:
            count += 1

            if count == 3:
                return True
        else:
            count = 1

    return False

def lacks_confusing_letters(password_values):
    confusing = [ord('i'), ord('o'), ord('l')]
    for c in confusing:
        if c in password_values:
            return False

    return True

def contains_two_pairs_of_letters(password_values):
    num_pairs = 0
    skip_flag = False
    for i in range(1, len(password_values)):
        if skip_flag:
            skip_flag = False
            continue

        prev = password_values[i - 1]
        cur = password_values[i]

        if prev == cur:
            num_pairs += 1
            skip_flag = True

    return num_pairs >= 2

def main(filename):
    """Read password and determine next good one"""
    with open(filename, 'r') as f:
        string = f.read().strip()

    password = find_good_password(string)
    print(password)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
