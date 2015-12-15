#!/usr/bin/env python3
"""Solve Day 15/Part 1 of the AdventOfCode

=================================
Day 15: Science for Hungry People
=================================

Today, you set out on the task of perfecting your milk-dunking cookie
recipe. All you have to do is find the right balance of ingredients.

Your recipe leaves room for exactly 100 teaspoons of ingredients. You
make a list of the remaining ingredients you could use to finish the
recipe (your puzzle input) and their properties per teaspoon:

- capacity (how well it helps the cookie absorb milk)

- durability (how well it keeps the cookie intact when full of milk)

- flavor (how tasty it makes the cookie)

- texture (how it improves the feel of the cookie)

- calories (how many calories it adds to the cookie)

You can only measure ingredients in whole-teaspoon amounts accurately,
and you have to be accurate so you can reproduce your results in the
future. The total score of a cookie can be found by adding up each of
the properties (negative totals become 0) and then multiplying
together everything except calories.

For instance, suppose you have these two ingredients:

- Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8

- Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of
cinnamon (because the amounts of each ingredient must add up to 100)
would result in a cookie with the following properties:

- A capacity of 44*-1 + 56*2 = 68

- A durability of 44*-2 + 56*3 = 80

- A flavor of 44*6 + 56*-2 = 152

- A texture of 44*3 + 56*-1 = 76

Multiplying these together (68 * 80 * 152 * 76, ignoring calories for
now) results in a total score of 62842880, which happens to be the
best score possible given these ingredients. If any properties had
produced a negative total, it would have instead become zero, causing
the whole score to multiply to zero.

Given the ingredients in your kitchen and their properties, what is
the total score of the highest-scoring cookie you can make?

"""

import collections
import operator
import re

Ingredient = collections.namedtuple(
    'Ingredient',
    'name capacity durability flavor texture calories',
)

def read_ingredients(lines):
    """Return a list of ingredients based on the lines given

    >>> line = "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"
    >>> (cinnamon, ) = read_ingredients([line])
    >>> cinnamon
    Ingredient(name='Cinnamon', capacity=2, durability=3, flavor=-2, texture=-1, calories=3)

    """
    ingredients = []
    regexp = re.compile(
        r'(\w+): '
        r'capacity (-?\d+), '
        r'durability (-?\d+), '
        r'flavor (-?\d+), '
        r'texture (-?\d+), '
        r'calories (-?\d+)'
    )

    for line in lines:
        line = line.strip()
        match = regexp.match(line)

        (name, capacity, durability, flavor, texture, calories) = match.groups()
        ingredient = Ingredient(
            name,
            int(capacity),
            int(durability),
            int(flavor),
            int(texture),
            int(calories),
        )

        ingredients.append(ingredient)

    return ingredients

def score_ingredients(ingredients, counts):
    total = 1
    total *= max(0, sum(count * i.capacity for i, count in zip(ingredients, counts)))
    total *= max(0, sum(count * i.durability for i, count in zip(ingredients, counts)))
    total *= max(0, sum(count * i.flavor for i, count in zip(ingredients, counts)))
    total *= max(0, sum(count * i.texture for i, count in zip(ingredients, counts)))

    return total

def count_combinations(num_ingredients, total_amount, index=0, counts=None):
    """Yield all combinations for the counts of each ingredient

    >>> list(count_combinations(2, 3))
    [[0, 3], [1, 2], [2, 1], [3, 0]]

    """
    if counts is None:
        counts = [0] * num_ingredients

    if index == len(counts) - 1:
        counts[index] = total_amount

        yield counts[:]
        return

    for i in range(total_amount + 1):
        counts[index] = i

        remaining = total_amount - i

        yield from count_combinations(num_ingredients, remaining, index + 1, counts)

def find_best_combination(ingredients, total_amount):
    """Find the combination of ingredients that gives the highest score

    >>> ingredients = [
    ...     Ingredient("Butterscotch", -1, -2, 6, 3, 8),
    ...     Ingredient("Cinnamon", 2, 3, -2, -1, 3),
    ... ]
    >>> find_best_combination(ingredients, 100)
    (62842880, [44, 56])

    """
    best_score = 0
    best_counts = None
    for counts in count_combinations(len(ingredients), total_amount):
        score = score_ingredients(ingredients, counts)

        if score > best_score:
            best_score = score
            best_counts = counts

    return (best_score, best_counts)

def main(filename):
    """Read ingredients and print score of the best combination"""
    with open(filename, 'r') as f:
        ingredients = read_ingredients(f)

    score, counts = find_best_combination(ingredients, 100)
    print(score)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
