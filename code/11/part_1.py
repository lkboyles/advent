#!/usr/bin/env python3
"""Solve Day 11/Part 1 of the AdventOfCode

"""

import re

class Character(object):
    def __init__(self, character):
        self._min_value = ord('a') - ord('a')
        self._max_value = ord('z') - ord('a')
        self.value = ord(character) - ord('a')

    def __str__(self):
        """x

        >>> c = Character('a')
        >>> str(c)
        'a'

        >>> c = Character('z')
        >>> str(c)
        'z'

        """
        return chr(ord('a') + self.value)

    def increment(self):
        """x

        >>> c = Character('a')
        >>> c.increment()
        False
        >>> str(c)
        'b'

        >>> c = Character('z')
        >>> c.increment()
        True
        >>> str(c)
        'a'

        """
        self.value += 1
        if self.value > self._max_value:
            self.value = 0
            return True

        return False

class Password(object):
    def __init__(self, initial_password):
        """x

        >>> p = Password("foo")
        >>> str(p)
        'foo'

        """
        self.value = [Character(c) for c in reversed(initial_password)]
        self.reverse = list(reversed(self.value))

    def __str__(self):
        return ''.join(str(c) for c in self.reverse)

    def increment(self):
        """x

        >>> p = Password('xz')
        >>> p.increment()
        >>> str(p)
        'ya'

        >>> p = Password('xzz')
        >>> p.increment()
        >>> str(p)
        'yaa'

        """

        for character in self.value:
            if not character.increment():
                break

def find_good_password(password_string):
    """x

    >>> find_good_password('abcdefgh')
    'abcdffaa'
    >>> find_good_password('ghijklmn')
    'ghjaabcc'

    """
    password = Password(password_string)

    while True:
        password.increment()

        if meets_requirements(password):
            break

    return str(password)

def meets_requirements(password):
    """x

    >>> meets_requirements(Password('hijklmmn'))
    False
    >>> meets_requirements(Password('abbceffg'))
    False
    >>> meets_requirements(Password('abcdffaa'))
    True

    """
    string = str(password)

    if not has_ascending_sequence(string):
        return False

    if not lacks_confusing_letters(string):
        return False

    if not contains_two_pairs_of_letters(string):
        return False

    return True

def has_ascending_sequence(password):
    prev = ord(password[0])
    count = 1
    for character in password[1:]:
        value = ord(character)
        if value == prev + 1:
            count += 1
            prev = value

            if count == 3:
                return True
        else:
            count = 1

    return False

def lacks_confusing_letters(password):
    confusing = ['i', 'o', 'l']
    for c in confusing:
        if c in password:
            return False

    return True

def contains_two_pairs_of_letters(password):
    return len(re.findall(r'(.)\1', password)) >= 2

def main(filename):
    """Read string and apply look-and-say algorithm 40 times"""
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
