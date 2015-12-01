#!/usr/bin/env python3

"""Solve Day 1/Part 2 of the AdventOfCode

Santa is trying to deliver presents in a large apartment building, but
he can't find the right floor - the directions he got are a little
confusing. He starts on the ground floor (floor 0) and then follows
the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a
closing parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he
will never find the top or bottom floors.

find the position of the first character that causes him to enter the
basement (floor -1). The first character in the instructions has
position 1, the second character has position 2, and so on.

For example:

- ")" causes him to enter the basement at character position 1.

- "()())" causes him to enter the basement at character position 5.

What is the position of the character that causes Santa to first enter
the basement?

"""

def current_floor(data):
    """Yield the current floor based on the data"""
    floor = 0
    for char in data:
        if char == '(':
            floor += 1
        if char == ')':
            floor -= 1
        yield floor

def main(filename):
    """Print the first position where Santa goes to the basement"""
    with open(filename, 'r') as f:
        data = f.read()

    for position, floor in enumerate(current_floor(data), start=1):
        if floor == -1:
            break

    print(position)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
