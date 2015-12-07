#!/usr/bin/env python3
"""Solve Day 7/Part 1 of the AdventOfCode

=============================
Day 7: Some Assembly Required
=============================

This year, Santa brought little Bobby Tables a set of wires and
bitwise logic gates! Unfortunately, little Bobby is a little under the
recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a
16-bit signal (a number from 0 to 65535). A signal is provided to each
wire by a gate, another wire, or some specific value. Each wire can
only get a signal from one source, but can provide its signal to
multiple destinations. A gate provides no signal until all of its
inputs have a signal.

The included instructions booklet describe how to connect the parts
together: x AND y -> z means to connect wires x and y to an AND gate,
and then connect its output to wire z.

For example:

- "123 -> x" means that the signal 123 is provided to wire x.

- "x AND y -> z" means that the bitwise AND of wire x and wire y is
  provided to wire z.

- "p LSHIFT 2 -> q" means that the value from wire p is left-shifted
  by 2 and then provided to wire q.

- "NOT e -> f" means that the bitwise complement of the value from
  wire e is provided to wire f.

Other possible gates include OR (bitwise OR) and RSHIFT
(right-shift). If, for some reason, you'd like to emulate the circuit
instead, almost all programming languages (for example, C, JavaScript,
or Python) provide operators for these gates.

For example, here is a simple circuit:

    123 -> x
    456 -> y
    x AND y -> d
    x OR y -> e
    x LSHIFT 2 -> f
    y RSHIFT 2 -> g
    NOT x -> h
    NOT y -> i

After it is run, these are the signals on the wires:

    d: 72
    e: 507
    f: 492
    g: 114
    h: 65412
    i: 65079
    x: 123
    y: 456

In little Bobby's kit's instructions booklet (provided as your puzzle
input), what signal is ultimately provided to wire a?

"""

import re

class Circuit(object):
    """Represent a collection of wires with names"""
    def __init__(self):
        self.wires = {}

    def invalidate(self):
        for wire in self.wires.values():
            wire.invalidate()

    def get_wire(self, name):
        if name not in self.wires:
            wire = Wire(name)
            self.wires[name] = wire

        return self.wires[name]

class Wire(object):
    """Represent a wire and its value"""
    def __init__(self, name):
        self.name = name
        self.input_gate = None
        self.cached_value = None

    def __repr__(self):
        return "({!r}) -> {}".format(self.input_gate, self.name)

    def invalidate(self):
        self.cached_value = None

    def set_input_gate(self, gate):
        if gate is None:
            raise ValueError("Cannot set input gate to None")

        self.invalidate()
        self.input_gate = gate

    def get_value(self):
        if self.input_gate is None:
            raise ValueError("No input gate given for '{}'".format(self.name))

        if self.cached_value is None:
            self.cached_value = self.input_gate.get_value()

        return self.cached_value

class Gate(Wire):
    """Represent a gate in the circuit with inputs and an output

    >>> in_wire = Wire("in")
    >>> out_wire = Wire("out")

    >>> g = Gate(num_inputs=1, operator_name="Foo")
    >>> g.set_inputs([in_wire])
    >>> repr(g)
    'Foo in'

    """
    def __init__(self, num_inputs=0, operator_name="Gate"):
        self.inputs = []
        self.num_inputs = num_inputs
        self.operator_name = operator_name
        self.name = self.operator_name

    def __repr__(self):
        """Return the representation of the gate

        >>> a = Wire("a")
        >>> b = Wire("b")
        >>> g = Gate(operator_name="Foo")

        >>> g.num_inputs = 0
        >>> g.set_inputs([])
        >>> repr(g)
        'Foo'

        >>> g.num_inputs = 1
        >>> g.set_inputs([a])
        >>> repr(g)
        'Foo a'

        >>> g.num_inputs = 2
        >>> g.set_inputs([a, b])
        >>> repr(g)
        'a Foo b'

        >>> g.num_inputs = 3
        >>> g.set_inputs([a, a, b])
        >>> repr(g)
        Traceback (most recent call last):
         ...
        NotImplementedError

        """
        if self.num_inputs == 0:
            return "{}".format(self.operator_name)

        elif self.num_inputs == 1:
            return "{} {}".format(
                self.operator_name,
                self.inputs[0].name,
            )

        elif self.num_inputs == 2:
            return "{} {} {}".format(
                self.inputs[0].name,
                self.operator_name,
                self.inputs[1].name,
            )

        else:
            raise NotImplementedError()

    def set_inputs(self, inputs):
        """Set the inputs according to the gate's specification

        >>> wire = Wire("wire")
        >>> g = Gate(operator_name="Foo")

        >>> g.num_inputs = 1
        >>> g.set_inputs([wire])

        >>> g.set_inputs([wire, wire])
        Traceback (most recent call last):
         ...
        ValueError: len(inputs) expected to be 1

        """
        if len(inputs) != self.num_inputs:
            message = "len(inputs) expected to be {}".format(self.num_inputs)
            raise ValueError(message)

        self.inputs = inputs

    def get_value(self):
        """Update the output value based on the gate's logic

        >>> g = Gate(num_inputs=1, operator_name="Foo")
        >>> g._get_value = lambda input_values: 2*input_values[0]

        >>> wire = Wire("wire")
        >>> wire.set_input_gate(g)

        >>> wire.get_value()
        Traceback (most recent call last):
         ...
        ValueError: Not enough inputs given

        >>> in_wire = Wire("in")
        >>> in_wire.get_value = lambda: 10
        >>> g.set_inputs([in_wire])
        >>> wire.get_value()
        20

        """
        if len(self.inputs) < self.num_inputs:
            raise ValueError("Not enough inputs given")

        input_values = [i.get_value() for i in self.inputs]
        value = self._get_value(input_values)
        return value

    def _get_value(self, input_values):
        raise NotImplementedError()

class Constant(Gate):
    """Gate which always returns a single value

    >>> wire = Wire("wire")
    >>> g = Constant(1337)
    >>> wire.set_input_gate(g)
    >>> wire.get_value()
    1337

    """
    def __init__(self, constant):
        Gate.__init__(self, num_inputs=0, operator_name=str(constant))
        self.constant = constant

    def _get_value(self, input_values):
        return self.constant

class And(Gate):
    """Represent a "bitwise and" gate

    >>> g = And()
    >>> a = Constant(123)
    >>> b = Constant(456)
    >>> g.set_inputs([a, b])
    >>> g.get_value()
    72

    """
    def __init__(self):
        Gate.__init__(self, num_inputs=2, operator_name="AND")

    def _get_value(self, input_values):
        (first, second) = input_values
        return first & second

class Or(Gate):
    """Represent a "bitwise or" gate

    >>> g = Or()
    >>> a = Constant(123)
    >>> b = Constant(456)
    >>> g.set_inputs([a, b])
    >>> g.get_value()
    507

    """
    def __init__(self):
        Gate.__init__(self, num_inputs=2, operator_name="OR")

    def _get_value(self, input_values):
        (first, second) = input_values
        return first | second

class Lshift(Gate):
    """Represent a "bitwise left shift" gate

    >>> g = Lshift()
    >>> a = Constant(123)
    >>> b = Constant(2)
    >>> g.set_inputs([a, b])
    >>> g.get_value()
    492

    """
    def __init__(self):
        Gate.__init__(self, num_inputs=2, operator_name="LSHIFT")

    def _get_value(self, input_values):
        (first, second) = input_values
        return (first << second) & 0xFFFF

class Rshift(Gate):
    """Represent a "bitwise right shift" gate

    >>> g = Rshift()
    >>> a = Constant(456)
    >>> b = Constant(2)
    >>> g.set_inputs([a, b])
    >>> g.get_value()
    114

    """
    def __init__(self):
        Gate.__init__(self, num_inputs=2, operator_name="RSHIFT")

    def _get_value(self, input_values):
        (first, second) = input_values
        return first >> second

class Not(Gate):
    """Represent a "bitwise complement" gate

    >>> g = Not()
    >>> a = Constant(123)
    >>> g.set_inputs([a])
    >>> g.get_value()
    65412

    """
    def __init__(self):
        Gate.__init__(self, num_inputs=1, operator_name="NOT")

    def _get_value(self, input_values):
        (first, ) = input_values
        return (~ first) & 0xFFFF

def get_wire_for_name(circuit, name):
    try:
        as_int = int(name)
        return Constant(as_int)
    except ValueError:
        return circuit.get_wire(name)

def try_parse_no_operands_and_update(circuit, line):
    """Attempt to parse a statement with no operators

    >>> circuit = Circuit()
    >>> try_parse_no_operands_and_update(circuit, "123 -> a")
    (123) -> a
    >>> circuit.get_wire("a").get_value()
    123

    >>> try_parse_no_operands_and_update(circuit, "a -> b")
    ((123) -> a) -> b
    >>> circuit.get_wire("b").get_value()
    123

    >>> try_parse_no_operands_and_update(circuit, "Foo a -> b") is None
    True

    """
    no_operands = re.match(r'([a-z0-9]+) -> ([a-z]+)', line)
    if not no_operands:
        return None

    (source_name, target_name) = no_operands.groups()
    source = get_wire_for_name(circuit, source_name)
    target = get_wire_for_name(circuit, target_name)

    target.set_input_gate(source)

    return target

def try_parse_one_operand_and_update(circuit, line):
    """Attempt to parse a statement with one operand

    >>> circuit = Circuit()
    >>> try_parse_one_operand_and_update(circuit, "NOT 123 -> a")
    (NOT 123) -> a
    >>> circuit.get_wire("a").get_value()
    65412

    >>> try_parse_one_operand_and_update(circuit, "NOT a -> b")
    (NOT a) -> b
    >>> circuit.get_wire("b").get_value()
    123

    >>> try_parse_one_operand_and_update(circuit, "a FOO b -> c") is None
    True

    """
    one_operand = re.match(r'NOT ([a-z0-9]+) -> ([a-z]+)', line)
    if not one_operand:
        return None

    (source_name, target_name) = one_operand.groups()
    source = get_wire_for_name(circuit, source_name)
    target = get_wire_for_name(circuit, target_name)

    gate = Not()
    gate.set_inputs([source])

    target.set_input_gate(gate)

    return target

def try_parse_two_operands_and_update(circuit, line):
    """Attempt to parse a statement with two operands

    >>> circuit = Circuit()
    >>> try_parse_two_operands_and_update(circuit, "123 AND 456 -> a")
    (123 AND 456) -> a
    >>> circuit.get_wire("a").get_value()
    72

    >>> try_parse_two_operands_and_update(circuit, "123 OR 456 -> b")
    (123 OR 456) -> b
    >>> circuit.get_wire("b").get_value()
    507

    >>> try_parse_two_operands_and_update(circuit, "a AND b -> c")
    (a AND b) -> c
    >>> circuit.get_wire("c").get_value()
    72

    >>> try_parse_two_operands_and_update(circuit, "a 123 FOO b -> c") is None
    True

    """
    expr = r'([a-z0-9]+) (AND|OR|[LR]SHIFT) ([a-z0-9]+) -> ([a-z]+)'
    two_operands = re.match(expr, line)
    if not two_operands:
        return None

    (source1_name, operand, source2_name, target_name) = two_operands.groups()
    source1 = get_wire_for_name(circuit, source1_name)
    source2 = get_wire_for_name(circuit, source2_name)

    gate = None
    if operand == "AND":
        gate = And()
    elif operand == "OR":
        gate = Or()
    elif operand == "LSHIFT":
        gate = Lshift()
    elif operand == "RSHIFT":
        gate = Rshift()
    else:
        raise ValueError("Unknown operand: '{}'".format(operand))

    gate.set_inputs([source1, source2])

    target = get_wire_for_name(circuit, target_name)
    target.set_input_gate(gate)

    return target

def parse_line_and_update(circuit, line):
    """Parse line and update circuit layout

    >>> circuit = Circuit()
    >>> parse_line_and_update(circuit, "123 -> x")
    >>> parse_line_and_update(circuit, "456 -> y")
    >>> parse_line_and_update(circuit, "x AND y -> d")
    >>> parse_line_and_update(circuit, "x OR y -> e")
    >>> parse_line_and_update(circuit, "x LSHIFT 2 -> f")
    >>> parse_line_and_update(circuit, "y RSHIFT 2 -> g")
    >>> parse_line_and_update(circuit, "NOT x -> h")
    >>> parse_line_and_update(circuit, "NOT y -> i")

    >>> circuit.get_wire("d").get_value()
    72
    >>> circuit.get_wire("e").get_value()
    507
    >>> circuit.get_wire("f").get_value()
    492
    >>> circuit.get_wire("g").get_value()
    114

    >>> circuit.get_wire("h").get_value()
    65412
    >>> circuit.get_wire("i").get_value()
    65079
    >>> circuit.get_wire("x").get_value()
    123
    >>> circuit.get_wire("y").get_value()
    456

    """
    if try_parse_no_operands_and_update(circuit, line):
        return

    if try_parse_one_operand_and_update(circuit, line):
        return

    if try_parse_two_operands_and_update(circuit, line):
        return

    raise ValueError("Unrecognized line: '{}'".format(line))

def main(filename):
    """Read instructions for circuit and report wire 'a'"""
    circuit = Circuit()
    with open(filename, 'r') as f:
        for line in f:
            parse_line_and_update(circuit, line)

    wire_a = circuit.get_wire('a')
    print(wire_a.get_value())

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
