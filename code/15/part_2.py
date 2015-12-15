#!/usr/bin/env python3
"""Solve Day 15/Part 2 of the AdventOfCode

=================================
Day 15: Science for Hungry People
=================================

Your cookie recipe becomes wildly popular! Someone asks if you can
make another recipe that has exactly 500 calories per cookie (so they
can use it as a meal replacement). Keep the rest of your award-winning
process the same (100 teaspoons, same ingredients, same scoring
system).

For example, given the ingredients above, if you had instead selected
40 teaspoons of butterscotch and 60 teaspoons of cinnamon (which still
adds to 100), the total calorie count would be 40*8 + 60*3 = 500. The
total score would go down, though: only 57600000, the best you can do
in such trying circumstances.

Given the ingredients in your kitchen and their properties, what is
the total score of the highest-scoring cookie you can make with a
calorie total of 500?

"""

import part_1

def get_calories(ingredients, counts):
    """Determine the number of calories based on the counts

    >>> ingredients = [
    ...     part_1.Ingredient("Butterscotch", -1, -2, 6, 3, 8),
    ...     part_1.Ingredient("Cinnamon", 2, 3, -2, -1, 3),
    ... ]
    >>> get_calories(ingredients, [40, 60])
    500

    """
    return sum(count * i.calories for i, count in zip(ingredients, counts))

def find_best_combination(ingredients, total_amount, calories):
    """Find the combination of ingredients that gives the highest score
    with the given number of calories.

    >>> ingredients = [
    ...     part_1.Ingredient("Butterscotch", -1, -2, 6, 3, 8),
    ...     part_1.Ingredient("Cinnamon", 2, 3, -2, -1, 3),
    ... ]
    >>> find_best_combination(ingredients, 100, 500)
    (57600000, [40, 60])

    """
    best_score = 0
    best_counts = None
    for counts in part_1.count_combinations(len(ingredients), total_amount):
        if get_calories(ingredients, counts) != calories:
            continue

        score = part_1.score_ingredients(ingredients, counts)

        if score > best_score:
            best_score = score
            best_counts = counts

    return (best_score, best_counts)

def main(filename):
    """Read ingredients and print score of the best combination with 500
    calories"""
    with open(filename, 'r') as f:
        ingredients = part_1.read_ingredients(f)

    score, counts = find_best_combination(ingredients, 100, 500)
    print(score)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
