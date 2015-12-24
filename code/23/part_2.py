#!/usr/bin/env python3
"""Solve Day 23/Part 2 of the AdventOfCode

"""

import part_1

def main(filename):
    with open(filename, 'r') as f:
        instructions = []
        instructions.append(part_1.parse_instruction('inc a'))

        for line in f:
            instructions.append(part_1.parse_instruction(line))

    program = part_1.Program(instructions)
    while program.step():
        pass

    register_b = program.state.registers[1]

    print(register_b)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
