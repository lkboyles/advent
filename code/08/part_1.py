#!/usr/bin/env python3
"""Solve Day 8/Part 1 of the AdventOfCode

"""

# Comments and test code come later.

def count_characters(string):
    def get_character():
        nonlocal string
        character = string[0]
        string = string[1:]
        return character

    def consume(characters):
        nonlocal string
        if string[0] in characters:
            return False

        string = string[1:]
        return True

    def starting_quote():
        nonlocal num_code_characters
        character = get_character()
        if character == '"':
            num_code_characters += 1
            return any_character

        raise ValueError("Expected starting '\"', got {}".format(character))

    def any_character():
        nonlocal num_code_characters, num_actual_characters
        character = get_character()
        num_code_characters += 1
        if character == "\\":
            return escaped

        if character == '"':
            return None

        num_actual_characters += 1
        return any_character

    def escaped():
        nonlocal num_code_characters, num_actual_characters
        character = get_character()
        num_code_characters += 1
        if character == '"':
            num_actual_characters += 1
            return any_character

        if character == "\\":
            num_actual_characters += 1
            return any_character

        if character == 'x':
            return hexadecimal_first

        raise ValueError("Expected escaped sequence, got '{}'".format(character))

    def hexadecimal_first():
        nonlocal num_code_characters
        num_code_characters += 1
        _ = get_character()
        return hexadecimal_second

    def hexadecimal_second():
        nonlocal num_code_characters, num_actual_characters
        num_code_characters += 1
        num_actual_characters += 1
        _ = get_character()
        return any_character

    (num_actual_characters, num_code_characters) = (0, 0)

    state = starting_quote
    while state is not None:
        state = state()

    return num_actual_characters, num_code_characters

def main(filename):
    """Read instructions for circuit and report wire 'a'"""
    total_actual_characters = 0
    total_code_characters = 0
    with open(filename, 'r') as f:
        for line in f:
            (actual, code) = count_characters(line)
            total_actual_characters += actual
            total_code_characters += code

    delta = total_code_characters - total_actual_characters
    print(delta)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
