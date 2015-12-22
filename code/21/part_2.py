#!/usr/bin/env python3
"""Solve Day 21/Part 2 of the AdventOfCode

"""

import part_1

def main(filename):
    with open(filename, 'r') as f:
        boss = part_1.Character.from_lines(f)

    player_hit_points = 100
    losing_items = []
    for items in part_1.all_item_combinations():
        player = part_1.Character.from_items(player_hit_points, items)
        if not part_1.determine_winner(player.copy(), boss.copy()):
            losing_items.append(items)

    max_cost = max(sum(x.cost for x in items) for items in losing_items)
    print(max_cost)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
