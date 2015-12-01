#!/usr/bin/env python3
"""Solve Day 1/Part 1 of the AdventOfCode

Santa is trying to deliver presents in a large apartment building, but
he can't find the right floor - the directions he got are a little
confusing. He starts on the ground floor (floor 0) and then follows
the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a
closing parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he
will never find the top or bottom floors.

For example:

- "(())" and "()()" both result in floor 0.

- "(((" and "(()(()(" both result in floor 3.

- "))(((((" also results in floor 3.

- "())" and "))(" both result in floor -1 (the first basement level).

- ")))" and ")())())" both result in floor -3.

To what floor do the instructions take Santa?

"""

def main(filename):
    """Print the final floor that Santa ends at"""
    with open(filename, 'r') as f:
        data = f.read()

    open_paren = sum(1 for x in data if x == "(")
    close_paren = sum(1 for x in data if x == ")")

    floor = open_paren - close_paren

    print(floor)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
