#!/usr/bin/env python3
"""Solve Day 22/Part 1 of the AdventOfCode

"""

import itertools
import collections

################################################################
# Spells

class Spell(object):
    def __init__(self, name, cost, num_turns, effect):
        self.name = name
        self.cost = cost
        self.num_turns = num_turns
        self.effect = effect

    def __repr__(self):
        return "Spell(name={!r})".format(self.name)

    def cast(self):
        return CastedSpell(self.name, self.num_turns, self.effect)

class CastedSpell(object):
    def __init__(self, name, num_turns, effect):
        self.name = name
        self.num_turns = num_turns
        self.effect = effect

    def __repr__(self):
        return "CastedSpell(name={!r}, num_turns={!r})".format(
            self.name,
            self.num_turns,
        )

    def copy(self):
        return CastedSpell(self.name, self.num_turns, self.effect)

    def on_cast(self, game):
        self.effect.on_cast(game)

    def on_turn_start(self, game):
        self.effect.on_turn_start(game)

    def on_end(self, game):
        self.effect.on_end(game)

class Effect(object):
    def on_cast(self, game):
        raise NotImplementedError()

    def on_turn_start(self, game):
        raise NotImplementedError()

    def on_end(self, game):
        raise NotImplementedError()


class MagicMissileEffect(Effect):
    def on_cast(self, game):
        game.boss.hit_points -= 4

    def on_turn_start(self, game):
        pass

    def on_end(self, game):
        pass


class DrainEffect(Effect):
    def on_cast(self, game):
        game.boss.hit_points -= 2
        game.player.hit_points += 2

    def on_turn_start(self, game):
        pass

    def on_end(self, game):
        pass


class ShieldEffect(Effect):
    def on_cast(self, game):
        game.player.armor += 7

    def on_turn_start(self, game):
        pass

    def on_end(self, game):
        game.player.armor -= 7


class PoisonEffect(Effect):
    def on_cast(self, game):
        pass

    def on_turn_start(self, game):
        game.boss.hit_points -= 3

    def on_end(self, game):
        pass


class RechargeEffect(Effect):
    def on_cast(self, game):
        pass

    def on_turn_start(self, game):
        game.player.mana += 101

    def on_end(self, game):
        pass

spells = [
    Spell("Magic Missile", 53, 0, MagicMissileEffect()),
    Spell("Drain", 73, 0, DrainEffect()),
    Spell("Shield", 113, 6, ShieldEffect()),
    Spell("Poison", 173, 6, PoisonEffect()),
    Spell("Recharge", 229, 5, RechargeEffect()),
]

################################################################
# Character and Game

class Character(object):
    def __init__(self, hit_points, mana=0, damage=0, armor=0):
        self.hit_points = hit_points
        self.mana = mana
        self.damage = damage
        self.armor = armor

    def copy(self):
        return Character(self.hit_points, self.mana, self.damage, self.armor)

    def is_living(self):
        return self.hit_points > 0

class Game(object):
    def __init__(self, boss, player, is_player_turn, effects, casted_spells):
        self.boss = boss
        self.player = player
        self.is_player_turn = is_player_turn
        self.effects = effects
        self.casted_spells = casted_spells

    @classmethod
    def from_stats(cls, boss_hit_points, boss_damage, player_hit_points,
                   player_mana):
        boss = Character(boss_hit_points, damage=boss_damage)
        player = Character(player_hit_points, mana=player_mana)

        return cls(
            boss=boss,
            player=player,
            is_player_turn=True,
            effects=[],
            casted_spells=[],
        )

    def copy(self):
        return Game(
            self.boss.copy(),
            self.player.copy(),
            self.is_player_turn,
            self.effects[:],
            self.casted_spells[:],
        )

    def step(self):
#        import sys
#        print("boss: hp = {}".format(self.boss.hit_points), file=sys.stderr)
#        print("player: hp = {}, mana = {}".format(self.player.hit_points, self.player.mana), file=sys.stderr)

        game = self.copy()

        # Do start of turn effects and decrement timer
        for effect in game.effects:
            effect.on_turn_start(game)

            effect.num_turns -= 1
            if effect.num_turns == 0:
                effect.on_end(game)

        # Remove finished effects
        game.effects = [x for x in game.effects if x.num_turns > 0]

        # Player lost
        if game.player.hit_points <= 0:
            yield (False, self.casted_spells)
            return

        # Player won
        elif game.boss.hit_points <= 0:
            yield (True, self.casted_spells)
            return

        # Do player or boss' turn
        if self.is_player_turn:
            game.is_player_turn = False
            yield from self.step_player(game)
        else:
            game.is_player_turn = True
            yield from self.step_boss(game)

#        print(file=sys.stderr)

    def step_player(self, game):
        # Determine which spells can be casted
        castable_spells = [x for x in spells if x.cost <= game.player.mana]

        if len(castable_spells) == 0:
            yield (False, self.casted_spells)
            return

        # Attempt each one, creating a new game state
        for spell in castable_spells:
            new_game = game.copy()

#            import sys
#            print("Casting {}".format(spell.name), file=sys.stderr)

            # Cast spell
            new_game.player.mana -= spell.cost
            new_game.casted_spells.append(spell)

            effect = spell.cast()
            effect.on_cast(new_game)

            # Add spell's effects to list
            if effect.num_turns > 0:
                new_game.effects.append(effect)

            yield from new_game.step()

    def step_boss(self, game):
        game.player.hit_points -= max(1, self.boss.damage - self.player.armor)
        yield from game.step()

def main(filename):
    with open(filename, 'r') as f:
        boss_hit_points = int(f.readline().split(': ')[-1])
        boss_damage = int(f.readline().split(': ')[-1])

    player_hit_points = 50
    player_mana = 500

    game = Game.from_stats(
        boss_hit_points,
        boss_damage,
        player_hit_points,
        player_mana,
    )

    lowest_cost_win = float('inf')

    for (player_won, casted_spells) in game.step():
#        import sys; print("{!r}".format(casted_spells), file=sys.stderr)
        if not player_won:
            continue

        cost = sum(x.cost for x in casted_spells)
        if cost < lowest_cost_win:
            lowest_cost_win = cost
            import sys
            print("lowest_cost_win = {}".format(lowest_cost_win), file=sys.stderr)

    print(lowest_cost_win)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    main(**vars(args))
