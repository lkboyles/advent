#!/usr/bin/env python3
"""Solve Day 7/Part 1 of the AdventOfCode

"""

class Circuit(object):
    pass

class Wire(object):
    """Represent a wire and its value

    >>> w1 = Wire("a")
    >>> w1.set_value(10)
    >>> w1.get_value()
    10
    >>> w2 = Wire("b")
    >>> w2.set_value(15)
    >>> w2.get_value()
    15
    >>> w1.get_value()
    10

    """
    def __init__(self, name, value=None):
        self.name = name
        self.value = None

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

class Gate(object):
    """Represent a gate in the circuit with inputs and an output

    >>> in_wire = Wire("in")
    >>> out_wire = Wire("out")

    >>> g = Gate(num_inputs=1, operator_name="Foo")
    >>> g.set_inputs([in_wire])
    >>> g.set_output(out_wire)
    >>> repr(g)
    'Foo in -> out'

    """
    def __init__(self, num_inputs=0, operator_name="Gate"):
        self.inputs = []
        self.output = None
        self.num_inputs = num_inputs
        self.operator_name = operator_name

    def __repr__(self):
        """Return the representation of the gate

        >>> a = Wire("a")
        >>> b = Wire("b")
        >>> c = Wire("c")
        >>> g = Gate(operator_name="Foo")
        >>> g.set_output(c)

        >>> g.num_inputs = 0
        >>> g.set_inputs([])
        >>> repr(g)
        'Foo -> c'

        >>> g.num_inputs = 1
        >>> g.set_inputs([a])
        >>> repr(g)
        'Foo a -> c'

        >>> g.num_inputs = 2
        >>> g.set_inputs([a, b])
        >>> repr(g)
        'a Foo b -> c'

        >>> g.num_inputs = 3
        >>> g.set_inputs([a, a, b])
        >>> repr(g)
        Traceback (most recent call last):
         ...
        NotImplementedError

        """
        if self.num_inputs == 0:
            return "{} -> {}".format(self.operator_name, self.output.name)

        elif self.num_inputs == 1:
            return "{} {} -> {}".format(
                self.operator_name,
                self.inputs[0].name,
                self.output.name,
            )

        elif self.num_inputs == 2:
            return "{} {} {} -> {}".format(
                self.inputs[0].name,
                self.operator_name,
                self.inputs[1].name,
                self.output.name,
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

    def set_output(self, output):
        self.output = output

    def update(self):
        """Update the output value based on the gate's logic

        >>> wire = Wire("wire", 10)

        >>> g = Gate(num_inputs=0, operator_name="Foo")
        >>> g.get_output_value = lambda _: 1337
        >>> g.update()
        Traceback (most recent call last):
         ...
        ValueError: No output given

        >>> g.set_output(wire)
        >>> g.update()
        >>> wire.get_value()
        1337

        """
        if len(self.inputs) != self.num_inputs:
            raise ValueError("No inputs given")

        if self.output is None:
            raise ValueError("No output given")

        input_values = [i.get_value() for i in self.inputs]
        value = self.get_output_value(input_values)
        self.output.set_value(value)

    def get_output_value(self, input_values):
        raise NotImplementedError()

class Constant(Gate):
    """Gate which always returns a single value

    >>> wire = Wire("wire")
    >>> g = Constant(1337)
    >>> g.set_output(wire)
    >>> g.update()

    """
    def __init__(self, constant):
        Gate.__init__(self, num_inputs=0, operator_name=str(constant))
        self.constant = constant

    def get_output_value(self, input_values):
        return self.constant

class And(Gate):
    def __init__(self):
        Gate.__init__(self, num_inputs=2, operator_name="AND")

    def get_output_value(self, input_values):
        (first, second) = input_values
        return first & second

class Or(Gate):
    def __init__(self):
        Gate.__init__(self, num_inputs=2, operator_name="OR")

    def get_output_value(self, input_values):
        (first, second) = input_values
        return first | second

class Lshift(Gate):
    def __init__(self):
        Gate.__init__(self, num_inputs=2, operator_name="LSHIFT")

    def get_output_value(self, input_values):
        (first, second) = input_values
        return first << second

class Rshift(Gate):
    def __init__(self):
        Gate.__init__(self, num_inputs=2, operator_name="RSHIFT")

    def get_output_value(self, input_values):
        (first, second) = input_values
        return first >> second

class Not(Gate):
    def __init__(self):
        Gate.__init__(self, num_inputs=1, operator_name="NOT")

    def get_output_value(self, input_values):
        (first, ) = input_values
        return ~ first

def main(filename):
    """Read instructions for lights and count lit ones"""
    lights = ChristmasLights(1000)
    with open(filename, 'r') as f:
        for line in f:
            parse_and_update(lights, line)

    count = lights.count_lit()
    print(count)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
