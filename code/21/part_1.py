#!/usr/bin/env python3
"""Solve Day 21/Part 1 of the AdventOfCode

"""

import itertools

class Item(object):
    def __init__(self, item_type, name, cost, damage, armor):
        self.item_type = item_type
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor

    def __eq__(self, other):
        return self.item_type == other.item_type and self.name == other.name

    def __le__(self, other):
        if self.item_type < other.item_type:
            return True
        if self.name < other.name:
            return True
        return False

    def __repr__(self):
        return "Item(name={!r})".format(self.name)

    def __str__(self):
        return "{}".format(self.name)

    def is_weapon(self):
        return self.item_type == "weapon"

    def is_armor(self):
        return self.item_type == "armor"

    def is_ring(self):
        return self.item_type == "ring1" or self.item_type == "ring2"

store_items = [
    Item("weapon", "Dagger", 8, 4, 0),
    Item("weapon", "Shortsword", 10, 5, 0),
    Item("weapon", "Warhammer", 25, 6, 0),
    Item("weapon", "Longsword", 40, 7, 0),
    Item("weapon", "Greataxe", 74, 8, 0),

    Item("armor", "Leather", 13, 0, 1),
    Item("armor", "Chainmail", 31, 0, 2),
    Item("armor", "Splintmail", 53, 0, 3),
    Item("armor", "Bandedmail", 75, 0, 4),
    Item("armor", "Platemail", 102, 0, 5),

    Item("ring1", "Damage +1", 25, 1, 0),
    Item("ring1", "Damage +2", 50, 2, 0),
    Item("ring1", "Damage +3", 100, 3, 0),
    Item("ring1", "Defense +1", 20, 0, 1),
    Item("ring1", "Defense +2", 40, 0, 2),
    Item("ring1", "Defense +3", 80, 0, 3),

    Item("ring2", "Damage +1", 25, 1, 0),
    Item("ring2", "Damage +2", 50, 2, 0),
    Item("ring2", "Damage +3", 100, 3, 0),
    Item("ring2", "Defense +1", 20, 0, 1),
    Item("ring2", "Defense +2", 40, 0, 2),
    Item("ring2", "Defense +3", 80, 0, 3),
]

class Character(object):
    def __init__(self, hit_points, damage, armor):
        self.hit_points = hit_points
        self.damage = damage
        self.armor = armor

    @classmethod
    def from_items(cls, hit_points, items):
        damage = 0
        armor = 0
        for item in items:
            damage += item.damage
            armor += item.armor

        return cls(hit_points, damage, armor)

    @classmethod
    def from_lines(cls, lines):
        hit_points = None
        damage = None
        armor = None
        for line in lines:
            (attribute, value) = line.split(':')
            if attribute == "Hit Points":
                hit_points = int(value)
            elif attribute == "Damage":
                damage = int(value)
            elif attribute == "Armor":
                armor = int(value)

        return cls(hit_points, damage, armor)

    def copy(self):
        return Character(self.hit_points, self.damage, self.armor)

    def attack(self, other):
        other.hit_points -= max(1, self.damage - other.armor)

    def is_living(self):
        return self.hit_points > 0

def item_combinations(size):
    for combination in itertools.combinations(store_items, size):
        # Exactly 1 weapon
        num_weapons = sum(x.is_weapon() for x in combination)
        if num_weapons != 1:
            continue

        # No more than 1 armor
        num_armors = sum(x.is_armor() for x in combination)
        if num_armors > 1:
            continue

        # No more than 2 rings
        num_rings = sum(x.is_ring() for x in combination)
        if num_rings > 2:
            continue

        # Rings must be distinct
        num_distinct_rings = len(set(x.name for x in combination if x.is_ring()))
        if num_distinct_rings != num_rings:
            continue

        yield combination

def all_item_combinations():
    for size in range(5):
        yield from item_combinations(size)

def determine_winner(player, boss):
    """True if player wins, False otherwise"""
    while True:
        player.attack(boss)
        if not boss.is_living():
            return True

        boss.attack(player)
        if not player.is_living():
            return False

def main(filename):
    with open(filename, 'r') as f:
        boss = Character.from_lines(f)

    player_hit_points = 100
    winning_items = []
    for items in all_item_combinations():
        player = Character.from_items(player_hit_points, items)
        if determine_winner(player.copy(), boss.copy()):
            winning_items.append(items)

    min_cost = min(sum(x.cost for x in items) for items in winning_items)
    print(min_cost)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
