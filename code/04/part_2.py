#!/usr/bin/env python3
"""Solve Day 4/Part 2 of the AdventOfCode

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

Find the solution that makes the hash start with 6 zeros.

"""

import multiprocessing

import part_1

def main(filename, num_processes):
    """Find the 6-zero solution of the AdventCoin problem"""
    with open(filename, 'r') as f:
        starting_string = f.read().strip()

    if num_processes == 0:
        num_processes = multiprocessing.cpu_count()

    finder = part_1.AdventCoinFinder(
        num_processes,
        starting_string,
        6,
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
