#!/usr/bin/env python3
"""Solve Day 23/Part 1 of the AdventOfCode

"""

import re

class Program(object):
    def __init__(self, instructions):
        self.instructions = instructions
        self.state = State()

    def step(self):
        pc = self.state.program_counter
        if pc >= len(self.instructions):
            return False

        instruction = self.instructions[pc]
        instruction.step(self.state)

        return True

class State(object):
    def __init__(self):
        self.registers = [0] * 2
        self.program_counter = 0

class Instruction(object):
    def step(self, state):
        raise NotImplementedError()

class Half(Instruction):
    def __init__(self, register_number):
        self.register_number = register_number

    def step(self, state):
        state.registers[self.register_number] //= 2
        state.program_counter += 1

class Triple(Instruction):
    def __init__(self, register_number):
        self.register_number = register_number

    def step(self, state):
        state.registers[self.register_number] *= 3
        state.program_counter += 1

class Increment(Instruction):
    def __init__(self, register_number):
        self.register_number = register_number

    def step(self, state):
        state.registers[self.register_number] += 1
        state.program_counter += 1

class Jump(Instruction):
    def __init__(self, offset):
        self.offset = offset

    def step(self, state):
        state.program_counter += self.offset

class JumpIfEven(Instruction):
    def __init__(self, register_number, offset):
        self.register_number = register_number
        self.offset = offset

    def step(self, state):
        if state.registers[self.register_number] % 2 == 0:
            state.program_counter += self.offset
        else:
            state.program_counter += 1

class JumpIfOne(Instruction):
    def __init__(self, register_number, offset):
        self.register_number = register_number
        self.offset = offset

    def step(self, state):
        if state.registers[self.register_number] == 1:
            state.program_counter += self.offset
        else:
            state.program_counter += 1

def parse_instruction(line):
    register_mapping = { 'a': 0, 'b': 1 }

    match = re.match(r'hlf ([a-z])', line)
    if match:
        return Half(register_mapping[match.group(1)])

    match = re.match(r'tpl ([a-z])', line)
    if match:
        return Triple(register_mapping[match.group(1)])

    match = re.match(r'inc ([a-z])', line)
    if match:
        return Increment(register_mapping[match.group(1)])

    match = re.match(r'jmp ([+-]\d+)', line)
    if match:
        return Jump(int(match.group(1)))

    match = re.match(r'jie ([a-z]), ([+-]\d+)', line)
    if match:
        return JumpIfEven(register_mapping[match.group(1)], int(match.group(2)))

    match = re.match(r'jio ([a-z]), ([+-]\d+)', line)
    if match:
        return JumpIfOne(register_mapping[match.group(1)], int(match.group(2)))

    raise ValueError("Could not parse '{}'".format(line))

def main(filename):
    with open(filename, 'r') as f:
        instructions = []
        for line in f:
            instructions.append(parse_instruction(line))

    program = Program(instructions)
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
