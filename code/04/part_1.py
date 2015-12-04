#!/usr/bin/env python3
"""Solve Day 4/Part 1 of the AdventOfCode

=================================
Day 4: The Ideal Stocking Stuffer
=================================

Santa needs help mining some AdventCoins (very similar to bitcoins) to
use as gifts for all the economically forward-thinking little girls
and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start
with at least five zeroes. The input to the MD5 hash is some secret
key (your puzzle input, given below) followed by a number in
decimal. To mine AdventCoins, you must find Santa the lowest positive
number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.

For example:

- If your secret key is "abcdef", the answer is 609043, because the
  MD5 hash of "abcdef609043" starts with five zeroes
  ("000001dbbfa..."), and it is the lowest such number to do so.

- If your secret key is "pqrstuv", the lowest number it combines with
  to make an MD5 hash starting with five zeroes is 1048970; that is,
  the MD5 hash of "pqrstuv1048970" looks like "000006136ef...."

Find the solution that makes the hash start with 5 zeros.

"""

import multiprocessing
import hashlib

class AdventCoinFinder(object):
    """Find the solution to a particular AdventCoin problem

    The AdventCoin problem is defined by the starting string and the
    number of zeros to find at the start of the hash. Additionally,
    this class accepts a number of processes to spread the computation
    across.

    >>> finder = AdventCoinFinder(1, "abcdef", 5)
    >>> finder.find_solution(609000)
    609043

    More specifically, this class functions as follows:

    - func:`find_solution` creates 1 process that produces batches of
      solutions (func:`solution_producer`) and multiple testing
      processes (func:`test_solutions`).

      It then waits on a `result_queue` which contains tuples of
      (solution, result), where solution is the integer that was
      tested, and result is a boolean for whether the solution is
      actually correct.

      If any correct solution is found, we set a flag that alerts the
      other processes to exit.

    - func:`test_solutions` gets batches of solutions from the
      `test_queue` that the func:`solution_producer` created, and
      checks each solution and pushes the result on the `result_queue`.

    - func:`solution_producer` ensures that there's always enough
      batches of solutions on the `test_queue`, pushing more on it if
      necessary.

    """
    def __init__(self, num_processes, starting_string, num_zeros_to_find):
        """Construct the finder and set up multiprocessing queues"""
        self.num_processes = num_processes
        self.starting_string = starting_string
        self.num_zeros_to_find = num_zeros_to_find

        # Holds all the batches of potential solutions
        self.test_queue = multiprocessing.Queue()

        # Holds all of the results from checking
        self.result_queue = multiprocessing.Queue()

        # Alerts the remaining processes to exit
        self.finished = multiprocessing.Event()

    def find_solution(self, starting_solution=0):
        """Find the solution to the problem

        This function starts all of the processes and waits until a
        solution is found by one of them.

        """
        # Creates the solution producer
        self.producer = multiprocessing.Process(
            target=self.solution_producer,
            args=(starting_solution, ),
        )

        # Creates a process for each of the solution checkers
        self.processes = [
            multiprocessing.Process(target=self.test_solutions, args=())
            for _ in range(self.num_processes)
        ]

        # Start the threads
        self.producer.start()
        for process in self.processes:
            process.start()

        # Get the solution
        solution = None
        while True:
            solution, result = self.result_queue.get()
            if result:
                break

        # Alert the processes to exit
        self.finished.set()

        # Wait for the processes to finish
        producer.join()
        for process in self.processes:
            process.join()

        return solution

    def test_solutions(self):
        """Check each solution to determine if it is correct

        This function reads potential solutions from the producer and
        checks if it is the correct solution to the current problem.

        """
        while True:
            # Check if we should exit now
            if self.finished.is_set():
                break

            # Get the next batch of solutions
            solutions = self.test_queue.get()

            for solution in solutions:
                # Test each solution to see if it is correct
                result = check_solution(
                    self.starting_string,
                    solution,
                    self.num_zeros_to_find,
                )

                # To limit the number of items on the result queue,
                # only push correct solutions.
                if result:
                    self.result_queue.put((solution, result))

    def solution_producer(self, starting_solution):
        """Produces potential solutions to check"""
        # The current solution to start the next batch on
        solution = starting_solution

        # We want the queue to be a certain size so that no process
        # will have to wait on the next one
        expected_queue_size = 2 * self.num_processes

        # Each batch of solutions should be this size
        solutions_per_batch = 64

        # Continue until we are signaled to stop
        while not self.finished.is_set():
            # If the queue is too small, we need to push the next
            # batch onto it
            while self.test_queue.qsize() < expected_queue_size:
                solutions = [
                    solution + i
                    for i in range(solutions_per_batch)
                ]

                self.test_queue.put(solutions)
                solution += solutions_per_batch

def check_solution(starting_string, solution, num_zeros_to_find):
    """Check if a potential solution is correct

    A solution is an integer, $n$, which when concatenated with a
    particular string will cause its MD5 hash to starting with a
    certain number of zeros. For example, with the starting string
    "foo" and potential solution $n=1337$, the string that will be
    hashed is "foo1337".

    >>> check_solution("abcdef", 609043, 5)
    True
    >>> check_solution("abcdef", 609042, 5)
    False

    >>> check_solution("pqrstuv", 1048970, 5)
    True
    >>> check_solution("pqrstuv", 1048969, 5)
    False

    """
    string = starting_string + str(solution)
    md5 = get_md5_hash(string)
    return md5.startswith("0" * num_zeros_to_find)

def get_md5_hash(string):
    """Find the MD5 hash of a given string

    >>> get_md5_hash("hello")
    '5d41402abc4b2a76b9719d911017c592'
    >>> get_md5_hash("")
    'd41d8cd98f00b204e9800998ecf8427e'

    """
    return hashlib.md5(string.encode("UTF-8")).hexdigest()

def main(filename, num_processes):
    """Find the 5-zero solution of the AdventCoin problem"""
    with open(filename, 'r') as f:
        starting_string = f.read().strip()

    if num_processes == 0:
        num_processes = multiprocessing.cpu_count()

    finder = AdventCoinFinder(
        num_processes,
        starting_string,
        5,
    )
    solution = finder.find_solution()

    print(solution)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--num-processes', type=int, default=0, nargs='?',
                        help='Number of testing processes (0 means cpu count)')
    args = parser.parse_args()

    main(**vars(args))
